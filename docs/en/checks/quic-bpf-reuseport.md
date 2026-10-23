---
title: "QUIC BPF Reuseport"
description: "Detect quic_bpf + reuseport combination that silently drops QUIC connections after reload."
---

# QUIC BPF Reuseport

_Gixy Check ID: `quic_bpf_reuseport`_


## Overview

The `quic_bpf_reuseport` check detects a dangerous combination of three NGINX settings that causes **~50% of QUIC (HTTP/3) connections to silently fail** after every `nginx -s reload`:

1. `quic_bpf on;` in the `events {}` block
2. `reuseport` on a QUIC listen socket
3. `worker_processes` > 1 (or `auto`)

This is a known upstream NGINX bug ([nginx/nginx#425](https://github.com/nginx/nginx/issues/425)) that remains unfixed in mainline.

For a detailed explanation, see the [GetPageSpeed article](https://www.getpagespeed.com/server-setup/nginx/nginx-http3-reload-quic-connections-fail).

## What it detects

Triggers when **all three** conditions are present simultaneously.

## Examples

### Bad: All three conditions present

```nginx
worker_processes auto;

events {
    quic_bpf on;
}

http {
    server {
        listen 443 quic reuseport;
        listen 443 ssl;
        server_name example.com;
    }
}
```

### Good: quic_bpf disabled

```nginx
worker_processes auto;

events {
    quic_bpf off;
}

http {
    server {
        listen 443 quic reuseport;
        listen 443 ssl;
        server_name example.com;
    }
}
```

### Good: Single worker (bug doesn't trigger)

```nginx
worker_processes 1;

events {
    quic_bpf on;
}

http {
    server {
        listen 443 quic reuseport;
        listen 443 ssl;
        server_name example.com;
    }
}
```

## Fix

Disable `quic_bpf` by changing `quic_bpf on;` to `quic_bpf off;` in the `events {}` block. Alternatively, use [nginx-mod](https://www.getpagespeed.com/nginx-mod-a-better-faster-nginx-build) which includes the fix.
