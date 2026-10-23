---
title: "缺失或弱 HSTS 头部"
description: "确保 HTTPS 站点上有强 HSTS 配置。使用长 max-age 和 includeSubDomains 来阻止降级和 cookie 劫持风险。"
---

# 缺失或弱 HSTS 头部

_Gixy 检查 ID：`hsts_header`_


## 概述

`hsts_header` 插件检测 HTTPS 服务器上缺失或弱的 **HSTS** 配置。

HSTS（HTTP 严格传输安全）通过 `Strict-Transport-Security` 响应头传递，有助于保护用户免受：
- 协议降级攻击
- cookie 劫持

## 检测内容

### 1. 缺失 HSTS 头部

检测缺少以下配置的 HTTPS 服务器：

```nginx
add_header Strict-Transport-Security "...";
```

### 2. 弱 HSTS max-age

检测 `max-age` 少于 6 个月（15768000 秒）的 HSTS。

## 示例

### ❌ 错误：缺失 HSTS

```nginx
http {
    server {
        listen 443 ssl;
        # 缺失：add_header Strict-Transport-Security
    }
}
```

### ✅ 正确：HSTS max-age 为 1 年

```nginx
http {
    server {
        listen 443 ssl;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    }
}
```

## 注意事项

- 配置了 `ssl_reject_handshake on;` 的服务器会被跳过，因为它们永远不会发送 HTTP 响应头。
