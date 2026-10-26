# InforSuiteLB_sec 安全检查详解

> 本文档已与代码（v2.0.3.3，共 **35 个内置检查项**）逐项核对。
> 每个检查项包含：问题说明、典型示例、修复建议，以及**代码实现逻辑**（该插件在源码中是怎么判定的）。

## 1. 如何理解 InforSuiteLB_sec

InforSuiteLB_sec 是 InforSuiteLB 配置静态分析器。`InforSuiteLB -t` 主要检查语法和配置可加载性；InforSuiteLB_sec 会进一步检查配置模式是否可能导致 SSRF、响应头注入、路径穿越、访问控制绕过、TLS 加固不足等问题。

- **告警不等于已证实漏洞**：静态分析可能产生误报，也可能无法覆盖运行时逻辑。
- **未告警不等于安全**：工具只覆盖已实现的规则，不能代替渗透测试和业务逻辑审查。
- **修复后要验证**：先运行 `InforSuiteLB -t`，再执行 InforSuiteLB_sec，最后通过测试请求和响应头验证真实行为。

## 2. Security Checks 总览

下表"严重级别"列与代码实际输出一致（`LOW` / `MEDIUM` / `HIGH`，个别检查按命中情况分档）。

| 检查项 | 检查 ID | 严重级别 | 主要风险 |
|---|---|---|---|
| SSRF | `ssrf` | HIGH | 用户影响上游地址，代理访问非预期目标 |
| HTTP Response Splitting | `http_splitting` | HIGH | CR/LF 注入响应头或响应内容 |
| Origin/Referer 校验 | `origins` | LOW / MEDIUM / HIGH | 来源校验正则可被绕过 |
| `add_header` 重定义 | `add_header_redefinition` | LOW（安全头被丢弃时 MEDIUM） | 子级配置导致安全头丢失 |
| Host Header Spoofing | `host_spoofing` | MEDIUM | 不可信 Host 影响跳转、缓存或上游逻辑 |
| `valid_referers` 中的 `none` | `valid_referers` | HIGH | 缺少 Referer 的请求也被允许 |
| 多行响应头 | `add_header_multiline` | LOW / HIGH | 动态变量导致响应头注入或头部被截断 |
| 文件系统根目录暴露 | `filesystem_root_exposure` | MEDIUM | 错误的文件路径映射扩大可访问范围 |
| Alias 路径穿越 | `alias_traversal` | MEDIUM / HIGH | `alias` 与 `location` 路径拼接不当 |
| Location 中危险的 `if` | `if_is_evil` | HIGH | rewrite 阶段控制流产生意外行为 |
| Allow 没有 Deny | `allow_without_deny` | HIGH | IP 白名单未形成预期的默认拒绝 |
| `return` 绕过 Allow/Deny | `return_bypasses_allow_deny` | MEDIUM | 访问控制规则未按预期执行 |
| 用 `add_header` 设置 Content-Type | `add_header_content_type` | LOW | 头部与实际 MIME 类型不一致 |
| `proxy_pass` 路径规范化 | `proxy_pass_normalized` | MEDIUM | 前后端对路径解码/规范化理解不同 |
| `proxy_pass` 静态 DNS 解析 | `missing_resolver` | MEDIUM（命中云厂商域名时 HIGH） | 上游 DNS 变更后地址未按预期刷新 |
| InforSuiteLB 版本泄露 | `version_disclosure` | HIGH | 暴露版本或构建信息，便于指纹识别 |
| 缺少 `default_server` | `default_server_flag` | LOW | 未匹配 Host 的请求进入非预期站点 |
| `error_log off` | `error_log_off` | MEDIUM | 关闭错误日志，影响审计和排障 |
| map/geo 块缺少 default | `hash_without_default` | MEDIUM | 哈希映射块没有兜底值，未知键行为意外 |
| Location 正则未锚定 | `unanchored_regex` | LOW | 正则意外匹配更广泛 URI、匹配变慢 |
| ReDoS | `regex_redos` | HIGH | 特制输入导致正则匹配消耗过多 CPU |
| 无效正则捕获组 | `invalid_regex` | MEDIUM | 捕获组引用错位，路由或变量值异常 |
| 外部 DNS Resolver | `resolver_external` | HIGH | 运行时 DNS 依赖外部解析器，存在投毒风险 |
| HSTS 缺失或较弱 | `hsts_header` | MEDIUM（缺失）/ LOW（max-age 过短） | HTTPS 降级或首次访问被劫持风险 |
| 弱 SSL/TLS | `weak_ssl_tls` | HIGH / MEDIUM / LOW | 允许过时协议或不安全密码套件 |
| HTTP/2 421 误导向请求 | `http2_misdirected_request` | LOW | 多域名/连接复用场景处理不当 |
| OCSP Stapling 缺少 Resolver | `ssl_stapling_without_resolver` | MEDIUM | 证书状态查询无法正常解析 |
| Let's Encrypt OCSP Stapling | `ssl_stapling_letsencrypt` | LOW | 对证书链/OCSP 配置的适用性提示 |
| 后量子 `ssl_ecdh_curve` 启动问题 | `ssl_ecdh_curve` | HIGH | 不兼容曲线配置可能导致 InforSuiteLB 无法启动 |
| Status 页面暴露 | `status_page_exposed` | MEDIUM | 运行状态、连接等信息被未授权访问 |
| QUIC BPF Reuseport | `quic_bpf_reuseport` | HIGH | 多 worker + QUIC reload 后约 50% 连接被丢 |
| `keepalive_requests` 过低 | `low_keepalive_requests` | LOW | 长连接复用请求数过少，性能下降 |
| 正则 location 可改为精确匹配 | `regex_exact_match` | LOW | 可用更快的精确匹配替代的正则 |
| `try_files` 未配 `open_file_cache` | `try_files_is_evil_too` | MEDIUM | 每次请求都做文件检查，产生性能开销 |
| rlimit 与连接数不匹配 | `worker_rlimit_nofile_vs_connections` | MEDIUM | 文件句柄数不足导致连接被拒绝 |

---

## 3. 各检查项详细说明

### 3.1 SSRF（Server-Side Request Forgery 服务端请求伪造）

- **问题说明：** 如果客户端能够影响 `proxy_pass` 的协议、主机或路径，InforSuiteLB 可能替攻击者向非预期目标发起请求。目标可能包括内网服务、云元数据端点或其他本不应由外部访问的服务。

- **常见危险模式：** 把用户输入通过正则捕获后直接拼进 `proxy_pass`；即使 location 带 `internal`，若可由不安全的 rewrite、`error_page` 或上游 `X-Accel-Redirect` 间接触发，仍需检查。

- **不推荐示例：**
  ```nginx
  location ~ ^/proxy/(.*)/(.*)$ {
      proxy_pass $1://$2;
  }
  ```

- **建议做法：**
  - 尽量使用固定的 `upstream` 主机，不接受用户控制的目标地址。
  - 目标集合有限时，用 `map` 将允许值映射到固定上游。
  - 真正仅供内部调用的 location 使用 `internal;`，并审查所有内部跳转入口。
  - 如业务必须代理动态目标，使用严格的允许列表、规范化和服务端签名机制；不能只靠简单字符串过滤。

- **代码实现逻辑：** 插件订阅 `proxy_pass` 指令，先用正则把参数拆成 `scheme`（如 `http://`）和 `host` 两段；如果当前 location 标记了 `internal` 则跳过。否则对这两段做变量追踪（`compile_script`），只要其中某个变量"可能包含点号"（说明它可被用户输入控制、能拼出任意主机名）就报 HIGH，并把变量的来源指令链一起展示在报告中。

### 3.2 HTTP Response Splitting（HTTP 响应拆分）

- **问题说明：** 不可信数据包含 CR/LF（回车/换行，通常是 `%0d%0a`）并被拼入响应头或其他 HTTP 消息字段时，可能注入额外响应头，严重时影响缓存或响应边界。

- **常见位置：** `add_header`、`proxy_set_header`、`return`、`rewrite`、`proxy_pass`；尤其关注从 URI 解码而来的 `$uri`、`$document_uri` 和正则捕获变量。

- **不推荐示例：**
  ```nginx
  location ~ ^/v1/(?<action>[^.]*)\.json$ {
      add_header X-Action $action;
  }
  ```
  `[^.]*` 并不排除换行字符，因此不能保证捕获值安全。

- **建议做法：**
  - 不把原始用户输入直接写入响应头。
  - 使用明确的字符白名单，例如仅允许 `[A-Za-z0-9_-]+` 的业务标识。
  - 避免将解码后的 `$uri` 用于构造头部；选择变量前要理解它的编码和规范化语义。
  - 对必须动态输出的值，在应用层进行严格验证和正确编码。

- **代码实现逻辑：** 插件订阅 `rewrite`、`return`、`add_header`、`proxy_set_header`、`proxy_pass` 五类指令，取出其中待输出的字符串值（`proxy_pass` 取第 1 个参数，其余取第 2 个）。再对字符串里的每个变量做追踪，若该变量"可能包含换行符 `\n`"（非 `proxy_*` 类指令还额外检查 `\r`）就报 HIGH，并附上变量提供方的指令链，定位换行是从哪个用户输入传进来的。

### 3.3 Origin & Referer Validation（来源校验问题）

- **问题说明：** 使用 `Origin` 或 `Referer` 判断请求是否来自可信站点时，正则过宽、未锚定、只匹配域名子串或忽略端口/协议，可能让恶意站点通过校验。

- **常见误区：** 把 `trusted.example.com.attacker.test` 当作 `trusted.example.com`；只检查字符串包含可信域名；把 Referer 当作唯一的身份验证机制。

- **不推荐配置**
  ```nginx
  if ($http_origin ~* ((^https://www\.yandex\.ru)|(^https://ya\.ru)$)) {
      add_header 'Access-Control-Allow-Origin' "$http_origin";
      add_header 'Access-Control-Allow-Credentials' 'true';
  }
  ```

- **建议做法：**
  - 对允许的 scheme、hostname 和必要端口进行精确解析和匹配，而不是只做子串判断。
  - 对状态变更请求使用 CSRF token、SameSite Cookie 等纵深防御。
  - `Origin`/`Referer` 可能缺失或被隐私策略剥离，缺失时应按业务安全模型明确拒绝还是允许，不能无意中放行。

- **代码实现逻辑：** 插件只处理形如 `if ($http_origin ~ ...)` / `if ($http_referer ~ ...)` 的条件（把变量名错写成 `$http_referrer` 会直接报 HIGH）。它用正则"反推"出能匹配该正则的测试字符串，并刻意构造两种恶意变体——后缀拼 `.evil.com`、前缀拼 `evil.com`——再解析这些变体的域名，如果能匹配过你的正则就说明它能被不可信域绕过。另外 `post_audit` 阶段还会识别 `map $http_origin ...` + `add_header Access-Control-Allow-Origin $var` 的组合，走同一套判定。支持 `--origins-domains`（指定你的可信注册域）、`--origins-https-only`、`--origins-lower-hostname` 三个命令行参数。

### 3.4 `add_header` Redefinition（响应头继承/重定义）

- **问题说明：** InforSuiteLB 的 `add_header` 继承行为容易被误解。通常只有当当前配置层级没有定义任何 `add_header` 时，才会继承上层的 `add_header` 指令；子级只新增一个头时，可能导致上层定义的其他安全头不再生效。

- **不推荐示例：**

  ```nginx
  server {
      add_header X-Content-Type-Options nosniff always;
      add_header Strict-Transport-Security "max-age=31536000" always;

      location /app/ {
          add_header X-App app;
      }
  }
  ```
  `/app/` 中的响应不会继承 server 级的其他 `add_header`。

- **建议做法：**
  - 在需要设置头部的每个层级明确列出完整集合，或采用经过验证的统一 include 模板。
  - 在适用的 InforSuiteLB 版本中评估 `add_header_inherit merge` 指令（插件识别到它会豁免本检查）。
  - 关注错误响应：根据需求使用 `always`。

- **代码实现逻辑：** 插件按 `server` / `location` / `if` 块逐个审计，对比"当前块的 add_header 名集合"和"父块的 add_header 名集合"，计算差集——父块有、当前块没有的头部就是被"截断"的头部。普通丢失报 LOW；但如果被丢的是 CSP、HSTS、X-Frame-Options 等安全头（代码内置了安全头名单），或 Cache-Control: no-store 这类条件性安全值，升级为 MEDIUM。可用 `--add-header-redefinition-headers` 参数限定只报告指定的头部。

### 3.5 Host Header Spoofing（Host 头伪造）

- **问题说明：** `$http_host` 通常反映客户端提交的 Host 头，可能包含非预期值。若将其用于重定向、生成绝对 URL、缓存键或转发给上游，可能导致 Host 头投毒、错误链接或密码重置链接被污染等问题。

- **不推荐配置**

  ```nginx
  location @app {
    proxy_set_header Host $http_host;
    # Other proxy params
    proxy_pass http://backend;
  }
  ```

- **建议做法：**

  - 使用明确的 `server_name` 和默认虚拟主机拒绝未知 Host。
  - 对应用所需的外部主机名使用固定配置或严格允许列表。
  - 转发 Host 时确认上游的信任边界；不要把客户端可控的 Host 当作已验证域名。

- **代码实现逻辑：** 插件订阅 `proxy_set_header` 指令，仅当第一个参数是 `Host`（大小写不敏感）时检查它的值：如果值等于 `$http_host`，或以 `$arg_` 开头（从 URL 参数取主机名，风险更高），就报 MEDIUM，并自动给出把 `$http_host` 替换为 `$host`（由 `server_name` 决定、不可被客户端任意伪造）的修复建议。

### 3.6 `valid_referers` 中的 `none`

- **问题说明：** InforSuiteLB 的 `valid_referers` 中，`none` 表示允许没有 Referer 头的请求被视为有效来源。若该判断被用于保护下载、热链控制或访问敏感资源，攻击者可能通过不发送 Referer 绕过限制。

- **不推荐配置**

  ```nginx
  location / {
      # 只允许没有 Referer 的请求
      valid_referers none;
  }
  ```

- **重要区别：** Referer 校验不是强身份认证，也不应作为保护敏感 API 的唯一控制。

- **建议做法：** 只有在明确接受缺失 Referer 的业务场景才使用 `none`；敏感资源应使用登录态、授权校验、签名 URL 或其他可靠机制。

- **代码实现逻辑：** 插件直接订阅 `valid_referers` 指令，遍历其参数列表，只要包含字面量 `none` 就报 HIGH，并附带"从参数中删掉 none"的修复补丁（重新生成一条不含 none 的 `valid_referers ...;` 指令）。

### 3.7 Multiline Response Headers（多行响应头）

- **问题说明：** 动态变量可能包含换行或由用户控制的多行内容；把这类值放入响应头可能造成响应头注入。它与 HTTP 响应拆分密切相关，但该检查聚焦于多行头部值。

- **不推荐配置**

  ```nginx
  add_header Content-Security-Policy "
      default-src: 'none';
      script-src data: https://yastatic.net;
      style-src data: https://yastatic.net;
      img-src data: https://yastatic.net;
      font-src data: https://yastatic.net;";

  more_set_headers -t 'text/html text/plain'
      'X-Foo: Bar
          multiline';
  ```

- **建议做法：** 响应头只使用受控常量或严格校验后的短值；不要把任意用户文本、换行符或未经验证的上游内容直接放进 `add_header`。

- **代码实现逻辑：** 插件订阅 `add_header` 以及 headers-more 模块的 `more_set_headers`，逐个检查头部值字符串中是否出现换行。分两种情况：换行后紧跟空格或 Tab（合法的折行续行写法）报 LOW；裸 `\n`（没有缩进续行）说明这个多行值会被 InforSuiteLB 截断成不完整头部，直接报 HIGH。

### 3.8 Filesystem Root Exposure（文件系统根目录暴露）

- **问题说明：** `root` 或路径拼接配置不当，可能让 URL 映射到比预期更广的文件系统范围，暴露配置文件、备份文件、源码或其他敏感文件。具体风险取决于 URI 映射、目录布局和权限。

- **不推荐配置**

  ```nginx
  location / {
      root /;
  }

  location /files/ {
      alias /;
  }
  ```

- **建议做法：**
  - 为站点配置专用的、最小化的静态文件目录。
  - 不把站点根目录指向操作系统根目录、应用源码根目录或包含秘密的目录。
  - 配合文件系统权限，禁止 InforSuiteLB worker 读取不必要的文件。
  - 明确处理隐藏文件、备份文件和敏感扩展名。

- **代码实现逻辑：** 插件订阅 `root` 和 `alias` 指令，取路径参数做归一化（`posixpath.normpath`）。如果归一化结果去掉所有 `/` 后是空字符串——也就是这个路径解析后正好是文件系统根 `/`——就报 MEDIUM。路径里含 `$` 变量的会跳过（无法静态判断）。

### 3.9 Alias Path Traversal（`alias` 路径穿越）

- **问题说明：** `alias` 与 `location` 的路径替换规则和 `root` 不同。尤其是正则/前缀 location 与 `alias` 的组合不正确时，URI 可能映射到预期目录之外，形成路径穿越或文件暴露。

- **常见风险配置：**
  ```nginx
  location /static {
      alias /srv/www/static/;
  }
  ```
  `location` 与 `alias` 的尾部斜杠不一致是常见问题模式之一；具体是否可利用还要看 URI 和版本行为。

- **建议做法：**
  ```nginx
  location /static/ {
      alias /srv/www/static/;
  }
  ```
  或根据目录映射需要使用 `root`。正则 location 使用 `alias` 时应仔细核对捕获组和文档规则。

- **代码实现逻辑：** 插件订阅 `alias`，向上找到父级 location。对前缀型 location（无修饰符或 `^~`）：只要 location 路径不以 `/` 结尾而 alias 以 `/` 结尾，就是经典穿越模式，报 HIGH；其他拼接问题报 MEDIUM。对正则型 location（`~` / `~*`）：把 alias 路径切成字面段和 `$1`/`$2` 捕获段，再回到 location 正则里定位每个捕获组的位置，检查"捕获组前面是否有斜杠边界、变量能否以 `.` 开头、能否包含 `/`"，按可利用程度组合判定 HIGH 或 MEDIUM。

### 3.10 Location 中的 `if is evil`

- **问题说明：** `if` 在 InforSuiteLB rewrite 模块中的语义与常规编程语言的 `if` 不完全相同。某些在 `location` 中使用 `if` 的写法可能改变处理阶段或导致意外的配置行为，出现错误响应、重写逻辑绕过或安全策略不一致。

- **不推荐配置**

  ```nginx
  location /crash {

      set $true 1;

      if ($true) {
          # fastcgi_pass here
          fastcgi_pass  127.0.0.1:9000;
      }

  }
  ```

- **建议做法：**
  - 优先使用 `try_files`、`map`、独立的 `location` 或在应用层实现复杂条件逻辑。
  - 并非所有 `if` 都必然有漏洞；应按具体指令组合和控制流判断。
  - 不要在未经测试的情况下机械删除所有 `if`。

- **代码实现逻辑：** 插件对每条指令检查其直接父块是不是 `if` 块：是才继续，否则跳过。在 `if` 块内部，只有 `rewrite ... last/redirect/permanent` 和 `return` 被认为是安全的；其他指令（如 `proxy_pass`、`fastcgi_pass`、`alias`、`set` 等）出现在 `if` 里、且这个 `if` 又位于 `location` 内时，就报 HIGH。

### 3.11 Allow Without Deny（只有 allow，没有 deny）

- **问题说明：** `allow`/`deny` 的规则顺序与默认策略可能和管理员预期不一致。若意图是只允许某些 IP，却没有最终的 `deny all;`，其他来源可能仍能访问。

- **不推荐示例：**

  ```nginx
  location /admin/ {
      allow 192.0.2.10;
      allow 192.0.2.11;
  }
  ```

- **注意：** `allow`/`deny` 是基于客户端地址的访问控制；若前面有反向代理，必须正确配置可信代理来源和真实客户端 IP 处理，否则可能信任可伪造的地址头。

- **代码实现逻辑：** 插件订阅 `allow` 指令，遇到 `allow` 时向上取它的直接作用域（跳过 include 嵌套），遍历该作用域的所有同级子指令，如果找不到任何一条 `deny` 就报 HIGH。两种情况豁免：`allow all;` 本身（无条件放行），以及嵌套 location 里对子 location 单独放行父级禁区的合法写法。附带自动修复：在最后一条 allow 后面补一行 `deny all;`。

### 3.12 `return` 绕过 Allow/Deny（`return` 与访问控制）

- **问题说明：** 在 InforSuite 请求处理流程中，同一作用域内的 `return` 会先于 `allow`/`deny` 访问控制生效，因此不能假设它一定会按预期经过后续的 IP 访问控制阶段。若把 `return` 当作访问控制策略的一部分，可能造成策略失效。

- **不推荐配置**

  ```nginx
  location / {
    allow 127.0.0.1;
    deny all;
    return 200 "hi";
  }
  ```

- **建议做法：** 把访问控制放在语义明确且实际会执行的阶段；不要仅靠 `return` 语句推断访问权限。对于敏感路径，使用明确的认证/授权方案。

- **代码实现逻辑：** 插件同时订阅 `allow` 和 `deny` 指令；每遇到一条，就在其父作用域（含嵌套父级）里递归查找是否存在 `return` 指令。只要同作用域内既有 allow/deny 又有 return，就报 MEDIUM，并把两条指令的位置都标出来，方便人工判断实际执行顺序。

### 3.13 用 `add_header` 设置 Content-Type

- **问题说明：** `add_header` 是添加响应头的指令，不是设置响应 MIME 类型的正确方式。用它设置 `Content-Type` 可能造成重复或不一致的头部，影响浏览器对内容的解释。

- **不推荐配置**

  ```nginx
  add_header Content-Type text/plain;
  ```

- **建议做法：** 通过 `types`、`default_type`、文件扩展名映射或应用上游正确设置 MIME 类型；需要防止 MIME 嗅探时可加 `X-Content-Type-Options: nosniff`。

- **代码实现逻辑：** 插件订阅 `add_header`，比较头部名是否为 `Content-Type`（大小写不敏感）。若是，再检查当前及所有父作用域里是否存在 `proxy_hide_header` / `fastcgi_hide_header` 等指令且专门隐藏了 Content-Type——这是合法覆盖后端 Content-Type 的模式，会豁免。否则报 LOW，并建议改用 `default_type`。

### 3.14 `proxy_pass` Path Normalization（代理路径规范化问题）

- **问题说明：** InforSuiteLB 与上游应用可能对 URI 解码、重复斜杠、点段、百分号编码和路径规范化采取不同处理方式。若前端授权检查的路径与后端实际处理路径不一致，可能出现访问控制绕过或请求路由差异。

- **不推荐配置**

  ```nginx
  location /api/ {
      # Includes a path component after the host
      proxy_pass http://backend/api/;  # Normalization/decoding may occur
  }
  ```

- **建议做法：**
  - 明确 `proxy_pass` 是否带 URI 部分，并理解其替换规则。
  - 让前端和上游对路径规范化采取一致策略。
  - 不要仅在 InforSuiteLB 上对一个路径字符串做授权，却让上游按不同规则解析。
  - 对编码斜杠、双重编码、点段、重复斜杠等边界情况进行回归测试。

- **代码实现逻辑：** 插件订阅 `proxy_pass`，先确认它位于 HTTP location 内（stream 模块、`=` 精确匹配 location 直接跳过），然后解析出 proxy_pass 里 host 后面是否带了路径。如果带了固定路径，且同 location 内存在 `rewrite ^ $request_uri;`（把原始 URI 原样回写），但 proxy_pass 的路径里没有使用 `$uri` 或 `$1` 这类变量来跟随重写后的 URI，就报 MEDIUM——这是经典的"前端做了解码规范化、上游收到的却是原始编码 URI"的不一致场景。

### 3.15 `proxy_pass` 静态 DNS 解析/缺少 Resolver

- **问题说明：** InforSuiteLB 对普通域名上游的解析通常在配置加载时完成；如果 DNS 地址变化，已加载的 worker 不会自动按业务期望刷新。使用变量形式的 `proxy_pass` 时，必须配置 `resolver` 才能进行运行时解析。

- **不推荐配置**

  ```nginx
  # This WON'T re-resolve without a resolver directive!
  set $backend api.example.com;
  proxy_pass http://$backend;  # ← Plugin will warn about missing resolver
  ```

- **建议做法：**
  - 固定上游且变更由发布流程管理时，可使用 `upstream` 并明确 reload 流程。
  - 需要动态解析时，配置可信 `resolver` 和适当的 `valid` 缓存策略；确认当前 InforSuiteLB 版本支持相应参数。
  - DNS 解析器应可信且可用，避免把解析失败变成大面积代理故障。

- **代码实现逻辑：** 插件订阅 `proxy_pass` / `fastcgi_pass` / `uwsgi_pass` / `scgi_pass` / `grpc_pass`。三种情形会告警：(1) 目标地址里用了 `$` 变量，但当前作用域及祖先找不到 `resolver` 指令；(2) 引用了 `upstream` 块，但块内的 `server` 指令没有 `resolve` 参数；(3) 固定域名在配置加载时一次性解析。域名分两类：命中内置云厂商名单（AWS/GCP/Azure/Cloudflare 等数十条）报 HIGH，其他普通外部域名报 MEDIUM；内网后缀（`.internal`、`consul`、K8s Pod 形态等）和 RFC 保留测试域名会豁免。

### 3.16 InforSuiteLB Version Disclosure（版本信息泄露）

- **问题说明：** `server_tokens on;` 或 `server_tokens build;` 会在错误页或 `Server` 响应头中暴露 InforSuiteLB 版本；部分构建还可能暴露更多构建信息。攻击者可用这些信息缩小已知漏洞范围。

- **建议配置：**
  ```nginx
  http {
      server_tokens off;
  }
  ```

- **边界：** 隐藏版本只是减少指纹信息，不能代替安全更新。发行版可能回补安全修复而保留旧的版本号。

- **代码实现逻辑：** 插件订阅 `server_tokens`：参数为 `on` 或 `build` 直接报 HIGH（附替换为 `off` 的修复）。另外在全配置扫描阶段：如果 http 级没有设置任何 `server_tokens`，就逐个检查每个 server 块——没有显式 `server_tokens off;` 的 server 块（默认值即 `on`）都会补报一条"Missing server_tokens"，并附在 `server {` 后插入 `server_tokens off;` 的修复。

### 3.17 Missing `default_server`（缺少默认虚拟主机）

- **问题说明：** 一个监听地址/端口上的请求如果没有匹配 `server_name`，会由该地址端口的默认 server 处理。若没有显式设置默认站点，配置文件顺序可能决定哪个站点接收未知 Host 请求。

- **建议做法：**
  ```nginx
  server {
      listen 80 default_server;
      server_name _;
      return 444;
  }
  ```
  HTTPS 场景还应考虑默认 TLS server、证书选择和未知 SNI/Host 的处理策略。

- **代码实现逻辑：** 插件在全配置扫描阶段工作（不按单条指令触发）。先归一化每个 `listen` 指令为"地址:端口"形式的 socket key（支持 IPv4、IPv6、通配 `*`），把监听同一 socket 的 server 分组成一类；如果一组里有 2 个以上 server，却没有任何一个带 `default_server` 标志，就对该组报 LOW，建议显式声明默认站点。

### 3.18 `error_log off`（关闭错误日志）

- **问题说明：** `error_log off;` 不是合法配置（`off` 不是合法的日志级别），会导致错误日志实际失效，削弱事件调查、异常诊断和安全审计能力。

- **建议做法：** 配置合适的错误日志路径和级别，例如 `error_log /var/log/inforsuitelb/error.log warn;`；保护日志文件权限、轮转策略和磁盘空间。生产环境不要为了消除日志噪音而完全关闭错误日志。

- **代码实现逻辑：** 插件订阅 `error_log` 指令，只看第一个参数是否为字面量 `off`——是则报 MEDIUM。提供两种修复：改为写入有效路径（默认给出 `/var/log/InforSuiteLB/error.log warn`），或者如果确实想丢弃日志，改为 `/dev/null crit`。

### 3.19 map/geo 块缺少 Default（哈希映射兜底值）

- **问题说明：** `map` 和 `geo` 块用"键 → 值"的查表方式工作。如果块内没有 `default` 项，任何未匹配到的键都会得到未定义/空值，可能让访问控制黑白名单、限流 key 等逻辑在边界输入下产生意外行为（例如 `map $uri $limit { /admin 1; }` 没有 default 时，未知 URI 的 `$limit` 为空串而非 0）。

- **不推荐配置**

  ```nginx
  # No default → unknown keys inherit nothing/surprising behavior
  map $request_uri $allowed {
      /admin 0;
  }

  # No default in geo
  geo $block_client {
      192.0.2.0/24 1;
  }
  ```

- **建议做法：** 为每个 `map` / `geo` 块显式写一行 `default`，并让默认值对应"最安全"的那个分支（通常是拒绝方向）。

- **代码实现逻辑：** 插件订阅 `map` 和 `geo` 块，沿 include 收集块内所有映射项，判断是否存在源值为 `default`、目标值非空的项。geo 块无论有几条映射都强制要求 default；map 块有个豁免——非 default 映射项只有 1 条时不报（这种写法常用于"空键禁用 limit_req/limit_conn"的合法场景）。缺失时报 MEDIUM。注意：本检查**不**涉及哈希表大小参数（`*_hash_max_size`、`*_hash_bucket_size`）。

### 3.20 Unanchored Regex in Location（未锚定的 Location 正则）

- **问题说明：** `location ~` 的正则若未使用适当的起止锚点，不仅可能匹配到比预期更广的 URI 子串，还会让 InforSuiteLB 在多个 location 之间逐个扫描比对，拖慢请求处理。

- **不推荐配置：**

  ```nginx
  location ~ \.php {
      # ...
  }
  ```

- **建议做法：** 根据路由目的使用 `^`、`$` 等锚点，例如对 PHP 文件路由使用明确的文件名模式，并结合 `try_files`/文件存在性检查。锚点设计要符合真实 URL 需求。

- **代码实现逻辑：** 插件订阅 `location` 块，只处理正则型 location（modifier 为 `~` 或 `~*`）。调用 location 对象的 `needs_anchor()` 方法判断该正则路径是否缺少首尾锚点（如 `\.php` 应写成 `\.php$`），缺锚时报 LOW，提示加上锚点以加速匹配并避免意外匹配子串。

### 3.21 ReDoS（正则表达式拒绝服务）

- **问题说明：** 某些复杂正则在特制输入下会触发大量回溯，消耗 CPU，造成请求延迟甚至服务拒绝。InforSuiteLB 使用 PCRE/PCRE2 的具体行为取决于构建和版本。

- **高风险模式特征：** 嵌套量词、重叠的重复分组、多个可匹配相同字符的分支，尤其用于匹配攻击者可控的 URI。

- **不推荐配置**

  ```nginx
  # BAD - (a+)+ causes exponential backtracking
  location ~ ^/(a+)+$ {
      return 200;
  }

  # BAD - nested groups with quantifiers
  location ~ ^/((ab)+)+/files$ {
      return 200;
  }

  # BAD - star inside plus
  location ~ ^/(a*)+/path$ {
      return 200;
  }
  ```

- **建议做法：**
  - 简化正则，避免不必要的嵌套重复和歧义。
  - 尽可能用前缀 location、精确匹配或简单字符白名单替代复杂正则。
  - 对 URI 长度和请求速率设置合理限制；不要将其作为修复坏正则的唯一措施。
  - 加 `--deep` 参数可启用更精确的自动机分析（需额外安装 ReDoctor 库）。

- **代码实现逻辑：** 插件从 `location`、`if`、`rewrite`、`server_name`、`map` 五类指令中提取出所有正则表达式（自动识别 `~` / `~*` 大小写不敏感），然后用项目内置的正则解析器（sre_parse）做三类静态检测：(1) 嵌套量词，如 `(a+)+`（指数级回溯）；(2) 重叠分支，如 `(a|ab)+`（多项式回溯）；(3) 相邻重叠贪婪量词，如 `.*.*end`。对有安全边界（首个字符已确定不匹配）的情形会排除以减少误报。命中即报 HIGH。开启 `--regex-redos-deep` 或全局 `--deep` 后，会改用 ReDoctor 自动机 + 有界 fuzzing 做更精确的分析。

### 3.22 Invalid Regex Capture Groups（无效捕获组）

- **问题说明：** 正则捕获组的数量、命名或引用方式不一致，可能导致 `$1`、`$2` 或命名变量取值错误，从而影响重写、代理目标、文件路径或响应头。

- **不推荐配置**

  ```nginx
  server {
      location / {
          # (?i) is a case-insensitive flag, NOT a capturing group
          rewrite "(?i)/" $1 break;
      }
  }
  ```

- **建议做法：** 优先使用命名捕获组（如 `(?<name>...)`），减少数字捕获组因正则修改而发生错位；确保每个引用都来自正确的匹配上下文。

- **代码实现逻辑：** 插件订阅 `rewrite` 和 `set` 指令，用正则 `\$([1-9]\d*)` 抓出所有 `$1`、`$2` 形式的反向引用。对 `rewrite`：取 pattern 反推它实际定义了几个捕获组，"引用了但没定义"的差集非空就报 MEDIUM。对 `set`：沿父链向上找最近的 `if` 块，用 if 的正则作为组来源做同样的差集判断。正则本身解析失败时静默跳过。

### 3.23 External DNS Resolver Security（外部 DNS Resolver）

- **问题说明：** `resolver` 指定的 DNS 服务器会影响 InforSuiteLB 的运行时域名解析。使用公共解析器（如 `1.1.1.1`、`8.8.8.8`）意味着运行时域名查询会走出本机网络，带来 DNS 投毒、审计盲区和数据泄露方面的问题。

- **不推荐配置**

  ```nginx
  # Public, external resolvers (unsafe)
  resolver 1.1.1.1 8.8.8.8;

  # Variable-based upstream resolution depends on resolver
  set $backend upstream.internal.example;
  location / {
      proxy_pass http://$backend;
  }
  ```

- **建议做法：**
  - 优先使用组织管理的递归解析器或平台提供的可信 DNS。
  - 限制解析器网络访问，按环境管理超时和缓存有效期。
  - 不要把 `1.1.1.1` 或 `8.8.8.8` 之类公共解析器视为所有企业环境的通用最佳实践；应符合网络和合规要求。

- **代码实现逻辑：** 插件订阅 `resolver` 指令，调用指令对象的 `get_external_nameservers()` 方法，判断参数中是否包含非本地（外部）DNS 服务器。只要存在外部地址就报 HIGH（DNS 投毒风险），并给出两种修复：替换为 `127.0.0.53`（systemd-resolved 本地桩）或 `127.0.0.1`。

### 3.24 Missing or Weak HSTS（HSTS 缺失或较弱）

- **问题说明：** HSTS（HTTP Strict Transport Security）让浏览器在策略有效期内强制使用 HTTPS，降低后续访问被降级到 HTTP 的风险。缺少 HSTS 或 `max-age` 过短会削弱保护。

- **建议配置示例：**
  ```nginx
  add_header Strict-Transport-Security "max-age=31536000" always;
  ```

- **注意：** 仅在 HTTPS 响应中发送 HSTS。`includeSubDomains` 会影响所有子域，`preload` 涉及额外的长期承诺；确认全部子域均支持 HTTPS 后再启用。不要在未验证的域名上盲目使用 preload。

- **代码实现逻辑：** 插件在全配置扫描阶段工作。先从 http 块开始，逐 server 检查：只处理 `listen` 带 `ssl` 或端口 443 的 SSL server（`ssl_reject_handshake on` 的会跳过，因为它不回正常响应）。继承策略与真实行为一致——server 自己定义了任何 `add_header` 就只看 server 级，否则回退到 http 级。然后在有效头部列表里找 `Strict-Transport-Security`：找不到报 MEDIUM；找到了但 `max-age` 小于 15768000（6 个月）报 LOW。附一键修复：改为 `max-age=31536000; includeSubDomains`。

### 3.25 Weak SSL/TLS Configuration（弱 SSL/TLS 配置）

- **问题说明：** 允许已弃用协议、弱密码套件或不恰当的 TLS 参数，可能降低传输加密的安全性。现代部署一般应禁用 SSLv3、TLS 1.0 和 TLS 1.1，并按客户端兼容性与组织标准选择 TLS 1.2/1.3。

- **配置方向示例：**
  ```nginx
  ssl_protocols TLSv1.2 TLSv1.3;
  ```

- **建议做法：**

  - 按官方建议管理密码套件、会话票据、证书链和私钥权限。
  - 不要直接照搬过时的 cipher 列表；TLS 1.3 的套件配置方式与 TLS 1.2 不完全相同。

- **代码实现逻辑：** 插件订阅 `ssl_protocols`、`ssl_ciphers`、`ssl_prefer_server_ciphers` 三条指令。`ssl_protocols` 参数与内置禁用名单（SSLv2/SSLv3/TLSv1/TLSv1.1）求交集，非空报 HIGH。`ssl_ciphers` 按 `:` 切分后逐项与弱算法名单（EXPORT/NULL/DES/3DES/RC4/MD5/ADH/LOW 等）匹配；纯 TLSv1.3 部署会跳过（因为 ssl_ciphers 对 TLSv1.3 不生效）。`ssl_prefer_server_ciphers on` 在没有配套 `ssl_conf_command` 时报 LOW。全配置扫描阶段还会对 SSL server 检查"http 和 server 两级都没设 ssl_protocols / ssl_ciphers"的缺失情形，报 MEDIUM 并附 Mozilla 推荐配置串。

### 3.26 HTTP/2 Misdirected Request（421）

- **问题说明：** HTTP/2 连接复用可能让浏览器在同一连接上尝试访问多个源站。如果 TLS 证书、SNI、Host 与虚拟主机配置不匹配，可能出现请求被路由到错误站点或需要返回 `421 Misdirected Request` 的情况。

- **不推荐配置**

  ```nginx
  http {
      server {
          listen 443 ssl default_server;
          http2 on;
          ssl_reject_handshake on;
      }
  }
  ```

- **建议做法：** 确保每个 HTTPS 虚拟主机的 `server_name`、证书 SAN、SNI 和上游路由匹配；不要让默认站点意外承接不相关域名。

- **代码实现逻辑：** 插件在全配置扫描阶段工作，需要四个条件**同时**满足才报 LOW：(a) server 里有 `ssl_reject_handshake on;`；(b) 某个 `listen` 带 `default_server`；(c) 启用了 HTTP/2（`http2 on;` 或 listen 带 `http2` 参数）；(d) 没有任何 `location /` 或 `location = /` 内部带 `return 421;`。命中后给出的自动修复就是补一个 `location / { return 421; }`。

### 3.27 OCSP Stapling Without Resolver

- **问题说明：** 开启 OCSP Stapling 时，InforSuiteLB 需要在线解析证书状态响应服务（OCSP Responder）的域名。没有适当的 `resolver` 时，状态查询无法进行，stapling 会静默失效。

- **不推荐配置**

  ```nginx
  server {
      listen 443 ssl;
      server_name example.com;

      ssl_certificate     /etc/ssl/certs/example.com.pem;
      ssl_certificate_key /etc/ssl/private/example.com.key;

      ssl_stapling on;
      ssl_stapling_verify on;
  }
  ```

- **建议配置方向：**
  ```nginx
  resolver 192.0.2.53 valid=300s;
  ssl_stapling on;
  ssl_stapling_verify on;
  ```
  `192.0.2.53` 仅为文档示例地址，实际必须替换为环境中可信、可达的 DNS 解析器；并按证书链配置可信 CA。

- **代码实现逻辑：** 插件按 server 块审计。先确认是 SSL server（listen 参数含 `ssl` / `quic` / `http3`）；再解析 `ssl_stapling` 的生效值（server 级没有就沿父链向 http/root 级继承），不是 `on` 直接跳过；最后在 server 自身及所有祖先作用域里查找 `resolver` 指令——找不到就报 MEDIUM。

### 3.28 OCSP Stapling with Let's Encrypt Certificate

- **问题说明：** Let's Encrypt 已于 2025 年 8 月起关停其 OCSP 响应服务（ACME 社区推动的"无 OCSP"方向）。如果你的证书来自 Let's Encrypt（证书路径在 `/etc/letsencrypt/` 下）却还开着 `ssl_stapling on;`，stapling 实际上不会产生任何效果，属于无效配置。

- **不推荐配置**

  ```nginx
  server {
      listen 443 ssl;
      server_name example.com;

      ssl_certificate         /etc/letsencrypt/live/example.com/fullchain.pem;
      ssl_certificate_key     /etc/letsencrypt/live/example.com/privkey.pem;
      ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

      resolver 127.0.0.1 valid=300s;

      ssl_stapling on;         # nothing to staple
      ssl_stapling_verify on;
  }
  ```

- **建议做法：** Let's Encrypt 证书直接关闭 stapling（`ssl_stapling off;`）；其他 CA 的证书以其官方文档和实际 InforSuiteLB/OpenSSL 日志为准，不要因为启用了 `ssl_stapling on` 就认定客户端一定收到 stapled 响应。

- **代码实现逻辑：** 插件骨架与 3.27 相同：先确认 SSL server 且 `ssl_stapling` 生效值为 `on`；然后收集 server 及所有祖先作用域下 `ssl_certificate` 和 `ssl_trusted_certificate` 指令的路径，只要有任意一条路径以 `/etc/letsencrypt/` 开头（硬编码前缀），就报 LOW，并附带把 `ssl_stapling` 改为 `off` 的修复补丁。

### 3.29 后量子曲线配置导致 InforSuiteLB 无法启动

- **问题说明：** 将 OpenSSL 不认识的曲线名称写入 `ssl_ecdh_curve`（例如旧版本上直接写 `X25519MLKEM768`），master 进程会在启动时拒绝整张曲线表，导致配置测试失败、服务起不来。

- **不推荐配置**

  ```nginx
  server {
      listen 443 ssl;
      server_name example.com;

      ssl_certificate     /etc/ssl/certs/example.com.pem;
      ssl_certificate_key /etc/ssl/private/example.com.key;

      # One unknown name and the master process refuses to start
      ssl_ecdh_curve X25519MLKEM768:X25519:prime256v1;
  }
  ```

- **建议做法：**
  - 对后量子混合曲线（MLKEM / Kyber），在前面加 `?` 容错前缀（如 `?X25519MLKEM768`），让不认识它的 OpenSSL 版本跳过而不是报错。
  - 变更前执行 `InforSuiteLB -t`，并确保有回滚方案。

- **代码实现逻辑：** 插件订阅 `ssl_ecdh_curve`，把参数按 `:` 切分成曲线列表逐个检查：以 `?` 开头的直接放过（这就是 OpenSSL 3.3+ 的容错写法）；否则曲线名大写后只要包含 `MLKEM` 或 `KYBER` 子串，就报 HIGH。自动修复是给所有 risky 曲线前面加 `?`。

### 3.30 Status Page Exposed（状态页面暴露）

- **问题说明：** InforSuiteLB 状态页（`stub_status`）暴露活动连接、请求计数、读写等待状态等运营信息。虽然这些信息不一定直接包含业务数据，但可能帮助攻击者推断负载、流量模式和服务状态。

- **不推荐配置**

  ```nginx
  location /status {
      stub_status;
  }
  ```

- **建议做法：**
  - 使用 `stub_status` 时限制到可信监控网络、localhost 或经过认证的监控系统。
  - 不要将状态页无保护地暴露在公网。
  - 结合网络 ACL、认证和最小权限。

- **代码实现逻辑：** 插件订阅 `stub_status` 指令。如果所在 server 全部是 `unix:` socket 监听（本地内部使用）直接放过；否则取 stub_status 所在的父作用域，检查两件事：是否出现过任意 `allow` 指令，以及是否有 `deny all;` 兜底。两者缺一就报 MEDIUM，并在 reason 里说明缺的是白名单还是缺了 deny all。

### 3.31 QUIC BPF Reuseport

- **问题说明：** 当 `quic_bpf on;` 与 QUIC 监听 socket 上的 `reuseport` 同时使用、且配置了多个 worker 进程时，每次 reload 之后约有一半 QUIC 连接会被静默丢弃（上游已知问题 #425）。

- **不推荐配置**

  ```nginx
  worker_processes auto;

  quic_bpf on;
  events {}

  http {
      server {
          listen 443 quic reuseport;
          listen 443 ssl;
          server_name example.com;
      }
  }
  ```

- **建议做法：** 二选一：关闭 `quic_bpf`，或者把 QUIC 监听上的 `reuseport` 去掉。对照所用 InforSuiteLB QUIC 实现、Linux 内核与发行版文档，在目标系统实测多 worker 下的 UDP/QUIC 负载分配。

- **代码实现逻辑：** 插件在全配置扫描阶段工作，三个条件全部满足才报 HIGH（只报一次）：(1) 主上下文有 `quic_bpf on;`；(2) `worker_processes` 显式配置且不等于 1（`auto` 或 >1 都算，未配置则默认为 1，安全跳过）；(3) 任意 server 的 `listen` 参数同时包含 `quic` 和 `reuseport`。附带的自动修复是把 `quic_bpf` 改为 `off`。

### 3.32 `keepalive_requests` 过低（新增）

- **问题说明：** `keepalive_requests` 决定一个长连接上最多能复用处理多少个请求。默认值（100）在高并发站点下会导致连接频繁重建、TCP 和 TLS 握手开销增大。

- **不推荐配置：**
  ```nginx
  http {
      keepalive_requests 100;
  }
  ```

- **建议做法：** 至少设为 `1000`；高流量站点可设到 `10000`。

- **代码实现逻辑：** 插件订阅 `keepalive_requests`，把参数转成整数，小于硬编码阈值 1000 就报 LOW。提供两个自动修复选项：改成 1000 或改成 10000。注意它只审计当前这条指令本身，不做 http/server/upstream 之间的继承分析。

### 3.33 正则 location 可改为精确匹配（新增）

- **问题说明：** 有些 location 虽然写成正则形式（`location ~ ^/api/health$`），但它实际上精确对应一个固定路径。InforSuiteLB 对 `location = /path` 精确匹配是 O(1) 查表，比逐条正则比对快得多。

- **不推荐配置：**
  ```nginx
  location ~ ^/api/health$ {
      proxy_pass http://backend;
  }
  ```

- **建议做法：** 改成 `location = /api/health { ... }`。

- **代码实现逻辑：** 插件订阅 `location` 块，只处理大小写敏感的正则 location（`~`；`~*` 不报，因为精确匹配不区分大小写语义不兼容）。把正则反推回字面路径——只有当正则去掉锚点后恰好等价于一个固定字符串（如 `^/api/health$`）时，才报 LOW，并附自动修复：把 `location ~ ^/api/health$` 整行替换为 `location = /api/health`。

### 3.34 `try_files` 未配 `open_file_cache`（新增）

- **问题说明：** `try_files` 会对每个请求按顺序检查文件是否存在，这在没有启用 `open_file_cache` 时会转化为每请求一次磁盘 stat 系统调用，造成可观的性能开销。

- **不推荐配置：**
  ```nginx
  location /static/ {
      alias /srv/www/static/;
      try_files $uri $uri/ =404;
  }
  ```

- **建议做法：** 搭配启用 `open_file_cache`（并配合 `open_file_cache_valid`、`open_file_cache_min_uses` 等参数）缓存文件存在性检查结果。

- **代码实现逻辑：** 插件订阅 `try_files`，沿当前作用域向上（location → server → http）查找 `open_file_cache` 指令：找不到，或找到但参数为 `off`，就报 MEDIUM。自动修复是在 try_files 后面追加一行 `open_file_cache max=1000 inactive=20s;`（推荐值硬编码）。它只查"有没有开"，不校验 cache 的子参数是否合理。

### 3.35 rlimit 与连接数不匹配（新增）

- **问题说明：** 每个 InforSuiteLB 连接会同时占用读端和写端两个文件描述符，因此 `worker_rlimit_nofile`（进程可打开的文件句柄上限）应至少是 `worker_connections` 的两倍。设置过小或缺失会在高并发下直接拒绝新连接。

- **不推荐配置：**
  ```nginx
  events {
      worker_connections 1024;
  }
  ```
  （此时未配 `worker_rlimit_nofile`，受系统默认 rlimit 限制。）

- **建议做法：**
  ```nginx
  worker_rlimit_nofile 20480;

  events {
      worker_connections 10240;
  }
  ```

- **代码实现逻辑：** 插件订阅 `worker_connections` 指令，取其数值后沿作用域向上找 `worker_rlimit_nofile`。两种情况报 MEDIUM：(1) 找到了但数值小于 `worker_connections × 2`；(2) 根本没配 `worker_rlimit_nofile`。该检查没有自动修复（阈值和环境相关）。

---

## 4. 使用说明

以下内容基于 `inforsuitelb_sec --help` 的实际输出（版本 v2.0.3.3）。

### 4.1 基本语法

```bash
inforsuitelb_sec [全局选项] [插件选项] <配置文件> [<配置文件2> ...]
```

- 位置参数是一个或多个 **被审计的 InforSuiteLB 配置文件**；不写时默认尝试读 `/usr/local/InforSuiteLB/conf/InforSuiteLB.conf`。
- 位置参数写 `-` 表示从 **标准输入（stdin）** 读取配置，方便管道使用。

> 本项目推荐用自带虚拟环境运行：`.venv/bin/inforsuitelb_sec ...`（`.venv/bin/` 是 Python 虚拟环境里的可执行文件目录，后面紧跟工具名）。

### 4.2 常用参数一览

| 参数 | 说明 |
|---|---|
| `-h`, `--help` | 显示帮助；**帮助输出最末尾的 `available checks` 列表就是全部 35 个内置检查项的 ID** |
| `-v`, `--version` | 显示版本号 |
| `-c FILE`, `--config FILE` | 指定**工具自身**的配置文件（不是被审计的配置） |
| `--write-config PATH` | 把当前命令行参数写入一个工具配置文件，下次直接 `-c` 复用 |
| `-l` / `-ll` / `-lll` | 按严重级别过滤：`-l`=LOW 及以上（默认），`-ll`=MEDIUM 及以上，`-lll`=只看 HIGH |
| `-f {console,text,json,checkstyle}` | 输出格式。终端直连默认 console，管道/重定向默认 text |
| `-o FILE` | 把报告写入文件而不是屏幕 |
| `-d`, `--debug` | 开启调试日志（排查解析问题时用） |
| `--deep` | 深度模式：启用更慢但更精确的检查（当前即 ReDoctor 深度 ReDoS 分析，需安装 ReDoctor 库） |
| `--checks a,b,c` | 只运行指定的检查项（逗号分隔） |
| `--skips a,b,c` | 跳过指定的检查项 |
| `--disable-includes` | 不展开配置里的 `include` 指令 |
| `--vars-dirs DIR1,DIR2` | 指定存放自定义变量 drop-in 文件的目录 |
| `--fix` | 自动把建议的修复写回配置文件（默认会生成 `.bak` 备份） |
| `--fix-dry-run` | 只显示将要应用的修复，不修改文件 |
| `--no-backup` | 配合 `--fix`，不生成 `.bak` 备份 |
| `--server` | 服务模式：通过 stdin/stdout 以 NDJSON 协议交互（供编辑器/平台集成） |

插件专属参数（只有定义了可调参数的检查才有）：

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--regex-redos-deep true/false` | 对 ReDoS 检查启用 ReDoctor 自动机深度分析 | false |
| `--add-header-redefinition-headers A,B` | 只报告被丢弃的这些响应头（逗号分隔） | 空（全部报告） |
| `--origins-domains example.com,foo.bar` | 声明你的可信注册域，供 origins 检查判断同源 | `*`（不做第三方域校验） |
| `--origins-https-only true/false` | origins/referer 只允许 https 协议 | false |
| `--origins-lower-hostname true/false` | 校验前把域名转小写 | true |

此外：

- 工具本身支持环境变量传参，前缀为 `INFORSUITELB_SEC_`，例如 `INFORSUITELB_SEC_ORIGINS_DOMAINS=example.com`。
- 默认会读取工具配置文件 `/etc/inforsuitelb_sec/inforsuitelb_sec.cfg` 和 `~/.config/inforsuitelb_sec/inforsuitelb_sec.conf`（存在才生效）。

### 4.3 输出报告字段

每条问题包含：

- `Problem: [检查ID] 摘要` —— 检查项 ID 与一句话标题
- `Severity` —— LOW / MEDIUM / HIGH
- `Description` —— 该类问题的通用说明
- `Reason` —— 在**当前配置**里具体命中了什么
- `Pseudo config` —— 触发问题的最小配置片段（含文件行号）

### 4.4 常用示例

```bash
# 1. 最基本：审计项目自带的示例配置
.venv/bin/inforsuitelb_sec demo_inforsuitelb.conf

# 2. 只看 HIGH 级别问题（接入 CI 时常用）
.venv/bin/inforsuitelb_sec -lll /etc/inforsuitelb/inforsuitelb.conf

# 3. 输出 JSON 到文件，方便脚本或平台解析
.venv/bin/inforsuitelb_sec -f json demo_inforsuitelb.conf -o report.json

# 4. 只跑某几个检查（逗号分隔检查 ID）
.venv/bin/inforsuitelb_sec --checks ssrf,weak_ssl_tls demo_inforsuitelb.conf

# 5. 跳过某几个检查
.venv/bin/inforsuitelb_sec --skips regex_redos,unanchored_regex demo_inforsuitelb.conf

# 6. 从 stdin 读取配置（不落地文件，例如远程拉取后审计）
curl -s http://example.com/inforsuitelb.conf | .venv/bin/inforsuitelb_sec -

# 7. 先预演自动修复（不改文件，只打印 diff）
.venv/bin/inforsuitelb_sec --fix-dry-run demo_inforsuitelb.conf

# 8. 确认无误后真正应用修复（自动生成 demo_inforsuitelb.conf.bak）
.venv/bin/inforsuitelb_sec --fix demo_inforsuitelb.conf

# 9. 深度 ReDoS 分析（需 pip 安装 redoctor）
.venv/bin/inforsuitelb_sec --deep demo_inforsuitelb.conf

# 10. 告诉 origins 检查你的可信域名，减少误报
.venv/bin/inforsuitelb_sec --origins-domains example.com,example.org demo_inforsuitelb.conf

# 11. checkstyle 格式输出，接入 CI 静态分析插件
.venv/bin/inforsuitelb_sec -f checkstyle demo_inforsuitelb.conf
```

### 4.5 退出码（用于 CI/CD 判断）

| 退出码 | 含义 |
|---|---|
| `0` | 审计完成，未发现任何问题 |
| `1` | 发现了问题（报告数量 > 0），或被审计的配置文件有语法/解析错误 |
| `2` | 启用了 `--deep` / `--regex-redos-deep` 但未安装 ReDoctor 库 |

典型 CI 用法：

```bash
.venv/bin/inforsuitelb_sec -lll -f checkstyle -o report.xml /etc/inforsuitelb/inforsuitelb.conf
# 退出码非 0 即失败，可据此阻断流水线
```
