# MCP Markdown Stdio Server

这是一个基于 stdio 协议的 MCP 服务器，用于接收大模型生成的 markdown 文案，并保存为 markdown 文件。

## 使用方法

1. 进入项目目录：
   ```bash
   cd markdown
   ```
2. 运行服务器：
   ```bash
   python main.py
   ```
3. 通过标准输入发送 JSON 格式的请求，每行一个 JSON，例如：
   ```json
   {"markdown": "# 标题\n内容..."}
   ```
4. 程序会将 markdown 内容保存为以时间戳命名的 `.md` 文件，并在标准输出返回结果：
   ```json
   {"status": "ok", "filename": "1688888888888.md"}
   ```

## 依赖

- Python 3.7 及以上
- 无需额外依赖，仅用标准库 