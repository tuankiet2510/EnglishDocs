# -*- coding: utf-8 -*-
"""
File: generate_master_webapp.py
Kiến trúc sư giao diện: Principal Educational Product Designer & Frontend Architect
Mục đích: Chuyển đổi toàn diện cuốn Cẩm nang HTML thành Ứng dụng Học tập Tương tác Cao Cấp
(Interactive Educational Web Application) dành cho học sinh lớp 9 ôn thi vào 10.
Tích hợp:
1. Hệ thống Quiz tương tác 2 chế độ: Chế độ Luyện tập (Practice) & Chế độ Thi thử (Exam).
2. Trục thời gian ngữ pháp tương tác (Interactive Tense Timeline).
3. Trình thuật toán cây quyết định phát âm (Interactive Decision Wizards cho ED, S/ES, TH, Trọng âm).
4. Công cụ phát âm IPA âm thanh qua Web Speech API (100% Offline).
5. Thanh điều hướng thông minh (ScrollSpy, Tìm kiếm thời gian thực, Dark/Light mode, Lưu tiến độ LocalStorage).
"""

import os
import sys
import re
import html
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

MODULE_FILES = [
    ("PHẦN 1: NGỮ ÂM & TRỌNG ÂM (CÂU THẦN CHÚ ĐỘC QUYỀN)", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_ed_mastery.md", "1. Cách phát âm đuôi -ED: Thần chú 'Khi Sang Sông Phải Chờ Phà' + 10 Tính từ bẫy", "ed"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_s_es_mastery.md", "2. Cách phát âm đuôi -S/-ES: Thần chú 'Thời Phong Kiến Phương Tây' + 'Sáu Chạy Xe SH'", "ses"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_trong_am_mastery.md", "3. Quy tắc Trọng âm từ (Word Stress): Danh-Tính âm 1, Động từ âm 2 & Thần chú Hậu tố", "stress"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_th.md", "4. Cách phát âm TH (/θ/ vs /ð/): Từ nội dung vs Từ chức năng", "th"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_ae_e.md", "5. Phân biệt nguyên âm /æ/ (A bẹt) và /e/ (E ngắn)", "aee"),
    ]),
    ("PHẦN 2: NGỮ PHÁP & BIẾN ĐỔI CÂU (TRỌNG TÂM CHIẾM 70% ĐIỂM)", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_10_cau_truc_bien_doi_cau.md", "6. Cẩm nang 10 Cấu trúc Biến đổi câu (Sentence Transformation)", "transform"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_12_thi_mastery.md", "7. Hệ thống 12 Thì & Ma trận phối hợp thì Feynman", "tenses"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_menh_de_quan_he.md", "8. Mệnh đề quan hệ & Tuyệt chiêu Rút gọn MĐQH", "relative"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_word_form_va_su_hoa_hop.md", "9. Cấu tạo từ (Word Form) & Hòa hợp Chủ - Vị (S-V Agreement)", "wordform"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_ving_to_v_mastery.md", "10. Danh động từ & Động từ nguyên mẫu (V-ing vs To-V)", "ving"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_cau_hoi_duoi_mastery.md", "11. Câu hỏi đuôi & Trợ động từ (Question Tags)", "tags"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_mao_tu_articles_mastery.md", "12. Mạo từ (Articles: A, An, The & Zero Article)", "articles"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_gioi_tu_prepositions_mastery.md", "13. Giới từ (Prepositions: In, On, At & Collocations)", "prepos"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_dong_tu_khuyet_thieu_mastery.md", "14. Động từ khuyết thiếu (Modal Verbs)", "modals"),
    ]),
    ("PHẦN 3: TỪ VỰNG CHỌN LỌC", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_3_phrasal_verbs_mastery.md", "15. Top 50 Cụm động từ (Phrasal Verbs) Tủ Thi Vào 10", "phrasal"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_3_dong_nghia_trai_nghia_mastery.md", "16. Cẩm nang Từ đồng nghĩa & Trái nghĩa (Synonyms & Antonyms)", "synonym"),
    ])
]

def render_inline(text: str) -> str:
    """Render inline markdown styling: bold, italic, code, underline, audio tags."""
    # Underline phonetics target: e.g. b**a**d -> b<u>a</u>d or **th**is -> <u>th</u>is
    # Preserve backticks
    text = re.sub(r"`([^`]+)`", r"<code class='inline-code'>\1</code>", text)
    # Target phonetic letters in bold: e.g. book**s** -> book<u class='phonetic-target'>s</u>
    text = re.sub(r"\*\*([a-zA-Z\-_/]+)\*\*", r"<strong class='phonetic-highlight'>\1</strong>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    
    # Add audio button for IPA transcriptions: /.../
    # e.g. /wɒntɪd/ or /ˈneɪkɪd/
    def add_audio_btn(match):
        ipa_str = match.group(0)
        # extract preceding word if possible
        return f"<span class='ipa-wrap'>{ipa_str}</span>"
    
    # text = re.sub(r"/[^/\n]{2,30}/", add_audio_btn, text)
    return text

def parse_quizzes(text: str, mod_id: str):
    """Parse multiple choice and transformation questions with answer keys."""
    questions = []
    answers = {}
    
    # Extract answers from toggle block: +++ ... +++
    m_toggle = re.search(r'\+\+\+\s+([^\n]+)\n(.*?)(?:\+\+\+|\Z)', text, re.DOTALL)
    if m_toggle:
        ans_block = m_toggle.group(2)
        for line in ans_block.splitlines():
            line = line.strip().replace("`", "")
            if not line:
                continue
            m_a = re.match(r"^\s*(?:\*\*)?(?:Câu\s+)?(\d+)[\.:\s]+(?:Đáp\s+án\s+|Chọn\s+)?(?:\*\*)?([A-D])?(?:\*\*)?[\.:\s\(\)]*(.*)", line, re.IGNORECASE)
            if m_a:
                q_num = m_a.group(1)
                opt = m_a.group(2)
                exp = m_a.group(3).strip().rstrip("*").strip()
                if not opt:
                    m_opt = re.search(r"(?:Đáp án|Chọn)\s*(?:\*\*)?([A-D])(?:\*\*)?", line, re.IGNORECASE)
                    if m_opt:
                        opt = m_opt.group(1).upper()
                answers[q_num] = {
                    "correct": opt.upper() if opt else None,
                    "explanation": exp or line
                }

    # Extract questions before toggle block
    content_before_ans = text[:m_toggle.start()] if m_toggle else text
    lines = content_before_ans.splitlines()
    
    # Find start of quiz section
    quiz_start_idx = -1
    for idx, l in enumerate(lines):
        if re.search(r"##+\s+.*?(?:THỰC CHIẾN|TRẮC NGHIỆM|BÀI TẬP)", l, re.IGNORECASE):
            quiz_start_idx = idx
            break
            
    if quiz_start_idx == -1:
        return questions, text # no quiz section
        
    non_quiz_text = "\n".join(lines[:quiz_start_idx])
    quiz_lines = lines[quiz_start_idx:]
    
    i = 0
    while i < len(quiz_lines):
        line = quiz_lines[i].strip()
        m_q = re.match(r"^(?:-\s*)?(?:\*\*)?(?:Câu\s+)?(\d+)[\.:\s]+(?:\([^\)]+\):?\s*)?(?:\*\*)?(.*)$", line)
        if m_q and not line.startswith("+++") and not line.startswith("##"):
            q_num = m_q.group(1)
            rest_line = m_q.group(2).strip()
            clean_rest = rest_line.replace("`", "")
            
            opt_matches = list(re.finditer(r"([A-D])\.\s*([^\|]+)(?:\||\Z)", clean_rest))
            stem = rest_line
            opts = {}
            if len(opt_matches) >= 3:
                stem = clean_rest[:opt_matches[0].start()].strip()
                for om in opt_matches:
                    opts[om.group(1)] = om.group(2).strip()
            else:
                if i + 1 < len(quiz_lines):
                    next_line = quiz_lines[i+1].strip().replace("`", "")
                    next_opt_matches = list(re.finditer(r"([A-D])\.\s*([^\|]+)(?:\||\Z)", next_line))
                    if len(next_opt_matches) >= 3:
                        for nom in next_opt_matches:
                            opts[nom.group(1)] = nom.group(2).strip()
                        i += 1
                        
            if opts:
                ans_info = answers.get(q_num, {})
                questions.append({
                    "id": f"{mod_id}_q{q_num}",
                    "num": q_num,
                    "type": "mcq",
                    "stem": stem or "Chọn đáp án có cách phát âm hoặc ngữ pháp chuẩn xác nhất:",
                    "options": opts,
                    "correct": ans_info.get("correct"),
                    "explanation": ans_info.get("explanation", "")
                })
            elif stem and not stem.startswith("Dạng") and not stem.startswith("Ví dụ") and len(stem) > 5:
                ans_info = answers.get(q_num, {})
                questions.append({
                    "id": f"{mod_id}_q{q_num}",
                    "num": q_num,
                    "type": "transformation",
                    "stem": stem,
                    "model_answer": ans_info.get("explanation", "")
                })
        i += 1
        
    return questions, non_quiz_text

def build_quiz_html(questions, mod_id: str, title: str) -> str:
    """Generate high-end interactive quiz component with Practice and Exam modes."""
    if not questions:
        return ""
        
    mcqs = [q for q in questions if q["type"] == "mcq"]
    trans = [q for q in questions if q["type"] == "transformation"]
    
    html_parts = []
    html_parts.append(f"""
    <div class="interactive-quiz-wrapper" id="quiz_{mod_id}" data-mod-id="{mod_id}" data-total="{len(mcqs)}">
      <div class="quiz-header-panel">
        <div class="quiz-title-box">
          <span class="quiz-icon-badge">⚡</span>
          <div>
            <h3 class="quiz-main-title">THỰC CHIẾN ÔN THI: {html.escape(title)}</h3>
            <p class="quiz-sub-desc">Chuẩn đề thi tuyển sinh vào 10 (Sở GD Quảng Ngãi & Toàn quốc) • {len(questions)} câu</p>
          </div>
        </div>
        <div class="quiz-mode-pill">
          <span class="mode-label">Chế độ đang mở:</span>
          <span class="mode-tag mode-tag-practice active" data-mode="practice">🎯 Luyện tập</span>
          <span class="mode-tag mode-tag-exam" data-mode="exam">⏱️ Thi thử</span>
        </div>
      </div>
      
      <!-- Quiz Progress Tracker -->
      <div class="quiz-tracker-bar">
        <div class="tracker-info">
          <span>Tiến độ làm bài: <strong class="answered-count">0</strong>/{len(mcqs)} câu</span>
          <span class="score-display hidden">Điểm số: <strong class="score-val">0</strong>/{len(mcqs)}</span>
        </div>
        <div class="tracker-progress-track">
          <div class="tracker-progress-fill" style="width: 0%"></div>
        </div>
      </div>
    """)
    
    # MCQ Questions
    for q in mcqs:
        qid = q["id"]
        qnum = q["num"]
        stem = render_inline(q["stem"])
        correct = q["correct"] or ""
        explanation = render_inline(q["explanation"])
        
        # Audio speaker button detection if single word
        stem_audio_btn = ""
        m_word = re.search(r"\b([a-zA-Z]{3,15})\b", stem)
        if m_word and len(stem) < 30:
            stem_audio_btn = f"<button class='audio-speaker-btn' onclick='playSpeech(\"{m_word.group(1)}\")' title='Nghe phát âm từ này'>🔊</button>"
        
        html_parts.append(f"""
        <div class="quiz-question-card" id="card_{qid}" data-qid="{qid}" data-correct="{correct}">
          <div class="question-meta-row">
            <span class="question-number-badge">Câu {int(qnum):02d}</span>
            <span class="question-status-badge status-unanswered">Chưa làm</span>
          </div>
          <div class="question-stem-text">{stem} {stem_audio_btn}</div>
          
          <div class="quiz-options-grid">
        """)
        
        for opt_key in ["A", "B", "C", "D"]:
            if opt_key in q["options"]:
                opt_val = render_inline(q["options"][opt_key])
                # Audio button for phonetic options like bad, man, dogs, etc.
                clean_w = re.sub(r"<[^>]+>", "", opt_val).strip()
                opt_audio = ""
                if len(clean_w) <= 15 and clean_w.isalpha():
                    opt_audio = f"<span class='opt-audio-btn' onclick='event.stopPropagation(); playSpeech(\"{clean_w}\")' title='Nghe phát âm'>🔊</span>"
                    
                html_parts.append(f"""
                <button type="button" class="quiz-option-btn" data-qid="{qid}" data-opt="{opt_key}" onclick="handleOptionSelect('{qid}', '{opt_key}')">
                  <span class="opt-letter-circle">{opt_key}</span>
                  <span class="opt-content-text">{opt_val}</span>
                  {opt_audio}
                  <span class="opt-feedback-icon"></span>
                </button>
                """)
                
        html_parts.append(f"""
          </div>
          
          <!-- Immediate Explanation (Practice Mode) -->
          <div class="question-explanation-panel hidden" id="exp_{qid}">
            <div class="exp-header">
              <span class="exp-badge">💡 GIẢI THÍCH CHI TIẾT CÂU {qnum}</span>
              <span class="exp-correct-key">Đáp án chuẩn: <strong>{correct}</strong></span>
            </div>
            <div class="exp-body-text">{explanation}</div>
            <button class="retry-question-btn" onclick="retryQuestion('{qid}')">🔄 Làm lại câu này</button>
          </div>
        </div>
        """)
        
    # Sentence Transformation Questions
    if trans:
        html_parts.append("""
        <div class="transformation-section-title">
          <h4>✍️ BÀI TẬP TỰ LUẬN: BIẾN ĐỔI CÂU & TỰ LUYỆN TẬP</h4>
          <p>Nhập câu trả lời của bạn vào ô bên dưới, sau đó bấm "Đối chiếu đáp án mẫu" để so sánh cấu trúc:</p>
        </div>
        """)
        for q in trans:
            qid = q["id"]
            qnum = q["num"]
            stem = render_inline(q["stem"])
            model_ans = render_inline(q["model_answer"])
            html_parts.append(f"""
            <div class="transformation-card" id="card_{qid}">
              <div class="trans-meta"><span class="question-number-badge">Câu {int(qnum):02d}</span></div>
              <div class="trans-stem">{stem}</div>
              <div class="trans-input-row">
                <input type="text" class="trans-input-box" id="input_{qid}" placeholder="Nhập câu viết lại tương đương tại đây...">
                <button class="trans-check-btn" onclick="toggleTransAnswer('{qid}')">🔍 Đối chiếu đáp án</button>
              </div>
              <div class="trans-model-answer hidden" id="model_{qid}">
                <div class="model-badge">✅ ĐÁP ÁN MẪU & PHÂN TÍCH:</div>
                <div class="model-text">{model_ans}</div>
              </div>
            </div>
            """)
            
    # Exam Submission & Score Card Footer
    html_parts.append(f"""
      <div class="quiz-footer-actions">
        <button class="submit-exam-btn" onclick="submitExam('{mod_id}')">🚀 Nộp bài thi thử & Chấm điểm</button>
        <button class="reset-quiz-btn" onclick="resetQuizSection('{mod_id}')">🔄 Làm lại toàn bộ</button>
      </div>
      
      <!-- Exam Results Modal / Banner -->
      <div class="exam-result-banner hidden" id="result_{mod_id}">
        <div class="result-banner-content">
          <div class="result-score-circle">
            <span class="result-score-number" id="score_num_{mod_id}">0</span>
            <span class="result-score-max">/{len(mcqs)}</span>
          </div>
          <div class="result-details">
            <h4 class="result-heading">KẾT QUẢ THI THỬ</h4>
            <p class="result-comment" id="comment_{mod_id}">Hoàn thành xuất sắc!</p>
            <div class="result-meta-tags">
              <span class="result-tag" id="pct_{mod_id}">Tỉ lệ đúng: 100%</span>
              <span class="result-tag" id="time_tag_{mod_id}">Đã lưu vào bộ nhớ tiến độ</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """)
    
    return "\n".join(html_parts)

def build_interactive_wizards():
    """Build high-end interactive decision trees and visualizers for Pronunciation & Tenses."""
    return {
        "ed": """
        <div class="interactive-wizard-card" id="wizard_ed">
          <div class="wizard-header">
            <span class="wizard-icon">🪄</span>
            <div>
              <h4 class="wizard-title">CÔNG CỤ TRA CỨU NHANH: PHÁT ÂM ĐUÔI -ED TRONG 3 GIÂY</h4>
              <p class="wizard-desc">Nhập một từ bất kỳ hoặc bấm vào các bước bên dưới để máy tính phân loại âm thanh tức thì:</p>
            </div>
          </div>
          <div class="wizard-interactive-flow">
            <div class="wizard-input-box">
              <input type="text" id="ed_word_input" placeholder="Ví dụ: wanted, washed, played, naked..." oninput="testEdWord(this.value)">
              <button onclick="testEdWord(document.getElementById('ed_word_input').value)">Kiểm tra ngay</button>
            </div>
            <div class="wizard-result-box" id="ed_result_box">
              <span class="wiz-res-label">Kết quả phân tích:</span>
              <span class="wiz-res-badge" id="ed_res_badge">Nhập từ để kiểm tra...</span>
              <span class="wiz-res-rule" id="ed_res_rule"></span>
            </div>
            <div class="wizard-quick-tags">
              <span>Thử nhanh từ mẫu:</span>
              <button onclick="setEdWord('wanted')">wanted</button>
              <button onclick="setEdWord('watched')">watched</button>
              <button onclick="setEdWord('played')">played</button>
              <button onclick="setEdWord('naked')">naked (bẫy tính từ)</button>
              <button onclick="setEdWord('laughed')">laughed (gh)</button>
              <button onclick="setEdWord('wicked')">wicked (bẫy)</button>
            </div>
          </div>
        </div>
        """,
        "ses": """
        <div class="interactive-wizard-card" id="wizard_ses">
          <div class="wizard-header">
            <span class="wizard-icon">🪄</span>
            <div>
              <h4 class="wizard-title">CÔNG CỤ TRA CỨU NHANH: PHÁT ÂM ĐUÔI -S / -ES TRONG 3 GIÂY</h4>
              <p class="wizard-desc">Kiểm tra ngay quy tắc "Thời phong kiến" vs "Sáu chạy xe SH":</p>
            </div>
          </div>
          <div class="wizard-interactive-flow">
            <div class="wizard-input-box">
              <input type="text" id="ses_word_input" placeholder="Ví dụ: books, watches, plays, houses..." oninput="testSesWord(this.value)">
              <button onclick="testSesWord(document.getElementById('ses_word_input').value)">Kiểm tra ngay</button>
            </div>
            <div class="wizard-result-box" id="ses_result_box">
              <span class="wiz-res-label">Kết quả phân tích:</span>
              <span class="wiz-res-badge" id="ses_res_badge">Nhập từ để kiểm tra...</span>
              <span class="wiz-res-rule" id="ses_res_rule"></span>
            </div>
            <div class="wizard-quick-tags">
              <span>Thử nhanh từ mẫu:</span>
              <button onclick="setSesWord('books')">books</button>
              <button onclick="setSesWord('watches')">watches</button>
              <button onclick="setSesWord('plays')">plays</button>
              <button onclick="setSesWord('houses')">houses (bẫy /zɪz/)</button>
              <button onclick="setSesWord('months')">months</button>
              <button onclick="setSesWord('clothes')">clothes</button>
            </div>
          </div>
        </div>
        """,
        "tenses": """
        <div class="interactive-timeline-container" id="timeline_widget">
          <div class="timeline-widget-header">
            <span class="tl-icon">⏳</span>
            <div>
              <h4 class="tl-title">MA TRẬN TRỤC THỜI GIAN NGỮ PHÁP TƯƠNG TÁC (FEYNMAN TIMELINE)</h4>
              <p class="tl-desc">Bấm vào bất kỳ thì nào trên trục để xem trực quan vị trí thời gian, công thức chuẩn và bẫy đề thi:</p>
            </div>
          </div>
          <div class="timeline-visual-track">
            <div class="tl-time-axis">
              <span class="axis-point past">QUÁ KHỨ (PAST)</span>
              <span class="axis-point present active">HIỆN TẠI (PRESENT)</span>
              <span class="axis-point future">TƯƠNG LAI (FUTURE)</span>
            </div>
            <div class="tl-pills-row">
              <button class="tl-pill" onclick="selectTimelineTense('past_simple')">Quá khứ đơn</button>
              <button class="tl-pill" onclick="selectTimelineTense('past_cont')">Quá khứ tiếp diễn</button>
              <button class="tl-pill" onclick="selectTimelineTense('past_perf')">Quá khứ hoàn thành</button>
              <button class="tl-pill active" onclick="selectTimelineTense('pres_simple')">Hiện tại đơn</button>
              <button class="tl-pill" onclick="selectTimelineTense('pres_cont')">Hiện tại tiếp diễn</button>
              <button class="tl-pill highlight" onclick="selectTimelineTense('pres_perf')">Hiện tại hoàn thành (Trọng tâm)</button>
              <button class="tl-pill" onclick="selectTimelineTense('fut_simple')">Tương lai đơn</button>
              <button class="tl-pill" onclick="selectTimelineTense('near_fut')">Tương lai gần</button>
            </div>
          </div>
          <div class="timeline-detail-card" id="timeline_detail_card">
            <!-- Dynamic content populated by JS -->
          </div>
        </div>
        """
    }

def md_to_html_body(md_text: str) -> str:
    """Parse standard markdown body lines with tables, callouts, and lists."""
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
            html_parts.append("<hr class='content-divider'>")
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
                html_parts.append(f"<div class='mermaid-wrapper'><div class='mermaid'>{raw_code}</div></div>")
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
            icon_map = {
                "BLUE": "💎",
                "GREEN": "💡",
                "YELLOW": "⚠️",
                "RED": "🚨",
                "PURPLE": "⭐"
            }
            c_icon = icon_map.get(c_type, "📌")
            content_html = "<br>".join(render_inline(cl) for cl in c_lines)
            html_parts.append(f"""
            <div class='callout {cls_name}'>
              <div class='callout-icon'>{c_icon}</div>
              <div class='callout-body'>{content_html}</div>
            </div>
            """)
            continue

        # Regular blockquote: > ...
        if line.startswith(">"):
            b_lines = [line[1:].strip()]
            i += 1
            while i < n and lines[i].startswith(">"):
                b_lines.append(lines[i][1:].strip())
                i += 1
            b_html = "<br>".join(render_inline(bl) for bl in b_lines)
            html_parts.append(f"<blockquote class='modern-quote'>{b_html}</blockquote>")
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
                html_parts.append(f"<div class='table-responsive'><table class='master-table'><thead><tr>{th_html}</tr></thead><tbody>{''.join(tb_html)}</tbody></table></div>")
            continue

        # Bullet list
        if line.startswith("- ") or line.startswith("* "):
            html_parts.append(f"<li class='bullet-item'>{render_inline(line[2:])}</li>")
            i += 1
            continue

        # Paragraph
        html_parts.append(f"<p class='paragraph'>{render_inline(line)}</p>")
        i += 1

    return "\n".join(html_parts)

def build_full_application():
    wizards = build_interactive_wizards()
    sections_html = []
    toc_html = []
    
    total_quizzes_in_app = 0
    module_summaries = []

    for part_idx, (part_title, modules) in enumerate(MODULE_FILES, 1):
        toc_html.append(f"""
        <div class="toc-category-group" data-cat="{part_idx}">
          <div class="toc-cat-header">
            <span class="toc-cat-badge">Phần {part_idx}</span>
            <span class="toc-cat-title">{part_title.split(':')[1].strip() if ':' in part_title else part_title}</span>
          </div>
          <ul class="toc-items-list">
        """)
        
        for file_path, mod_name, mod_id in modules:
            anchor = f"mod_{mod_id}"
            toc_html.append(f"""
            <li class="toc-item" data-target="{anchor}">
              <a href="#{anchor}" class="toc-link">
                <span class="toc-dot"></span>
                <span class="toc-text">{mod_name}</span>
              </a>
            </li>
            """)
            
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_text = f.read()
                    
                questions, text_without_quiz = parse_quizzes(raw_text, mod_id)
                body_html = md_to_html_body(text_without_quiz)
                quiz_html = build_quiz_html(questions, mod_id, mod_name)
                total_quizzes_in_app += len([q for q in questions if q["type"] == "mcq"])
                
                # Check if this module has a custom interactive wizard widget
                wizard_widget = wizards.get(mod_id, "")
                
                module_summaries.append({
                    "id": anchor,
                    "title": mod_name,
                    "part": part_title,
                    "questions_count": len(questions)
                })
                
                sections_html.append(f"""
                <section id="{anchor}" class="module-card-section" data-mod-id="{mod_id}" data-category="{part_idx}">
                  <div class="module-badge-row">
                    <span class="module-part-tag">{part_title.split(':')[0]}</span>
                    <span class="module-status-pill">⭐ Chuẩn ma trận Sở GD Quảng Ngãi</span>
                    <span class="module-qcount-pill">{len(questions)} câu thực chiến</span>
                  </div>
                  
                  {wizard_widget}
                  
                  <div class="module-content-body">
                    {body_html}
                  </div>
                  
                  {quiz_html}
                </section>
                """)
            else:
                sections_html.append(f"""
                <section id="{anchor}" class="module-card-section">
                  <p><em>File {file_path} đang được cập nhật.</em></p>
                </section>
                """)
                
        toc_html.append("</ul></div>")

    # Embed complete responsive UI & JS into Master Template
    app_html = f"""<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cẩm Nang Sư Phạm Ôn Thi Vào 10 Tiếng Anh - Master EdTech App 2026-2027</title>
  
  <!-- Modern Google Fonts with full Vietnamese support -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  
  <!-- Mermaid.js for Visual Knowledge Graphs -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'base',
      themeVariables: {{
        primaryColor: '#eff6ff',
        primaryTextColor: '#1e3a8a',
        primaryBorderColor: '#3b82f6',
        lineColor: '#64748b',
        secondaryColor: '#f0fdf4',
        tertiaryColor: '#fefce8',
        fontSize: '15px',
        fontFamily: 'Plus Jakarta Sans, sans-serif'
      }}
    }});
  </script>

  <style>
    /* ==============================================================================
       1. CSS CUSTOM PROPERTIES & DESIGN TOKENS (LIGHT & DARK THEMES)
       ============================================================================== */
    :root {{
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --primary-light: #eff6ff;
      --primary-rgb: 37, 99, 235;
      
      --accent-teal: #0d9488;
      --accent-purple: #7c3aed;
      
      --success: #16a34a;
      --success-light: #f0fdf4;
      --success-border: #bbf7d0;
      
      --warning: #d97706;
      --warning-light: #fefce8;
      --warning-border: #fde047;
      
      --error: #dc2626;
      --error-light: #fef2f2;
      --error-border: #fecaca;
      
      --bg-body: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-subtle: #f1f5f9;
      
      --border-color: #e2e8f0;
      --border-subtle: #cbd5e1;
      
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-soft: #64748b;
      
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
      --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
      
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-heading: 'Outfit', 'Plus Jakarta Sans', sans-serif;
      --font-mono: 'JetBrains Mono', Consolas, monospace;
      
      --sidebar-width: 320px;
      --header-height: 70px;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-xl: 24px;
    }}

    [data-theme="dark"] {{
      --primary: #3b82f6;
      --primary-hover: #60a5fa;
      --primary-light: rgba(59, 130, 246, 0.15);
      
      --bg-body: #0b0f19;
      --bg-surface: #111827;
      --bg-card: #131b2e;
      --bg-subtle: #1e293b;
      
      --border-color: #1f293d;
      --border-subtle: #334155;
      
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-soft: #94a3b8;
      
      --success: #22c55e;
      --success-light: rgba(34, 197, 94, 0.15);
      --success-border: #166534;
      
      --error: #ef4444;
      --error-light: rgba(239, 68, 68, 0.15);
      --error-border: #991b1b;
      
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }}

    /* ==============================================================================
       2. GLOBAL RESETS & TYPOGRAPHY
       ============================================================================== */
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html {{
      scroll-behavior: smooth;
      font-size: 16px;
    }}

    body {{
      font-family: var(--font-body);
      background-color: var(--bg-body);
      color: var(--text-main);
      line-height: 1.7;
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    h1, h2, h3, h4, h5, h6 {{
      font-family: var(--font-heading);
      color: var(--text-main);
      font-weight: 700;
      letter-spacing: -0.02em;
    }}

    a {{
      color: var(--primary);
      text-decoration: none;
      transition: color 0.2s ease;
    }}

    a:hover {{
      color: var(--primary-hover);
    }}

    code, pre {{
      font-family: var(--font-mono);
    }}

    .inline-code {{
      background: var(--bg-subtle);
      color: var(--primary);
      padding: 3px 7px;
      border-radius: var(--radius-sm);
      font-size: 0.9em;
      font-weight: 600;
      border: 1px solid var(--border-color);
    }}

    .phonetic-highlight {{
      color: #e11d48;
      text-decoration: underline;
      text-decoration-thickness: 2.5px;
      text-underline-offset: 3px;
    }}

    /* ==============================================================================
       3. TOP STICKY NAVBAR & CONTROLS
       ============================================================================== */
    .app-header {{
      position: sticky;
      top: 0;
      z-index: 1000;
      height: var(--header-height);
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      transition: background 0.3s ease, border-color 0.3s ease;
    }}

    [data-theme="dark"] .app-header {{
      background: rgba(17, 24, 39, 0.85);
      border-color: var(--border-color);
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .sidebar-toggle-btn {{
      display: none;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      border-radius: var(--radius-sm);
      width: 40px;
      height: 40px;
      font-size: 1.2rem;
      cursor: pointer;
      align-items: center;
      justify-content: center;
    }}

    .brand-logo-link {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }}

    .brand-icon-wrapper {{
      width: 42px;
      height: 42px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, #2563eb, #3b82f6);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 1.35rem;
      box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
    }}

    .brand-text-block h1 {{
      font-size: 1.15rem;
      margin: 0;
      line-height: 1.2;
    }}

    .brand-text-block span {{
      font-size: 0.75rem;
      color: var(--text-soft);
      font-weight: 500;
    }}

    .header-center {{
      flex: 1;
      max-width: 480px;
      margin: 0 24px;
      position: relative;
    }}

    .search-input-box {{
      width: 100%;
      height: 42px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: 9999px;
      padding: 0 18px 0 42px;
      font-size: 0.92rem;
      color: var(--text-main);
      outline: none;
      transition: all 0.2s ease;
    }}

    .search-input-box:focus {{
      border-color: var(--primary);
      background: var(--bg-surface);
      box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.15);
    }}

    .search-icon-svg {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-soft);
      pointer-events: none;
    }}

    .search-results-dropdown {{
      position: absolute;
      top: calc(100% + 8px);
      left: 0;
      right: 0;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-xl);
      max-height: 380px;
      overflow-y: auto;
      display: none;
      z-index: 1001;
    }}

    .search-result-item {{
      padding: 10px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-color);
      cursor: pointer;
      transition: background 0.15s ease;
    }}

    .search-result-item:hover {{
      background: var(--primary-light);
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .mode-switch-btn {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .mode-switch-btn:hover {{
      border-color: var(--primary);
      background: var(--primary-light);
    }}

    .theme-toggle-btn {{
      width: 40px;
      height: 40px;
      border-radius: 9999px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.1rem;
      transition: all 0.2s ease;
    }}

    .theme-toggle-btn:hover {{
      border-color: var(--primary);
      transform: rotate(15deg);
    }}

    /* Global Progress Bar under header */
    .global-progress-line {{
      position: absolute;
      bottom: 0;
      left: 0;
      height: 3px;
      background: linear-gradient(90deg, #2563eb, #10b981);
      width: 0%;
      transition: width 0.3s ease;
    }}

    /* ==============================================================================
       4. APP LAYOUT: SIDEBAR + MAIN CONTENT
       ============================================================================== */
    .app-layout-container {{
      display: flex;
      min-height: calc(100vh - var(--header-height));
      max-width: 1560px;
      margin: 0 auto;
      padding: 0 16px;
      position: relative;
    }}

    .app-sidebar {{
      width: var(--sidebar-width);
      position: sticky;
      top: var(--header-height);
      height: calc(100vh - var(--header-height));
      overflow-y: auto;
      padding: 24px 16px 40px 0;
      border-right: 1px solid var(--border-color);
      flex-shrink: 0;
    }}

    .sidebar-inner-block {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    .toc-cat-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      font-weight: 700;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--primary);
    }}

    .toc-cat-badge {{
      background: var(--primary-light);
      padding: 2px 6px;
      border-radius: var(--radius-sm);
    }}

    .toc-items-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}

    .toc-link {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      border-radius: var(--radius-md);
      font-size: 0.9rem;
      color: var(--text-muted);
      font-weight: 500;
      line-height: 1.4;
      transition: all 0.15s ease;
    }}

    .toc-link:hover {{
      background: var(--bg-subtle);
      color: var(--primary);
    }}

    .toc-item.active .toc-link {{
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 700;
    }}

    .toc-dot {{
      width: 6px;
      height: 6px;
      border-radius: 9999px;
      background: var(--border-subtle);
      transition: transform 0.2s ease, background 0.2s ease;
      flex-shrink: 0;
    }}

    .toc-item.active .toc-dot {{
      background: var(--primary);
      transform: scale(1.6);
    }}

    /* Main Content Area */
    .app-main-content {{
      flex: 1;
      min-width: 0;
      padding: 32px 32px 80px 48px;
      max-width: 1040px;
    }}

    /* Hero Banner Card */
    .hero-banner-card {{
      background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #0d9488 100%);
      color: white;
      padding: 44px 36px;
      border-radius: var(--radius-xl);
      box-shadow: 0 12px 30px -5px rgba(37, 99, 235, 0.35);
      margin-bottom: 36px;
      position: relative;
      overflow: hidden;
    }}

    .hero-banner-card::after {{
      content: '';
      position: absolute;
      top: -40px;
      right: -40px;
      width: 200px;
      height: 200px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 9999px;
      pointer-events: none;
    }}

    .hero-badge {{
      display: inline-block;
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(8px);
      padding: 4px 14px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 14px;
      letter-spacing: 0.04em;
    }}

    .hero-title {{
      font-size: 2.2rem;
      color: white;
      margin-bottom: 12px;
      line-height: 1.25;
    }}

    .hero-subtitle {{
      font-size: 1.1rem;
      opacity: 0.94;
      line-height: 1.6;
      max-width: 800px;
    }}

    .hero-stats-row {{
      display: flex;
      gap: 24px;
      margin-top: 24px;
      padding-top: 20px;
      border-top: 1px solid rgba(255, 255, 255, 0.2);
      flex-wrap: wrap;
    }}

    .hero-stat-item strong {{
      font-size: 1.4rem;
      display: block;
    }}

    .hero-stat-item span {{
      font-size: 0.85rem;
      opacity: 0.85;
    }}

    /* ==============================================================================
       5. MODULE SECTIONS & PEDAGOGICAL COMPONENTS
       ============================================================================== */
    .module-card-section {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 40px;
      margin-bottom: 48px;
      box-shadow: var(--shadow-sm);
      transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }}

    .module-card-section:hover {{
      box-shadow: var(--shadow-md);
      border-color: var(--border-subtle);
    }}

    .module-badge-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}

    .module-part-tag {{
      background: var(--primary-light);
      color: var(--primary);
      font-size: 0.8rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
      text-transform: uppercase;
    }}

    .module-status-pill {{
      background: var(--success-light);
      color: var(--success);
      font-size: 0.8rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
    }}

    .module-qcount-pill {{
      background: var(--bg-subtle);
      color: var(--text-soft);
      font-size: 0.8rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
    }}

    h1.section-title {{
      font-size: 1.85rem;
      margin-bottom: 24px;
      padding-bottom: 14px;
      border-bottom: 2px solid var(--border-color);
      color: var(--text-main);
    }}

    h2.sub-title {{
      font-size: 1.45rem;
      margin: 36px 0 18px 0;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    h3.topic-title {{
      font-size: 1.2rem;
      margin: 26px 0 14px 0;
      color: var(--primary);
    }}

    .content-divider {{
      border: 0;
      height: 1px;
      background: var(--border-color);
      margin: 32px 0;
    }}

    .paragraph {{
      margin-bottom: 16px;
      color: var(--text-muted);
      font-size: 1.02rem;
    }}

    .bullet-item {{
      margin-left: 24px;
      margin-bottom: 8px;
      color: var(--text-muted);
      font-size: 1.02rem;
    }}

    /* Callout Design System (Feynman Core, Rules, Exceptions, Traps) */
    .callout {{
      display: flex;
      gap: 16px;
      padding: 20px 24px;
      border-radius: var(--radius-md);
      margin: 24px 0;
      border: 1px solid transparent;
      box-shadow: var(--shadow-sm);
    }}

    .callout-icon {{
      font-size: 1.5rem;
      flex-shrink: 0;
      line-height: 1.2;
    }}

    .callout-body {{
      font-size: 1rem;
      line-height: 1.65;
    }}

    .callout-blue {{
      background: #eff6ff;
      border-color: #bfdbfe;
      color: #1e3a8a;
    }}
    [data-theme="dark"] .callout-blue {{
      background: rgba(30, 58, 138, 0.25);
      border-color: #1e40af;
      color: #bfdbfe;
    }}

    .callout-green {{
      background: #f0fdf4;
      border-color: #bbf7d0;
      color: #14532d;
    }}
    [data-theme="dark"] .callout-green {{
      background: rgba(20, 83, 45, 0.25);
      border-color: #166534;
      color: #bbf7d0;
    }}

    .callout-yellow {{
      background: #fefce8;
      border-color: #fef08a;
      color: #713f12;
    }}
    [data-theme="dark"] .callout-yellow {{
      background: rgba(113, 63, 18, 0.25);
      border-color: #854d0e;
      color: #fef08a;
    }}

    .callout-red {{
      background: #fef2f2;
      border-color: #fecaca;
      color: #7f1d1d;
    }}
    [data-theme="dark"] .callout-red {{
      background: rgba(127, 29, 29, 0.25);
      border-color: #991b1b;
      color: #fecaca;
    }}

    .callout-purple {{
      background: #faf5ff;
      border-color: #e9d5ff;
      color: #581c87;
    }}
    [data-theme="dark"] .callout-purple {{
      background: rgba(88, 28, 135, 0.25);
      border-color: #6b21a8;
      color: #e9d5ff;
    }}

    /* Table Styles */
    .table-responsive {{
      overflow-x: auto;
      margin: 24px 0;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
    }}

    .master-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.95rem;
      text-align: left;
    }}

    .master-table th {{
      background: var(--bg-subtle);
      color: var(--text-main);
      font-weight: 700;
      padding: 14px 18px;
      border-bottom: 2px solid var(--border-color);
    }}

    .master-table td {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-muted);
    }}

    .master-table tr:last-child td {{
      border-bottom: 0;
    }}

    .master-table tr:hover td {{
      background: var(--primary-light);
    }}

    /* Mermaid Graph Wrapper */
    .mermaid-wrapper {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 24px;
      margin: 28px 0;
      display: flex;
      justify-content: center;
      overflow-x: auto;
    }}

    /* ==============================================================================
       6. INTERACTIVE PRONUNCIATION WIZARDS & TENSE TIMELINE
       ============================================================================== */
    .interactive-wizard-card {{
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.05), rgba(13, 148, 136, 0.05));
      border: 2px dashed var(--primary);
      border-radius: var(--radius-lg);
      padding: 24px 28px;
      margin: 28px 0;
    }}

    .wizard-header {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 18px;
    }}

    .wizard-icon {{
      font-size: 2rem;
    }}

    .wizard-title {{
      font-size: 1.15rem;
      color: var(--primary);
      margin: 0;
    }}

    .wizard-desc {{
      font-size: 0.9rem;
      color: var(--text-soft);
      margin: 2px 0 0 0;
    }}

    .wizard-input-box {{
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
    }}

    .wizard-input-box input {{
      flex: 1;
      height: 46px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 0 16px;
      font-size: 1rem;
      color: var(--text-main);
      outline: none;
    }}

    .wizard-input-box input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.15);
    }}

    .wizard-input-box button {{
      padding: 0 24px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: var(--radius-md);
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      transition: background 0.2s ease;
    }}

    .wizard-input-box button:hover {{
      background: var(--primary-hover);
    }}

    .wizard-result-box {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }}

    .wiz-res-label {{
      font-weight: 600;
      color: var(--text-soft);
    }}

    .wiz-res-badge {{
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 800;
      font-size: 1.15rem;
      padding: 4px 14px;
      border-radius: 9999px;
    }}

    .wiz-res-rule {{
      color: var(--text-muted);
      font-size: 0.95rem;
    }}

    .wizard-quick-tags {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      font-size: 0.85rem;
      color: var(--text-soft);
    }}

    .wizard-quick-tags button {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.82rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .wizard-quick-tags button:hover {{
      border-color: var(--primary);
      color: var(--primary);
    }}

    /* Timeline Widget Styles */
    .interactive-timeline-container {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 28px;
      margin: 32px 0;
      box-shadow: var(--shadow-sm);
    }}

    .timeline-widget-header {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 24px;
    }}

    .tl-icon {{
      font-size: 2rem;
    }}

    .tl-title {{
      font-size: 1.25rem;
      color: var(--text-main);
      margin: 0;
    }}

    .tl-desc {{
      font-size: 0.9rem;
      color: var(--text-soft);
      margin: 2px 0 0 0;
    }}

    .timeline-visual-track {{
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 24px;
    }}

    .tl-time-axis {{
      display: flex;
      justify-content: space-between;
      position: relative;
      margin-bottom: 20px;
      padding: 0 10px;
    }}

    .tl-time-axis::before {{
      content: '';
      position: absolute;
      top: 50%;
      left: 20px;
      right: 20px;
      height: 3px;
      background: linear-gradient(90deg, #94a3b8, #3b82f6, #10b981);
      z-index: 1;
      transform: translateY(-50%);
    }}

    .axis-point {{
      position: relative;
      z-index: 2;
      background: var(--bg-surface);
      border: 2px solid var(--border-subtle);
      padding: 4px 14px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--text-soft);
    }}

    .axis-point.active {{
      border-color: var(--primary);
      color: var(--primary);
      box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.2);
    }}

    .tl-pills-row {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
    }}

    .tl-pill {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .tl-pill:hover {{
      border-color: var(--primary);
      color: var(--primary);
    }}

    .tl-pill.active {{
      background: var(--primary);
      color: white;
      border-color: var(--primary);
      box-shadow: 0 4px 10px rgba(var(--primary-rgb), 0.3);
    }}

    .tl-pill.highlight {{
      border-color: var(--warning);
      color: var(--warning);
    }}

    .timeline-detail-card {{
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 22px 24px;
      border-left: 5px solid var(--primary);
    }}

    /* ==============================================================================
       7. INTERACTIVE QUIZ ENGINE (PRACTICE VS EXAM MODES)
       ============================================================================== */
    .interactive-quiz-wrapper {{
      background: var(--bg-surface);
      border: 2px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 32px;
      margin: 40px 0;
      box-shadow: var(--shadow-md);
    }}

    .quiz-header-panel {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}

    .quiz-title-box {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .quiz-icon-badge {{
      font-size: 1.8rem;
    }}

    .quiz-main-title {{
      font-size: 1.3rem;
      margin: 0;
      color: var(--text-main);
    }}

    .quiz-sub-desc {{
      font-size: 0.88rem;
      color: var(--text-soft);
      margin: 2px 0 0 0;
    }}

    .quiz-mode-pill {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-subtle);
      padding: 4px;
      border-radius: 9999px;
      border: 1px solid var(--border-color);
    }}

    .mode-label {{
      font-size: 0.78rem;
      color: var(--text-soft);
      font-weight: 600;
      margin-left: 8px;
    }}

    .mode-tag {{
      padding: 5px 14px;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      color: var(--text-soft);
      transition: all 0.2s ease;
    }}

    .mode-tag.active {{
      background: var(--bg-surface);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }}

    /* Quiz Tracker Bar */
    .quiz-tracker-bar {{
      margin-bottom: 28px;
    }}

    .tracker-info {{
      display: flex;
      justify-content: space-between;
      font-size: 0.88rem;
      color: var(--text-soft);
      margin-bottom: 6px;
      font-weight: 600;
    }}

    .tracker-progress-track {{
      height: 8px;
      background: var(--bg-subtle);
      border-radius: 9999px;
      overflow: hidden;
    }}

    .tracker-progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, #2563eb, #10b981);
      border-radius: 9999px;
      transition: width 0.3s ease;
    }}

    /* Question Card */
    .quiz-question-card {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 24px;
      margin-bottom: 24px;
      transition: all 0.2s ease;
    }}

    .quiz-question-card:hover {{
      border-color: var(--border-subtle);
    }}

    .question-meta-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .question-number-badge {{
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 800;
      font-size: 0.82rem;
      padding: 3px 10px;
      border-radius: 9999px;
    }}

    .question-status-badge {{
      font-size: 0.78rem;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 9999px;
    }}

    .status-unanswered {{
      background: var(--bg-body);
      color: var(--text-soft);
    }}

    .status-correct {{
      background: var(--success-light);
      color: var(--success);
    }}

    .status-incorrect {{
      background: var(--error-light);
      color: var(--error);
    }}

    .question-stem-text {{
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 18px;
      line-height: 1.5;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .audio-speaker-btn {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      width: 32px;
      height: 32px;
      border-radius: 9999px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 0.95rem;
      cursor: pointer;
      color: var(--primary);
      transition: all 0.15s ease;
    }}

    .audio-speaker-btn:hover {{
      transform: scale(1.1);
      background: var(--primary-light);
    }}

    /* Quiz Options Grid */
    .quiz-options-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
    }}

    .quiz-option-btn {{
      background: var(--bg-surface);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      text-align: left;
      font-size: 1rem;
      color: var(--text-main);
      font-family: var(--font-body);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
    }}

    .quiz-option-btn:hover {{
      border-color: var(--primary);
      background: var(--primary-light);
      transform: translateY(-2px);
    }}

    .quiz-option-btn.selected {{
      border-color: var(--primary);
      background: var(--primary-light);
      box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.2);
    }}

    .quiz-option-btn.correct-choice {{
      border-color: var(--success) !important;
      background: var(--success-light) !important;
      color: var(--success) !important;
    }}

    .quiz-option-btn.wrong-choice {{
      border-color: var(--error) !important;
      background: var(--error-light) !important;
      color: var(--error) !important;
    }}

    .opt-letter-circle {{
      width: 28px;
      height: 28px;
      border-radius: 9999px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.85rem;
      flex-shrink: 0;
    }}

    .quiz-option-btn.selected .opt-letter-circle {{
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }}

    .opt-content-text {{
      flex: 1;
    }}

    .opt-audio-btn {{
      font-size: 0.85rem;
      padding: 4px;
      border-radius: 4px;
      color: var(--text-soft);
      cursor: pointer;
    }}

    .opt-audio-btn:hover {{
      color: var(--primary);
    }}

    /* Explanation Panel */
    .question-explanation-panel {{
      margin-top: 18px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      animation: fadeInDown 0.3s ease;
    }}

    @keyframes fadeInDown {{
      from {{
        opacity: 0;
        transform: translateY(-8px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    .exp-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
    }}

    .exp-badge {{
      font-weight: 700;
      font-size: 0.88rem;
      color: var(--primary);
    }}

    .exp-correct-key {{
      font-size: 0.88rem;
      color: var(--success);
    }}

    .exp-body-text {{
      font-size: 0.95rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 12px;
    }}

    .retry-question-btn {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-soft);
      padding: 4px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .retry-question-btn:hover {{
      border-color: var(--primary);
      color: var(--primary);
    }}

    /* Transformation Cards */
    .transformation-section-title {{
      margin: 32px 0 16px 0;
      padding-top: 20px;
      border-top: 1px solid var(--border-color);
    }}

    .transformation-section-title h4 {{
      font-size: 1.15rem;
      color: var(--text-main);
    }}

    .transformation-section-title p {{
      font-size: 0.9rem;
      color: var(--text-soft);
    }}

    .transformation-card {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 18px;
    }}

    .trans-meta {{
      margin-bottom: 8px;
    }}

    .trans-stem {{
      font-size: 1.05rem;
      font-weight: 600;
      margin-bottom: 12px;
    }}

    .trans-input-row {{
      display: flex;
      gap: 10px;
    }}

    .trans-input-box {{
      flex: 1;
      height: 42px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 0 16px;
      font-size: 0.95rem;
      color: var(--text-main);
      outline: none;
    }}

    .trans-input-box:focus {{
      border-color: var(--primary);
    }}

    .trans-check-btn {{
      padding: 0 18px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      font-weight: 600;
      font-size: 0.88rem;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .trans-check-btn:hover {{
      border-color: var(--primary);
      color: var(--primary);
    }}

    .trans-model-answer {{
      margin-top: 14px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--success);
      border-radius: var(--radius-md);
      padding: 14px 18px;
    }}

    .model-badge {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--success);
      margin-bottom: 4px;
    }}

    .model-text {{
      font-size: 0.95rem;
      color: var(--text-muted);
    }}

    /* Quiz Footer Actions & Results Banner */
    .quiz-footer-actions {{
      display: flex;
      gap: 14px;
      margin-top: 28px;
      flex-wrap: wrap;
    }}

    .submit-exam-btn {{
      flex: 1;
      height: 48px;
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: white;
      border: none;
      border-radius: var(--radius-md);
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
      transition: all 0.2s ease;
    }}

    .submit-exam-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
    }}

    .reset-quiz-btn {{
      padding: 0 20px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-soft);
      font-weight: 600;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .reset-quiz-btn:hover {{
      border-color: var(--error);
      color: var(--error);
    }}

    .exam-result-banner {{
      margin-top: 24px;
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(16, 185, 129, 0.1));
      border: 2px solid var(--success);
      border-radius: var(--radius-lg);
      padding: 24px 28px;
      animation: fadeInDown 0.4s ease;
    }}

    .result-banner-content {{
      display: flex;
      align-items: center;
      gap: 24px;
    }}

    .result-score-circle {{
      width: 72px;
      height: 72px;
      border-radius: 9999px;
      background: var(--success);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.5rem;
      flex-shrink: 0;
      box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
    }}

    .result-score-max {{
      font-size: 0.9rem;
      font-weight: 600;
      opacity: 0.85;
    }}

    .result-heading {{
      font-size: 1.25rem;
      margin: 0 0 4px 0;
      color: var(--text-main);
    }}

    .result-comment {{
      font-size: 0.95rem;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}

    .result-meta-tags {{
      display: flex;
      gap: 10px;
    }}

    .result-tag {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 2px 10px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text-soft);
    }}

    .hidden {{
      display: none !important;
    }}

    /* ==============================================================================
       8. FLOATING QUICK ACTIONS & BACK TO TOP
       ============================================================================== */
    .floating-tools-dock {{
      position: fixed;
      bottom: 28px;
      right: 28px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 999;
    }}

    .float-tool-btn {{
      width: 46px;
      height: 46px;
      border-radius: 9999px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: var(--shadow-lg);
      font-size: 1.2rem;
      transition: all 0.2s ease;
    }}

    .float-tool-btn:hover {{
      transform: translateY(-3px);
      border-color: var(--primary);
      color: var(--primary);
    }}

    /* ==============================================================================
       9. RESPONSIVE DESIGN BREAKPOINTS
       ============================================================================== */
    @media (max-width: 1024px) {{
      .app-sidebar {{
        position: fixed;
        left: -340px;
        top: var(--header-height);
        bottom: 0;
        background: var(--bg-surface);
        z-index: 1050;
        padding: 24px;
        box-shadow: var(--shadow-xl);
        transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      }}

      .app-sidebar.open {{
        left: 0;
      }}

      .sidebar-toggle-btn {{
        display: flex;
      }}

      .app-main-content {{
        padding: 24px 16px 80px 16px;
      }}
    }}

    @media (max-width: 768px) {{
      .header-center {{
        display: none;
      }}
      .hero-title {{
        font-size: 1.7rem;
      }}
      .module-card-section {{
        padding: 24px 18px;
      }}
      .quiz-options-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Print Optimization */
    @media print {{
      .app-header, .app-sidebar, .floating-tools-dock, .quiz-footer-actions, .wizard-interactive-flow {{
        display: none !important;
      }}
      .app-main-content {{
        max-width: 100% !important;
        padding: 0 !important;
      }}
      .module-card-section {{
        box-shadow: none !important;
        border: none !important;
        page-break-after: always;
      }}
    }}
  </style>
</head>
<body>

  <!-- 1. STICKY TOP APP HEADER -->
  <header class="app-header">
    <div class="header-left">
      <button class="sidebar-toggle-btn" id="sidebar_toggle" onclick="toggleSidebar()" title="Mở danh mục chuyên đề">☰</button>
      <a href="#" class="brand-logo-link">
        <div class="brand-icon-wrapper">🎓</div>
        <div class="brand-text-block">
          <h1>ANH VĂN 10 MASTERY</h1>
          <span>Cẩm Nang Tuyển Sinh 2026-2027</span>
        </div>
      </a>
    </div>

    <div class="header-center">
      <svg class="search-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="text" class="search-input-box" id="global_search" placeholder="Tìm chuyên đề, quy tắc, câu thần chú, thì... (Ctrl+K)" oninput="handleGlobalSearch(this.value)">
      <div class="search-results-dropdown" id="search_dropdown"></div>
    </div>

    <div class="header-right">
      <button class="mode-switch-btn" id="global_mode_btn" onclick="toggleGlobalMode()" title="Chuyển chế độ luyện tập hoặc thi thử">
        <span id="global_mode_icon">🎯</span>
        <span id="global_mode_text">Luyện tập</span>
      </button>
      <button class="theme-toggle-btn" id="theme_toggle" onclick="toggleTheme()" title="Chuyển giao diện Sáng / Tối">🌙</button>
    </div>
    
    <div class="global-progress-line" id="global_progress_line"></div>
  </header>

  <!-- 2. MAIN APP LAYOUT: SIDEBAR + CONTENT -->
  <div class="app-layout-container">
    
    <!-- LEFT SIDEBAR -->
    <aside class="app-sidebar" id="app_sidebar">
      <div class="sidebar-inner-block">
        <div class="sidebar-title-row">
          <span style="font-size: 0.82rem; font-weight: 700; color: var(--text-soft); text-transform: uppercase;">MỤC LỤC CHUYÊN ĐỀ ({len(module_summaries)})</span>
        </div>
        { "".join(toc_html) }
      </div>
    </aside>

    <!-- MAIN LEARNING AREA -->
    <main class="app-main-content">
      
      <!-- HERO BANNER -->
      <div class="hero-banner-card">
        <span class="hero-badge">HỆ THỐNG SƯ PHẠM ĐỘC QUYỀN • CHUẨN SỞ GD&ĐT QUẢNG NGÃI</span>
        <h2 class="hero-title">Cẩm Nang Sư Phạm Tiếng Anh Ôn Thi Vào 10 Master</h2>
        <p class="hero-subtitle">Học sâu hiểu bản chất (Feynman Core) kết hợp Bộ Thần Chú Tiếng Việt 5 giây ăn trọn 100% điểm Ngữ âm, Ngữ pháp & Từ vựng bẫy trong kỳ thi tuyển sinh.</p>
        
        <div class="hero-stats-row">
          <div class="hero-stat-item">
            <strong>16 Chuyên Đề</strong>
            <span>Đầy đủ Ngữ âm - Ngữ pháp - Từ vựng</span>
          </div>
          <div class="hero-stat-item">
            <strong>160 Câu Thực Chiến</strong>
            <span>Giải chi tiết từng phương án</span>
          </div>
          <div class="hero-stat-item">
            <strong>2 Chế Độ Học</strong>
            <span>Luyện tập tức thì & Thi thử tính điểm</span>
          </div>
          <div class="hero-stat-item">
            <strong>100% Offline</strong>
            <span>Lưu tiến độ tự động trên máy</span>
          </div>
        </div>
      </div>

      <!-- ALL 16 MODULE SECTIONS -->
      { "".join(sections_html) }

    </main>
  </div>

  <!-- FLOATING QUICK ACTIONS -->
  <div class="floating-tools-dock">
    <button class="float-tool-btn" onclick="scrollToTop()" title="Lên đầu trang">⬆</button>
    <button class="float-tool-btn" onclick="resetAllProgress()" title="Đặt lại toàn bộ tiến độ">🔄</button>
  </div>

  <!-- CLIENT-SIDE JS APPLICATION ENGINE -->
  <script>
    // ==============================================================================
    // 1. STATE MANAGEMENT & LOCAL STORAGE
    // ==============================================================================
    const APP_STORAGE_KEY = 'AnhVan10_Master_Progress_v1';
    
    let appState = {{
      theme: 'light',
      globalMode: 'practice', // 'practice' or 'exam'
      answers: {{}},          // qid -> user_selected_option
      examSubmitted: {{}},   // mod_id -> boolean
      examScores: {{}},      // mod_id -> score
      activeSection: null
    }};

    // Load from localStorage
    function loadSavedState() {{
      try {{
        const raw = localStorage.getItem(APP_STORAGE_KEY);
        if (raw) {{
          const parsed = JSON.parse(raw);
          appState = Object.assign(appState, parsed);
        }}
      }} catch (e) {{
        console.warn('Cannot load state:', e);
      }}
    }}

    function saveState() {{
      try {{
        localStorage.setItem(APP_STORAGE_KEY, JSON.stringify(appState));
        updateGlobalProgress();
      }} catch (e) {{
        console.warn('Cannot save state:', e);
      }}
    }}

    // ==============================================================================
    // 2. THEME ENGINE & UI TOGGLES
    // ==============================================================================
    function applyTheme(theme) {{
      document.documentElement.setAttribute('data-theme', theme);
      const btn = document.getElementById('theme_toggle');
      if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      appState.theme = theme;
      saveState();
    }}

    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(current === 'light' ? 'dark' : 'light');
    }}

    function toggleGlobalMode() {{
      const newMode = appState.globalMode === 'practice' ? 'exam' : 'practice';
      setGlobalMode(newMode);
    }}

    function setGlobalMode(mode) {{
      appState.globalMode = mode;
      const icon = document.getElementById('global_mode_icon');
      const text = document.getElementById('global_mode_text');
      if (icon && text) {{
        icon.textContent = mode === 'practice' ? '🎯' : '⏱️';
        text.textContent = mode === 'practice' ? 'Luyện tập' : 'Thi thử';
      }}
      
      // Update all quiz wrappers
      document.querySelectorAll('.interactive-quiz-wrapper').forEach(wrapper => {{
        const pTag = wrapper.querySelector('.mode-tag-practice');
        const eTag = wrapper.querySelector('.mode-tag-exam');
        if (mode === 'practice') {{
          pTag?.classList.add('active');
          eTag?.classList.remove('active');
        }} else {{
          eTag?.classList.add('active');
          pTag?.classList.remove('active');
        }}
      }});
      saveState();
    }}

    function toggleSidebar() {{
      const sb = document.getElementById('app_sidebar');
      sb?.classList.toggle('open');
    }}

    function scrollToTop() {{
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // ==============================================================================
    // 3. QUIZ ENGINE (PRACTICE VS EXAM)
    // ==============================================================================
    function handleOptionSelect(qid, optKey) {{
      const card = document.getElementById('card_' + qid);
      if (!card) return;
      
      const correctKey = card.getAttribute('data-correct') || '';
      const wrapper = card.closest('.interactive-quiz-wrapper');
      const modId = wrapper?.getAttribute('data-mod-id') || '';
      
      // Save answer
      appState.answers[qid] = optKey;
      saveState();
      
      // Update selection visual
      card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
        btn.classList.remove('selected');
        if (btn.getAttribute('data-opt') === optKey) {{
          btn.classList.add('selected');
        }}
      }});
      
      // Status badge
      const statusBadge = card.querySelector('.question-status-badge');
      
      if (appState.globalMode === 'practice') {{
        // Practice Mode: Instant Evaluation
        const isCorrect = (optKey.toUpperCase() === correctKey.toUpperCase());
        card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
          const bOpt = btn.getAttribute('data-opt');
          btn.classList.remove('correct-choice', 'wrong-choice');
          if (bOpt === correctKey) {{
            btn.classList.add('correct-choice');
          }} else if (bOpt === optKey && !isCorrect) {{
            btn.classList.add('wrong-choice');
          }}
        }});
        
        if (statusBadge) {{
          statusBadge.textContent = isCorrect ? '✓ Đúng' : '✗ Chưa đúng';
          statusBadge.className = 'question-status-badge ' + (isCorrect ? 'status-correct' : 'status-incorrect');
        }}
        
        // Reveal explanation
        const exp = document.getElementById('exp_' + qid);
        if (exp) exp.classList.remove('hidden');
      }} else {{
        // Exam Mode: Save selection without revealing correctness
        if (statusBadge) {{
          statusBadge.textContent = 'Đã chọn (' + optKey + ')';
          statusBadge.className = 'question-status-badge status-unanswered';
        }}
      }}
      
      updateQuizTracker(modId);
    }}

    function retryQuestion(qid) {{
      const card = document.getElementById('card_' + qid);
      if (!card) return;
      delete appState.answers[qid];
      saveState();
      
      card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
        btn.classList.remove('selected', 'correct-choice', 'wrong-choice');
      }});
      
      const statusBadge = card.querySelector('.question-status-badge');
      if (statusBadge) {{
        statusBadge.textContent = 'Chưa làm';
        statusBadge.className = 'question-status-badge status-unanswered';
      }}
      
      const exp = document.getElementById('exp_' + qid);
      if (exp) exp.classList.add('hidden');
      
      const wrapper = card.closest('.interactive-quiz-wrapper');
      const modId = wrapper?.getAttribute('data-mod-id') || '';
      updateQuizTracker(modId);
    }}

    function updateQuizTracker(modId) {{
      const wrapper = document.getElementById('quiz_' + modId);
      if (!wrapper) return;
      
      const total = parseInt(wrapper.getAttribute('data-total') || '0', 10);
      let answered = 0;
      
      wrapper.querySelectorAll('.quiz-question-card').forEach(card => {{
        const qid = card.getAttribute('data-qid');
        if (appState.answers[qid]) answered++;
      }});
      
      const countEl = wrapper.querySelector('.answered-count');
      if (countEl) countEl.textContent = answered;
      
      const fillEl = wrapper.querySelector('.tracker-progress-fill');
      if (fillEl && total > 0) {{
        fillEl.style.width = Math.round((answered / total) * 100) + '%';
      }}
    }}

    function submitExam(modId) {{
      const wrapper = document.getElementById('quiz_' + modId);
      if (!wrapper) return;
      
      const cards = wrapper.querySelectorAll('.quiz-question-card');
      const total = cards.length;
      let score = 0;
      let unanswered = 0;
      
      cards.forEach(card => {{
        const qid = card.getAttribute('data-qid');
        const correct = (card.getAttribute('data-correct') || '').toUpperCase();
        const userChoice = (appState.answers[qid] || '').toUpperCase();
        
        if (!userChoice) unanswered++;
        
        const isRight = (userChoice === correct);
        if (isRight) score++;
        
        // Highlight all options
        card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
          const bOpt = btn.getAttribute('data-opt');
          btn.classList.remove('correct-choice', 'wrong-choice');
          if (bOpt === correct) {{
            btn.classList.add('correct-choice');
          }} else if (bOpt === userChoice && !isRight) {{
            btn.classList.add('wrong-choice');
          }}
        }});
        
        // Status badge
        const badge = card.querySelector('.question-status-badge');
        if (badge) {{
          badge.textContent = isRight ? '✓ Đúng' : (userChoice ? '✗ Sai' : 'Chưa chọn');
          badge.className = 'question-status-badge ' + (isRight ? 'status-correct' : 'status-incorrect');
        }}
        
        // Reveal explanation
        const exp = document.getElementById('exp_' + qid);
        if (exp) exp.classList.remove('hidden');
      }});
      
      // Save exam result
      appState.examSubmitted[modId] = true;
      appState.examScores[modId] = score;
      saveState();
      
      // Show result banner
      const banner = document.getElementById('result_' + modId);
      const scoreNum = document.getElementById('score_num_' + modId);
      const comment = document.getElementById('comment_' + modId);
      const pctTag = document.getElementById('pct_' + modId);
      
      if (banner && scoreNum) {{
        scoreNum.textContent = score;
        const pct = Math.round((score / total) * 100);
        if (pctTag) pctTag.textContent = 'Tỉ lệ đúng: ' + pct + '%';
        if (comment) {{
          if (pct >= 90) comment.textContent = '🌟 Xuất sắc! Nắm vững 100% bản chất đề thi vào 10!';
          else if (pct >= 70) comment.textContent = '👍 Khá tốt! Hãy ôn lại các câu giải thích màu đỏ để không mất điểm.';
          else comment.textContent = '⚠️ Cần rà soát lại! Hãy đọc kỹ hộp bản chất Feynman phía trên.';
        }}
        banner.classList.remove('hidden');
        banner.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }}
    }}

    function resetQuizSection(modId) {{
      if (!confirm('Bạn có chắc chắn muốn làm lại toàn bộ câu hỏi trong chuyên đề này?')) return;
      const wrapper = document.getElementById('quiz_' + modId);
      if (!wrapper) return;
      
      wrapper.querySelectorAll('.quiz-question-card').forEach(card => {{
        const qid = card.getAttribute('data-qid');
        delete appState.answers[qid];
        card.querySelectorAll('.quiz-option-btn').forEach(btn => btn.classList.remove('selected', 'correct-choice', 'wrong-choice'));
        const badge = card.querySelector('.question-status-badge');
        if (badge) {{
          badge.textContent = 'Chưa làm';
          badge.className = 'question-status-badge status-unanswered';
        }}
        const exp = document.getElementById('exp_' + qid);
        if (exp) exp.classList.add('hidden');
      }});
      
      delete appState.examSubmitted[modId];
      delete appState.examScores[modId];
      saveState();
      
      const banner = document.getElementById('result_' + modId);
      if (banner) banner.classList.add('hidden');
      updateQuizTracker(modId);
    }}

    function toggleTransAnswer(qid) {{
      const el = document.getElementById('model_' + qid);
      if (el) el.classList.toggle('hidden');
    }}

    function updateGlobalProgress() {{
      const allCards = document.querySelectorAll('.quiz-question-card');
      const total = allCards.length;
      if (total === 0) return;
      
      let answered = 0;
      allCards.forEach(c => {{
        const qid = c.getAttribute('data-qid');
        if (appState.answers[qid]) answered++;
      }});
      
      const pct = Math.round((answered / total) * 100);
      const line = document.getElementById('global_progress_line');
      if (line) line.style.width = pct + '%';
    }}

    // ==============================================================================
    // 4. PRONUNCIATION INTERACTIVE WIZARDS (ED & S/ES)
    // ==============================================================================
    function testEdWord(word) {{
      const clean = (word || '').trim().toLowerCase();
      const badge = document.getElementById('ed_res_badge');
      const rule = document.getElementById('ed_res_rule');
      if (!clean) {{
        if (badge) badge.textContent = 'Nhập từ để kiểm tra...';
        if (rule) rule.textContent = '';
        return;
      }}
      
      // Exceptions list (adjectives ending in -ed)
      const exceptions = ['naked', 'wicked', 'sacred', 'beloved', 'crooked', 'ragged', 'hatred', 'wretched', 'learned', 'blessed'];
      if (exceptions.includes(clean)) {{
        badge.textContent = '/ɪd/ (NGOẠI LỆ TÍNH TỪ VÀNG)';
        rule.textContent = 'Từ này là tính từ đặc biệt, luôn phát âm là /ɪd/ bất kể âm tận cùng!';
        badge.style.color = '#dc2626';
        return;
      }}
      
      // Remove trailing ed if present
      let stem = clean;
      if (stem.endsWith('ed')) stem = stem.slice(0, -2);
      else if (stem.endsWith('d')) stem = stem.slice(0, -1);
      
      // Step 1: ending in t or d
      if (stem.endsWith('t') || stem.endsWith('te') || stem.endsWith('d') || stem.endsWith('de')) {{
        badge.textContent = '/ɪd/';
        rule.textContent = 'Âm cuối là /t/ hoặc /d/ ➔ Áp dụng Thần chú "TIỀN ĐÔ"!';
        badge.style.color = '#2563eb';
      }}
      // Step 2: Voiceless (Khi Sang Sông Phải Chờ Phà: k, s, sh, p, ch, f, x, ce)
      else if (stem.endsWith('k') || stem.endsWith('ke') || stem.endsWith('s') || stem.endsWith('ss') || 
               stem.endsWith('sh') || stem.endsWith('p') || stem.endsWith('pe') || stem.endsWith('ch') || 
               stem.endsWith('gh') || stem.endsWith('ph') || stem.endsWith('f') || stem.endsWith('x') || stem.endsWith('ce')) {{
        badge.textContent = '/t/';
        rule.textContent = 'Âm cuối vô thanh ➔ Áp dụng Thần chú "KHI SANG SÔNG PHẢI CHỜ PHÀ"!';
        badge.style.color = '#16a34a';
      }}
      // Step 3: Voiced & Vowels
      else {{
        badge.textContent = '/d/';
        rule.textContent = 'Âm hữu thanh / nguyên âm ➔ Đọc là /d/ (Quy tắc loại trừ)!';
        badge.style.color = '#7c3aed';
      }}
    }}

    function setEdWord(w) {{
      const inp = document.getElementById('ed_word_input');
      if (inp) {{
        inp.value = w;
        testEdWord(w);
      }}
    }}

    function testSesWord(word) {{
      const clean = (word || '').trim().toLowerCase();
      const badge = document.getElementById('ses_res_badge');
      const rule = document.getElementById('ses_res_rule');
      if (!clean) {{
        if (badge) badge.textContent = 'Nhập từ để kiểm tra...';
        if (rule) rule.textContent = '';
        return;
      }}
      
      // Houses exception
      if (clean === 'houses') {{
        badge.textContent = '/ˈhaʊ.zɪz/ (BẪY KINH ĐIỂN)';
        rule.textContent = 'Từ house /haʊs/ khi thêm -es đổi thành /z/ rồi mới thêm /ɪz/!';
        badge.style.color = '#dc2626';
        return;
      }}
      
      let stem = clean;
      if (stem.endsWith('es')) stem = stem.slice(0, -2);
      else if (stem.endsWith('s')) stem = stem.slice(0, -1);
      
      // Step 1: Sibilants /ɪz/ (s, ss, ch, sh, x, z, ge, ce)
      if (stem.endsWith('s') || stem.endsWith('ss') || stem.endsWith('ch') || stem.endsWith('sh') || 
          stem.endsWith('x') || stem.endsWith('z') || stem.endsWith('ge') || stem.endsWith('ce') || stem.endsWith('se')) {{
        badge.textContent = '/ɪz/';
        rule.textContent = 'Âm gió ➔ Áp dụng Thần chú "SÁU CHẠY XE SH ZUI ZẺ"!';
        badge.style.color = '#2563eb';
      }}
      // Step 2: Voiceless /s/ (p, k, f, t, th)
      else if (stem.endsWith('p') || stem.endsWith('k') || stem.endsWith('f') || stem.endsWith('ph') || 
               stem.endsWith('gh') || stem.endsWith('t') || stem.endsWith('th')) {{
        badge.textContent = '/s/';
        rule.textContent = 'Âm vô thanh ➔ Áp dụng Thần chú "THỜI PHONG KIẾN PHƯƠNG TÂY"!';
        badge.style.color = '#16a34a';
      }}
      // Step 3: Voiced & vowels /z/
      else {{
        badge.textContent = '/z/';
        rule.textContent = 'Âm hữu thanh còn lại & nguyên âm ➔ Đọc là /z/!';
        badge.style.color = '#7c3aed';
      }}
    }}

    function setSesWord(w) {{
      const inp = document.getElementById('ses_word_input');
      if (inp) {{
        inp.value = w;
        testSesWord(w);
      }}
    }}

    // ==============================================================================
    // 5. INTERACTIVE GRAMMAR TIMELINE
    // ==============================================================================
    const TENSE_DATA = {{
      past_simple: {{
        name: 'Quá khứ đơn (Past Simple)',
        feynman: 'Hành động ĐÃ CHẤM DỨT HOÀN TOÀN trong quá khứ, biết rõ thời gian, không còn dây dưa tới hiện tại.',
        formula: 'S + V2/ed (Khẳng định) | S + did not + V-inf (Phủ định) | Did + S + V-inf? (Nghi vấn)',
        signals: 'yesterday, ago, last (night/week/year), in 2020, when I was young.',
        trap: 'Bẫy đề thi: Khi có thời gian quá khứ cụ thể ➔ KHÔNG ĐƯỢC DÙNG Hiện tại hoàn thành!'
      }},
      past_cont: {{
        name: 'Quá khứ tiếp diễn (Past Continuous)',
        feynman: 'Hành động ĐANG DIỄN RA tại một thời điểm xác định trong quá khứ, hoặc đang diễn ra thì có hành động khác xen vào.',
        formula: 'S + was/were + V-ing',
        signals: 'at 8 p.m last night, at this time yesterday, while, when + S + V2/ed.',
        trap: 'Cặp thì kinh điển: Hành động ĐANG DIỄN RA (was/were V-ing) thì hành động khác XEN VÀO (V2/ed)!'
      }},
      past_perf: {{
        name: 'Quá khứ hoàn thành (Past Perfect)',
        feynman: 'Hành động xảy ra và hoàn tất TRƯỚC MỘT HÀNH ĐỘNG KHÁC trong quá khứ (Quá khứ của Quá khứ).',
        formula: 'S + had + V3/ed',
        signals: 'by the time, before, after, as soon as.',
        trap: 'After + Had V3/ed, V2/ed | Before + V2/ed, Had V3/ed.'
      }},
      pres_simple: {{
        name: 'Hiện tại đơn (Present Simple)',
        feynman: 'Sự thật hiển nhiên, chân lý tự nhiên, thói quen lặp đi lặp lại hoặc lịch trình tàu xe cố định.',
        formula: 'S + V(s/es) | S + do/does not + V-inf',
        signals: 'always, usually, often, sometimes, never, every day/week, once a month.',
        trap: 'Lịch trình tàu xe, máy bay trong tương lai VẪN DÙNG Hiện tại đơn (The train leaves at 7 a.m tomorrow).'
      }},
      pres_cont: {{
        name: 'Hiện tại tiếp diễn (Present Continuous)',
        feynman: 'Hành động đang diễn ra ngay lúc nói, hoặc phàn nàn thói quen xấu (với always).',
        formula: 'S + am/is/are + V-ing',
        signals: 'now, right now, at the moment, at present, Look!, Listen!, Be quiet!.',
        trap: 'Không dùng với động từ chỉ tri giác/sở hữu (know, believe, understand, have, like, love).'
      }},
      pres_perf: {{
        name: 'Hiện tại hoàn thành (Present Perfect - TRỌNG TÂM CHIẾM 40% ĐỀ)',
        feynman: 'CẦU NỐI giữa Quá khứ và Hiện tại: Bắt đầu từ quá khứ, kéo dài đến hiện tại và còn có thể tiếp diễn trong tương lai.',
        formula: 'S + have/has + V3/ed',
        signals: 'since (mốc TG), for (khoảng TG), already, yet, just, ever, never, recently, so far, up to now.',
        trap: '4 Cặp biến đổi câu tự luận bắt buộc vào 10: started V-ing ... ago ➔ have/has V3/ed for ...'
      }},
      fut_simple: {{
        name: 'Tương lai đơn (Future Simple)',
        feynman: 'Quyết định ĐỘT XUẤT ngay lúc nói, lời hứa, đe dọa, hoặc dự đoán không có căn cứ xác thực.',
        formula: 'S + will + V-inf',
        signals: 'tomorrow, next week, in the future, think, hope, promise.',
        trap: 'Mệnh đề sau liên từ thời gian (when, as soon as, before) TUYỆT ĐỐI KHÔNG DÙNG WILL mà lùi về Hiện tại đơn!'
      }},
      near_fut: {{
        name: 'Tương lai gần (Be going to)',
        feynman: 'Kế hoạch đã có dự định từ trước, hoặc dự đoán CÓ CĂN CỨ THỰC TẾ trước mắt (Ví dụ: Mây đen kéo tới ➔ Sắp mưa).',
        formula: 'S + am/is/are + going to + V-inf',
        signals: 'Look at those dark clouds!, plan, intend to.',
        trap: 'Phân biệt: Sấm chớp mây đen ➔ Dùng is going to rain (có bằng chứng), không dùng will rain.'
      }}
    }};

    function selectTimelineTense(tenseKey) {{
      const data = TENSE_DATA[tenseKey];
      if (!data) return;
      
      document.querySelectorAll('.tl-pill').forEach(p => p.classList.remove('active'));
      event?.target?.classList.add('active');
      
      const card = document.getElementById('timeline_detail_card');
      if (card) {{
        card.innerHTML = `
          <h4 style="font-size: 1.25rem; color: var(--primary); margin-bottom: 8px;">💎 ${{data.name}}</h4>
          <p style="font-size: 0.98rem; margin-bottom: 12px; color: var(--text-main);"><strong>Bản chất cốt lõi:</strong> ${{data.feynman}}</p>
          <div style="background: var(--bg-surface); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: var(--radius-sm); margin-bottom: 10px;">
            <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-soft); display: block; margin-bottom: 4px;">📐 CÔNG THỨC:</span>
            <code style="font-family: var(--font-mono); font-weight: 700; color: var(--primary); font-size: 1.05rem;">${{data.formula}}</code>
          </div>
          <div style="margin-bottom: 8px; font-size: 0.92rem; color: var(--text-muted);">
            <strong>🚨 Dấu hiệu nhận biết:</strong> <span style="color: var(--accent-teal); font-weight: 600;">${{data.signals}}</span>
          </div>
          <div style="font-size: 0.92rem; color: #dc2626; font-weight: 600; padding: 6px 10px; background: rgba(220, 38, 38, 0.08); border-radius: var(--radius-sm);">
            ${{data.trap}}
          </div>
        `;
      }}
    }}

    // ==============================================================================
    // 6. AUDIO SPEECH SYNTHESIS (100% OFFLINE)
    // ==============================================================================
    function playSpeech(word) {{
      if (!('speechSynthesis' in window)) {{
        alert('Trình duyệt của bạn không hỗ trợ Web Speech API.');
        return;
      }}
      window.speechSynthesis.cancel();
      const clean = (word || '').replace(/[^a-zA-Z\\s]/g, '').trim();
      if (!clean) return;
      
      const utter = new SpeechSynthesisUtterance(clean);
      utter.lang = 'en-US';
      utter.rate = 0.9;
      
      // Try to find English voice
      const voices = window.speechSynthesis.getVoices();
      const enVoice = voices.find(v => v.lang.startsWith('en'));
      if (enVoice) utter.voice = enVoice;
      
      window.speechSynthesis.speak(utter);
    }}

    // ==============================================================================
    // 7. REAL-TIME SEARCH & SCROLLSPY
    // ==============================================================================
    const MODULE_REGISTRY = {json.dumps(module_summaries)};

    function handleGlobalSearch(query) {{
      const dropdown = document.getElementById('search_dropdown');
      const q = (query || '').trim().toLowerCase();
      if (!q || !dropdown) {{
        if (dropdown) dropdown.style.display = 'none';
        return;
      }}
      
      const matches = MODULE_REGISTRY.filter(m => 
        m.title.toLowerCase().includes(q) || 
        m.part.toLowerCase().includes(q)
      );
      
      if (matches.length === 0) {{
        dropdown.innerHTML = '<div style="padding: 12px 16px; color: var(--text-soft); font-size: 0.9rem;">Không tìm thấy chuyên đề phù hợp...</div>';
      }} else {{
        dropdown.innerHTML = matches.map(m => `
          <div class="search-result-item" onclick="jumpToModule('${{m.id}}')">
            <div>
              <strong style="color: var(--text-main); font-size: 0.95rem;">${{m.title}}</strong>
              <div style="font-size: 0.78rem; color: var(--text-soft);">${{m.part}}</div>
            </div>
            <span style="font-size: 0.8rem; background: var(--primary-light); color: var(--primary); padding: 2px 8px; border-radius: 9999px;">${{m.questions_count}} câu</span>
          </div>
        `).join('');
      }}
      dropdown.style.display = 'block';
    }}

    function jumpToModule(id) {{
      const el = document.getElementById(id);
      if (el) {{
        el.scrollIntoView({{ behavior: 'smooth' }});
        const dropdown = document.getElementById('search_dropdown');
        if (dropdown) dropdown.style.display = 'none';
        const searchInput = document.getElementById('global_search');
        if (searchInput) searchInput.value = '';
      }}
    }}

    // Close search dropdown on click outside
    document.addEventListener('click', (e) => {{
      const searchBox = document.querySelector('.header-center');
      const dropdown = document.getElementById('search_dropdown');
      if (searchBox && !searchBox.contains(e.target) && dropdown) {{
        dropdown.style.display = 'none';
      }}
    }});

    // Keyboard shortcut Ctrl+K
    document.addEventListener('keydown', (e) => {{
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
        e.preventDefault();
        const searchInput = document.getElementById('global_search');
        searchInput?.focus();
      }}
    }});

    // ScrollSpy for Active Sidebar Navigation
    function initScrollSpy() {{
      const sections = document.querySelectorAll('.module-card-section');
      const navItems = document.querySelectorAll('.toc-item');
      
      window.addEventListener('scroll', () => {{
        let current = '';
        const scrollY = window.pageYOffset + 120;
        
        sections.forEach(sec => {{
          const top = sec.offsetTop;
          const height = sec.offsetHeight;
          if (scrollY >= top && scrollY < top + height) {{
            current = sec.getAttribute('id');
          }}
        }});
        
        navItems.forEach(item => {{
          item.classList.remove('active');
          if (item.getAttribute('data-target') === current) {{
            item.classList.add('active');
          }}
        }});
      }});
    }}

    function resetAllProgress() {{
      if (!confirm('Bạn có chắc chắn muốn đặt lại toàn bộ tiến độ làm bài trên toàn ứng dụng?')) return;
      localStorage.removeItem(APP_STORAGE_KEY);
      location.reload();
    }}

    // ==============================================================================
    // 8. INITIALIZATION
    // ==============================================================================
    window.addEventListener('DOMContentLoaded', () => {{
      loadSavedState();
      applyTheme(appState.theme || 'light');
      setGlobalMode(appState.globalMode || 'practice');
      selectTimelineTense('pres_perf');
      initScrollSpy();
      
      // Restore previously saved answers
      Object.keys(appState.answers).forEach(qid => {{
        const opt = appState.answers[qid];
        const card = document.getElementById('card_' + qid);
        if (card) {{
          card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
            if (btn.getAttribute('data-opt') === opt) {{
              btn.classList.add('selected');
            }}
          }});
          const badge = card.querySelector('.question-status-badge');
          if (badge) {{
            badge.textContent = 'Đã làm (' + opt + ')';
            badge.className = 'question-status-badge status-unanswered';
          }}
        }}
      }});
      
      // Update trackers
      document.querySelectorAll('.interactive-quiz-wrapper').forEach(w => {{
        const modId = w.getAttribute('data-mod-id');
        if (modId) updateQuizTracker(modId);
      }});
      
      updateGlobalProgress();
    }});
  </script>
</body>
</html>
"""
    return app_html

if __name__ == "__main__":
    print("=" * 70)
    print("BẮT ĐẦU TỔNG HỢP & XÂY DỰNG ỨNG DỤNG HỌC TẬP TƯƠNG TÁC CAO CẤP")
    print("=" * 70)
    
    output_html = build_full_application()
    target_path = "f:/OnThiC3/EnglishDocs/Cam_Nang_On_Thi_Vao_10_Master.html"
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(output_html)
        
    print(f"✅ THÀNH CÔNG RỰC RỠ! Đã xuất bản ứng dụng tại:")
    print(f"   -> {target_path} ({len(output_html.encode('utf-8')):,} bytes)")
    print("=" * 70)
