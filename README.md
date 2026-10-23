# InforSuiteLB_sec

InforSuiteLB_sec is a tool to analyze **InforSuiteLB** configuration.
Its main goal is to prevent security misconfiguration and automate flaw detection.

Currently supported Python versions are 3.7 and newer.

## Overview

InforSuiteLB_sec audits your InforSuiteLB configuration for a wide range of
security issues, including injection & forgery,  TLS & encryption
problems, filesystem path exposures, header security, access-control gaps,
DNS/resolver misconfigurations, and performance pitfalls.

It runs locally or in CI/CD on every configuration change.

## Usage

Analyze a configuration file:

```bash
inforsuitelb_sec /etc/inforsuitelb/conf/inforsuitelb.conf
```

Read from stdin:

```bash
cat inforsuitelb.conf | inforsuitelb_sec -
```

### Useful options

| Option | Description |
|--------|-------------|
| `-f {console,text,json,checkstyle}` | Output format |
| `-l` | List available checks |
| `-c CONFIG_FILE` | Load defaults from a config file |
| `--deep` | Enable deep ReDoS analysis (requires the `deep` extra) |
| `--server` | Run in server mode (NDJSON over stdin/stdout) |

Run `inforsuitelb_sec --help` for the full list of options and available checks.

## Output formats

- `console` — rich terminal output (default when `rich` is installed)
- `text` — plain text
- `json` — machine-readable JSON
- `checkstyle` — CheckStyle XML, suitable for CI integration

## Development

Install the required dependencies (see `requirements.txt` and
`requirements.dev.txt`) and run the test suite:

```bash
pytest
```
