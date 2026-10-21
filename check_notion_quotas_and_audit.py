# -*- coding: utf-8 -*-
"""
File: check_notion_quotas_and_audit.py
Kiểm tra tình trạng Quota, Rate Limit của Notion API & Rà soát toàn bộ các trang con trong EnglishDocs.
"""
import os
import sys
import time
import json
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
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

ROOT_PAGE_ID = "26aeb70c-17c5-8060-9c96-e578765d55ad"

def check_bot_and_quotas():
    print("=" * 60)
    print("1. KIỂM TRA BOT INTEGRATION & NOTION API QUOTA")
    print("=" * 60)
    
    t0 = time.time()
    res = requests.get("https://api.notion.com/v1/users/me", headers=HEADERS)
    lat = (time.time() - t0) * 1000
    
    if res.status_code != 200:
        print(f"[!] LỖI KẾT NỐI NOTION API: HTTP {res.status_code}")
        print(res.text)
        return False

    data = res.json()
    bot_info = data.get("bot", {})
    owner = bot_info.get("owner", {})
    limits = bot_info.get("workspace_limits", {})

    print(f"[+] Trạng thái Token: HỢP LỆ (Status 200 OK - Độ trễ: {lat:.1f}ms)")
    print(f"[+] Bot Name: {data.get('name')}")
    print(f"[+] Workspace Name: {bot_info.get('workspace_name')}")
    print(f"[+] Workspace ID: {bot_info.get('workspace_id')}")
    print(f"[+] Giới hạn file tải lên (Max File Upload): {limits.get('max_file_upload_size_in_bytes', 0) / (1024*1024):.1f} MB")
    print("\n[i] CƠ CHẾ NOTION API RATE LIMIT:")
    print("    - Notion áp dụng ngưỡng 3 requests/giây cho mỗi integration.")
    print("    - Nếu vượt ngưỡng, API trả về HTTP 429 kèm header 'Retry-After'.")
    print("    - notion_pedagogy_engine.py đã có cơ chế tự động đọc 'Retry-After' và chờ 1.5s để retry.")
    return True

def audit_page(page_id: str, depth: int = 0, title: str = ""):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    indent = "  " * depth
    try:
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 429:
            retry = float(res.headers.get("Retry-After", 1.5))
            time.sleep(retry)
            res = requests.get(url, headers=HEADERS)
        
        if res.status_code != 200:
            print(f"{indent}[!] Lỗi đọc page {page_id}: HTTP {res.status_code}")
            return

        blocks = res.json().get("results", [])
        child_pages = []
        child_toggles = []
        for b in blocks:
            b_type = b["type"]
            if b_type == "child_page":
                child_pages.append((b["id"], b["child_page"]["title"]))
            elif b.get("has_children") and b_type.startswith("heading"):
                heading_txt = "".join(t.get("plain_text", "") for t in b[b_type].get("rich_text", []))
                child_toggles.append((b["id"], heading_txt))

        print(f"{indent}📄 [{title or page_id}] -> Tổng số blocks: {len(blocks)} | Trang con trực tiếp: {len(child_pages)} | Toggle headings: {len(child_toggles)}")

        for cid, ctitle in child_pages:
            audit_page(cid, depth + 1, ctitle)

        for tid, ttitle in child_toggles:
            audit_page(tid, depth + 1, f"▶ Toggle: {ttitle}")

    except Exception as e:
        print(f"{indent}[!] Exception: {e}")

if __name__ == "__main__":
    ok = check_bot_and_quotas()
    if ok:
        print("\n" + "=" * 60)
        print("2. RÀ SOÁT CẤU TRÚC THỰC TẾ TRÊN NOTION (EnglishDocs Tree)")
        print("=" * 60)
        audit_page(ROOT_PAGE_ID, 0, "EnglishDocs (ROOT)")
