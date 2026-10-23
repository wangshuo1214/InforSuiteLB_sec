---
title: "HTTP/2 Misdirected Request (421)"
description: "For default ssl_reject_handshake with http2, return 421 in / to prevent misdirected handling in the wrong server block."
---

# HTTP/2 Misdirected Request Safeguard

_Gixy Check ID: `http2_misdirected_request`_


## Overview

The `http2_misdirected_request` plugin detects a potentially unsafe pattern where a TLS `default_server` with `ssl_reject_handshake on;` has HTTP/2 enabled but does **not** explicitly return **421 (Misdirected Request)** from `location /`.

This is commonly used as a defensive safeguard for edge-cases where requests can still be processed in an unexpected server context.

## What it detects

Triggers when all of the following are true:

- `ssl_reject_handshake on;` is present
- the server is marked `default_server` (or `default`)
- HTTP/2 is enabled (`http2 on;` or `listen ... http2`)
- there is no `location /` (or `location = /`) that does `return 421;`

## Examples

### ❌ Bad: Missing 421 safeguard

```nginx
http {
    server {
        listen 443 ssl default_server;
        http2 on;
        ssl_reject_handshake on;
    }
}
```

### ✅ Good: Explicitly return 421

```nginx
http {
    server {
        listen 443 ssl default_server;
        http2 on;
        ssl_reject_handshake on;

        location / {
            return 421;
        }
    }
}
```
