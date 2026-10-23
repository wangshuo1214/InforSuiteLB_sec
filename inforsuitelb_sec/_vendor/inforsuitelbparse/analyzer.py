# -*- coding: utf-8 -*-
from .errors import (
    InforParserDirectiveUnknownError,
    InforParserDirectiveContextError,
    InforParserDirectiveArgumentsError
)

# bit masks for different directive argument styles
INFOR_CONF_NOARGS = 0x00000001  # 0 args
INFOR_CONF_TAKE1  = 0x00000002  # 1 args
INFOR_CONF_TAKE2  = 0x00000004  # 2 args
INFOR_CONF_TAKE3  = 0x00000008  # 3 args
INFOR_CONF_TAKE4  = 0x00000010  # 4 args
INFOR_CONF_TAKE5  = 0x00000020  # 5 args
INFOR_CONF_TAKE6  = 0x00000040  # 6 args
INFOR_CONF_TAKE7  = 0x00000080  # 7 args
INFOR_CONF_BLOCK  = 0x00000100  # followed by block
INFOR_CONF_FLAG   = 0x00000200  # 'on' or 'off'
INFOR_CONF_ANY    = 0x00000400  # >=0 args
INFOR_CONF_1MORE  = 0x00000800  # >=1 args
INFOR_CONF_2MORE  = 0x00001000  # >=2 args

# some helpful argument style aliases
INFOR_CONF_TAKE12   = (INFOR_CONF_TAKE1 | INFOR_CONF_TAKE2)
INFOR_CONF_TAKE13   = (INFOR_CONF_TAKE1 | INFOR_CONF_TAKE3)
INFOR_CONF_TAKE23   = (INFOR_CONF_TAKE2 | INFOR_CONF_TAKE3)
INFOR_CONF_TAKE34   = (INFOR_CONF_TAKE3 | INFOR_CONF_TAKE4)
INFOR_CONF_TAKE123  = (INFOR_CONF_TAKE12 | INFOR_CONF_TAKE3)
INFOR_CONF_TAKE1234 = (INFOR_CONF_TAKE123 | INFOR_CONF_TAKE4)

# bit masks for different directive locations
INFOR_DIRECT_CONF      = 0x00010000  # main file (not used)
INFOR_MAIN_CONF        = 0x00040000  # main context
INFOR_EVENT_CONF       = 0x00080000  # events
INFOR_MAIL_MAIN_CONF   = 0x00100000  # mail
INFOR_MAIL_SRV_CONF    = 0x00200000  # mail > server
INFOR_STREAM_MAIN_CONF = 0x00400000  # stream
INFOR_STREAM_SRV_CONF  = 0x00800000  # stream > server
INFOR_STREAM_UPS_CONF  = 0x01000000  # stream > upstream
INFOR_HTTP_MAIN_CONF   = 0x02000000  # http
INFOR_HTTP_SRV_CONF    = 0x04000000  # http > server
INFOR_HTTP_LOC_CONF    = 0x08000000  # http > location
INFOR_HTTP_UPS_CONF    = 0x10000000  # http > upstream
INFOR_HTTP_SIF_CONF    = 0x20000000  # http > server > if
INFOR_HTTP_LIF_CONF    = 0x40000000  # http > location > if
INFOR_HTTP_LMT_CONF    = 0x80000000  # http > location > limit_except

# helpful directive location alias describing "any" context
# doesn't include INFOR_HTTP_SIF_CONF, INFOR_HTTP_LIF_CONF, or INFOR_HTTP_LMT_CONF
INFOR_ANY_CONF = (
    INFOR_MAIN_CONF | INFOR_EVENT_CONF | INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF |
    INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_STREAM_UPS_CONF |
    INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_UPS_CONF
)

"""
DIRECTIVES
~~~~~~~~~~
This dict maps directives to lists of bit masks that define their behavior.

Each bit mask describes these behaviors:
  - how many arguments the directive can take
  - whether or not it is a block directive
  - whether this is a flag (takes one argument that's either "on" or "off")
  - which contexts it's allowed to be in

Since some directives can have different behaviors in different contexts, we
  use lists of bit masks, each describing a valid way to use the directive.

Definitions for directives that're available in the open source version of
  InforSuiteLB were taken directively from the source code. In fact, the variable
  names for the bit masks defined above were taken from the InforSuiteLB source code.

Definitions for directives that're only available for InforSuiteLB+ were inferred
  from the InforSuiteLB product documentation.
"""
DIRECTIVES = {
    'absolute_redirect': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'accept_mutex': [
        INFOR_EVENT_CONF | INFOR_CONF_FLAG
    ],
    'accept_mutex_delay': [
        INFOR_EVENT_CONF | INFOR_CONF_TAKE1
    ],
    'access_log': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_1MORE
    ],
    'add_after_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'add_before_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'add_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE23
    ],
    'add_trailer': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE23
    ],
    'addition_types': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'aio': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'aio_write': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'alias': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'allow': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ancient_browser': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'ancient_browser_value': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'auth_basic': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_TAKE1
    ],
    'auth_basic_user_file': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_TAKE1
    ],
    'auth_http': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'auth_http_header': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE2
    ],
    'auth_http_pass_client_cert': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_FLAG
    ],
    'auth_http_timeout': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'auth_request': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'auth_request_set': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'autoindex': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'autoindex_exact_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'autoindex_format': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'autoindex_localtime': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'break': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_SIF_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_NOARGS
    ],
    'charset': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'charset_map': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE2
    ],
    'charset_types': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'chunked_transfer_encoding': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'client_body_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'client_body_in_file_only': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'client_body_in_single_buffer': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'client_body_temp_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1234
    ],
    'client_body_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'client_header_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'client_header_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'client_max_body_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'connection_pool_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'create_full_put_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'daemon': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_FLAG
    ],
    'dav_access': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE123
    ],
    'dav_methods': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'debug_connection': [
        INFOR_EVENT_CONF | INFOR_CONF_TAKE1
    ],
    'debug_points': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'default_type': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'deny': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'directio': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'directio_alignment': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'disable_symlinks': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'empty_gif': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'env': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'error_log': [
        INFOR_MAIN_CONF | INFOR_CONF_1MORE,
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_1MORE
    ],
    'error_page': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_2MORE
    ],
    'etag': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'events': [
        INFOR_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS
    ],
    'expires': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE12
    ],
    'fastcgi_bind': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'fastcgi_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'fastcgi_busy_buffers_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache_background_update': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_cache_bypass': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'fastcgi_cache_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache_lock': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_cache_lock_age': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache_lock_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache_max_range_offset': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache_methods': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'fastcgi_cache_min_uses': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'fastcgi_cache_revalidate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_cache_use_stale': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'fastcgi_cache_valid': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'fastcgi_catch_stderr': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_connect_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_force_ranges': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_hide_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_ignore_client_abort': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_ignore_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'fastcgi_index': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_intercept_errors': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_keep_conn': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_limit_rate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_max_temp_file_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_next_upstream': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'fastcgi_next_upstream_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_next_upstream_tries': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_no_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'fastcgi_param': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE23
    ],
    'fastcgi_pass': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_pass_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_pass_request_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_pass_request_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_read_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_request_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_send_lowat': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_send_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_socket_keepalive': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'fastcgi_split_path_info': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_store': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_store_access': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE123
    ],
    'fastcgi_temp_file_write_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_temp_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1234
    ],
    'flv': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'geo': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE12,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE12
    ],
    'geoip_city': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE12
    ],
    'geoip_country': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE12
    ],
    'geoip_org': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE12
    ],
    'geoip_proxy': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'geoip_proxy_recursive': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_FLAG
    ],
    'google_perftools_profiles': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_bind': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'grpc_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_connect_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_hide_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ignore_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'grpc_intercept_errors': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'grpc_next_upstream': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'grpc_next_upstream_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_next_upstream_tries': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_pass': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_pass_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_read_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_send_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_set_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'grpc_socket_keepalive': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'grpc_ssl_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ssl_certificate_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ssl_ciphers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ssl_crl': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ssl_name': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ssl_password_file': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ssl_protocols': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'grpc_ssl_server_name': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'grpc_ssl_session_reuse': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'grpc_ssl_trusted_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'grpc_ssl_verify': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'grpc_ssl_verify_depth': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'gunzip': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'gunzip_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'gzip': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_FLAG
    ],
    'gzip_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'gzip_comp_level': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'gzip_disable': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'gzip_http_version': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'gzip_min_length': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'gzip_proxied': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'gzip_static': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'gzip_types': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'gzip_vary': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'hash': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_UPS_CONF | INFOR_CONF_TAKE12
    ],
    'http': [
        INFOR_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS
    ],
    'http2_body_preread_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'http2_chunk_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'http2_idle_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'http2_max_concurrent_pushes': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'http2_max_concurrent_streams': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'http2_max_field_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'http2_max_header_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'http2_max_requests': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'http2_push': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'http2_push_preload': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'http2_recv_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'http2_recv_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'if': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_BLOCK | INFOR_CONF_1MORE
    ],
    'if_modified_since': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'ignore_invalid_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG
    ],
    'image_filter': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE123
    ],
    'image_filter_buffer': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'image_filter_interlace': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'image_filter_jpeg_quality': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'image_filter_sharpen': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'image_filter_transparency': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'image_filter_webp_quality': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'imap_auth': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE
    ],
    'imap_capabilities': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE
    ],
    'imap_client_buffer': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'include': [
        INFOR_ANY_CONF | INFOR_CONF_TAKE1
    ],
    'index': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'internal': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'ip_hash': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_NOARGS
    ],
    'keepalive': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE1
    ],
    'keepalive_disable': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'keepalive_requests': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE1
    ],
    'keepalive_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12,
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE1
    ],
    'large_client_header_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE2
    ],
    'least_conn': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_NOARGS,
        INFOR_STREAM_UPS_CONF | INFOR_CONF_NOARGS
    ],
    'limit_conn': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE2
    ],
    'limit_conn_dry_run': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'limit_conn_log_level': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'limit_conn_status': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'limit_conn_zone': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE2,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE2
    ],
    'limit_except': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_BLOCK | INFOR_CONF_1MORE
    ],
    'limit_rate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'limit_rate_after': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'limit_req': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE123
    ],
    'limit_req_dry_run': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'limit_req_log_level': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'limit_req_status': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'limit_req_zone': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE34
    ],
    'lingering_close': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'lingering_time': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'lingering_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'listen': [
        INFOR_HTTP_SRV_CONF | INFOR_CONF_1MORE,
        INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_SRV_CONF | INFOR_CONF_1MORE
    ],
    'load_module': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'location': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE12
    ],
    'lock_file': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'log_format': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'log_not_found': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'log_subrequest': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'mail': [
        INFOR_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS
    ],
    'map': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE2,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE2
    ],
    'map_hash_bucket_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'map_hash_max_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'master_process': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_FLAG
    ],
    'max_ranges': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_bind': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'memcached_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_connect_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_gzip_flag': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_next_upstream': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'memcached_next_upstream_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_next_upstream_tries': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_pass': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_read_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_send_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'memcached_socket_keepalive': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'merge_slashes': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG
    ],
    'min_delete_depth': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'mirror': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'mirror_request_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'modern_browser': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'modern_browser_value': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'mp4': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'mp4_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'mp4_max_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'msie_padding': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'msie_refresh': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'multi_accept': [
        INFOR_EVENT_CONF | INFOR_CONF_FLAG
    ],
    'open_file_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'open_file_cache_errors': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'open_file_cache_min_uses': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'open_file_cache_valid': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'open_log_file_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1234,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1234
    ],
    'output_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'override_charset': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_FLAG
    ],
    'pcre_jit': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_FLAG
    ],
    'perl': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_TAKE1
    ],
    'perl_modules': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'perl_require': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'perl_set': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE2
    ],
    'pid': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'pop3_auth': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE
    ],
    'pop3_capabilities': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE
    ],
    'port_in_redirect': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'postpone_output': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'preread_buffer_size': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'preread_timeout': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'protocol': [
        INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_bind': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE12
    ],
    'proxy_buffer': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'proxy_busy_buffers_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cache_background_update': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_cache_bypass': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'proxy_cache_convert_head': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_cache_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cache_lock': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_cache_lock_age': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cache_lock_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cache_max_range_offset': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cache_methods': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'proxy_cache_min_uses': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cache_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'proxy_cache_revalidate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_cache_use_stale': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'proxy_cache_valid': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'proxy_connect_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_cookie_domain': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'proxy_cookie_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'proxy_download_rate': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_force_ranges': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_headers_hash_bucket_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_headers_hash_max_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_hide_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_http_version': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ignore_client_abort': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_ignore_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'proxy_intercept_errors': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_limit_rate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_max_temp_file_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_method': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_next_upstream': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_next_upstream_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_next_upstream_tries': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_no_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'proxy_pass': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_pass_error_message': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_pass_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_pass_request_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_pass_request_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_protocol': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_protocol_timeout': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_read_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_redirect': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'proxy_request_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'proxy_requests': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_responses': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_send_lowat': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_send_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_set_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_set_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'proxy_socket_keepalive': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_ssl': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_ssl_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ssl_certificate_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ssl_ciphers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ssl_crl': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ssl_name': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ssl_password_file': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ssl_protocols': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_1MORE
    ],
    'proxy_ssl_server_name': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_ssl_session_reuse': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_ssl_trusted_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_ssl_verify': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'proxy_ssl_verify_depth': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_store': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_store_access': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE123
    ],
    'proxy_temp_file_write_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_temp_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1234
    ],
    'proxy_timeout': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'proxy_upload_rate': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'random': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_NOARGS | INFOR_CONF_TAKE12,
        INFOR_STREAM_UPS_CONF | INFOR_CONF_NOARGS | INFOR_CONF_TAKE12
    ],
    'random_index': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'read_ahead': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'real_ip_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'real_ip_recursive': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'recursive_error_pages': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'referer_hash_bucket_size': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'referer_hash_max_size': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'request_pool_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'reset_timedout_connection': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'resolver': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE,
        INFOR_HTTP_UPS_CONF | INFOR_CONF_1MORE,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_1MORE
    ],
    'resolver_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'return': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_SIF_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'rewrite': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_SIF_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE23
    ],
    'rewrite_log': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_SIF_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_FLAG
    ],
    'root': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'satisfy': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_bind': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'scgi_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'scgi_busy_buffers_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_cache_background_update': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_cache_bypass': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'scgi_cache_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_cache_lock': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_cache_lock_age': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_cache_lock_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_cache_max_range_offset': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_cache_methods': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'scgi_cache_min_uses': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_cache_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'scgi_cache_revalidate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_cache_use_stale': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'scgi_cache_valid': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'scgi_connect_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_force_ranges': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_hide_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_ignore_client_abort': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_ignore_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'scgi_intercept_errors': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_limit_rate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_max_temp_file_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_next_upstream': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'scgi_next_upstream_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_next_upstream_tries': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_no_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'scgi_param': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE23
    ],
    'scgi_pass': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_pass_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_pass_request_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_pass_request_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_read_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_request_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_send_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_socket_keepalive': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'scgi_store': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_store_access': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE123
    ],
    'scgi_temp_file_write_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'scgi_temp_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1234
    ],
    'secure_link': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'secure_link_md5': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'secure_link_secret': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'send_lowat': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'send_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'sendfile': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_FLAG
    ],
    'sendfile_max_chunk': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'server': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS,
        INFOR_HTTP_UPS_CONF | INFOR_CONF_1MORE,
        INFOR_MAIL_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS,
        INFOR_STREAM_UPS_CONF | INFOR_CONF_1MORE
    ],
    'server_name': [
        INFOR_HTTP_SRV_CONF | INFOR_CONF_1MORE,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'server_name_in_redirect': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'server_names_hash_bucket_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'server_names_hash_max_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'server_tokens': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'set': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_SIF_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE2
    ],
    'set_real_ip_from': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'slice': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'smtp_auth': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE
    ],
    'smtp_capabilities': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE
    ],
    'smtp_client_buffer': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'smtp_greeting_delay': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'source_charset': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'spdy_chunk_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'spdy_headers_comp': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'split_clients': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE2,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE2
    ],
    'ssi': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_FLAG
    ],
    'ssi_last_modified': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'ssi_min_file_chunk': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'ssi_silent_errors': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'ssi_types': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'ssi_value_length': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'ssl': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_FLAG
    ],
    'ssl_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_certificate_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_ciphers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_client_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_crl': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_dhparam': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_early_data': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG
    ],
    'ssl_ecdh_curve': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_engine': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_handshake_timeout': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_password_file': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_prefer_server_ciphers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_FLAG,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'ssl_preread': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'ssl_protocols': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_1MORE,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_1MORE
    ],
    'ssl_session_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE12,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE12
    ],
    'ssl_session_ticket_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_session_tickets': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_FLAG,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'ssl_session_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_stapling': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG
    ],
    'ssl_stapling_file': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_stapling_responder': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_stapling_verify': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG
    ],
    'ssl_trusted_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_verify_client': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'ssl_verify_depth': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'starttls': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'stream': [
        INFOR_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS
    ],
    'stub_status': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS | INFOR_CONF_TAKE1
    ],
    'sub_filter': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'sub_filter_last_modified': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'sub_filter_once': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'sub_filter_types': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'subrequest_output_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'tcp_nodelay': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG,
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'tcp_nopush': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'thread_pool': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE23
    ],
    'timeout': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'timer_resolution': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'try_files': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_2MORE
    ],
    'types': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_BLOCK | INFOR_CONF_NOARGS
    ],
    'types_hash_bucket_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'types_hash_max_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'underscores_in_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_CONF_FLAG
    ],
    'uninitialized_variable_warn': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_SIF_CONF | INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_FLAG
    ],
    'upstream': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE1
    ],
    'use': [
        INFOR_EVENT_CONF | INFOR_CONF_TAKE1
    ],
    'user': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE12
    ],
    'userid': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'userid_domain': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'userid_expires': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'userid_mark': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'userid_name': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'userid_p3p': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'userid_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'userid_service': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_bind': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'uwsgi_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'uwsgi_busy_buffers_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache_background_update': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache_bypass': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_cache_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache_lock': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_cache_lock_age': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache_lock_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache_max_range_offset': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache_methods': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_cache_min_uses': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_cache_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'uwsgi_cache_revalidate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_cache_use_stale': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_cache_valid': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_connect_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_force_ranges': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_hide_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ignore_client_abort': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_ignore_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_intercept_errors': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_limit_rate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_max_temp_file_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_modifier1': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_modifier2': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_next_upstream': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_next_upstream_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_next_upstream_tries': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_no_cache': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_param': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE23
    ],
    'uwsgi_pass': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_pass_header': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_pass_request_body': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_pass_request_headers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_read_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_request_buffering': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_send_timeout': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_socket_keepalive': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_ssl_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ssl_certificate_key': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ssl_ciphers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ssl_crl': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ssl_name': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ssl_password_file': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ssl_protocols': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'uwsgi_ssl_server_name': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_ssl_session_reuse': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_ssl_trusted_certificate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_ssl_verify': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'uwsgi_ssl_verify_depth': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_store': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_store_access': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE123
    ],
    'uwsgi_temp_file_write_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'uwsgi_temp_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1234
    ],
    'valid_referers': [
        INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'variables_hash_bucket_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'variables_hash_max_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'worker_aio_requests': [
        INFOR_EVENT_CONF | INFOR_CONF_TAKE1
    ],
    'worker_connections': [
        INFOR_EVENT_CONF | INFOR_CONF_TAKE1
    ],
    'worker_cpu_affinity': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_1MORE
    ],
    'worker_priority': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'worker_processes': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'worker_rlimit_core': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'worker_rlimit_nofile': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'worker_shutdown_timeout': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'working_directory': [
        INFOR_MAIN_CONF | INFOR_DIRECT_CONF | INFOR_CONF_TAKE1
    ],
    'xclient': [
        INFOR_MAIL_MAIN_CONF | INFOR_MAIL_SRV_CONF | INFOR_CONF_FLAG
    ],
    'xml_entities': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'xslt_last_modified': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'xslt_param': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'xslt_string_param': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'xslt_stylesheet': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'xslt_types': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'zone': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_UPS_CONF | INFOR_CONF_TAKE12
    ],

    # InforSuiteLB+ directives [definitions inferred from docs]
    'api': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS | INFOR_CONF_TAKE1
    ],
    'auth_jwt': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'auth_jwt_claim_set': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'auth_jwt_header_set': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'auth_jwt_key_file': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'auth_jwt_key_request': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'auth_jwt_leeway': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'f4f': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'f4f_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'fastcgi_cache_purge': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'health_check': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_ANY,
        INFOR_STREAM_SRV_CONF | INFOR_CONF_ANY
    ],
    'health_check_timeout': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'hls': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'hls_buffers': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE2
    ],
    'hls_forward_args': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'hls_fragment': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'hls_mp4_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'hls_mp4_max_buffer_size': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'js_access': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'js_content': [
        INFOR_HTTP_LOC_CONF | INFOR_HTTP_LMT_CONF | INFOR_CONF_TAKE1
    ],
    'js_filter': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'js_include': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'js_path': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE1
    ],
    'js_preread': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'js_set': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE2,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE2
    ],
    'keyval': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE3,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_TAKE3,
    ],
    'keyval_zone': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_1MORE,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_1MORE,
    ],
    'least_time': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE12,
        INFOR_STREAM_UPS_CONF | INFOR_CONF_TAKE12
    ],
    'limit_zone': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE3
    ],
    'match': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE1,
        INFOR_STREAM_MAIN_CONF | INFOR_CONF_BLOCK | INFOR_CONF_TAKE1
    ],
    'memcached_force_ranges': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_FLAG
    ],
    'mp4_limit_rate': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'mp4_limit_rate_after': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'ntlm': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_NOARGS
    ],
    'proxy_cache_purge': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'queue': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE12
    ],
    'scgi_cache_purge': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'session_log': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1
    ],
    'session_log_format': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_2MORE
    ],
    'session_log_zone': [
        INFOR_HTTP_MAIN_CONF | INFOR_CONF_TAKE23 | INFOR_CONF_TAKE4 | INFOR_CONF_TAKE5 | INFOR_CONF_TAKE6
    ],
    'state': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_UPS_CONF | INFOR_CONF_TAKE1
    ],
    'status': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'status_format': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE12
    ],
    'status_zone': [
        INFOR_HTTP_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1,
        INFOR_HTTP_LOC_CONF | INFOR_CONF_TAKE1,
        INFOR_HTTP_LIF_CONF | INFOR_CONF_TAKE1
    ],
    'sticky': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_1MORE
    ],
    'sticky_cookie_insert': [
        INFOR_HTTP_UPS_CONF | INFOR_CONF_TAKE1234
    ],
    'upstream_conf': [
        INFOR_HTTP_LOC_CONF | INFOR_CONF_NOARGS
    ],
    'uwsgi_cache_purge': [
        INFOR_HTTP_MAIN_CONF | INFOR_HTTP_SRV_CONF | INFOR_HTTP_LOC_CONF | INFOR_CONF_1MORE
    ],
    'zone_sync': [
        INFOR_STREAM_SRV_CONF | INFOR_CONF_NOARGS
    ],
    'zone_sync_buffers': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE2
    ],
    'zone_sync_connect_retry_interval': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_connect_timeout': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_interval': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_recv_buffer_size': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_server': [
        INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE12
    ],
    'zone_sync_ssl': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'zone_sync_ssl_certificate': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_ssl_certificate_key': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_ssl_ciphers': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_ssl_crl': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_ssl_name': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_ssl_password_file': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_ssl_protocols': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_1MORE
    ],
    'zone_sync_ssl_server_name': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'zone_sync_ssl_trusted_certificate': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_ssl_verify': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_FLAG
    ],
    'zone_sync_ssl_verify_depth': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ],
    'zone_sync_timeout': [
        INFOR_STREAM_MAIN_CONF | INFOR_STREAM_SRV_CONF | INFOR_CONF_TAKE1
    ]
}

# map for getting bitmasks from certain context tuples
CONTEXTS = {
    (): INFOR_MAIN_CONF,
    ('events',): INFOR_EVENT_CONF,
    ('mail',): INFOR_MAIL_MAIN_CONF,
    ('mail', 'server'): INFOR_MAIL_SRV_CONF,
    ('stream',): INFOR_STREAM_MAIN_CONF,
    ('stream', 'server'): INFOR_STREAM_SRV_CONF,
    ('stream', 'upstream'): INFOR_STREAM_UPS_CONF,
    ('http',): INFOR_HTTP_MAIN_CONF,
    ('http', 'server'): INFOR_HTTP_SRV_CONF,
    ('http', 'location'): INFOR_HTTP_LOC_CONF,
    ('http', 'upstream'): INFOR_HTTP_UPS_CONF,
    ('http', 'server', 'if'): INFOR_HTTP_SIF_CONF,
    ('http', 'location', 'if'): INFOR_HTTP_LIF_CONF,
    ('http', 'location', 'limit_except'): INFOR_HTTP_LMT_CONF
}

# contexts where arbitrary directive names are allowed (map keys, MIME types, etc.)
FREEFORM_CONTEXTS = {'map', 'types', 'charset_map', 'geo'}


def enter_block_ctx(stmt, ctx):
    # don't nest because INFOR_HTTP_LOC_CONF just means "location block in http"
    if ctx and ctx[0] == 'http' and stmt['directive'] == 'location':
        return ('http', 'location')

    # no other block contexts can be nested like location so just append it
    return ctx + (stmt['directive'],)


def analyze(fname, stmt, term, ctx=(), strict=False, check_ctx=True,
        check_args=True):

    directive = stmt['directive']
    line = stmt['line']

    # skip analysis for directives inside freeform contexts (map, types, etc.)
    # where arbitrary directive names are allowed as mapping keys or MIME types
    if ctx and ctx[-1] in FREEFORM_CONTEXTS:
        return

    # if strict and directive isn't recognized then throw error
    if strict and directive not in DIRECTIVES:
        reason = 'unknown directive "%s"' % directive
        raise InforParserDirectiveUnknownError(reason, fname, line)

    # if we don't know where this directive is allowed and how
    # many arguments it can take then don't bother analyzing it
    if ctx not in CONTEXTS or directive not in DIRECTIVES:
        return

    args = stmt.get('args') or []
    n_args = len(args)

    masks = DIRECTIVES[directive]

    # if this directive can't be used in this context then throw an error
    if check_ctx:
        masks = [mask for mask in masks if mask & CONTEXTS[ctx]]
        if not masks:
            reason = '"%s" directive is not allowed here' % directive
            raise InforParserDirectiveContextError(reason, fname, line)

    if not check_args:
        return

    valid_flag = lambda x: x.lower() in ('on', 'off')

    # do this in reverse because we only throw errors at the end if no masks
    # are valid, and typically the first bit mask is what the parser expects
    for mask in reversed(masks):
        # if the directive isn't a block but should be according to the mask
        if mask & INFOR_CONF_BLOCK and term != '{':
            reason = 'directive "%s" has no opening "{"'
            continue

        # if the directive is a block but shouldn't be according to the mask
        if not mask & INFOR_CONF_BLOCK and term != ';':
            reason = 'directive "%s" is not terminated by ";"'
            continue

        # use mask to check the directive's arguments
        if ((mask >> n_args & 1 and n_args <= 7) or  # NOARGS to TAKE7
            (mask & INFOR_CONF_FLAG and n_args == 1 and valid_flag(args[0])) or
            (mask & INFOR_CONF_ANY and n_args >= 0) or
            (mask & INFOR_CONF_1MORE and n_args >= 1) or
            (mask & INFOR_CONF_2MORE and n_args >= 2)):
            return
        elif mask & INFOR_CONF_FLAG and n_args == 1 and not valid_flag(args[0]):
            reason = 'invalid value "%s" in "%%s" directive, it must be "on" or "off"' % args[0]
        else:
            reason = 'invalid number of arguments in "%s" directive'

    raise InforParserDirectiveArgumentsError(reason % directive, fname, line)


def register_external_directives(directives):
    for directive, bitmasks in directives.iteritems():
        if bitmasks:
            DIRECTIVES[directive] = bitmasks
