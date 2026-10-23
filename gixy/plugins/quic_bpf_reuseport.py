"""
Plugin to detect the quic_bpf + reuseport + multiple workers combination.

When all three conditions are met simultaneously:
1. ``quic_bpf on;`` in the main context
2. ``reuseport`` on a QUIC listen socket
3. ``worker_processes`` > 1 (or ``auto``)

NGINX silently drops ~50% of QUIC connections after ``nginx -s reload``
due to stale BPF reuseport maps. This is a known upstream bug
(nginx/nginx#425) unfixed in mainline.
"""

import gixy
from gixy.plugins.plugin import Plugin


class quic_bpf_reuseport(Plugin):
    summary = "quic_bpf with reuseport silently drops QUIC connections after reload"
    severity = gixy.severity.HIGH
    description = (
        "When quic_bpf is enabled alongside reuseport on a QUIC listen socket "
        "and multiple worker processes, NGINX silently drops ~50% of QUIC "
        "connections after every reload. Disable quic_bpf or switch to nginx-mod."
    )
    directives = []
    supports_full_config = True
    _help_url = "https://www.getpagespeed.com/server-setup/nginx/nginx-http3-reload-quic-connections-fail"

    def audit(self, directive):
        return

    def post_audit(self, root):
        # 1. Check for quic_bpf on in the main context
        quic_bpf = root.some("quic_bpf")
        if not quic_bpf or not quic_bpf.args or quic_bpf.args[0] != "on":
            return

        # 2. Check worker_processes — only warn if explicitly > 1 or "auto"
        worker_procs = root.some("worker_processes")
        if not worker_procs or not worker_procs.args:
            # Not specified — NGINX defaults to 1, which is safe
            return

        value = worker_procs.args[0]
        if value == "1":
            return

        # value is "auto" or a number > 1 — the bug can trigger

        # 3. Scan all server blocks for listen with both quic and reuseport
        http_block = None
        for child in root.children:
            if child.name == "http":
                http_block = child
                break

        if not http_block:
            return

        for server_block in http_block.find_all_contexts_of_type("server"):
            for listen_dir in server_block.find("listen"):
                tokens_lower = [t.lower() for t in listen_dir.args]
                if "quic" in tokens_lower and "reuseport" in tokens_lower:
                    self.add_issue(
                        severity=self.severity,
                        directive=[quic_bpf, listen_dir],
                        summary=self.summary,
                        reason=(
                            "quic_bpf on + reuseport on a QUIC listener with "
                            "multiple workers causes ~50%% QUIC connection "
                            "drops after reload (nginx/nginx#425). "
                            "Either disable quic_bpf or switch to nginx-mod "
                            "which includes the fix for this bug."
                        ),
                        fixes=[
                            self.make_fix(
                                title="Disable quic_bpf",
                                search="quic_bpf on",
                                replace="quic_bpf off",
                                description=(
                                    "Turn off quic_bpf to prevent stale BPF reuseport maps after reload. "
                                    "Alternatively, switch to nginx-mod which includes the actual fix."
                                ),
                            ),
                        ],
                    )
                    # One issue per config is enough
                    return
