# -*- coding: utf-8 -*-
"""
File: update_root_dashboard.py
Tạo Bảng Điều Khiển Tổng Quan (Master Navigation Hub) ngay trên đầu trang EnglishDocs
(Page ID: 26aeb70c-17c5-8060-9c96-e578765d55ad) để người dùng thấy ngay toàn bộ 16 chuyên đề.
"""

import os
import sys
import requests
import json
import time

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
PARENT_PAGE_ID = "26aeb70c-17c5-8060-9c96-e578765d55ad"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def make_rich_text(text, bold=False, italic=False, code=False, color="default", link=None):
    obj = {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "code": code,
            "color": color
        }
    }
    if link:
        obj["text"]["link"] = {"url": link}
    return obj

def make_callout(icon, color, rich_text_list):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": icon},
            "color": color,
            "rich_text": rich_text_list
        }
    }

def make_heading_1(text, color="default"):
    return {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "color": color,
            "rich_text": [make_rich_text(text, bold=True)]
        }
    }

def make_heading_2(text, color="default"):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "color": color,
            "rich_text": [make_rich_text(text, bold=True)]
        }
    }

def make_paragraph(rich_text_list):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": rich_text_list
        }
    }

def make_divider():
    return {"object": "block", "type": "divider", "divider": {}}

def build_dashboard_blocks():
    blocks = []
    
    # 1. Master Banner Callout
    blocks.append(make_callout("🚀", "blue_background", [
        make_rich_text("HỆ THỐNG CẨM NANG ÔN THI TUYỂN SINH VÀO 10 TIẾNG ANH - MASTER 2026-2027\n", bold=True, color="blue"),
        make_rich_text("Chuẩn ma trận đề Sở GD&ĐT Quảng Ngãi (Form 36 câu / 45 câu).\n", bold=True),
        make_rich_text("⭐ Trạng thái hệ thống: ", bold=True, color="green"),
        make_rich_text("100% ĐÃ NÂNG CẤP & BỔ SUNG BỘ THẦN CHÚ TIẾNG VIỆT ĐỘC QUYỀN.\n"),
        make_rich_text("⚠️ LƯU Ý HIỂN THỊ TRÊN NOTION: ", bold=True, color="red"),
        make_rich_text("Các chuyên đề bên dưới nằm trong các khối Toggle ('▶ NGỮ PHÁP TIẾNG ANH') mặc định bị thu gọn trên Notion. Bạn hãy bấm vào mũi tên "),
        make_rich_text("▶", bold=True, color="red"),
        make_rich_text(" để mở ra hoặc click nhanh trực tiếp vào các đường link chuyên đề bên dưới:")
    ]))

    # 2. Bảng điều hướng Chuyên đề Ngữ âm
    blocks.append(make_callout("🗣️", "green_background", [
        make_rich_text("PHẦN 1: CHUYÊN ĐỀ NGỮ ÂM & TRỌNG ÂM (CÂU THẦN CHÚ ĂN TRỌN ĐIỂM)\n", bold=True, color="green"),
        make_rich_text("• [ĐÃ CẬP NHẬT] "),
        make_rich_text("Quy tắc phát âm đuôi -ED: Thần chú 'Khi Sang Sông Phải Chờ Phà' + 'Tiền Đô'\n", bold=True, link="https://www.notion.so/26ceb70c17c58043a717f7090ef8608b"),
        make_rich_text("• [ĐÃ CẬP NHẬT] "),
        make_rich_text("Quy tắc phát âm đuôi -S/-ES: Thần chú 'Thời Phong Kiến Phương Tây' + 'Sáu Chạy Xe SH'\n", bold=True, link="https://www.notion.so/26ceb70c17c5808d8f05eeb481030dcf"),
        make_rich_text("• [ĐÃ CẬP NHẬT] "),
        make_rich_text("Quy tắc Trọng âm từ (Word Stress Mastery): Danh-Tính âm 1, Động từ âm 2 & Thần chú Hậu tố\n", bold=True, link="https://www.notion.so/3ffeb70c17c581e7b995c0be4d1fc2e1"),
        make_rich_text("• [ĐÃ CẬP NHẬT] "),
        make_rich_text("Cách phát âm TH (/θ/ vs /ð/): Quy tắc từ nội dung vs từ chức năng\n", bold=True, link="https://www.notion.so/26ceb70c17c580aca20ecfda6f9f177d"),
        make_rich_text("• [ĐÃ CẬP NHẬT] "),
        make_rich_text("Cách phát âm /æ/ (A bẹt) vs /e/ (E ngắn)\n", bold=True, link="https://www.notion.so/26ceb70c17c580d9aae2f3c17035c264"),
        make_rich_text("• [ĐÃ CẬP NHẬT] "),
        make_rich_text("Bảng Phiên Âm IPA chuẩn Quốc Tế (44 âm chuẩn Anh - Mỹ)\n", bold=True, link="https://www.notion.so/26ceb70c17c580b79f42c91372922a49")
    ]))

    # 3. Bảng điều hướng Chuyên đề Ngữ pháp
    blocks.append(make_callout("📘", "purple_background", [
        make_rich_text("PHẦN 2: CHUYÊN ĐỀ NGỮ PHÁP & BIẾN ĐỔI CÂU (TRỌNG TÂM CHIẾM 70% ĐIỂM)\n", bold=True, color="purple"),
        make_rich_text("• [TRỌNG ĐIỂM] "),
        make_rich_text("10 Cấu trúc Biến đổi câu kinh điển (Ước, Điều kiện, So sánh, Bị động, Gián tiếp...)\n", bold=True, link="https://www.notion.so/26aeb70c17c580138bf1d5f84e60bc0b"),
        make_rich_text("• [TRỌNG ĐIỂM] "),
        make_rich_text("12 Thì Tiếng Anh & Ma Trận Trục Thời Gian Feynman\n", bold=True, link="https://www.notion.so/26aeb70c17c580188f09f6a9ead9e8d4"),
        make_rich_text("• [TRỌNG ĐIỂM] "),
        make_rich_text("Mệnh đề quan hệ & Tuyệt chiêu Rút gọn mệnh đề quan hệ\n", bold=True, link="https://www.notion.so/26ceb70c17c5809fbc2dc9f05d830266"),
        make_rich_text("• [NÂNG CẤP] "),
        make_rich_text("Word Form & Hòa hợp Chủ ngữ - Động từ (S-V Agreement)\n", bold=True, link="https://www.notion.so/26ceb70c17c580c5afedf0a7531b77af"),
        make_rich_text("• [NÂNG CẤP] "),
        make_rich_text("Dạng động từ V-ing & To V (Bảng động từ 2 nhóm ý nghĩa)\n", bold=True, link="https://www.notion.so/26ceb70c17c5802b818ac5f8d7002c28"),
        make_rich_text("• [NÂNG CẤP] "),
        make_rich_text("Câu hỏi đuôi (Tag Questions) & 9 Bẫy ngoại lệ\n", bold=True, link="https://www.notion.so/274eb70c17c580628c0ef8d5428cb752"),
        make_rich_text("• [NÂNG CẤP] "),
        make_rich_text("Mạo từ (A / An / The / Zero Article)\n", bold=True, link="https://www.notion.so/26ceb70c17c58047a018c48c762656f6"),
        make_rich_text("• [NÂNG CẤP] "),
        make_rich_text("Giới từ Thời gian & Nơi chốn (In / On / At Pyramids)\n", bold=True, link="https://www.notion.so/26ceb70c17c580db87a3ce3fe150c607"),
        make_rich_text("• [NÂNG CẤP] "),
        make_rich_text("Động từ khuyết thiếu (Modal Verbs: Must, Should, May, Might...)\n", bold=True, link="https://www.notion.so/26ceb70c17c5801daa07d5eff2b458ca")
    ]))

    # 4. Bảng điều hướng Từ vựng & Tài liệu Offline
    blocks.append(make_callout("📗", "yellow_background", [
        make_rich_text("PHẦN 3: TỪ VỰNG CHỌN LỌC & CẨM NANG TOÀN TẬP OFFLINE\n", bold=True, color="brown"),
        make_rich_text("• [TỪ VỰNG] "),
        make_rich_text("Top 50 Phrasal Verbs xuất hiện nhiều nhất trong đề thi vào 10\n", bold=True, link="https://www.notion.so/26ceb70c17c580b8b2ccf0a12eda075d"),
        make_rich_text("• [TỪ VỰNG] "),
        make_rich_text("1000+ Cặp từ đồng nghĩa & trái nghĩa ăn trọn 0.5 - 1.0 điểm\n", bold=True, link="https://www.notion.so/26deb70c17c5809a8749e720654a8f22"),
        make_rich_text("• [OFFLINE BOOKLET] "),
        make_rich_text("File Cẩm Nang Toàn Tập: Cam_Nang_On_Thi_Vao_10_Master.html (230 KB - Mở trực tiếp trên Chrome/Edge)", bold=True)
    ]))

    blocks.append(make_divider())
    return blocks

def append_dashboard():
    blocks = build_dashboard_blocks()
    # Insert right after the third block (id: 3ffeb70c-17c5-80cf-9786-d6d2194eb2ba) or after the link block
    target_after = "3ffeb70c-17c5-80cf-9786-d6d2194eb2ba"
    
    url = f"https://api.notion.com/v1/blocks/{PARENT_PAGE_ID}/children"
    payload = {
        "children": blocks,
        "after": target_after
    }
    
    print(f"[+] Đang đẩy Master Dashboard vào trang gốc EnglishDocs (sau block {target_after})...")
    res = requests.patch(url, headers=HEADERS, json=payload)
    if res.status_code == 200:
        print("✅ THÀNH CÔNG! Đã gắn Master Navigation Dashboard ngay trên đầu trang chủ EnglishDocs!")
        return True
    else:
        print(f"❌ LỖI: HTTP {res.status_code}")
        print(res.text)
        # Fallback to appending at bottom if 'after' fails
        print("[*] Thử append thông thường...")
        fallback_res = requests.patch(url, headers=HEADERS, json={"children": blocks})
        if fallback_res.status_code == 200:
            print("✅ Append thông thường thành công!")
            return True
        return False

if __name__ == "__main__":
    append_dashboard()
