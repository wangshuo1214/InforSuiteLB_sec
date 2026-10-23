import logging
import os

from inforsuitelb_sec.core.regexp import Regexp
from inforsuitelb_sec.core.variable import Variable

LOG = logging.getLogger(__name__)

BUILTIN_VARIABLES = {
    "uri": r"/[^\x20\t]*",
    "document_uri": r"/[^\x20\t]*",
    "arg_": r"[^\s&]+",
    "args": r"[^\s]+",
    "query_string": r"[^\s]+",
    "request_uri": r"/[^\s]*",
    "http_": r"[\x21-\x7e]",
    "upstream_http_": "",
    "upstream_cookie_": "",
    "upstream_trailer_": None,
    "proxy_add_x_forwarded_for": "",
    "proxy_host": "",
    "proxy_port": "",
    "proxy_protocol_addr": None,
    "proxy_protocol_port": "",
    "proxy_protocol_server_addr": None,
    "proxy_protocol_server_port": None,
    "proxy_protocol_tlv_": None,
    "fastcgi_path_info": "",
    "fastcgi_script_name": "",
    "content_type": "",
    "cookie_": "",
    "host": "",
    "hostname": "",
    "limit_rate": "",
    "memcached_key": "",
    "realpath_root": "",
    "remote_user": "",
    "request": "",
    "request_body": "",
    "request_completion": "",
    "request_filename": "",
    "request_id": "",
    "slice_range": "",
    "secure_link": "",
    "secure_link_expires": "",
    "sent_http_": "",
    "sent_trailer_": None,
    "server_name": "",
    # "Secure" variables that can't content or strictly limited user input
    "ancient_browser": None,
    "binary_remote_addr": None,
    "body_bytes_sent": None,
    "bytes_received": None,
    "bytes_sent": None,
    "connection": None,
    "connection_requests": None,
    "connection_time": None,
    "connections_active": None,
    "connections_reading": None,
    "connections_waiting": None,
    "connections_writing": None,
    "content_length": None,
    "date_gmt": None,
    "date_local": None,
    "document_root": "/etc/inforsuitelb",
    "geoip_": None,
    "gzip_ratio": None,
    "http2": None,
    "http3": None,
    "https": None,
    "invalid_referer": None,
    "is_args": None,
    "is_request_port": None,
    "limit_conn_status": None,
    "limit_req_status": None,
    "jwt_": None,
    "modern_browser": None,
    "msec": None,
    "msie": None,
    "inforsuitelb_version": None,
    "pid": None,
    "pipe": None,
    "protocol": None,
    "realip_remote_addr": None,
    "realip_remote_port": None,
    "remote_addr": None,
    "remote_port": None,
    "request_body_file": None,
    "request_length": None,
    "request_method": None,
    "request_port": None,
    "request_time": None,
    "scheme": None,
    "server_addr": None,
    "server_port": None,
    "server_protocol": None,
    "session_log_binary_id": None,
    "session_log_id": None,
    "session_time": None,
    "spdy": None,
    "spdy_request_priority": None,
    "ssl_": None,
    "status": None,
    "tcpinfo_": None,
    "time_iso8601": None,
    "time_local": None,
    "uid_got": None,
    "uid_reset": None,
    "uid_set": None,
    "upstream_addr": None,
    "upstream_bytes_received": None,
    "upstream_bytes_sent": None,
    "upstream_cache_status": None,
    "upstream_connect_time": None,
    "upstream_first_byte_time": None,
    "upstream_header_time": None,
    "upstream_response_length": None,
    "upstream_response_time": None,
    "upstream_session_time": None,
    "upstream_status": None,
}


# Additional variables loaded from drop-in configuration files
EXTRA_VARIABLES = {}


def clear_custom_variables():
    """Clear variables loaded from drop-in files (useful for tests)."""
    EXTRA_VARIABLES.clear()


def _normalize_value_token(token):
    """Parse a token from a drop-in variable file into a usable value.

    Supported forms:
    - "" or '' → empty string (treated as not user-controlled)
    - r'...'/r"..." → regex pattern string
    - '...'/"..." → literal string
    - none/null (case-insensitive) → None
    - empty/missing value → empty string
    Trailing commas are tolerated.
    """
    if token is None:
        return ""

    token = token.strip().rstrip(",").strip()
    if token.lower() in ("none", "null"):
        return None

    # Strip possible raw prefix
    if len(token) > 2 and token[0] in ("r", "R") and token[1] in ("'", '"'):
        token = token[1:]

    # Strip quotes
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        token = token[1:-1]

    # For regex patterns we just return the inside content (without r/quotes)
    return token


def _parse_dropin_file(file_path):
    """Parse a single drop-in file and return a dict of variables.

    Each non-empty, non-comment line should be of the form:
        name <value>
    where value follows _normalize_value_token rules.
    """
    result = {}
    try:
        with open(file_path) as fh:
            for raw_line in fh:
                line = raw_line.strip()
                if not line or line.startswith("#") or line.startswith(";"):
                    continue

                # Fast-path parse: find first whitespace after a valid identifier
                i = 0
                n = len(line)
                # identifier start
                c0 = line[0]
                if not (c0.isalpha() or c0 == "_"):
                    LOG.info(
                        "Skip malformed custom variable line in %s: %r",
                        file_path,
                        raw_line.rstrip("\n"),
                    )
                    continue
                i = 1
                while i < n and (line[i].isalnum() or line[i] == "_"):
                    i += 1
                name = line[:i]
                # skip spaces between name and value
                j = i
                while j < n and line[j].isspace():
                    j += 1
                value_token = line[j:]
                # Allow optional separator characters between name and value
                # If the line used name = value or name: value, drop the first char
                if value_token[:1] in ("=", ":"):
                    value_token = value_token[1:].strip()
                result[name] = _normalize_value_token(value_token)
    except Exception as e:
        LOG.warning("Failed to load custom variables from %s: %s", file_path, e)
    return result


def load_custom_variables_from_dirs(paths):
    """Load additional variables from provided directories.

    - Reads all files with extensions .cfg or .conf
    - Merges into EXTRA_VARIABLES (later files override earlier ones)
    """
    if not paths:
        return
    for base in paths:
        if not base:
            continue
        expanded = os.path.expanduser(base)
        if not os.path.isdir(expanded):
            continue
        try:
            entries = sorted(os.listdir(expanded))
        except OSError:
            continue
        for fname in entries:
            if not (fname.endswith(".cfg") or fname.endswith(".conf")):
                continue
            fpath = os.path.join(expanded, fname)
            if not os.path.isfile(fpath):
                continue
            parsed = _parse_dropin_file(fpath)
            if parsed:
                EXTRA_VARIABLES.update(parsed)


def _iter_all_variable_items():
    # EXTRA overrides BUILTIN on duplicates
    # Preserve prefix variables (ending with '_') semantics
    # Order: EXTRA first, then BUILTIN
    for k, v in EXTRA_VARIABLES.items():
        yield k, v
    for k, v in BUILTIN_VARIABLES.items():
        if k not in EXTRA_VARIABLES:
            yield k, v


def is_builtin(name):
    if isinstance(name, int):
        # Indexed variables can't be builtin
        return False
    for builtin, _ in _iter_all_variable_items():
        if builtin.endswith("_"):
            if name.startswith(builtin):
                return True
        elif name == builtin:
            return True
    return False


def builtin_var(name):
    for builtin, regexp in _iter_all_variable_items():
        if builtin.endswith("_"):
            if not name.startswith(builtin):
                continue
        elif name != builtin:
            continue

        if regexp:
            return Variable(
                name=name, value=Regexp(regexp, strict=True, case_sensitive=False)
            )
        return Variable(name=name, value="builtin", have_script=False)
    return None


def fake_var(name):
    return Variable(name=name, value=name, have_script=False)
