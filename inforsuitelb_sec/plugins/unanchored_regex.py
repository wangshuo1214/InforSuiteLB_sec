"""Module for unanchored_regex plugin."""

import inforsuitelb_sec
from inforsuitelb_sec.directives.block import LocationBlock
from inforsuitelb_sec.plugins.plugin import Plugin


class unanchored_regex(Plugin):
    r"""
    Insecure example:
        location ~ \.php {

        }
    """

    summary = "Regular expressions without anchors can be slow"
    severity = inforsuitelb_sec.severity.LOW
    description = "Regular expressions without anchors can be slow"
    directives = ["location"]

    def audit(self, directive: LocationBlock):
        # check for `location ~ \.php` instead of `location ~ \.php$`
        if not directive.is_regex:
            return
        if directive.needs_anchor():
            self.add_issue(
                severity=inforsuitelb_sec.severity.LOW,
                directive=[directive],
                reason="Regular expressions without anchors can be slow",
            )
