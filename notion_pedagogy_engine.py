# -*- coding: utf-8 -*-
"""
File: f:/OnThiC3/EnglishDocs/notion_pedagogy_engine.py
Công cụ biên dịch Markdown Sư phạm (DSL) và đồng bộ tốc độ cao lên Notion API.
Giải quyết triệt để lỗi tràn Token LLM và nghẽn Rate Limit.
"""
import os
import re
import sys
import json
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_notion_token():
    token = os.getenv("NOTION_API_TOKEN", "")
    if not token:
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("NOTION_API_TOKEN="):
                        token = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                        break
    return token

NOTION_TOKEN = get_notion_token()
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

CALLOUT_MAP = {
    "BLUE": ("🟦", "blue_background"),
    "GREEN": ("💡", "green_background"),
    "YELLOW": ("⚠️", "yellow_background"),
    "RED": ("🟥", "red_background"),
    "PURPLE": ("🚀", "purple_background"),
}

NOTION_LANGUAGES = {
    "abap", "abc", "agda", "arduino", "ascii art", "assembly", "bash", "basic", "bnf", "c",
    "c#", "c++", "clojure", "coffeescript", "coq", "css", "dart", "dhall", "diff", "docker",
    "ebnf", "elixir", "elm", "erlang", "f#", "flow", "fortran", "gherkin", "glsl", "go",
    "graphql", "groovy", "haskell", "hcl", "html", "idris", "java", "javascript", "json",
    "julia", "kotlin", "latex", "less", "lisp", "livescript", "llvm ir", "lua", "makefile",
    "markdown", "markup", "matlab", "mathematica", "mermaid", "nix", "notion formula",
    "objective-c", "ocaml", "pascal", "perl", "php", "plain text", "powershell", "prolog",
    "protobuf", "purescript", "python", "r", "racket", "reason", "ruby", "rust", "sass",
    "scala", "scheme", "scss", "shell", "smalltalk", "solidity", "sql", "swift", "toml",
    "typescript", "vb.net", "verilog", "vhdl", "visual basic", "webassembly", "xml", "yaml",
    "java/c/c++/c#"
}

def normalize_notion_lang(raw_lang: str) -> str:
    l = raw_lang.strip().lower()
    mapping = {
        "text": "plain text",
        "txt": "plain text",
        "sh": "bash",
        "zsh": "bash",
        "js": "javascript",
        "ts": "typescript",
        "py": "python",
        "py3": "python",
        "md": "markdown"
    }
    l = mapping.get(l, l)
    return l if l in NOTION_LANGUAGES else "plain text"

def api_request(method: str, url: str, **kwargs) -> dict:
    """Gọi Notion API với cơ chế tự động chờ khi chạm Rate Limit (HTTP 429)."""
    for attempt in range(5):
        res = SESSION.request(method, url, **kwargs)
        if res.status_code == 429:
            wait = float(res.headers.get("Retry-After", 1.5))
            time.sleep(wait)
            continue
        if res.status_code >= 400:
            print(f"[!] Notion API Error ({res.status_code}): {res.text}", file=sys.stderr)
        res.raise_for_status()
        return res.json() if res.text else {}
    raise RuntimeError(f"Notion API failed after 5 retries: {url}")

def list_shallow_index(page_id: str):
    """Chỉ lấy danh sách tiêu đề & child_page ở độ sâu 1 (không đệ quy gây tràn 100 blocks)."""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    items = []
    while url:
        data = api_request("GET", url)
        for b in data.get("results", []):
            b_type = b["type"]
            if b_type == "child_page":
                items.append({"id": b["id"], "type": "child_page", "title": b["child_page"]["title"]})
            elif b_type in ("heading_1", "heading_2", "heading_3"):
                txt = "".join(t.get("plain_text", "") for t in b[b_type].get("rich_text", []))
                items.append({"id": b["id"], "type": b_type, "title": txt})
        nxt = data.get("next_cursor")
        url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100&start_cursor={nxt}" if nxt else None
    return items

def clear_page_blocks_fast(page_id: str):
    """Xóa toàn bộ block cũ của trang (trừ child_page) bằng ThreadPool 3 workers + TCP Keep-Alive."""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    block_ids = []
    while url:
        data = api_request("GET", url)
        for b in data.get("results", []):
            if b["type"] != "child_page":
                block_ids.append(b["id"])
        nxt = data.get("next_cursor")
        url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100&start_cursor={nxt}" if nxt else None

    if not block_ids:
        return 0

    def _del(bid):
        api_request("DELETE", f"https://api.notion.com/v1/blocks/{bid}")
        time.sleep(0.25)  # Giữ nhịp ~3 req/s chuẩn Notion API

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(_del, bid) for bid in block_ids]
        for f in as_completed(futures):
            f.result()
    return len(block_ids)

def parse_inline_rich_text(text: str) -> list:
    """Biên dịch cú pháp **bold**, *italic*, `code` trong Markdown sang mảng rich_text của Notion."""
    pattern = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)")
    parts = pattern.split(text)
    rich_texts = []
    for part in parts:
        if not part:
            continue
        ann = {"bold": False, "italic": False, "code": False, "color": "default"}
        content = part
        if part.startswith("`") and part.endswith("`"):
            ann["code"] = True
            content = part[1:-1]
        elif part.startswith("**") and part.endswith("**"):
            ann["bold"] = True
            content = part[2:-2]
        elif part.startswith("*") and part.endswith("*"):
            ann["italic"] = True
            content = part[1:-1]
        rich_texts.append({
            "type": "text",
            "text": {"content": content[:2000]},
            "annotations": ann
        })
    return rich_texts or [{"type": "text", "text": {"content": ""}}]

def compile_markdown_dsl(md_text: str) -> list:
    """
    Biên dịch Markdown Sư phạm sang danh sách Notion Blocks:
    - > [!BLUE|GREEN|YELLOW|RED|PURPLE] Nội dung -> Callout màu tương ứng
    - +++ Tiêu đề Toggle ... +++ -> Khối Toggle ẩn/hiện đáp án
    - ```mermaid ... ``` -> Sơ đồ Mermaid hoặc ASCII Timeline
    - | Cột 1 | Cột 2 | -> Bảng Notion (Table block)
    """
    lines = md_text.splitlines()
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue

        # Divider
        if line.strip() == "---":
            blocks.append({"object": "block", "type": "divider", "divider": {}})
            i += 1
            continue

        # Headings
        if line.startswith("### "):
            blocks.append({"object": "block", "type": "heading_3", "heading_3": {"rich_text": parse_inline_rich_text(line[4:])}})
            i += 1
            continue
        if line.startswith("## "):
            blocks.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": parse_inline_rich_text(line[3:])}})
            i += 1
            continue
        if line.startswith("# "):
            blocks.append({"object": "block", "type": "heading_1", "heading_1": {"rich_text": parse_inline_rich_text(line[2:])}})
            i += 1
            continue

        # Code / Mermaid / ASCII Timeline
        if line.strip().startswith("```"):
            lang = normalize_notion_lang(line.strip()[3:].strip())
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "language": lang,
                    "rich_text": [{"type": "text", "text": {"content": "\n".join(code_lines)[:2000]}}]
                }
            })
            continue

        # Callout: > [!BLUE] ...
        m_callout = re.match(r"^>\s*\[!(BLUE|GREEN|YELLOW|RED|PURPLE)\]\s*(.*)$", line)
        if m_callout:
            c_type, first_line = m_callout.groups()
            icon, bg_color = CALLOUT_MAP[c_type]
            c_lines = [first_line] if first_line else []
            i += 1
            while i < n and lines[i].startswith(">"):
                c_lines.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            blocks.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "icon": {"type": "emoji", "emoji": icon},
                    "color": bg_color,
                    "rich_text": parse_inline_rich_text("\n".join(c_lines))
                }
            })
            continue

        # Toggle block: +++ Title ... +++
        if line.startswith("+++ "):
            toggle_title = line[4:].strip()
            t_children = []
            i += 1
            while i < n and lines[i].strip() != "+++":
                if lines[i].strip():
                    t_children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": parse_inline_rich_text(lines[i].strip())}
                    })
                i += 1
            i += 1
            blocks.append({
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "color": "green_background",
                    "rich_text": parse_inline_rich_text(toggle_title),
                    "children": t_children[:95]
                }
            })
            continue

        # Markdown Table
        if line.strip().startswith("|") and line.strip().endswith("|"):
            table_rows = []
            while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                raw_row = lines[i].strip()[1:-1]
                cells = [c.strip() for c in raw_row.split("|")]
                # Bỏ qua dòng phân cách |---|---|
                if not all(re.match(r"^:?-+:?$", c) for c in cells):
                    table_rows.append(cells)
                i += 1
            if table_rows:
                width = max(len(r) for r in table_rows)
                notion_rows = []
                for r in table_rows:
                    padded = (r + [""] * width)[:width]
                    notion_rows.append({
                        "object": "block",
                        "type": "table_row",
                        "table_row": {"cells": [parse_inline_rich_text(cell) for cell in padded]}
                    })
                blocks.append({
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": width,
                        "has_column_header": True,
                        "has_row_header": False,
                        "children": notion_rows
                    }
                })
            continue

        # Bulleted List
        if line.startswith("- ") or line.startswith("* "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": parse_inline_rich_text(line[2:])}
            })
            i += 1
            continue

        # Quote
        if line.startswith("> "):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {"rich_text": parse_inline_rich_text(line[2:])}
            })
            i += 1
            continue

        # Default Paragraph
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": parse_inline_rich_text(line)}
        })
        i += 1

    return blocks

def push_markdown_to_page(page_id: str, md_file: str, replace: bool = True):
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    blocks = compile_markdown_dsl(md_content)
    if replace:
        deleted = clear_page_blocks_fast(page_id)
        print(f"[+] Cleared {deleted} old blocks from page {page_id}")

    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    for idx in range(0, len(blocks), 80):
        batch = blocks[idx:idx + 80]
        api_request("PATCH", url, json={"children": batch})
        print(f"[+] Appended batch {idx // 80 + 1} ({len(batch)} blocks)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notion Pedagogy Engine CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_idx = sub.add_parser("index", help="Lấy danh sách trang con ở độ sâu 1")
    p_idx.add_argument("--page-id", required=True)

    p_sync = sub.add_parser("sync", help="Đẩy file Markdown DSL lên Notion Page")
    p_sync.add_argument("--page-id", required=True)
    p_sync.add_argument("--file", required=True)
    p_sync.add_argument("--append-only", action="store_true")

    args = parser.parse_args()
    if args.cmd == "index":
        res = list_shallow_index(args.page_id)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif args.cmd == "sync":
        push_markdown_to_page(args.page_id, args.file, replace=not args.append_only)