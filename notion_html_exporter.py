# File: notion_html_exporter.py
import os
import html
import requests
from typing import List, Dict, Any

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

def fetch_blocks_recursive(block_id: str) -> List[Dict[str, Any]]:
    """Đệ quy lấy toàn bộ block và sub-block từ Notion Page mà không tốn LLM token."""
    blocks = []
    url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
    while url:
        res = requests.get(url, headers=HEADERS).json()
        for b in res.get("results", []):
            if b.get("has_children") and b["type"] != "child_page":
                b["children"] = fetch_blocks_recursive(b["id"])
            blocks.append(b)
        next_cursor = res.get("next_cursor")
        url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100&start_cursor={next_cursor}" if next_cursor else None
    return blocks

def render_rich_text(rich_text_arr: List[Dict[str, Any]]) -> str:
    """Chuyển đổi Rich Text của Notion (bold, italic, color, code, link) sang HTML."""
    out = []
    for rt in rich_text_arr:
        text = html.escape(rt.get("plain_text", "")).replace("\n", "<br>")
        ann = rt.get("annotations", {})
        color = ann.get("color", "default")
        
        if ann.get("code"): text = f"<code class='inline-code'>{text}</code>"
        if ann.get("bold"): text = f"<strong>{text}</strong>"
        if ann.get("italic"): text = f"<em>{text}</em>"
        if ann.get("strikethrough"): text = f"<del>{text}</del>"
        if ann.get("underline"): text = f"<u>{text}</u>"
        if color != "default": text = f"<span class='notion-{color}'>{text}</span>"
        if rt.get("href"): text = f"<a href='{html.escape(rt['href'])}' target='_blank'>{text}</a>"
        out.append(text)
    return "".join(out)

def blocks_to_html(blocks: List[Dict[str, Any]]) -> str:
    """Chuyển danh sách Notion Blocks sang chuỗi HTML giữ nguyên định dạng."""
    html_parts = []
    for b in blocks:
        b_type = b["type"]
        data = b.get(b_type, {})
        color_cls = f"notion-{data.get('color', 'default')}" if data.get("color") else ""
        text_html = render_rich_text(data.get("rich_text", []))
        children_html = blocks_to_html(b.get("children", [])) if "children" in b else ""

        if b_type in ("heading_1", "heading_2", "heading_3"):
            tag = f"h{b_type[-1]}"
            html_parts.append(f"<{tag} class='{color_cls}'>{text_html}</{tag}>{children_html}")
        elif b_type == "paragraph":
            html_parts.append(f"<p class='{color_cls}'>{text_html or '&nbsp;'}</p>{children_html}")
        elif b_type == "callout":
            icon = data.get("icon", {}).get("emoji", "💡")
            html_parts.append(f"<div class='callout {color_cls}'><div class='callout-icon'>{icon}</div><div class='callout-content'>{text_html}{children_html}</div></div>")
        elif b_type == "quote":
            html_parts.append(f"<blockquote class='{color_cls}'>{text_html}{children_html}</blockquote>")
        elif b_type in ("bulleted_list_item", "numbered_list_item"):
            html_parts.append(f"<li class='{color_cls}'>{text_html}{children_html}</li>")
        elif b_type == "toggle":
            html_parts.append(f"<details class='toggle {color_cls}'><summary>{text_html}</summary><div class='toggle-body'>{children_html}</div></details>")
        elif b_type == "code":
            lang = data.get("language", "plaintext")
            raw_code = "".join([rt.get("plain_text", "") for rt in data.get("rich_text", [])])
            if lang == "mermaid":
                html_parts.append(f"<div class='mermaid'>{raw_code}</div>")
            else:
                html_parts.append(f"<pre><code class='language-{lang}'>{html.escape(raw_code)}</code></pre>")
        elif b_type == "divider":
            html_parts.append("<hr>")
        elif b_type == "table":
            rows_html = []
            for idx, r in enumerate(b.get("children", [])):
                cells = r.get("table_row", {}).get("cells", [])
                tag = "th" if (idx == 0 and data.get("has_column_header")) else "td"
                row_str = "".join([f"<{tag}>{render_rich_text(c)}</{tag}>" for c in cells])
                rows_html.append(f"<tr>{row_str}</tr>")
            html_parts.append(f"<table class='notion-table'>{''.join(rows_html)}</table>")
    return "\n".join(html_parts)

def export_notion_page_to_html(page_id: str, output_file: str = "EnglishDocs_Export.html", title: str = "EnglishDocs Master Guide"):
    """Hàm chính: Kéo dữ liệu từ Notion Page ID và xuất ra file HTML hoàn chỉnh."""
    blocks = fetch_blocks_recursive(page_id)
    body_content = blocks_to_html(blocks)
    
    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad: true, theme: 'default' }});</script>
<style>
  :root {{ --text: #2c3e50; --bg: #ffffff; }}
  body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; line-height: 1.65; color: var(--text); max-width: 920px; margin: 40px auto; padding: 0 24px; }}
  h1, h2, h3 {{ font-weight: 700; margin-top: 1.4em; margin-bottom: 0.5em; }}
  h1 {{ border-bottom: 2px solid #eaecef; padding-bottom: 8px; }}
  .inline-code {{ background: rgba(135,131,120,0.15); color: #eb5757; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }}
  .callout {{ display: flex; align-items: flex-start; padding: 16px; border-radius: 8px; margin: 14px 0; border: 1px solid rgba(0,0,0,0.06); }}
  .callout-icon {{ font-size: 1.4em; margin-right: 12px; line-height: 1.2; }}
  .callout-content {{ flex: 1; }}
  blockquote {{ border-left: 4px solid #37352f; margin: 14px 0; padding: 8px 16px; background: #f9f9f8; font-style: italic; }}
  details.toggle {{ margin: 10px 0; padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 6px; }}
  details.toggle summary {{ font-weight: 600; cursor: pointer; }}
  .toggle-body {{ padding-top: 10px; padding-left: 16px; }}
  .notion-table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
  .notion-table th, .notion-table td {{ border: 1px solid #dfe2e5; padding: 10px 12px; text-align: left; }}
  .notion-table th {{ background: #f6f8fa; font-weight: 600; }}
  /* Notion Colors & Highlights */
  .notion-blue {{ color: #0b6e99; }} .notion-green {{ color: #0f7b6c; }} .notion-red {{ color: #e03e3e; }} .notion-yellow {{ color: #dfab01; }} .notion-purple {{ color: #6940a5; }} .notion-orange {{ color: #d9730d; }}
  .notion-blue_background {{ background: #e7f3f8; padding: 2px 6px; border-radius: 4px; }}
  .notion-green_background {{ background: #edf3ec; padding: 2px 6px; border-radius: 4px; }}
  .notion-yellow_background {{ background: #fbf3db; padding: 2px 6px; border-radius: 4px; }}
  .notion-red_background {{ background: #fbe4e4; padding: 2px 6px; border-radius: 4px; }}
  .notion-purple_background {{ background: #f6f3f9; padding: 2px 6px; border-radius: 4px; }}
  .notion-gray_background {{ background: #f1f1ef; padding: 2px 6px; border-radius: 4px; }}
  .mermaid {{ text-align: center; margin: 20px 0; padding: 16px; background: #fafafa; border-radius: 8px; }}
</style>
</head>
<body>
<h1>📘 {html.escape(title)}</h1>
{body_content}
</body>
</html>"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    return os.path.abspath(output_file)