# -*- coding: utf-8 -*-
"""
File: export_english_mastery_booklet.py
Biên dịch toàn bộ hệ thống Chuyên đề Ngữ âm, Ngữ pháp & Từ vựng thành 1 cuốn Cẩm nang HTML Offline duy nhất.
Tích hợp Mermaid.js, Toggle đáp án, bảng biểu và styling cao cấp.
"""
import os
import re
import html
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

MODULE_FILES = [
    ("PHẦN 1: NGỮ ÂM & TRỌNG ÂM (CÂU THẦN CHÚ ĐỘC QUYỀN)", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_ed_mastery.md", "1. Cách phát âm đuôi -ED: Thần chú 'Khi Sang Sông Phải Chờ Phà' + 10 Tính từ bẫy"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_s_es_mastery.md", "2. Cách phát âm đuôi -S/-ES: Thần chú 'Thời Phong Kiến Phương Tây' + 'Sáu Chạy Xe SH'"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_trong_am_mastery.md", "3. Quy tắc Trọng âm từ (Word Stress): Danh-Tính âm 1, Động từ âm 2 & Thần chú Hậu tố"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_th.md", "4. Cách phát âm TH (/θ/ vs /ð/): Từ nội dung vs Từ chức năng"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_ae_e.md", "5. Phân biệt nguyên âm /æ/ (A bẹt) và /e/ (E ngắn)"),
    ]),
    ("PHẦN 2: NGỮ PHÁP & BIẾN ĐỔI CÂU (TRỌNG TÂM CHIẾM 70% ĐIỂM)", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_10_cau_truc_bien_doi_cau.md", "6. Cẩm nang 10 Cấu trúc Biến đổi câu (Sentence Transformation)"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_12_thi_mastery.md", "7. Hệ thống 12 Thì & Ma trận phối hợp thì Feynman"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_menh_de_quan_he.md", "8. Mệnh đề quan hệ & Tuyệt chiêu Rút gọn MĐQH"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_word_form_va_su_hoa_hop.md", "9. Cấu tạo từ (Word Form) & Hòa hợp Chủ - Vị (S-V Agreement)"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_ving_to_v_mastery.md", "10. Danh động từ & Động từ nguyên mẫu (V-ing vs To-V)"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_cau_hoi_duoi_mastery.md", "11. Câu hỏi đuôi & Trợ động từ (Question Tags)"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_mao_tu_articles_mastery.md", "12. Mạo từ (Articles: A, An, The & Zero Article)"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_gioi_tu_prepositions_mastery.md", "13. Giới từ (Prepositions: In, On, At & Collocations)"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_dong_tu_khuyet_thieu_mastery.md", "14. Động từ khuyết thiếu (Modal Verbs)"),
    ]),
    ("PHẦN 3: TỪ VỰNG CHỌN LỌC", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_3_phrasal_verbs_mastery.md", "15. Top 50 Cụm động từ (Phrasal Verbs) Tủ Thi Vào 10"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_3_dong_nghia_trai_nghia_mastery.md", "16. Cẩm nang Từ đồng nghĩa & Trái nghĩa (Synonyms & Antonyms)"),
    ])
]

def render_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code class='inline-code'>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text

def md_to_html(md_text: str) -> str:
    lines = md_text.splitlines()
    html_parts = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue

        if line.strip() == "---":
            html_parts.append("<hr>")
            i += 1
            continue

        if line.startswith("# "):
            html_parts.append(f"<h1 class='section-title'>{render_inline(line[2:])}</h1>")
            i += 1
            continue
        if line.startswith("## "):
            html_parts.append(f"<h2 class='sub-title'>{render_inline(line[3:])}</h2>")
            i += 1
            continue
        if line.startswith("### "):
            html_parts.append(f"<h3 class='topic-title'>{render_inline(line[4:])}</h3>")
            i += 1
            continue

        # Code & Mermaid
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip().lower()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            raw_code = "\n".join(code_lines)
            if lang == "mermaid":
                html_parts.append(f"<div class='mermaid'>{raw_code}</div>")
            else:
                html_parts.append(f"<pre class='code-block'><code>{html.escape(raw_code)}</code></pre>")
            continue

        # Callouts: > [!BLUE|GREEN|YELLOW|RED|PURPLE]
        m_callout = re.match(r"^>\s*\[!(BLUE|GREEN|YELLOW|RED|PURPLE)\]\s*(.*)$", line)
        if m_callout:
            c_type, first_line = m_callout.groups()
            c_lines = [first_line] if first_line else []
            i += 1
            while i < n and lines[i].startswith(">"):
                c_lines.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            cls_name = f"callout-{c_type.lower()}"
            content_html = "<br>".join(render_inline(cl) for cl in c_lines)
            html_parts.append(f"<div class='callout {cls_name}'>{content_html}</div>")
            continue

        # Toggle: +++ Title ... +++
        if line.startswith("+++ "):
            toggle_title = line[4:].strip()
            t_lines = []
            i += 1
            while i < n and lines[i].strip() != "+++":
                if lines[i].strip():
                    t_lines.append(lines[i].strip())
                i += 1
            i += 1
            body_html = "".join(f"<p>{render_inline(tl)}</p>" for tl in t_lines)
            html_parts.append(f"<details class='toggle-box'><summary>{render_inline(toggle_title)}</summary><div class='toggle-body'>{body_html}</div></details>")
            continue

        # Table
        if line.strip().startswith("|") and line.strip().endswith("|"):
            table_rows = []
            while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                raw_row = lines[i].strip()[1:-1]
                cells = [c.strip() for c in raw_row.split("|")]
                if not all(re.match(r"^:?-+:?$", c) for c in cells):
                    table_rows.append(cells)
                i += 1
            if table_rows:
                header = table_rows[0]
                rows = table_rows[1:]
                th_html = "".join(f"<th>{render_inline(c)}</th>" for c in header)
                tb_html = []
                for r in rows:
                    td_html = "".join(f"<td>{render_inline(c)}</td>" for c in r)
                    tb_html.append(f"<tr>{td_html}</tr>")
                html_parts.append(f"<table class='master-table'><thead><tr>{th_html}</tr></thead><tbody>{''.join(tb_html)}</tbody></table>")
            continue

        # Bullet list
        if line.startswith("- ") or line.startswith("* "):
            html_parts.append(f"<li class='bullet-item'>{render_inline(line[2:])}</li>")
            i += 1
            continue

        # Regular Paragraph
        html_parts.append(f"<p class='paragraph'>{render_inline(line)}</p>")
        i += 1

    return "\n".join(html_parts)

def generate_master_booklet():
    toc_html = []
    content_html = []

    for part_title, modules in MODULE_FILES:
        toc_html.append(f"<div class='toc-group'><div class='toc-heading'>{part_title}</div><ul class='toc-list'>")
        for file_path, mod_name in modules:
            anchor = re.sub(r"[^a-zA-Z0-9_-]", "", mod_name.lower().replace(" ", "_"))
            toc_html.append(f"<li><a href='#{anchor}'>{mod_name}</a></li>")

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                mod_html = md_to_html(text)
                content_html.append(f"<section id='{anchor}' class='module-section'><div class='module-badge'>{part_title}</div>{mod_html}</section>")
            else:
                content_html.append(f"<section id='{anchor}' class='module-section'><p><em>File {file_path} chưa được tạo.</em></p></section>")
        toc_html.append("</ul></div>")

    template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cẩm Nang Sư Phạm Tiếng Anh Ôn Thi Vào 10 - Master Guide</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad: true, theme: 'default' }});</script>
<style>
  :root {{
    --primary: #1e3a8a;
    --primary-light: #3b82f6;
    --bg-main: #f8fafc;
    --card-bg: #ffffff;
    --text-main: #0f172a;
    --text-sub: #475569;
    --border-color: #e2e8f0;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.7;
    color: var(--text-main);
    background: var(--bg-main);
    margin: 0;
    padding: 0;
  }}
  .container {{
    max-width: 1040px;
    margin: 0 auto;
    padding: 40px 24px;
  }}
  header.hero {{
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    color: white;
    padding: 48px 32px;
    border-radius: 16px;
    box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
    margin-bottom: 32px;
    text-align: center;
  }}
  header.hero h1 {{ margin: 0 0 12px 0; font-size: 2.2rem; font-weight: 800; }}
  header.hero p {{ margin: 0; font-size: 1.15rem; opacity: 0.92; }}
  .nav-toc {{
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 40px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }}
  .nav-toc h2 {{ margin-top: 0; color: var(--primary); font-size: 1.4rem; }}
  .toc-heading {{ font-weight: 700; color: #1e40af; margin-top: 14px; font-size: 1.05rem; }}
  .toc-list {{ list-style-type: none; padding-left: 16px; margin: 6px 0; }}
  .toc-list li {{ margin-bottom: 6px; }}
  .toc-list a {{ color: #2563eb; text-decoration: none; font-weight: 500; }}
  .toc-list a:hover {{ text-decoration: underline; }}
  .module-section {{
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 36px 32px;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  }}
  .module-badge {{
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 12px;
  }}
  h1.section-title {{ font-size: 1.8rem; color: var(--primary); margin-top: 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }}
  h2.sub-title {{ font-size: 1.35rem; color: #1e293b; margin-top: 28px; }}
  h3.topic-title {{ font-size: 1.15rem; color: #334155; margin-top: 20px; }}
  .inline-code {{
    background: #f1f5f9;
    color: #e11d48;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Consolas', monospace;
    font-size: 0.9em;
  }}
  .callout {{
    padding: 16px 20px;
    border-radius: 8px;
    margin: 18px 0;
    font-size: 0.98rem;
  }}
  .callout-blue {{ background: #eff6ff; border-left: 5px solid #3b82f6; color: #1e3a8a; }}
  .callout-green {{ background: #f0fdf4; border-left: 5px solid #22c55e; color: #14532d; }}
  .callout-yellow {{ background: #fefce8; border-left: 5px solid #eab308; color: #713f12; }}
  .callout-red {{ background: #fef2f2; border-left: 5px solid #ef4444; color: #7f1d1d; }}
  .callout-purple {{ background: #faf5ff; border-left: 5px solid #a855f7; color: #581c87; }}
  .code-block {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 18px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: 'Consolas', monospace;
    font-size: 0.92rem;
  }}
  .master-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 0.95rem;
  }}
  .master-table th, .master-table td {{
    border: 1px solid #cbd5e1;
    padding: 10px 14px;
    text-align: left;
  }}
  .master-table th {{
    background: #f1f5f9;
    font-weight: 700;
    color: #1e293b;
  }}
  .master-table tr:nth-child(even) {{ background: #f8fafc; }}
  details.toggle-box {{
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    padding: 12px 18px;
    margin: 20px 0;
  }}
  details.toggle-box summary {{
    font-weight: 700;
    color: #166534;
    cursor: pointer;
    outline: none;
  }}
  .toggle-body {{
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px dashed #86efac;
    font-size: 0.95rem;
  }}
  .mermaid {{
    text-align: center;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
  }}
  footer {{
    text-align: center;
    margin-top: 48px;
    color: #64748b;
    font-size: 0.9rem;
    padding: 24px;
  }}
</style>
</head>
<body>
<div class="container">
  <header class="hero">
    <h1>📘 CẨM NANG SƯ PHẠM TIẾNG ANH ÔN THI VÀO 10</h1>
    <p>Hệ thống hóa toàn diện Ngữ âm & IPA • Ngữ pháp & Biến đổi câu • Từ vựng trọng điểm (Chuẩn Sở GD Quảng Ngãi)</p>
  </header>

  <nav class="nav-toc">
    <h2>📑 MỤC LỤC CHUYÊN ĐỀ ĐÃ CHUẨN HÓA</h2>
    {''.join(toc_html)}
  </nav>

  <main>
    {''.join(content_html)}
  </main>

  <footer>
    <p>EnglishDocs Master Knowledge Base • Đồng bộ Notion API & Xuất bản Offline HTML hoàn chỉnh</p>
  </footer>
</div>
</body>
</html>"""

    out_file = "f:/OnThiC3/EnglishDocs/Cam_Nang_On_Thi_Vao_10_Master.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"[+] Successfully generated master offline booklet at: {out_file} ({os.path.getsize(out_file):,} bytes)")

if __name__ == "__main__":
    generate_master_booklet()
