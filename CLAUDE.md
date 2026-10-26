# InforSuiteLB_sec 项目说明

> 这个文件是给 AI 助手（Claude Code）的项目记忆：每次在本目录启动对话时会自动读取。
> 内容由人工维护，项目有大的变化时请同步更新。

## 项目是什么

一个 **InforSuiteLB 配置安全审计工具**：读取 InforSuiteLB 的配置文件（conf），自动发现
安全隐患（弱 SSL/TLS 配置、header 缺失、路径暴露、正则表达式风险、访问控制漏洞等），
可本地运行或接入 CI/CD。

- 前身是开源项目 **gixy / gixy-ng**（nginx 配置审计工具），本项目是它的**二开改名版**。
- Python 包名：`inforsuitelb_sec`；命令行工具名：`inforsuitelb_sec`。
- 品牌写法：产品叫 **InforSuiteLB**，代码/命令里一律用 `inforsuitelb_sec`（不要出现 nginx、gixy）。

## 二开改动约定（重要，git 历史里能看到）

- 已**去除 PyPI 相关内容**（不发布到 PyPI）。
- 已**去除 CVE 相关内容**（不要在输出/报告里引入 CVE 编号）。
- 已**取消 "Additional info" 信息的打印**。
- 所有面向用户的文案使用 inforsuitelb 品牌，不保留原 nginx/gixy 的字样。

## 常用命令（用项目自带的 .venv，Python 3.9）

```bash
# 跑全部测试（应全绿）
.venv/bin/pytest

# 分析一个配置文件
.venv/bin/inforsuitelb_sec demo_inforsuitelb.conf

# 列出所有内置检查项
.venv/bin/inforsuitelb_sec -l

# 代码风格检查
.venv/bin/ruff check inforsuitelb_sec/
```

注意：用户是 **Python 初学者**，解释命令时要说清每个部分的含义，并给可直接复制的完整命令。

## 代码结构

```
inforsuitelb_sec/            # 主包
├── __main__.py              # 入口：python -m inforsuitelb_sec
├── cli.py                   # 命令行参数解析、main()
├── core/                    # 核心框架
│   ├── config.py            # 配置解析（基于 inforsuitelbparse）
│   ├── context.py           # 遍历配置时的上下文
│   ├── manager.py           # 审计流程编排
│   ├── plugins_manager.py    # 插件加载与分发
│   ├── issue.py / severity.py# 发现项与严重级别模型
│   └── variable.py          # 变量/宏处理
├── directives/              # directive / block 数据模型
├── plugins/                 # ★ 36 个安全检查插件，一个文件 = 一项检查
└── _vendor/                 # 内嵌的第三方代码（勿动）
tests/                       # 测试目录，结构与主包一一对应（tests/plugins/ 等）
scripts/                     # 辅助脚本（兼容性检查、硬编码 IP 检查）
demo_inforsuitelb.conf       # 示例配置文件
```

## 开发惯例：新增/修改一项安全检查

- 在 `inforsuitelb_sec/plugins/` 下建一个文件，继承 `Plugin` 基类
  （参考 `weak_ssl_tls.py` 的写法）。
- 每个插件声明自己关心的 directive，框架在遍历配置时回调对应方法。
- 对应的测试放在 `tests/plugins/`，命名与插件对应。
- 改完跑 `.venv/bin/pytest` 确认全绿再提交。

## 其他

- 代码风格用 ruff（配置见 `ruff.toml`），另有 bandit 安全扫描配置在 `pyproject.toml`。
- 支持 Docker 构建（见 `Dockerfile`）。
- 输出格式：console / text / json / checkstyle 四种。
