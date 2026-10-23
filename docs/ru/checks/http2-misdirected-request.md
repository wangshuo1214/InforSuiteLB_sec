---
title: "HTTP/2 Misdirected Request (421)"
description: "При использовании ssl_reject_handshake с http2 возвращайте 421 в / для предотвращения обработки запросов в неправильном серверном блоке."
---

# Защита от HTTP/2 Misdirected Request

_Идентификатор проверки Gixy: `http2_misdirected_request`_


## Обзор

Плагин `http2_misdirected_request` обнаруживает потенциально небезопасный паттерн, когда TLS `default_server` с `ssl_reject_handshake on;` имеет включённый HTTP/2, но **не** возвращает явно **421 (Misdirected Request)** из `location /`.

Это обычно используется как защитная мера для граничных случаев, когда запросы всё ещё могут обрабатываться в неожиданном серверном контексте.

## Что обнаруживается

Срабатывает, когда выполняются все следующие условия:

- присутствует `ssl_reject_handshake on;`
- сервер помечен как `default_server` (или `default`)
- HTTP/2 включён (`http2 on;` или `listen ... http2`)
- отсутствует `location /` (или `location = /`) с `return 421;`

## Примеры

### ❌ Плохо: Отсутствует защита с 421

```nginx
http {
    server {
        listen 443 ssl default_server;
        http2 on;
        ssl_reject_handshake on;
    }
}
```

### ✅ Хорошо: Явный возврат 421

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
