<br />
<div align="center">
  <h3 align="center">Ollama Commit Message</h3>
  <p align="center">
    <br />
    <a href="https://github.com/yuchenyang1994/ollama-commit-message"></a>
    <br />
    <br />
  </p>
</div>

## About The Project

This is a [pre-commit](https://pre-commit.com/) hook. This is a pre-commit hook using ollama to write git commit messages.

## Getting Started

1. install [pre-commit](https://pre-commit.com/#install)

2. add the following to your .pre-commit-config.yaml:

```yaml
repos:
-   repo: https://github.com/yuchenyang1994/ollama-commit-message
    rev: v0.1.0
    hooks:
    -   id: ollama-commit-message
        args: [-m, "<ollama model>", "--host". "<Ollama Host: default: http://localhost:11434>"]
        verbose: true
```

3. install hooks

```sh
pre-commit install --hook-type commit-msg
```

Okay, AI will help you complete your message with every submission.
