---
title: "Отсутствующий или слабый заголовок HSTS"
description: "Обеспечьте надёжную настройку HSTS на HTTPS-сайтах. Используйте длительный max-age и includeSubDomains для защиты от атак понижения протокола и перехвата cookie."
---

# Отсутствующий или слабый заголовок HSTS

_Идентификатор проверки Gixy: `hsts_header`_


## Обзор

Плагин `hsts_header` обнаруживает отсутствующую или слабую конфигурацию **HSTS** на HTTPS-серверах.

HSTS (HTTP Strict Transport Security) передаётся через заголовок ответа `Strict-Transport-Security` и помогает защитить пользователей от:
- атак понижения протокола
- перехвата cookie

## Что обнаруживается

### 1. Отсутствующий заголовок HSTS

Обнаруживает HTTPS-серверы без:

```nginx
add_header Strict-Transport-Security "...";
```

### 2. Слабый max-age в HSTS

Обнаруживает HSTS с `max-age` менее 6 месяцев (15768000 секунд).

## Примеры

### ❌ Плохо: Отсутствует HSTS

```nginx
http {
    server {
        listen 443 ssl;
        # Отсутствует: add_header Strict-Transport-Security
    }
}
```

### ✅ Хорошо: HSTS с max-age 1 год

```nginx
http {
    server {
        listen 443 ssl;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    }
}
```

## Примечания

- Серверы с настройкой `ssl_reject_handshake on;` пропускаются, так как они никогда не отправляют HTTP-заголовки ответа.
