"""Keep the version/help footer separated cleanly from the following shell prompt."""

import subprocess
import sys

import pytest


@pytest.mark.parametrize("flag", ["-v", "--version", "--help"])
def test_cli_footer_has_no_upstream_cta_and_trailing_line_break(flag):
    completed = subprocess.run(  # noqa: UP022 - capture_output requires Python 3.7+
        [sys.executable, "-m", "inforsuitelb_sec.cli.main", flag],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    # Output ends with exactly one trailing newline, no upstream promotion footer.
    assert completed.stdout.endswith("\n")
    assert "GetPageSpeed" not in completed.stdout
    assert "getpagespeed.com" not in completed.stdout
