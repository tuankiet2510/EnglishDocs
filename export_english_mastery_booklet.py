# -*- coding: utf-8 -*-
"""
File: export_english_mastery_booklet.py
Biên dịch toàn bộ hệ thống Chuyên đề Ngữ âm, Ngữ pháp & Từ vựng thành Ứng dụng Học tập Tương tác Cao Cấp
(Interactive Educational Web Application) tại file Cam_Nang_On_Thi_Vao_10_Master.html.
"""
import os
import sys

# Import core application builder engine
from generate_master_webapp import build_full_application

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
            
    print("=" * 70)
    print("BIÊN TẬP & XUẤT BẢN CẨM NANG ÔN THI VÀO 10 MASTER (INTERACTIVE APP)")
    print("=" * 70)
    
    html_content = build_full_application()
    target_path = "f:/OnThiC3/EnglishDocs/Cam_Nang_On_Thi_Vao_10_Master.html"
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[+] Đã biên tập thành công file ứng dụng web độc lập:")
    print(f"    -> {target_path} ({len(html_content.encode('utf-8')):,} bytes)")
    print("=" * 70)
