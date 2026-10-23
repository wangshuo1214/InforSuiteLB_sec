---
title: "HTTP/2 Misdirected Request (421)"
description: "对于使用 http2 的默认 ssl_reject_handshake，在 / 返回 421 以防止在错误的 server 块中处理误导请求。"
---

# HTTP/2 Misdirected Request 保护

_Gixy 检查 ID：`http2_misdirected_request`_


## 概述

`http2_misdirected_request` 插件检测一种潜在不安全的模式，即 TLS `default_server` 启用了 `ssl_reject_handshake on;` 并启用了 HTTP/2，但**没有**在 `location /` 中显式返回 **421（Misdirected Request）**。

这通常用作边缘情况的防御性保护措施，在这些情况下，请求仍可能在意外的服务器上下文中被处理。

## 检测内容

当以下所有条件都为真时触发：

- 存在 `ssl_reject_handshake on;`
- 服务器被标记为 `default_server`（或 `default`）
- HTTP/2 已启用（`http2 on;` 或 `listen ... http2`）
- 没有 `location /`（或 `location = /`）执行 `return 421;`

## 示例

### ❌ 错误：缺少 421 保护

```nginx
http {
    server {
        listen 443 ssl default_server;
        http2 on;
        ssl_reject_handshake on;
    }
}
```

### ✅ 正确：显式返回 421

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
