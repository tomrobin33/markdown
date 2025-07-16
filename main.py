import sys
import json
import time
import os

def save_markdown(content: str, output_dir: str = "./") -> str:
    timestamp = int(time.time() * 1000)
    filename = f"{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def main():
    # 启动时输出 ready 信号
    print(json.dumps({"status": "ready"}), flush=True)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            # 处理 JSON-RPC 协议
            if isinstance(data, dict) and "method" in data:
                method = data["method"]
                if method == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get("id"),
                        "result": {
                            "capabilities": {},
                            "protocolVersion": data.get("params", {}).get("protocolVersion", "2024-11-05"),
                            "serverInfo": {
                                "name": "markdown-mcp-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                    print(json.dumps(response), flush=True)
                elif method == "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get("id"),
                        "result": []
                    }
                    print(json.dumps(response), flush=True)
                elif method in ["markdown/generate", "markdown/save"]:
                    # 兼容 markdown/generate 和 markdown/save 方法
                    markdown_content = data.get("params", {}).get("markdown")
                    if not markdown_content:
                        response = {
                            "jsonrpc": "2.0",
                            "id": data.get("id"),
                            "error": {
                                "code": -32602,
                                "message": "Missing 'markdown' in params"
                            }
                        }
                    else:
                        filename = save_markdown(markdown_content, output_dir=".")
                        response = {
                            "jsonrpc": "2.0",
                            "id": data.get("id"),
                            "result": {"status": "ok", "filename": filename}
                        }
                    print(json.dumps(response), flush=True)
                else:
                    # 统一返回 -32601 Method not implemented
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get("id"),
                        "error": {
                            "code": -32601,
                            "message": f"Method '{method}' not implemented"
                        }
                    }
                    print(json.dumps(response), flush=True)
                continue
            # 兼容原有简单json格式
            markdown_content = data.get("markdown")
            if markdown_content:
                filename = save_markdown(markdown_content, output_dir=".")
                print(json.dumps({"status": "ok", "filename": filename}), flush=True)
                continue
            print(json.dumps({"status": "error", "msg": "No 'markdown' field"}), flush=True)
        except Exception as e:
            print(json.dumps({"status": "error", "msg": str(e)}), flush=True)

if __name__ == "__main__":
    main() 