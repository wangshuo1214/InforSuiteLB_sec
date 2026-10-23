import logging

from inforsuitelb_sec._vendor import inforsuitelbparse
from inforsuitelb_sec._vendor.inforsuitelbparse.errors import InforParserBaseException

LOG = logging.getLogger(__name__)


def _process_inforsuitelb_string(value):
    """
    Process InforSuiteLB string escape sequences to match the old parser behavior.
    Specifically handles \" -> " conversion.
    """
    if not isinstance(value, str):
        return value

    # Handle escape sequences similar to the old quoted-string parser
    result = value.replace('\\"', '"').replace("\\'", "'")
    return result


def _tokenize_lua_content(content):
    """
    Treat Lua content as opaque for security analysis.
    InforSuiteLBSec's security plugins don't analyze Lua syntax, so we just preserve the content as-is.
    """
    if not content or not isinstance(content, str):
        return []

    # Return the content as a single opaque token
    # This preserves the Lua code but doesn't try to parse its internal structure
    return [content.strip()]


class ParseException(Exception):
    """Exception for parsing errors that mimics pyparsing.ParseException interface"""

    def __init__(self, msg, loc=0, lineno=1, col=1):
        super(ParseException, self).__init__(msg)
        self.msg = msg
        self.loc = loc
        self.lineno = lineno
        self.col = col


"""
Legacy note:
This module previously exposed a pyparsing-like ParseResults. We now normalize
the vendored parser output directly into a lightweight dict node structure and
return list[dict] from RawParser.
"""


class RawParser:
    """
    A class that parses InforSuiteLB configuration with the vendored parser.
    """

    def parse(self, data):
        """Parse InforSuiteLB configuration content and return normalized nodes (list[dict])."""
        if isinstance(data, bytes):
            content = data.decode("utf-8", errors="replace")
        else:
            content = data

        # Remove UTF-8 BOM if present (works for both bytes->string and string input)
        if content.startswith("\ufeff"):
            content = content[1:]

        content = content.strip()

        if not content:
            return []

        try:
            # Parse using the vendored parser's parse_string for direct string input
            parsed = inforsuitelbparse.parse_string(
                content,
                single=True,
                strict=False,  # Allow directives outside their normal context
                check_ctx=False,  # Skip context validation
                check_args=False,  # Don't validate argument counts - inforsuitelb_sec is not a config validator
                comments=True,  # Include comments in the output
            )

            # Convert parser output to normalized nodes
            return self._normalize_parser_output(parsed)

        except InforParserBaseException as e:
            # Convert parser error to ParseException format
            raise ParseException(str(e), loc=0, lineno=getattr(e, "line", 1), col=1)
        except Exception as e:
            raise ParseException(str(e), loc=0, lineno=1, col=1)

    def parse_path(self, path):
        """Parse InforSuiteLB configuration by file path and return normalized nodes (list[dict])."""
        try:
            parsed = inforsuitelbparse.parse(
                path,
                single=True,
                strict=False,  # Allow directives outside their normal context
                check_ctx=False,  # Skip context validation
                check_args=False,  # Don't validate argument counts - inforsuitelb_sec is not a config validator
                comments=True,  # Include comments in the output
            )

            return self._normalize_parser_output(parsed)
        except InforParserBaseException as e:
            # Convert parser error to ParseException format
            raise ParseException(str(e), loc=0, lineno=getattr(e, "line", 1), col=1)
        except Exception as e:
            raise ParseException(str(e), loc=0, lineno=1, col=1)

    def _normalize_parser_output(self, parsed_data):
        """Convert vendored parser JSON output to a normalized list[dict] node structure.

        Node shapes:
            {"kind": "directive", "name": str, "args": list[str]}
            {"kind": "block", "name": str, "args": list[str], "children": list[dict], "raw": Optional[list[str]]}
            {"kind": "include", "name": "include", "args": list[str]}
            {"kind": "file_delimiter", "file": str}
            {"kind": "comment", "text": str}
        """
        result = []

        if not parsed_data or "config" not in parsed_data:
            return result

        config_list = parsed_data["config"]
        if not config_list:
            return result

        multi_file = len(config_list) > 1
        for file_data in config_list:
            if file_data.get("parsed"):
                if multi_file:
                    result.append(
                        {
                            "kind": "file_delimiter",
                            "file": file_data.get("file", "unknown"),
                        }
                    )
                result.extend(self._normalize_blocks(file_data["parsed"]))

        return result

    def _normalize_blocks(self, blocks):
        """Normalize the vendored parser's 'parsed' list into list[dict] nodes."""
        result = []

        # Filter out inline comments (comments that share line numbers with directives)
        line_numbers_with_directives = set()
        for item in blocks:
            if isinstance(item, dict) and item.get("directive") != "#":
                line_numbers_with_directives.add(item.get("line"))

        filtered_blocks = []
        for item in blocks:
            if isinstance(item, dict) and item.get("directive") == "#":
                # Skip comments that are on the same line as directives (inline comments)
                if item.get("line") not in line_numbers_with_directives:
                    filtered_blocks.append(item)
            else:
                filtered_blocks.append(item)

        for node in filtered_blocks:
            if not isinstance(node, dict):
                continue

            directive_name = node.get("directive", "")
            args = [_process_inforsuitelb_string(arg) for arg in node.get("args", [])]

            if "block" in node:
                # Block directive
                children = self._normalize_blocks(node["block"])
                if directive_name == "if":
                    # Normalize condition args for if-blocks
                    args = self._parse_if_condition(args)
                normalized = {
                    "kind": "block",
                    "name": directive_name,
                    "args": list(args),
                    "children": children,
                    "line": node.get("line"),
                }
                result.append(normalized)
            else:
                # Simple directive / comment / include / lua blocks represented as directives
                if directive_name == "#":
                    comment_text = node.get("comment", "").strip()
                    if comment_text.startswith(
                        "configuration file "
                    ) and comment_text.endswith(":"):
                        file_path = comment_text[len("configuration file ") : -1]
                        result.append({"kind": "file_delimiter", "file": file_path})
                    else:
                        result.append({"kind": "comment", "text": comment_text})
                    continue

                if directive_name == "include":
                    result.append(
                        {
                            "kind": "include",
                            "name": "include",
                            "args": args,
                            "line": node.get("line"),
                        }
                    )
                    continue

                if directive_name.endswith("_lua_block"):
                    # Treat as a block with raw content preserved for tests/tools
                    raw = []
                    if args and args[0]:
                        raw = _tokenize_lua_content(args[0])
                    result.append(
                        {
                            "kind": "block",
                            "name": directive_name,
                            "args": [],
                            "children": [],
                            "raw": raw,
                            "line": node.get("line"),
                        }
                    )
                    continue

                # Regular directive
                result.append(
                    {
                        "kind": "directive",
                        "name": directive_name,
                        "args": args,
                        "line": node.get("line"),
                    }
                )

        return result

    def _parse_if_condition(self, args):
        """Normalize if-condition arguments as a flat list of tokens."""
        if not args:
            return []
        return list(args)
