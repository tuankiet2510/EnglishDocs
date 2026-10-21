# -*- coding: utf-8 -*-
"""
File: add_stress_vietnamese_tricks.py
Bổ sung mục 'BỘ THẦN CHÚ TIẾNG VIỆT ĐỘC QUYỀN XỬ GỌN BÀI TRỌNG ÂM TRONG 5 GIÂY'
vào trang Quy tắc Trọng âm từ (Word Stress Mastery) - ID: 3ffeb70c-17c5-81e7-b995-c0be4d1fc2e1
"""

import os
import sys
import requests
import json

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
PAGE_ID = "3ffeb70c-17c5-81e7-b995-c0be4d1fc2e1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def make_rich_text(text, bold=False, italic=False, code=False, color="default"):
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": bold,
            "italic": italic,
            "code": code,
            "color": color
        }
    }

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

def make_heading_2(text, color="default"):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "color": color,
            "rich_text": [make_rich_text(text, bold=True)]
        }
    }

def make_divider():
    return {"object": "block", "type": "divider", "divider": {}}

def append_tricks():
    blocks = [
        make_divider(),
        make_heading_2("🔥 BỘ THẦN CHÚ TIẾNG VIỆT ĐỘC QUYỀN ĂN TRỌN 2 CÂU TRỌNG ÂM (5 GIÂY/CÂU)", color="red"),
        
        # Thần chú 1
        make_callout("💡", "blue_background", [
            make_rich_text("THẦN CHÚ 1: 'DANH TÍNH NHẤT - ĐỘNG TỪ NHÌ'\n", bold=True, color="blue"),
            make_rich_text("• Danh từ & Tính từ 2 âm tiết ➔ Đa số đánh trọng âm vào "),
            make_rich_text("ÂM 1", bold=True, color="blue"),
            make_rich_text(" (TA-ble, DOC-tor, HAP-py, CLE-ver).\n"),
            make_rich_text("• Động từ 2 âm tiết ➔ Đa số đánh trọng âm vào "),
            make_rich_text("ÂM 2", bold=True, color="blue"),
            make_rich_text(" (de-CIDE, re-LAX, be-GIN, en-JOY).\n"),
            make_rich_text("• 🚨 Mẹo nhớ ngoại lệ động từ nhấn âm 1: ", bold=True, color="red"),
            make_rich_text("'HÃY VÀO MỞ CỬA LẮNG NGHE CHUYỆN GÌ ĐÃ XẢY RA'\n", bold=True),
            make_rich_text("  ➔ EN-ter (vào), O-pen (mở), LI-sten (nghe), HAP-pen (xảy ra), VIS-it (thăm), AN-swer (trả lời) ➔ Đều nhấn âm 1!")
        ]),
        
        # Thần chú 2
        make_callout("🎯", "green_background", [
            make_rich_text("THẦN CHÚ 2: 'HÚT TRỌNG ÂM - ĐÈ NẶNG CHÍNH MÌNH'\n", bold=True, color="green"),
            make_rich_text("Các từ có đuôi: "),
            make_rich_text("-ee, -eer, -ese, -ique, -esque, -ain (động từ)\n", bold=True, code=True),
            make_rich_text("Câu thần chú: "),
            make_rich_text("\"Ê - EER - ESE - IQUE - AIN: GẶP LÀ ĐÈ NẶNG CHÍNH MÌNH\"\n", bold=True, color="green"),
            make_rich_text("➔ Trọng âm rơi ngay vào chính đuôi đó:\n"),
            make_rich_text("• train-EE, engi-NEER, Vietna-MESE, chi-NESE, u-NIQUE, tech-NIQUE, enter-TAIN.")
        ]),
        
        # Thần chú 3
        make_callout("⚡", "purple_background", [
            make_rich_text("THẦN CHÚ 3: 'LÙI 1 BƯỚC VỀ TRƯỚC'\n", bold=True, color="purple"),
            make_rich_text("Các từ có đuôi: "),
            make_rich_text("-ic, -tion, -sion, -ian, -ial, -ity, -ious, -eous, -itive\n", bold=True, code=True),
            make_rich_text("Câu thần chú: "),
            make_rich_text("\"ÍCH - SÂN - DÂN - AN - Ơ - ỢT: LÙI 1 BƯỚC VỀ TRƯỚC\"\n", bold=True, color="purple"),
            make_rich_text("➔ Trọng âm rơi vào âm tiết ĐỨNG NGAY TRƯỚC đuôi đó:\n"),
            make_rich_text("• scien-TIF-ic, infor-MA-tion, de-CI-sion, mu-SI-cian, com-PET-i-tive, his-TOR-i-cal.")
        ]),
        
        # Thần chú 4
        make_callout("🌀", "yellow_background", [
            make_rich_text("THẦN CHÚ 4: 'ĐẾM LÙI BA ÂM TỪ ĐUÔI'\n", bold=True, color="brown"),
            make_rich_text("Các từ có đuôi: "),
            make_rich_text("-ate, -fy, -ise / -ize, -gy, -phy, -my, -cy\n", bold=True, code=True),
            make_rich_text("Câu thần chú: "),
            make_rich_text("\"ẾT - PHAI - AI - GY - PHY: ĐẾM LÙI BA ÂM TỪ ĐUÔI\"\n", bold=True, color="brown"),
            make_rich_text("➔ Trọng âm rơi vào âm tiết thứ 3 tính từ cuối lên:\n"),
            make_rich_text("• ED-u-cate (âm 1), OR-gan-ise (âm 1), TECH-nol-o-gy (âm 2), PHO-tog-ra-phy (âm 2).")
        ]),

        # Thần chú 5
        make_callout("🛡️", "red_background", [
            make_rich_text("THẦN CHÚ 5: 'Ơ NHẸ VÀ I NGẮN - NÉ XA KHÔNG NHẬN TRỌNG ÂM'\n", bold=True, color="red"),
            make_rich_text("• Âm "),
            make_rich_text("/ə/ (ơ nhẹ)", bold=True),
            make_rich_text(" và âm "),
            make_rich_text("/ɪ/ (i ngắn lướt)", bold=True),
            make_rich_text(" là 2 nguyên âm yếu nhất trong tiếng Anh. Chúng "),
            make_rich_text("KHÔNG BAO GIỜ nhận trọng âm!\n", bold=True, color="red"),
            make_rich_text("• Khi gặp /ə/, trọng âm sẽ 'nhảy' sang âm bên cạnh:\n"),
            make_rich_text("  - a-BOUT /əˈbaʊt/ ➔ Nhấn âm 2.\n"),
            make_rich_text("  - ba-NA-na /bəˈnɑː.nə/ ➔ Nhấn âm 2.\n"),
            make_rich_text("  - PO-lice /pəˈliːs/ ➔ Nhấn âm 2.")
        ]),
        make_divider()
    ]
    
    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    print(f"[+] Đang đẩy Bộ Thần Chú Tiếng Việt vào trang Trọng âm ({PAGE_ID})...")
    res = requests.patch(url, headers=HEADERS, json={"children": blocks})
    if res.status_code == 200:
        print("✅ THÀNH CÔNG! Đã cập nhật trọn bộ Thần chú Tiếng Việt cho Word Stress trên Notion!")
        return True
    else:
        print(f"❌ LỖI: HTTP {res.status_code}")
        print(res.text)
        return False

if __name__ == "__main__":
    append_tricks()
