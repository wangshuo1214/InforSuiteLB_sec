import gixy
from gixy.plugins.plugin import Plugin


class status_page_exposed(Plugin):
    """Detect stub_status directives that are publicly accessible without IP restrictions."""

    summary = "stub_status is publicly accessible without IP restrictions."
    severity = gixy.severity.MEDIUM
    description = (
        "The stub_status module exposes NGINX server metrics including "
        "active connections, requests handled, and connection states. "
        "Without proper IP restrictions, this information is accessible "
        "to anyone and can aid attackers in reconnaissance."
    )
    directives = ["stub_status"]

    def _server_uses_only_unix_sockets(self, directive):
        """Check if the enclosing server block only listens on Unix sockets.

        Args:
            directive: The directive to check.

        Returns:
            True if the server block has at least one listen directive and all
            of them use Unix sockets.
        """
        for parent in directive.parents:
            if parent.name == "server":
                listen_directives = parent.find("listen")
                if not listen_directives:
                    return False
                return all(
                    d.args and d.args[0].lower().startswith("unix:")
                    for d in listen_directives
                )
        return False

    def audit(self, directive):
        """Audit stub_status directive for missing access restrictions.

        Args:
            directive: The stub_status directive to audit.
        """
        if self._server_uses_only_unix_sockets(directive):
            return

        parent = directive.parent
        if not parent:
            return

        # Handle includes - climb to real parent context
        while parent and getattr(parent, "name", None) == "include":
            parent = parent.parent
            if not parent:
                return

        # Check for allow/deny directives in same scope
        has_allow = False
        has_deny_all = False

        for child in parent.children:
            if child.name == "allow":
                has_allow = True
            elif child.name == "deny" and child.args == ["all"]:
                has_deny_all = True

        # Report if missing proper restrictions
        if not has_allow or not has_deny_all:
            reasons = []
            if not has_allow:
                reasons.append("no allow directive to whitelist trusted IPs")
            if not has_deny_all:
                reasons.append("no 'deny all' to block unauthorized access")

            self.add_issue(
                directive=directive,
                reason="stub_status exposed: " + "; ".join(reasons),
            )
