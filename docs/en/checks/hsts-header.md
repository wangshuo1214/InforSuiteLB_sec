---
title: "Missing or Weak HSTS Header"
description: "Ensure strong HSTS on HTTPS sites. Enforce long max-age and subdomains to block downgrade and cookie hijack risks."
---

# Missing or Weak HSTS Header

_Gixy Check ID: `hsts_header`_


## Overview

The `hsts_header` plugin detects missing or weak **HSTS** configuration in HTTPS servers.

HSTS (HTTP Strict Transport Security) is delivered via the `Strict-Transport-Security` response header and helps protect users against:
- protocol downgrade attacks
- cookie hijacking

## What it detects

### 1. Missing HSTS header

Detects HTTPS servers missing:

```nginx
add_header Strict-Transport-Security "...";
```

### 2. Weak HSTS max-age

Detects HSTS with `max-age` less than 6 months (15768000 seconds).

## Examples

### ❌ Bad: Missing HSTS

```nginx
http {
    server {
        listen 443 ssl;
        # Missing: add_header Strict-Transport-Security
    }
}
```

### ✅ Good: HSTS with 1 year max-age

```nginx
http {
    server {
        listen 443 ssl;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    }
}
```

## Notes

- Servers configured with `ssl_reject_handshake on;` are skipped, because they never emit HTTP response headers.
- The [`ngx_security_headers`](https://github.com/GetPageSpeed/ngx_security_headers) module (`security_headers on;`) is recognized as providing HSTS — no separate `add_header` is required.
- The `more_set_headers` directive (from the [headers-more](https://github.com/openresty/headers-more-nginx-module) module) setting `Strict-Transport-Security` is also recognized.
