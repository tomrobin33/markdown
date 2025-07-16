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
            markdown_content = data.get("markdown")
            if not markdown_content:
                print(json.dumps({"status": "error", "msg": "No 'markdown' field"}), flush=True)
                continue
            filename = save_markdown(markdown_content, output_dir=".")
            print(json.dumps({"status": "ok", "filename": filename}), flush=True)
        except Exception as e:
            print(json.dumps({"status": "error", "msg": str(e)}), flush=True)

if __name__ == "__main__":
    main() 