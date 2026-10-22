# -*- coding: utf-8 -*-
"""
File: generate_master_webapp.py
Kiến trúc sư giao diện: Senior Product Designer, Senior Frontend Architect & Learning Experience (LX) Expert.
Mục đích: Chuyển đổi toàn diện cuốn Cẩm nang HTML thành Ứng dụng Học tập Tương tác Đẳng Cấp EdTech
(Interactive Educational Web Application) chuẩn Duolingo, Brilliant, Quizizz, Linear, Stripe.

Tính năng đột phá:
1. Hệ thống Quiz trắc nghiệm chuẩn EdTech: Lưới 2x2 cân đối, nút bấm 3D xúc giác (Tactile Buttons),
   âm thanh phản hồi Web Audio API (Chime chiến thắng & Gentle hint 100% offline), giải thích Active Recall.
2. Sơ đồ Mermaid tối ưu hóa giao diện: Khắc phục triệt để lỗi hình thoi phình to, tương thích Dark/Light mode tự động.
3. Bộ Wizard tra cứu âm học thông minh (Interactive Pronunciation & Stress Decision Flowcards).
4. Ma trận trục thời gian ngữ pháp Feynman (Interactive Tense Timeline).
5. Công cụ phát âm IPA âm thanh qua Web Speech API (100% Offline).
6. Thanh điều hướng thông minh (ScrollSpy, Tìm kiếm thời gian thực Ctrl+K, Dark/Light mode, Lưu tiến độ LocalStorage).
7. Hệ thống theo dõi tiến độ thời gian thực (Gamification Badges trên Sidebar TOC).
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
    ("PHẦN 1: NGỮ ÂM & TRỌNG ÂM", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_ed_mastery.md", "1. Quy tắc phát âm đuôi -ED và các trường hợp đặc biệt", "ed"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_s_es_mastery.md", "2. Quy tắc phát âm đuôi -S và -ES", "ses"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_trong_am_mastery.md", "3. Quy tắc trọng âm của từ (Word Stress)", "stress"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_th.md", "4. Cách phát âm âm TH (/θ/ và /ð/)", "th"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_1_phat_am_ae_e.md", "5. Phân biệt nguyên âm /æ/ và /e/", "aee"),
    ]),
    ("PHẦN 2: NGỮ PHÁP & CẤU TRÚC CÂU", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_10_cau_truc_bien_doi_cau.md", "6. 10 cấu trúc viết lại câu phổ biến (Sentence Transformation)", "transform"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_12_thi_mastery.md", "7. Hệ thống các thì và nguyên tắc phối hợp thì", "tenses"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_menh_de_quan_he.md", "8. Mệnh đề quan hệ và cách rút gọn mệnh đề", "relative"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_word_form_va_su_hoa_hop.md", "9. Cấu tạo từ (Word Form) và sự hòa hợp chủ vị", "wordform"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_ving_to_v_mastery.md", "10. Danh động từ và động từ nguyên mẫu (V-ing và To-V)", "ving"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_cau_hoi_duoi_mastery.md", "11. Câu hỏi đuôi (Question Tags)", "tags"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_mao_tu_articles_mastery.md", "12. Mạo từ (A, An, The và Zero Article)", "articles"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_gioi_tu_prepositions_mastery.md", "13. Giới từ chỉ thời gian, nơi chốn và các cụm thông dụng", "prepos"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_2_dong_tu_khuyet_thieu_mastery.md", "14. Động từ khuyết thiếu (Modal Verbs)", "modals"),
    ]),
    ("PHẦN 3: TỪ VỰNG CHỌN LỌC", [
        ("f:/OnThiC3/EnglishDocs/chuyen_de_3_phrasal_verbs_mastery.md", "15. 50 cụm động từ (Phrasal Verbs) thường gặp trong đề thi", "phrasal"),
        ("f:/OnThiC3/EnglishDocs/chuyen_de_3_dong_nghia_trai_nghia_mastery.md", "16. Từ đồng nghĩa và trái nghĩa (Synonyms & Antonyms)", "synonym"),
    ])
]

DEFAULT_INSTRUCTIONS = {
    "ed": "Chọn từ có phần gạch chân đuôi **-ed** phát âm khác với các từ còn lại:",
    "ses": "Chọn từ có phần gạch chân đuôi **-s / -es** phát âm khác với các từ còn lại:",
    "stress": "Chọn từ có vị trí **trọng âm chính** khác với các từ còn lại:",
    "th": "Chọn từ có phần gạch chân **th** phát âm khác với các từ còn lại:",
    "aee": "Chọn từ có phần nguyên âm gạch chân phát âm khác với các từ còn lại:",
    "transform": "Viết lại các câu sau sao cho nghĩa không đổi:",
    "wordform": "Cho dạng đúng của từ trong ngoặc để hoàn thành câu:",
    "tenses": "Chia dạng đúng của động từ trong ngoặc:",
    "relative": "Chọn đại từ quan hệ thích hợp nhất để hoàn thành câu:",
    "ving": "Chọn dạng đúng của động từ (V-ing hay To-V):",
    "tags": "Chọn câu hỏi đuôi chính xác nhất:",
    "articles": "Chọn mạo từ thích hợp (A, An, The hoặc Ø):",
    "prepos": "Chọn giới từ chính xác nhất để hoàn thành câu:",
    "modals": "Chọn động từ khuyết thiếu chính xác nhất:",
    "phrasal": "Chọn cụm động từ (Phrasal Verb) phù hợp nhất:",
    "synonym": "Chọn từ đồng nghĩa (CLOSEST) hoặc trái nghĩa (OPPOSITE) phù hợp:"
}

def render_inline(text: str) -> str:
    """Render inline markdown styling: code, phonetic highlight, bold, italic."""
    text = re.sub(r"`([^`]+)`", r"<code class='inline-code'>\1</code>", text)
    # Target phonetic letters in bold: e.g. book**s** -> book<span class='phonetic-highlight'>s</span>
    text = re.sub(r"\*\*([a-zA-Z\-_/]+)\*\*", r"<span class='phonetic-highlight'>\1</span>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text

def parse_quizzes(text: str, mod_id: str):
    """Parse multiple choice and transformation questions with answer keys and smart stem extraction."""
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
        return questions, text
        
    non_quiz_text = "\n".join(lines[:quiz_start_idx])
    quiz_lines = lines[quiz_start_idx:]
    
    # Find section-wide instruction line (e.g. "Chọn từ có phần đuôi -ed phát âm khác...")
    section_instruction = ""
    for l in quiz_lines[1:]:
        l_str = l.strip()
        if not l_str or l_str.startswith("+++") or l_str.startswith("#"):
            continue
        if re.match(r"^(?:-\s*)?(?:\*\*)?(?:Câu\s+)?\d+[\.:\s]+", l_str):
            break
        section_instruction = l_str
        break
        
    fallback_instruction = section_instruction or DEFAULT_INSTRUCTIONS.get(mod_id, "Chọn đáp án chính xác nhất để hoàn thành câu:")
    
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
                final_stem = stem if stem and len(stem) > 3 else fallback_instruction
                questions.append({
                    "id": f"{mod_id}_q{q_num}",
                    "num": q_num,
                    "type": "mcq",
                    "stem": final_stem,
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
    """Generate high-end interactive quiz component with balanced 2x2 grid and tactile Duolingo styling."""
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
            <p class="quiz-sub-desc">Chuẩn ma trận đề tuyển sinh vào 10 Sở GD&ĐT • {len(questions)} câu thực chiến</p>
          </div>
        </div>
        <div class="quiz-mode-pill">
          <span class="mode-label">Chế độ học:</span>
          <button type="button" class="mode-tag mode-tag-practice active" data-mode="practice" onclick="setGlobalMode('practice')">🎯 Luyện tập tức thì</button>
          <button type="button" class="mode-tag mode-tag-exam" data-mode="exam" onclick="setGlobalMode('exam')">⏱️ Thi thử tính điểm</button>
        </div>
      </div>
      
      <!-- Quiz Progress Tracker -->
      <div class="quiz-tracker-bar">
        <div class="tracker-info">
          <span>Tiến độ chuyên đề: <strong class="answered-count">0</strong>/{len(mcqs)} câu đã trả lời</span>
          <span class="score-display hidden">Điểm thi thử: <strong class="score-val">0</strong>/{len(mcqs)}</span>
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
            stem_audio_btn = f"<button type='button' class='audio-speaker-btn' onclick='playSpeech(\"{m_word.group(1)}\")' title='Nghe phát âm từ này'>🔊</button>"
        
        html_parts.append(f"""
        <div class="quiz-question-card" id="card_{qid}" data-qid="{qid}" data-correct="{correct}">
          <div class="question-meta-row">
            <div class="meta-left-group">
              <span class="question-number-pill">CÂU {int(qnum):02d}</span>
              <span class="question-points-pill">1 ĐIỂM</span>
            </div>
            <div class="meta-right-group">
              <span class="question-status-badge status-unanswered">Chưa làm</span>
            </div>
          </div>
          
          <div class="question-stem-wrapper">
            <div class="question-stem-text">{stem} {stem_audio_btn}</div>
          </div>
          
          <!-- Perfectly Balanced 2x2 Options Grid -->
          <div class="quiz-options-grid">
        """)
        
        for opt_key in ["A", "B", "C", "D"]:
            if opt_key in q["options"]:
                opt_val = render_inline(q["options"][opt_key])
                clean_w = re.sub(r"<[^>]+>", "", opt_val).strip()
                opt_audio = ""
                if len(clean_w) <= 15 and clean_w.isalpha():
                    opt_audio = f"""<button type="button" class="opt-audio-chip" onclick="event.stopPropagation(); playSpeech('{clean_w}')" title="Nghe phát âm '{clean_w}'" aria-label="Nghe phát âm">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77zm-2.5 0L6.5 7.5H3c-.55 0-1 .45-1 1v7c0 .55.45 1 1 1h3.5l5 4.27c.67.57 1.5.09 1.5-.77V4c0-.86-.83-1.34-1.5-.77z"/></svg>
                    </button>"""
                    
                html_parts.append(f"""
                <div class="quiz-option-btn" role="button" tabindex="0" data-qid="{qid}" data-opt="{opt_key}" onclick="handleOptionSelect('{qid}', '{opt_key}')" onkeydown="if(event.key==='Enter'||event.key===' '){{handleOptionSelect('{qid}', '{opt_key}');event.preventDefault();}}">
                  <span class="opt-letter-circle">{opt_key}</span>
                  <span class="opt-content-text">{opt_val}</span>
                  <div class="opt-action-group">
                    {opt_audio}
                    <span class="opt-feedback-icon"></span>
                  </div>
                </div>
                """)
                
        html_parts.append(f"""
          </div>
          
          <!-- Detailed Pedagogical Explanation Card -->
          <div class="question-explanation-panel hidden" id="exp_{qid}">
            <div class="exp-header">
              <div class="exp-title-row">
                <span class="exp-bulb-icon">💡</span>
                <div>
                  <span class="exp-badge">GIẢI THÍCH CHI TIẾT & BẢN CHẤT SƯ PHẠM</span>
                  <span class="exp-qnum">Câu {qnum}</span>
                </div>
              </div>
              <span class="exp-correct-pill">Đáp án đúng: <strong>{correct}</strong></span>
            </div>
            <div class="exp-body-text">{explanation}</div>
            <div class="exp-actions-row">
              <button type="button" class="retry-question-btn" onclick="retryQuestion('{qid}')">
                <span>🔄</span> Làm lại câu này (Active Recall)
              </button>
            </div>
          </div>
        </div>
        """)
        
    # Sentence Transformation Questions
    if trans:
        html_parts.append("""
        <div class="transformation-section-title">
          <h4>✍️ BÀI TẬP TỰ LUẬN: BIẾN ĐỔI CÂU & TỰ LUYỆN TẬP</h4>
          <p>Nhập câu viết lại tương đương của bạn vào ô bên dưới, sau đó bấm "Đối chiếu đáp án mẫu" để so sánh cấu trúc:</p>
        </div>
        """)
        for q in trans:
            qid = q["id"]
            qnum = q["num"]
            stem = render_inline(q["stem"])
            model_ans = render_inline(q["model_answer"])
            html_parts.append(f"""
            <div class="transformation-card" id="card_{qid}">
              <div class="trans-meta"><span class="question-number-pill">CÂU {int(qnum):02d}</span></div>
              <div class="trans-stem">{stem}</div>
              <div class="trans-input-row">
                <input type="text" class="trans-input-box" id="input_{qid}" placeholder="Nhập câu viết lại tương đương tại đây...">
                <button type="button" class="trans-check-btn" onclick="toggleTransAnswer('{qid}')">🔍 Đối chiếu đáp án</button>
              </div>
              <div class="trans-model-answer hidden" id="model_{qid}">
                <div class="model-badge">✅ ĐÁP ÁN MẪU & PHÂN TÍCH BẢN CHẤT:</div>
                <div class="model-text">{model_ans}</div>
              </div>
            </div>
            """)
            
    # Exam Submission & Score Card Footer
    html_parts.append(f"""
      <div class="quiz-footer-actions">
        <button type="button" class="submit-exam-btn" onclick="submitExam('{mod_id}')">🚀 Nộp bài thi thử & Chấm điểm</button>
        <button type="button" class="reset-quiz-btn" onclick="resetQuizSection('{mod_id}')">🔄 Làm lại toàn bộ</button>
      </div>
      
      <!-- Exam Results Banner -->
      <div class="exam-result-banner hidden" id="result_{mod_id}">
        <div class="result-banner-content">
          <div class="result-score-circle">
            <span class="result-score-number" id="score_num_{mod_id}">0</span>
            <span class="result-score-max">/{len(mcqs)}</span>
          </div>
          <div class="result-details">
            <h4 class="result-heading">KẾT QUẢ THI THỬ CHUYÊN ĐỀ</h4>
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
              <h4 class="wizard-title">TRA CỨU QUY TẮC PHÁT ÂM ĐUÔI -ED</h4>
              <p class="wizard-desc">Nhập một từ bất kỳ hoặc chọn các từ mẫu để kiểm tra cách phát âm và quy tắc tương ứng:</p>
            </div>
          </div>
          <div class="wizard-interactive-flow">
            <div class="wizard-input-box">
              <input type="text" id="ed_word_input" placeholder="Ví dụ: wanted, washed, played, naked..." oninput="testEdWord(this.value)">
              <button type="button" onclick="testEdWord(document.getElementById('ed_word_input').value)">Kiểm tra & Phát âm 🔊</button>
            </div>
            <div class="wizard-result-box" id="ed_result_box">
              <span class="wiz-res-label">Kết quả phân tích:</span>
              <span class="wiz-res-badge" id="ed_res_badge">Nhập từ để kiểm tra...</span>
              <span class="wiz-res-rule" id="ed_res_rule"></span>
            </div>
            <div class="wizard-quick-tags">
              <span>Thử nhanh từ mẫu:</span>
              <button type="button" onclick="setEdWord('wanted')">wanted</button>
              <button type="button" onclick="setEdWord('watched')">watched</button>
              <button type="button" onclick="setEdWord('played')">played</button>
              <button type="button" onclick="setEdWord('naked')">naked (tính từ đặc biệt /ɪd/)</button>
              <button type="button" onclick="setEdWord('laughed')">laughed (đuôi gh /t/)</button>
              <button type="button" onclick="setEdWord('wicked')">wicked (ngoại lệ /ɪd/)</button>
            </div>
          </div>
        </div>
        """,
        "ses": """
        <div class="interactive-wizard-card" id="wizard_ses">
          <div class="wizard-header">
            <span class="wizard-icon">🪄</span>
            <div>
              <h4 class="wizard-title">TRA CỨU QUY TẮC PHÁT ÂM ĐUÔI -S / -ES</h4>
              <p class="wizard-desc">Kiểm tra nhanh cách phát âm đuôi /s/, /z/ hoặc /ɪz/ theo âm tận cùng:</p>
            </div>
          </div>
          <div class="wizard-interactive-flow">
            <div class="wizard-input-box">
              <input type="text" id="ses_word_input" placeholder="Ví dụ: books, watches, plays, houses..." oninput="testSesWord(this.value)">
              <button type="button" onclick="testSesWord(document.getElementById('ses_word_input').value)">Kiểm tra & Phát âm 🔊</button>
            </div>
            <div class="wizard-result-box" id="ses_result_box">
              <span class="wiz-res-label">Kết quả phân tích:</span>
              <span class="wiz-res-badge" id="ses_res_badge">Nhập từ để kiểm tra...</span>
              <span class="wiz-res-rule" id="ses_res_rule"></span>
            </div>
            <div class="wizard-quick-tags">
              <span>Thử nhanh từ mẫu:</span>
              <button type="button" onclick="setSesWord('books')">books</button>
              <button type="button" onclick="setSesWord('watches')">watches</button>
              <button type="button" onclick="setSesWord('plays')">plays</button>
              <button type="button" onclick="setSesWord('houses')">houses (biến âm /zɪz/)</button>
              <button type="button" onclick="setSesWord('months')">months</button>
              <button type="button" onclick="setSesWord('clothes')">clothes</button>
            </div>
          </div>
        </div>
        """,
        "tenses": """
        <div class="interactive-timeline-container" id="timeline_widget">
          <div class="timeline-widget-header">
            <span class="tl-icon">⏳</span>
            <div>
              <h4 class="tl-title">TRỤC THỜI GIAN HỆ THỐNG CÁC THÌ TRONG TIẾNG ANH</h4>
              <p class="tl-desc">Bấm vào từng thì trên trục thời gian để xem trực quan vị trí, cấu trúc và dấu hiệu nhận biết:</p>
            </div>
          </div>
          <div class="timeline-visual-track">
            <div class="tl-time-axis">
              <span class="axis-point past">QUÁ KHỨ (PAST)</span>
              <span class="axis-point present active">HIỆN TẠI (PRESENT)</span>
              <span class="axis-point future">TƯƠNG LAI (FUTURE)</span>
            </div>
            <div class="tl-pills-row">
              <button type="button" class="tl-pill" onclick="selectTimelineTense('past_simple')">Quá khứ đơn</button>
              <button type="button" class="tl-pill" onclick="selectTimelineTense('past_cont')">Quá khứ tiếp diễn</button>
              <button type="button" class="tl-pill" onclick="selectTimelineTense('past_perf')">Quá khứ hoàn thành</button>
              <button type="button" class="tl-pill" onclick="selectTimelineTense('pres_simple')">Hiện tại đơn</button>
              <button type="button" class="tl-pill" onclick="selectTimelineTense('pres_cont')">Hiện tại tiếp diễn</button>
              <button type="button" class="tl-pill highlight active" onclick="selectTimelineTense('pres_perf')">Hiện tại hoàn thành (Trọng tâm)</button>
              <button type="button" class="tl-pill" onclick="selectTimelineTense('fut_simple')">Tương lai đơn</button>
              <button type="button" class="tl-pill" onclick="selectTimelineTense('near_fut')">Tương lai gần</button>
            </div>
          </div>
          <div class="timeline-detail-card" id="timeline_detail_card">
            <!-- Dynamic content populated by JS -->
          </div>
        </div>
        """
    }

def md_to_html_body(md_text: str, mod_id: str = "gen") -> str:
    """Parse standard markdown body lines with tables, callouts, lists, and modernized Mermaid wrappers."""
    lines = md_text.splitlines()
    html_parts = []
    i = 0
    n = len(lines)
    diag_idx = 0

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

        # Code & Modern Mermaid with Floating Zoom Controls (No redundant header bar)
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
                diag_idx += 1
                diag_id = f"diag_{mod_id}_{diag_idx}"
                html_parts.append(f"""
                <div class="mermaid-container" id="container_{diag_id}">
                  <div class="mermaid-zoom-toolbar" aria-label="Điều khiển thu phóng sơ đồ">
                    <button type="button" class="diag-zoom-btn" onclick="zoomMermaid('{diag_id}', 1.25)" title="Phóng to (+)" aria-label="Phóng to">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
                    </button>
                    <button type="button" class="diag-zoom-btn" onclick="zoomMermaid('{diag_id}', 0.8)" title="Thu nhỏ (-)" aria-label="Thu nhỏ">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
                    </button>
                    <button type="button" class="diag-zoom-btn" onclick="resetMermaidZoom('{diag_id}')" title="Kích thước gốc (↺)" aria-label="Đặt lại kích thước">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
                    </button>
                  </div>
                  <div class="mermaid-viewport" id="viewport_{diag_id}">
                    <div class="mermaid-content" id="content_{diag_id}">
                      <div class="mermaid">{raw_code}</div>
                    </div>
                  </div>
                </div>
                """)
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
    # Nạp dữ liệu 7 bộ đề thi trực tiếp từ exam_database.json
    exam_db_path = r"f:/OnThiC3/EnglishDocs/exam_database.json"
    if os.path.exists(exam_db_path):
        with open(exam_db_path, "r", encoding="utf-8") as f:
            exam_db_raw = f.read().replace("</script>", "<\\/script>")
    else:
        exam_db_raw = "[]"

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
            
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_text = f.read()
                    
                questions, text_without_quiz = parse_quizzes(raw_text, mod_id)
                body_html = md_to_html_body(text_without_quiz, mod_id)
                quiz_html = build_quiz_html(questions, mod_id, mod_name)
                total_quizzes_in_app += len([q for q in questions if q["type"] == "mcq"])
                
                wizard_widget = wizards.get(mod_id, "")
                
                module_summaries.append({
                    "id": anchor,
                    "title": mod_name,
                    "part": part_title,
                    "mod_id": mod_id,
                    "questions_count": len(questions)
                })
                
                toc_html.append(f"""
                <li class="toc-item" data-target="{anchor}" id="toc_{mod_id}">
                  <a href="#{anchor}" class="toc-link">
                    <span class="toc-dot" id="toc_dot_{mod_id}"></span>
                    <span class="toc-text">{mod_name}</span>
                    <span class="toc-badge-count" id="toc_badge_{mod_id}">0/{len([q for q in questions if q["type"] == "mcq"])}</span>
                  </a>
                </li>
                """)
                
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
                toc_html.append(f"""
                <li class="toc-item" data-target="{anchor}">
                  <a href="#{anchor}" class="toc-link">
                    <span class="toc-dot"></span>
                    <span class="toc-text">{mod_name} (Đang cập nhật)</span>
                  </a>
                </li>
                """)
                sections_html.append(f"""
                <section id="{anchor}" class="module-card-section">
                  <p><em>File {file_path} đang được cập nhật.</em></p>
                </section>
                """)
                
        toc_html.append("</ul></div>")
        
        # Bổ sung Phần 4: Luyện đề & Thi thử vào TOC
        toc_html.append('''
        <div class="toc-category-group" data-cat="4">
          <div class="toc-cat-header">
            <span class="toc-cat-badge">Phần 4</span>
            <span class="toc-cat-title">Luyện Đề & Thi Thử Vào 10</span>
          </div>
          <ul class="toc-items-list">
            <li class="toc-item" data-target="mod_exam_arena" id="toc_exam_arena">
              <a href="#mod_exam_arena" class="toc-link">
                <span class="toc-dot"></span>
                <span class="toc-text">🏆 Trung Tâm Luyện Đề & Thi Thử</span>
                <span class="toc-badge-count" style="background:#f59e0b;color:#fff;font-weight:700;">7 Đề Thi</span>
              </a>
            </li>
          </ul>
        </div>
''')

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
      flowchart: {{
        curve: 'basis',
        nodeSpacing: 12,
        rankSpacing: 18,
        padding: 8,
        useMaxWidth: true
      }},
      themeVariables: {{
        primaryColor: '#eff6ff',
        primaryTextColor: '#1e3a8a',
        primaryBorderColor: '#3b82f6',
        lineColor: '#64748b',
        secondaryColor: '#f0fdf4',
        tertiaryColor: '#fefce8',
        fontSize: '12px',
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
      --success-border: #86efac;
      
      --warning: #d97706;
      --warning-light: #fefce8;
      --warning-border: #fde047;
      
      --error: #dc2626;
      --error-light: #fef2f2;
      --error-border: #fca5a5;
      
      --bg-body: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-subtle: #f1f5f9;
      
      --border-color: #e2e8f0;
      --border-subtle: #cbd5e1;
      
      --text-main: #0f172a;
      --text-muted: #334155;
      --text-soft: #64748b;
      
      --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
      --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
      
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-heading: 'Outfit', 'Plus Jakarta Sans', sans-serif;
      --font-mono: 'JetBrains Mono', Consolas, monospace;
      
      --sidebar-width: 330px;
      --header-height: 70px;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --radius-xl: 24px;
    }}

    [data-theme="dark"] {{
      --primary: #3b82f6;
      --primary-hover: #60a5fa;
      --primary-light: rgba(59, 130, 246, 0.16);
      --primary-rgb: 59, 130, 246;
      
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
      --success-light: rgba(34, 197, 94, 0.16);
      --success-border: #166534;
      
      --error: #ef4444;
      --error-light: rgba(239, 68, 68, 0.16);
      --error-border: #991b1b;
      
      --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.4);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.6);
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
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      font-size: 0.9em;
      font-weight: 600;
      border: 1px solid var(--border-color);
    }}

    /* High-Contrast Luminous Phonetic Highlight */
    .phonetic-highlight {{
      color: #d97706;
      background: rgba(217, 119, 6, 0.12);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 800;
      border-bottom: 2px solid #d97706;
      letter-spacing: 0.02em;
    }}

    [data-theme="dark"] .phonetic-highlight {{
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.16);
      border-bottom-color: #38bdf8;
      text-shadow: 0 0 10px rgba(56, 189, 248, 0.35);
    }}

    /* ==============================================================================
       3. TOP STICKY NAVBAR & CONTROLS
       ============================================================================== */
    .app-header {{
      position: sticky;
      top: 0;
      z-index: 1000;
      height: var(--header-height);
      background: rgba(255, 255, 255, 0.88);
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
      background: rgba(17, 24, 39, 0.88);
      border-color: var(--border-color);
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .header-action-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .header-icon-btn {{
      width: 40px;
      height: 40px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--bg-surface);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-md);
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      outline: none;
      box-shadow: var(--shadow-sm);
    }}

    .header-icon-btn:hover {{
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary);
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(var(--primary-rgb), 0.2);
    }}

    .header-icon-btn:active {{
      transform: translateY(1px);
      box-shadow: none;
    }}

    .header-icon-btn:focus-visible {{
      box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.35);
    }}

    /* Desktop Sidebar Collapsible State */
    body.sidebar-collapsed .app-sidebar {{
      display: none;
    }}
    body.sidebar-collapsed .app-main-content {{
      max-width: 100%;
    }}

    .header-center {{
      flex: 1;
      max-width: 460px;
      margin: 0 24px;
      position: relative;
    }}

    .search-input-box {{
      width: 100%;
      height: 42px;
      background: var(--bg-subtle);
      border: 1.5px solid var(--border-color);
      border-radius: 9999px;
      padding: 0 18px 0 44px;
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
      padding: 12px 18px;
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
      gap: 10px;
    }}

    .sound-toggle-btn, .mode-switch-btn, .theme-toggle-btn {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-subtle);
      border: 1.5px solid var(--border-color);
      padding: 7px 14px;
      border-radius: 9999px;
      font-size: 0.86rem;
      font-weight: 700;
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .sound-toggle-btn:hover, .mode-switch-btn:hover, .theme-toggle-btn:hover {{
      border-color: var(--primary);
      background: var(--primary-light);
      color: var(--primary);
    }}

    .theme-toggle-btn {{
      width: 42px;
      height: 42px;
      padding: 0;
      justify-content: center;
      font-size: 1.15rem;
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
      font-weight: 800;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--primary);
    }}

    .toc-cat-badge {{
      background: var(--primary-light);
      padding: 2px 7px;
      border-radius: var(--radius-sm);
    }}

    .toc-items-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .toc-link {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 9px 12px;
      border-radius: var(--radius-md);
      font-size: 0.88rem;
      color: var(--text-muted);
      font-weight: 500;
      line-height: 1.4;
      transition: all 0.15s ease;
      position: relative;
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
      width: 7px;
      height: 7px;
      border-radius: 9999px;
      background: var(--border-subtle);
      transition: transform 0.2s ease, background 0.2s ease;
      flex-shrink: 0;
    }}

    .toc-item.active .toc-dot {{
      background: var(--primary);
      transform: scale(1.6);
    }}

    .toc-text {{
      flex: 1;
    }}

    .toc-badge-count {{
      font-size: 0.74rem;
      font-weight: 700;
      background: var(--bg-subtle);
      color: var(--text-soft);
      padding: 2px 7px;
      border-radius: 9999px;
      border: 1px solid var(--border-color);
      flex-shrink: 0;
      transition: all 0.2s ease;
    }}

    .toc-badge-count.completed {{
      background: var(--success-light);
      color: var(--success);
      border-color: var(--success-border);
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
      width: 220px;
      height: 220px;
      background: rgba(255, 255, 255, 0.08);
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
      font-size: 1.08rem;
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
      font-size: 1.45rem;
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

    /* Callouts */
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

    /* ==============================================================================
       MERMAID DIAGRAM: COMPACT CONTAINER & FLOATING ZOOM TOOLBAR
       ============================================================================== */
    /* Code Block Formatting */
    .code-block {{
      background: var(--bg-subtle);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin: 18px 0;
      overflow-x: auto;
      max-width: 100%;
      box-sizing: border-box;
      font-family: var(--font-mono);
      font-size: 0.9rem;
      line-height: 1.6;
      color: var(--text-main);
      white-space: pre-wrap;
      word-break: break-word;
      scrollbar-width: thin;
    }}

    /* Mobile Sidebar Backdrop */
    .sidebar-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.45);
      backdrop-filter: blur(2px);
      -webkit-backdrop-filter: blur(2px);
      z-index: 1040;
      opacity: 0;
      transition: opacity 0.25s ease;
    }}
    .sidebar-backdrop.active {{
      display: block;
      opacity: 1;
    }}

    .mermaid-container {{
      position: relative;
      background: var(--bg-surface);
      border: 1.5px solid var(--border-color);
      border-radius: var(--radius-lg);
      margin: 16px 0 20px;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      max-width: 100%;
    }}

    .mermaid-container:hover {{
      border-color: var(--primary);
      box-shadow: var(--shadow-md);
    }}

    .mermaid-zoom-toolbar {{
      position: absolute;
      top: 8px;
      right: 8px;
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 3px;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 2px 4px;
      box-shadow: var(--shadow-sm);
    }}

    [data-theme="dark"] .mermaid-zoom-toolbar {{
      background: rgba(30, 41, 59, 0.92);
      border-color: rgba(255, 255, 255, 0.12);
    }}

    .diag-zoom-btn {{
      width: 26px;
      height: 26px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      border: none;
      border-radius: 4px;
      color: var(--text-soft);
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .diag-zoom-btn:hover {{
      background: var(--primary-light);
      color: var(--primary);
      transform: scale(1.08);
    }}

    .diag-zoom-btn:active {{
      transform: scale(0.95);
    }}

    .mermaid-viewport {{
      width: 100%;
      min-height: 90px;
      max-height: 280px;
      overflow: auto;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 12px 14px;
      cursor: grab;
      user-select: none;
      background: var(--bg-card);
      scrollbar-width: thin;
      box-sizing: border-box;
    }}

    .mermaid-viewport:active {{
      cursor: grabbing;
    }}

    .mermaid-content {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transform-origin: center center;
      transition: transform 0.15s cubic-bezier(0.2, 0, 0, 1);
      max-width: 100%;
      width: auto;
      margin: 0 auto;
    }}

    .mermaid-content .mermaid {{
      display: flex;
      justify-content: center;
      align-items: center;
      max-width: 100%;
      width: auto;
    }}

    .mermaid-content .mermaid svg {{
      max-width: min(100%, 640px) !important;
      max-height: 250px !important;
      width: auto !important;
      height: auto !important;
      font-family: var(--font-body) !important;
      display: block;
      margin: 0 auto;
      overflow: visible;
    }}

    /* Dark mode overrides for Mermaid diagram */
    [data-theme="dark"] .mermaid svg .edgePath .path {{
      stroke: #60a5fa !important;
      stroke-width: 2.2px !important;
    }}

    [data-theme="dark"] .mermaid svg marker path {{
      fill: #60a5fa !important;
    }}

    [data-theme="dark"] .mermaid svg .edgeLabel {{
      background-color: #0b0f19 !important;
      color: #93c5fd !important;
      fill: #93c5fd !important;
      font-weight: 600 !important;
    }}

    [data-theme="dark"] .mermaid svg .edgeLabel rect {{
      fill: #111827 !important;
      opacity: 0.9 !important;
    }}

    /* ==============================================================================
       6. INTERACTIVE PRONUNCIATION WIZARDS & TENSE TIMELINE
       ============================================================================== */
    .interactive-wizard-card {{
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.06), rgba(13, 148, 136, 0.06));
      border: 2px dashed var(--primary);
      border-radius: var(--radius-lg);
      padding: 26px 28px;
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
      height: 48px;
      background: var(--bg-surface);
      border: 1.5px solid var(--border-color);
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
      font-weight: 700;
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
      padding: 5px 12px;
      border-radius: 9999px;
      font-size: 0.84rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .wizard-quick-tags button:hover {{
      border-color: var(--primary);
      color: var(--primary);
      transform: translateY(-1px);
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
      padding: 7px 14px;
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
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      color: var(--text-soft);
      border: none;
      background: transparent;
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
      border: 1.5px solid var(--border-color);
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

    .meta-left-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .question-number-pill {{
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 800;
      font-size: 0.82rem;
      padding: 3px 10px;
      border-radius: 9999px;
      letter-spacing: 0.04em;
    }}

    .question-points-pill {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-soft);
      font-weight: 700;
      font-size: 0.74rem;
      padding: 2px 8px;
      border-radius: 9999px;
    }}

    .question-status-badge {{
      font-size: 0.78rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 9999px;
      transition: all 0.2s ease;
    }}

    .status-unanswered {{
      background: var(--bg-surface);
      color: var(--text-soft);
      border: 1px solid var(--border-color);
    }}

    .status-correct {{
      background: var(--success-light);
      color: var(--success);
      border: 1px solid var(--success-border);
    }}

    .status-incorrect {{
      background: var(--error-light);
      color: var(--error);
      border: 1px solid var(--error-border);
    }}

    .question-stem-wrapper {{
      margin-bottom: 18px;
    }}

    .question-stem-text {{
      font-size: 1.08rem;
      font-weight: 600;
      color: var(--text-main);
      line-height: 1.55;
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

    /* ==============================================================================
       QUIZ OPTIONS GRID: STRICT 2-COLUMN BALANCED LAYOUT (NO 3-1 SPLIT)
       ============================================================================== */
    .quiz-options-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 14px;
    }}

    @media (max-width: 640px) {{
      .quiz-options-grid {{
        grid-template-columns: 1fr;
        gap: 10px;
      }}
    }}

    /* Duolingo / Quizizz / Brilliant Style Tactile 3D Option Buttons */
    .quiz-option-btn {{
      background: var(--bg-surface);
      border: 2px solid var(--border-color);
      border-bottom: 3.5px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 14px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      cursor: pointer;
      text-align: left;
      font-size: 1.02rem;
      font-weight: 500;
      color: var(--text-main);
      font-family: var(--font-body);
      transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      user-select: none;
      outline: none;
      box-sizing: border-box;
      width: 100%;
    }}

    .quiz-option-btn:hover {{
      border-color: var(--primary);
      background: var(--primary-light);
      transform: translateY(-2px);
      border-bottom-width: 4px;
    }}

    .quiz-option-btn:active {{
      transform: translateY(2px);
      border-bottom-width: 2px;
    }}

    .quiz-option-btn:focus-visible {{
      box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.35);
    }}

    .quiz-option-btn.selected {{
      border-color: var(--primary);
      border-bottom-color: var(--primary-hover);
      background: var(--primary-light);
      color: var(--primary);
      box-shadow: 0 0 0 2px rgba(var(--primary-rgb), 0.2);
    }}

    .quiz-option-btn.correct-choice {{
      border-color: var(--success) !important;
      border-bottom-color: #15803d !important;
      background: var(--success-light) !important;
      color: var(--success) !important;
      animation: optionBounce 0.35s ease;
    }}

    .quiz-option-btn.wrong-choice {{
      border-color: var(--error) !important;
      border-bottom-color: #b91c1c !important;
      background: var(--error-light) !important;
      color: var(--error) !important;
      animation: optionShake 0.4s ease;
    }}

    @keyframes optionBounce {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.02); }}
    }}

    @keyframes optionShake {{
      0%, 100% {{ transform: translateX(0); }}
      20%, 60% {{ transform: translateX(-4px); }}
      40%, 80% {{ transform: translateX(4px); }}
    }}

    .opt-letter-circle {{
      width: 32px;
      height: 32px;
      border-radius: var(--radius-sm);
      background: var(--bg-subtle);
      border: 1.5px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.9rem;
      color: var(--text-soft);
      flex-shrink: 0;
      transition: all 0.2s ease;
    }}

    .quiz-option-btn:hover .opt-letter-circle {{
      border-color: var(--primary);
      color: var(--primary);
      background: var(--bg-surface);
    }}

    .quiz-option-btn.selected .opt-letter-circle {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
    }}

    .quiz-option-btn.correct-choice .opt-letter-circle {{
      background: var(--success);
      color: #ffffff;
      border-color: var(--success);
    }}

    .quiz-option-btn.wrong-choice .opt-letter-circle {{
      background: var(--error);
      color: #ffffff;
      border-color: var(--error);
    }}

    .opt-content-text {{
      flex: 1;
      padding: 0 4px;
      font-size: 1.05rem;
      letter-spacing: -0.01em;
    }}

    .opt-action-group {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }}

    .opt-audio-chip {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: 9999px;
      width: 32px;
      height: 32px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--text-soft);
      cursor: pointer;
      transition: all 0.2s ease;
      font-size: 0.85rem;
      flex-shrink: 0;
    }}

    .opt-audio-chip:hover {{
      background: var(--primary-light);
      color: var(--primary);
      border-color: var(--primary);
      transform: scale(1.15);
    }}

    .opt-feedback-icon {{
      font-weight: 800;
      font-size: 1.1rem;
      display: none;
    }}

    .quiz-option-btn.correct-choice .opt-feedback-icon {{
      display: inline-block;
      color: var(--success);
    }}
    .quiz-option-btn.wrong-choice .opt-feedback-icon {{
      display: inline-block;
      color: var(--error);
    }}

    /* Explanation Panel */
    .question-explanation-panel {{
      margin-top: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 18px 22px;
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
      margin-bottom: 10px;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .exp-title-row {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .exp-bulb-icon {{
      font-size: 1.2rem;
    }}

    .exp-badge {{
      font-weight: 800;
      font-size: 0.86rem;
      color: var(--primary);
      letter-spacing: 0.02em;
    }}

    .exp-qnum {{
      font-size: 0.76rem;
      background: var(--primary-light);
      color: var(--primary);
      padding: 2px 6px;
      border-radius: var(--radius-sm);
      margin-left: 6px;
      font-weight: 700;
    }}

    .exp-correct-pill {{
      font-size: 0.88rem;
      color: var(--success);
      background: var(--success-light);
      padding: 3px 10px;
      border-radius: 9999px;
      font-weight: 700;
      border: 1px solid var(--success-border);
    }}

    .exp-body-text {{
      font-size: 0.96rem;
      color: var(--text-muted);
      line-height: 1.65;
      margin-bottom: 14px;
    }}

    .exp-actions-row {{
      display: flex;
      gap: 10px;
    }}

    .retry-question-btn {{
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-soft);
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}

    .retry-question-btn:hover {{
      border-color: var(--primary);
      color: var(--primary);
      background: var(--primary-light);
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
      height: 44px;
      background: var(--bg-surface);
      border: 1.5px solid var(--border-color);
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
      border: 1.5px solid var(--border-color);
      color: var(--text-main);
      font-weight: 700;
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
      height: 50px;
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: white;
      border: none;
      border-radius: var(--radius-md);
      font-size: 1.02rem;
      font-weight: 800;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
      transition: all 0.2s ease;
    }}

    .submit-exam-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45);
    }}

    .reset-quiz-btn {{
      padding: 0 22px;
      background: var(--bg-subtle);
      border: 1.5px solid var(--border-color);
      color: var(--text-soft);
      font-weight: 700;
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
      width: 76px;
      height: 76px;
      border-radius: 9999px;
      background: var(--success);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.55rem;
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
      border: 1.5px solid var(--border-color);
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
       9. RESPONSIVE DESIGN BREAKPOINTS (MOBILE-FIRST & ADAPTIVE SYSTEM)
       ============================================================================== */
    html, body {{
      overflow-x: hidden;
      max-width: 100vw;
    }}

    /* Desktop Sidebar Collapsible State - Keep content readable */
    body.sidebar-collapsed .app-main-content {{
      max-width: 100%;
    }}

    /* Tablet & Medium Screens */
    @media (max-width: 1024px) {{
      .app-sidebar {{
        position: fixed;
        left: -320px;
        top: var(--header-height);
        bottom: 0;
        width: 300px;
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
        padding: 24px 20px 80px 20px;
        max-width: 100%;
      }}
    }}

    /* Tablets & Small Laptops */
    @media (max-width: 768px) {{
      .app-header {{
        padding: 0 16px;
      }}

      .header-center {{
        display: none;
      }}

      .hero-banner-card {{
        padding: 28px 20px;
        margin-bottom: 28px;
      }}

      .hero-title {{
        font-size: clamp(1.4rem, 4.5vw, 1.85rem);
      }}

      .hero-subtitle {{
        font-size: 0.96rem;
      }}

      .hero-stats-row {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
      }}

      .module-card-section {{
        padding: 24px 18px;
        margin-bottom: 32px;
      }}

      .exam-arena-hero {{
        flex-direction: column;
        align-items: stretch;
        gap: 18px;
        padding: 20px;
      }}

      .arena-icon-badge {{
        font-size: 2.2rem;
        padding: 12px;
      }}

      .arena-quick-stats {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        width: 100%;
      }}

      .arena-stat-badge {{
        min-width: 0;
      }}

      .exam-cards-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Standard Mobile Phones (<= 640px) */
    @media (max-width: 640px) {{
      .header-pill-btn .btn-text-label,
      .sound-toggle-btn .btn-text-label,
      #global_mode_text {{
        display: none !important;
      }}

      .sound-toggle-btn, .mode-switch-btn, .theme-toggle-btn {{
        padding: 0 10px;
        min-width: 38px;
        height: 38px;
        justify-content: center;
        font-size: 1rem;
      }}

      .quiz-options-list {{
        grid-template-columns: 1fr !important;
        gap: 10px;
      }}

      .score-summary-grid {{
        grid-template-columns: 1fr;
        gap: 10px;
      }}

      .exam-runner-header {{
        padding: 12px 14px;
        flex-wrap: wrap;
        gap: 10px;
      }}

      .exam-timer-box {{
        order: -1;
      }}
    }}

    /* Small Mobile Phones (<= 480px) */
    @media (max-width: 480px) {{
      .hero-banner-card {{
        padding: 20px 14px;
        border-radius: var(--radius-lg);
      }}

      .hero-badge {{
        font-size: 0.74rem;
        padding: 3px 10px;
      }}

      .hero-title {{
        font-size: clamp(1.22rem, 5vw, 1.55rem);
      }}

      .hero-subtitle {{
        font-size: 0.9rem;
      }}

      .hero-stats-row {{
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        padding-top: 14px;
        margin-top: 16px;
      }}

      .hero-stat-item strong {{
        font-size: 1.2rem;
      }}

      .hero-stat-item span {{
        font-size: 0.76rem;
      }}

      .module-card-section {{
        padding: 18px 12px;
        border-radius: var(--radius-md);
      }}

      .module-badge-row {{
        flex-wrap: wrap;
        gap: 6px;
      }}

      .module-part-tag, .module-status-pill, .module-qcount-pill {{
        font-size: 0.72rem;
        padding: 3px 8px;
      }}

      .table-responsive {{
        margin: 14px -6px;
        border-radius: var(--radius-sm);
      }}

      .master-table th, .master-table td {{
        padding: 10px 10px;
        font-size: 0.85rem;
      }}

      .wizard-quick-tags button {{
        font-size: 0.78rem;
        padding: 4px 8px;
      }}

      .diag-zoom-btn {{
        width: 24px;
        height: 24px;
      }}

      .floating-tools-dock {{
        bottom: 16px;
        right: 16px;
        gap: 8px;
      }}

      .float-tool-btn {{
        width: 40px;
        height: 40px;
        font-size: 1rem;
      }}
    }}

    /* Extra Narrow Phones (<= 360px - e.g. iPhone SE / 320px) */
    @media (max-width: 360px) {{
      .app-header {{
        padding: 0 10px;
      }}

      .header-left {{
        gap: 6px;
      }}

      .header-icon-btn {{
        width: 34px;
        height: 34px;
      }}

      .header-right {{
        gap: 5px;
      }}

      .hero-stats-row {{
        grid-template-columns: 1fr;
      }}

      .arena-quick-stats {{
        grid-template-columns: 1fr;
      }}

      .wizard-interactive-flow {{
        padding: 12px 8px;
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

    /* ==============================================================================
       EXAM HUB & MOCK ARENA STYLES (EDTECH PREMIUM INTERFACE)
       ============================================================================== */
    .exam-hub-section {{
      position: relative;
      background: var(--bg-card);
      border-radius: var(--radius-xl);
      border: 1px solid var(--border-light);
      box-shadow: var(--shadow-md);
      padding: 32px;
      margin-bottom: 40px;
      overflow: hidden;
    }}

    .exam-arena-hero {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 24px;
      padding: 28px;
      border-radius: var(--radius-lg);
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(124, 58, 237, 0.06) 100%);
      border: 1px solid rgba(37, 99, 235, 0.15);
      margin-bottom: 28px;
      flex-wrap: wrap;
    }}

    .exam-arena-hero-content {{
      display: flex;
      align-items: flex-start;
      gap: 20px;
      max-width: 720px;
    }}

    .arena-icon-badge {{
      font-size: 2.8rem;
      line-height: 1;
      background: var(--primary-light);
      padding: 16px;
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .arena-title-wrap .arena-title {{
      font-family: var(--font-heading);
      font-size: 1.65rem;
      font-weight: 800;
      color: var(--text-heading);
      margin-bottom: 8px;
      line-height: 1.25;
    }}

    .arena-title-wrap .arena-subtitle {{
      font-size: 0.95rem;
      color: var(--text-muted);
      line-height: 1.55;
    }}

    .arena-quick-stats {{
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .arena-stat-badge {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      padding: 12px 18px;
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      min-width: 95px;
    }}

    .arena-stat-badge .stat-number {{
      font-family: var(--font-heading);
      font-size: 1.4rem;
      font-weight: 800;
      color: var(--primary);
    }}

    .arena-stat-badge .stat-text {{
      font-size: 0.75rem;
      color: var(--text-muted);
      font-weight: 600;
      margin-top: 2px;
      text-align: center;
    }}

    /* FILTERS TABS BAR */
    .exam-filters-bar {{
      display: flex;
      gap: 10px;
      padding: 6px;
      background: var(--bg-canvas);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      margin-bottom: 24px;
      overflow-x: auto;
      scrollbar-width: thin;
    }}

    .exam-filter-btn {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-weight: 600;
      font-size: 0.88rem;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}

    .exam-filter-btn:hover {{
      background: var(--primary-light);
      color: var(--primary);
    }}

    .exam-filter-btn.active {{
      background: var(--primary);
      color: #ffffff;
      box-shadow: var(--shadow-sm);
    }}

    .exam-filter-btn .filter-count {{
      background: rgba(0, 0, 0, 0.08);
      padding: 2px 7px;
      border-radius: 12px;
      font-size: 0.75rem;
    }}

    .exam-filter-btn.active .filter-count {{
      background: rgba(255, 255, 255, 0.25);
      color: #ffffff;
    }}

    /* EXAM CARDS GRID */
    .exam-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
      gap: 24px;
      margin-bottom: 30px;
    }}

    .exam-card-item {{
      background: var(--bg-canvas);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-lg);
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
      position: relative;
    }}

    .exam-card-item:hover {{
      transform: translateY(-4px);
      box-shadow: var(--shadow-lg);
      border-color: var(--primary);
    }}

    .card-top-badges {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .card-badge {{
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 14px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}

    .badge-official {{
      background: #fef2f2;
      color: #dc2626;
      border: 1px solid #fecaca;
    }}

    .badge-new {{
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #bfdbfe;
    }}

    .badge-danang {{
      background: #ecfdf5;
      color: #059669;
      border: 1px solid #a7f3d0;
    }}

    .badge-semester {{
      background: #fdf4ff;
      color: #c026d3;
      border: 1px solid #f5d0fe;
    }}

    .badge-practice {{
      background: #fffbeb;
      color: #d97706;
      border: 1px solid #fde68a;
    }}

    .card-year-tag {{
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 600;
    }}

    .card-exam-title {{
      font-family: var(--font-heading);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 6px;
      line-height: 1.35;
    }}

    .card-exam-subtitle {{
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 14px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .card-meta-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 18px;
    }}

    .card-chip {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      padding: 4px 9px;
      border-radius: var(--radius-sm);
      font-size: 0.78rem;
      color: var(--text-body);
      font-weight: 500;
    }}

    .card-best-score-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      background: var(--bg-card);
      border-radius: var(--radius-sm);
      border: 1px dashed var(--border-light);
      margin-bottom: 16px;
      font-size: 0.82rem;
    }}

    .best-score-badge {{
      font-weight: 700;
      color: var(--success);
      background: var(--success-light);
      padding: 2px 8px;
      border-radius: 8px;
    }}

    .card-action-buttons {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}

    .card-btn {{
      padding: 9px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
      border: 1px solid transparent;
      text-align: center;
    }}

    .card-btn.practice {{
      background: var(--bg-card);
      color: var(--primary);
      border-color: var(--primary);
    }}

    .card-btn.practice:hover {{
      background: var(--primary-light);
    }}

    .card-btn.exam {{
      background: var(--primary);
      color: #ffffff;
      box-shadow: var(--shadow-sm);
    }}

    .card-btn.exam:hover {{
      background: var(--primary-hover);
      box-shadow: var(--shadow-md);
    }}

    /* ==============================================================================
       INTERACTIVE EXAM PLAYER STYLES
       ============================================================================== */
    .exam-player-wrapper {{
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-xl);
      overflow: hidden;
      box-shadow: var(--shadow-xl);
      margin-top: 10px;
    }}

    .exam-player-header-sticky {{
      position: sticky;
      top: 60px;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 24px;
      background: var(--bg-card);
      border-bottom: 1px solid var(--border-light);
      box-shadow: var(--shadow-sm);
      backdrop-filter: blur(10px);
    }}

    .player-left-info {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .exam-back-btn {{
      background: var(--bg-canvas);
      border: 1px solid var(--border-light);
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-body);
      cursor: pointer;
      transition: background 0.2s;
    }}

    .exam-back-btn:hover {{
      background: var(--primary-light);
      color: var(--primary);
    }}

    .player-exam-title {{
      font-family: var(--font-heading);
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 2px;
    }}

    .player-exam-meta-pills {{
      display: flex;
      gap: 6px;
    }}

    .exam-mode-pill {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 8px;
      background: #eff6ff;
      color: #2563eb;
    }}

    .exam-meta-pill {{
      font-size: 0.72rem;
      padding: 2px 7px;
      border-radius: 8px;
      background: var(--bg-canvas);
      color: var(--text-muted);
    }}

    /* CENTER TIMER */
    .player-center-timer {{
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 140px;
    }}

    .timer-display-wrap {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .timer-digits {{
      font-family: var(--font-mono);
      font-size: 1.3rem;
      font-weight: 700;
      color: var(--text-heading);
      letter-spacing: 0.05em;
    }}

    .timer-digits.warning {{
      color: #d97706;
      animation: pulseWarning 1s infinite;
    }}

    .timer-digits.danger {{
      color: #dc2626;
      animation: pulseDanger 0.8s infinite;
    }}

    @keyframes pulseDanger {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.08); opacity: 0.8; }}
    }}

    .timer-progress-bar {{
      width: 100%;
      height: 4px;
      background: var(--border-light);
      border-radius: 2px;
      margin-top: 4px;
      overflow: hidden;
    }}

    .timer-progress-fill {{
      height: 100%;
      background: var(--primary);
      transition: width 0.5s ease;
    }}

    .player-right-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .exam-toggle-palette-btn {{
      background: var(--bg-canvas);
      border: 1px solid var(--border-light);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .exam-submit-btn {{
      background: linear-gradient(135deg, #16a34a, #15803d);
      color: #ffffff;
      border: none;
      padding: 9px 18px;
      border-radius: var(--radius-sm);
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(22, 163, 74, 0.3);
      transition: transform 0.15s ease, filter 0.15s ease;
    }}

    .exam-submit-btn:hover {{
      filter: brightness(1.1);
      transform: translateY(-1px);
    }}

    /* SPLIT LAYOUT */
    .exam-split-layout {{
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: 0;
      min-height: 600px;
    }}

    @media (max-width: 992px) {{
      .exam-split-layout {{
        grid-template-columns: 1fr;
      }}
      .exam-palette-sidebar {{
        display: none;
      }}
      .exam-palette-sidebar.mobile-open {{
        display: block;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 99;
        max-height: 50vh;
        background: var(--bg-card);
        box-shadow: 0 -4px 20px rgba(0,0,0,0.2);
        border-radius: 16px 16px 0 0;
      }}
    }}

    .exam-questions-scroll-area {{
      padding: 30px;
      background: var(--bg-canvas);
      overflow-y: auto;
    }}

    .exam-section-header-banner {{
      background: var(--bg-card);
      border-left: 4px solid var(--primary);
      padding: 14px 18px;
      border-radius: var(--radius-sm);
      margin-bottom: 24px;
      margin-top: 16px;
      box-shadow: var(--shadow-sm);
    }}

    .exam-section-header-banner h4 {{
      font-family: var(--font-heading);
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 3px;
    }}

    .exam-section-header-banner p {{
      font-size: 0.84rem;
      color: var(--text-muted);
    }}

    /* EXAM QUESTION CARD */
    .exam-question-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 20px 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      scroll-margin-top: 140px;
    }}

    .exam-question-card.flagged {{
      border-color: #f59e0b;
      box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2);
    }}

    .exam-q-top-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .exam-q-num-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      font-size: 0.88rem;
      color: var(--text-heading);
    }}

    .exam-q-num-badge .q-num-circle {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      background: var(--primary);
      color: #ffffff;
      font-size: 0.78rem;
    }}

    .exam-q-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .q-audio-btn, .q-flag-btn {{
      background: var(--bg-canvas);
      border: 1px solid var(--border-light);
      width: 32px;
      height: 32px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.85rem;
      transition: all 0.15s ease;
    }}

    .q-audio-btn:hover {{
      background: var(--primary-light);
      color: var(--primary);
    }}

    .q-flag-btn.active {{
      background: #fef3c7;
      color: #d97706;
      border-color: #f59e0b;
    }}

    .exam-q-prompt-text {{
      font-size: 0.96rem;
      line-height: 1.6;
      color: var(--text-body);
      margin-bottom: 16px;
      font-weight: 500;
    }}

    /* REUSE QUIZ-OPTION-BTN ROBUST STYLES */
    .exam-options-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }}

    .exam-text-input-wrap {{
      margin-top: 12px;
    }}

    .exam-text-input {{
      width: 100%;
      padding: 12px 16px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-medium);
      background: var(--bg-canvas);
      color: var(--text-body);
      font-family: inherit;
      font-size: 0.92rem;
      line-height: 1.5;
      transition: border-color 0.2s;
    }}

    .exam-text-input:focus {{
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }}

    /* EXAM EXPLANATION ACCORDION */
    .exam-exp-box {{
      margin-top: 14px;
      padding: 14px 18px;
      border-radius: var(--radius-sm);
      background: var(--primary-light);
      border-left: 3px solid var(--primary);
      font-size: 0.88rem;
      line-height: 1.6;
      color: var(--text-body);
    }}

    .exam-exp-box.correct-box {{
      background: var(--success-light);
      border-color: var(--success);
    }}

    .exam-exp-box.incorrect-box {{
      background: #fef2f2;
      border-color: #dc2626;
    }}

    /* QUESTION PALETTE SIDEBAR */
    .exam-palette-sidebar {{
      background: var(--bg-card);
      border-left: 1px solid var(--border-light);
      padding: 24px;
      position: sticky;
      top: 125px;
      height: calc(100vh - 140px);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .palette-header .palette-title {{
      font-family: var(--font-heading);
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 12px;
    }}

    .palette-legend {{
      display: flex;
      gap: 12px;
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}

    .legend-item {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    .legend-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}

    .dot-unanswered {{ background: var(--border-medium); }}
    .dot-answered {{ background: var(--primary); }}
    .dot-flagged {{ background: #f59e0b; }}

    .palette-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin-bottom: 20px;
    }}

    .palette-btn {{
      aspect-ratio: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-light);
      background: var(--bg-canvas);
      color: var(--text-body);
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.15s ease;
      position: relative;
    }}

    .palette-btn:hover {{
      border-color: var(--primary);
      transform: scale(1.05);
    }}

    .palette-btn.answered {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
    }}

    .palette-btn.flagged::after {{
      content: '🚩';
      position: absolute;
      top: -5px;
      right: -5px;
      font-size: 0.65rem;
    }}

    .palette-btn.review-correct {{
      background: #16a34a !important;
      color: #fff !important;
    }}

    .palette-btn.review-incorrect {{
      background: #dc2626 !important;
      color: #fff !important;
    }}

    /* SCORE MODAL STYLES */
    .exam-score-modal {{
      position: fixed;
      inset: 0;
      z-index: 999;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      animation: fadeIn 0.25s ease;
    }}

    .exam-score-dialog {{
      background: var(--bg-card);
      border-radius: var(--radius-xl);
      border: 1px solid var(--border-light);
      box-shadow: var(--shadow-2xl);
      max-width: 640px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      padding: 36px;
      text-align: center;
    }}

    .score-trophy-badge {{
      font-size: 3.5rem;
      line-height: 1;
      margin-bottom: 12px;
      animation: bounceTrophy 1.2s ease infinite alternate;
    }}

    @keyframes bounceTrophy {{
      from {{ transform: translateY(0); }}
      to {{ transform: translateY(-8px); }}
    }}

    .score-dialog-title {{
      font-family: var(--font-heading);
      font-size: 1.55rem;
      font-weight: 800;
      color: var(--text-heading);
      margin-bottom: 6px;
    }}

    .score-dialog-subtitle {{
      font-size: 0.92rem;
      color: var(--text-muted);
      margin-bottom: 24px;
    }}

    .score-summary-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 28px;
    }}

    .score-stat-card {{
      background: var(--bg-canvas);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 16px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}

    .score-stat-card.primary-card {{
      background: var(--primary-light);
      border-color: rgba(37, 99, 235, 0.3);
    }}

    .stat-card-label {{
      font-size: 0.68rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 4px;
    }}

    .stat-card-value {{
      font-family: var(--font-heading);
      font-size: 2rem;
      font-weight: 800;
      color: var(--primary);
      line-height: 1.1;
    }}

    .stat-card-value.text-accent {{
      color: var(--accent-teal);
    }}

    .stat-card-sub {{
      font-size: 0.76rem;
      color: var(--text-muted);
      margin-top: 4px;
      font-weight: 600;
    }}

    /* SKILLS BREAKDOWN */
    .score-skills-breakdown {{
      background: var(--bg-canvas);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 24px;
      text-align: left;
    }}

    .skills-breakdown-title {{
      font-family: var(--font-heading);
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 14px;
    }}

    .skill-bar-row {{
      margin-bottom: 12px;
    }}

    .skill-bar-row:last-child {{
      margin-bottom: 0;
    }}

    .skill-info {{
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      font-weight: 600;
      margin-bottom: 4px;
    }}

    .skill-track {{
      height: 7px;
      background: var(--border-light);
      border-radius: 4px;
      overflow: hidden;
    }}

    .skill-fill {{
      height: 100%;
      border-radius: 4px;
      transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .fill-green {{ background: #16a34a; }}
    .fill-blue {{ background: #2563eb; }}
    .fill-amber {{ background: #f59e0b; }}
    .fill-purple {{ background: #9333ea; }}

    .pedagogical-advice-box {{
      background: #fefce8;
      border: 1px solid #fef08a;
      border-radius: var(--radius-md);
      padding: 16px 20px;
      text-align: left;
      margin-bottom: 26px;
    }}

    .pedagogical-advice-box .advice-header {{
      font-weight: 700;
      font-size: 0.88rem;
      color: #854d0e;
      margin-bottom: 4px;
    }}

    .pedagogical-advice-box .advice-body {{
      font-size: 0.85rem;
      color: #713f12;
      line-height: 1.55;
    }}

    .score-dialog-actions {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .score-action-btn {{
      padding: 12px 20px;
      border-radius: var(--radius-sm);
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      border: none;
    }}

    .score-action-btn.primary {{
      background: var(--primary);
      color: #ffffff;
    }}

    .score-action-btn.primary:hover {{
      background: var(--primary-hover);
    }}

    .score-action-btn.secondary {{
      background: var(--bg-canvas);
      color: var(--text-body);
      border: 1px solid var(--border-medium);
    }}

    .score-action-btn.secondary:hover {{
      background: var(--primary-light);
      color: var(--primary);
    }}

    .score-action-btn.outline {{
      background: transparent;
      color: var(--text-muted);
    }}

    .score-action-btn.outline:hover {{
      color: var(--text-body);
    }}
    
  </style>
</head>
<body>

  <!-- 1. STICKY TOP APP HEADER -->
  <header class="app-header">
    <div class="header-left">
      <div class="header-action-group">
        <button type="button" class="header-icon-btn" id="header_scroll_top" onclick="scrollToTop()" title="Lên đầu trang" aria-label="Lên đầu trang">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="18 15 12 9 6 15"></polyline>
          </svg>
        </button>
        <button type="button" class="header-icon-btn" id="sidebar_toggle" onclick="toggleSidebar()" title="Mở / đóng danh mục chuyên đề (Sidebar)" aria-label="Mở đóng danh mục">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
        </button>
      </div>
    </div>

    <div class="header-center">
      <svg class="search-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="text" class="search-input-box" id="global_search" placeholder="Tìm chuyên đề, quy tắc, cấu trúc câu... (Ctrl+K)" oninput="handleGlobalSearch(this.value)">
      <div class="search-results-dropdown" id="search_dropdown"></div>
    </div>

    <div class="header-right">
      <button type="button" class="sound-toggle-btn" id="sound_toggle_btn" onclick="toggleSound()" title="Bật/Tắt hiệu ứng âm thanh">
        🔊 <span class="btn-text-label">Âm thanh</span>
      </button>
      <button type="button" class="mode-switch-btn" id="global_mode_btn" onclick="toggleGlobalMode()" title="Chuyển chế độ luyện tập hoặc thi thử">
        <span id="global_mode_icon">🎯</span>
        <span id="global_mode_text">Luyện tập</span>
      </button>
      <button type="button" class="theme-toggle-btn" id="theme_toggle" onclick="toggleTheme()" title="Chuyển giao diện Sáng / Tối">🌙</button>
    </div>
    
    <div class="global-progress-line" id="global_progress_line"></div>
  </header>

  <!-- 2. MAIN APP LAYOUT: SIDEBAR + CONTENT -->
  <div class="sidebar-backdrop" id="sidebar_backdrop" onclick="toggleSidebar()"></div>
  <div class="app-layout-container">
    
    <!-- LEFT SIDEBAR -->
    <aside class="app-sidebar" id="app_sidebar">
      <div class="sidebar-inner-block">
        <div class="sidebar-title-row">
          <span style="font-size: 0.82rem; font-weight: 800; color: var(--text-soft); text-transform: uppercase;">MỤC LỤC 16 CHUYÊN ĐỀ</span>
        </div>
        { "".join(toc_html) }
      </div>
    </aside>

    <!-- MAIN LEARNING AREA -->
    <main class="app-main-content">
      
      <!-- HERO BANNER -->
      <div class="hero-banner-card">
        <span class="hero-badge">TÀI LIỆU ÔN THI VÀO LỚP 10 • THEO CHƯƠNG TRÌNH MỚI</span>
        <h2 class="hero-title">Cẩm Nang Ôn Thi Vào Lớp 10 Môn Tiếng Anh</h2>
        <p class="hero-subtitle">Hệ thống hóa 16 chuyên đề ngữ âm, ngữ pháp và từ vựng trọng tâm; kèm ví dụ minh họa, mẹo ghi nhớ quy tắc và 7 bộ đề thi tuyển sinh có lời giải chi tiết.</p>
        
        <div style="margin-top: 18px; margin-bottom: 22px;">
          <a href="#mod_exam_arena" style="display:inline-flex;align-items:center;gap:10px;padding:12px 24px;background:linear-gradient(135deg,#2563eb 0%,#1d4ed8 100%);color:#ffffff;border-radius:10px;font-weight:700;font-size:0.95rem;text-decoration:none;box-shadow:0 4px 14px rgba(37,99,235,0.35);transition:transform 0.2s,box-shadow 0.2s;">
            <span>Làm bài thi thử & luyện tập theo đề (7 bộ đề) →</span>
            <span style="background:rgba(255,255,255,0.25);padding:2px 8px;border-radius:12px;font-size:0.8rem;">Mới cập nhật</span>
          </a>
        </div>
        <div class="hero-stats-row">
          <div class="hero-stat-item">
            <strong>16 Chuyên Đề</strong>
            <span>Ngữ âm, ngữ pháp và từ vựng</span>
          </div>
          <div class="hero-stat-item">
            <strong>7 Bộ Đề Thi</strong>
            <span>Quảng Ngãi, Đà Nẵng, HK1 & HK2</span>
          </div>
          <div class="hero-stat-item">
            <strong>420+ Câu Hỏi</strong>
            <span>Có đáp án và giải thích chi tiết</span>
          </div>
          <div class="hero-stat-item">
            <strong>2 Chế Độ</strong>
            <span>Luyện tập từng câu & Thi bấm giờ</span>
          </div>
        </div>
      </div>

      <!-- ALL 16 MODULE SECTIONS -->
      { "".join(sections_html) }

      <!-- MODULE 4: TRUNG TÂM LUYỆN ĐỀ & PHÒNG THI THỬ VÀO 10 -->

    <!-- ==============================================================================
         MODULE LUYỆN ĐỀ & PHÒNG THI THỬ VÀO 10 (EXAM HUB & MOCK ARENA)
         ============================================================================== -->
    <section id="mod_exam_arena" class="module-card-section exam-hub-section" data-mod-id="exam_arena" data-category="4">
      <div class="module-badge-row">
        <span class="module-part-tag">PHẦN 4: LUYỆN ĐỀ & THI THỬ</span>
        <span class="module-status-pill">7 Bộ Đề Tuyển Sinh & Học Kỳ Lớp 9</span>
        <span class="module-qcount-pill">260+ Câu Hỏi Kèm Hướng Dẫn Giải</span>
      </div>

      <!-- EXAM HUB HERO BANNER -->
      <div class="exam-arena-hero">
        <div class="exam-arena-hero-content">
          <div class="arena-icon-badge">📝</div>
          <div class="arena-title-wrap">
            <h2 class="arena-title">Luyện Đề Thi Tuyển Sinh Vào Lớp 10</h2>
            <p class="arena-subtitle">Tổng hợp đề thi tuyển sinh chính thức (Quảng Ngãi, Đà Nẵng) và đề thi học kỳ lớp 9 theo chương trình mới. Hỗ trợ bấm giờ làm bài, chấm điểm tự động và xem lại lời giải chi tiết cho từng câu.</p>
          </div>
        </div>
        <div class="arena-quick-stats">
          <div class="arena-stat-badge">
            <span class="stat-number">7</span>
            <span class="stat-text">Bộ Đề Thi</span>
          </div>
          <div class="arena-stat-badge">
            <span class="stat-number">260+</span>
            <span class="stat-text">Câu Hỏi Luyện Thi</span>
          </div>
          <div class="arena-stat-badge">
            <span class="stat-number">100%</span>
            <span class="stat-text">Giải Thích Chi Tiết</span>
          </div>
          <div class="arena-stat-badge">
            <span class="stat-number">2</span>
            <span class="stat-text">Chế Độ Luyện Thi</span>
          </div>
        </div>
      </div>

      <!-- FILTER TABS BAR -->
      <div class="exam-filters-bar" id="examFiltersBar">
        <button type="button" class="exam-filter-btn active" data-filter="all" onclick="filterExams('all')">
          <span class="filter-icon">📚</span> Tất Cả Đề Thi <span class="filter-count">7</span>
        </button>
        <button type="button" class="exam-filter-btn" data-filter="quangngai" onclick="filterExams('quangngai')">
          <span class="filter-icon">🏛️</span> Tuyển Sinh Quảng Ngãi <span class="filter-count">3</span>
        </button>
        <button type="button" class="exam-filter-btn" data-filter="danang" onclick="filterExams('danang')">
          <span class="filter-icon">🌊</span> Tuyển Sinh Đà Nẵng <span class="filter-count">1</span>
        </button>
        <button type="button" class="exam-filter-btn" data-filter="semester" onclick="filterExams('semester')">
          <span class="filter-icon">📖</span> Học Kỳ 1 & 2 Lớp 9 <span class="filter-count">2</span>
        </button>
        <button type="button" class="exam-filter-btn" data-filter="practice" onclick="filterExams('practice')">
          <span class="filter-icon">🎯</span> Đề Luyện Tập 45 Câu <span class="filter-count">1</span>
        </button>
      </div>

      <!-- EXAM CARDS GRID -->
      <div class="exam-cards-grid" id="examCardsGrid">
        <!-- Dynamic Cards rendered via JS -->
      </div>

      <!-- INTERACTIVE EXAM PLAYER (HIDDEN BY DEFAULT) -->
      <div class="exam-player-wrapper" id="examPlayerWrapper" style="display: none;">
        <!-- STICKY ACTION BAR -->
        <div class="exam-player-header-sticky">
          <div class="player-left-info">
            <button type="button" class="exam-back-btn" onclick="exitExamPlayer()" title="Quay lại danh sách đề thi">
              ← Danh sách đề
            </button>
            <div class="player-title-box">
              <h3 class="player-exam-title" id="playerExamTitle">Đang tải đề thi...</h3>
              <div class="player-exam-meta-pills">
                <span class="exam-mode-pill" id="playerModePill">🎯 Luyện Tập Từng Câu</span>
                <span class="exam-meta-pill" id="playerDurationPill">⏱️ 60 phút</span>
                <span class="exam-meta-pill" id="playerQCountPill">❓ 40 câu</span>
              </div>
            </div>
          </div>

          <div class="player-center-timer" id="playerTimerBox">
            <div class="timer-display-wrap">
              <span class="timer-icon">⏱️</span>
              <span class="timer-digits" id="timerDigits">60:00</span>
            </div>
            <div class="timer-progress-bar">
              <div class="timer-progress-fill" id="timerProgressFill" style="width: 100%;"></div>
            </div>
          </div>

          <div class="player-right-actions">
            <button type="button" class="exam-toggle-palette-btn" onclick="toggleQuestionPalette()" title="Bật/Tắt Bảng điều hướng">
              🧭 <span class="btn-text-label">Bảng câu hỏi</span>
            </button>
            <button type="button" class="exam-submit-btn" id="examSubmitBtn" onclick="confirmSubmitExam()">
              🚀 Nộp Bài Thi
            </button>
          </div>
        </div>

        <!-- MAIN EXAM SPLIT VIEW -->
        <div class="exam-split-layout">
          <!-- LEFT: QUESTIONS CONTAINER -->
          <div class="exam-questions-scroll-area" id="examQuestionsScrollArea">
            <div class="exam-questions-inner" id="examQuestionsInner">
              <!-- Dynamically rendered questions list -->
            </div>
          </div>

          <!-- RIGHT: QUESTION PALETTE NAVIGATOR (STICKY) -->
          <aside class="exam-palette-sidebar" id="examPaletteSidebar">
            <div class="palette-header">
              <div class="palette-title">🧭 Bảng Điều Hướng Câu Hỏi</div>
              <div class="palette-legend">
                <span class="legend-item"><span class="legend-dot dot-unanswered"></span> Chưa làm</span>
                <span class="legend-item"><span class="legend-dot dot-answered"></span> Đã làm</span>
                <span class="legend-item"><span class="legend-dot dot-flagged"></span> Xem lại 🚩</span>
              </div>
            </div>

            <div class="palette-grid" id="paletteGrid">
              <!-- Dynamic Question buttons (1, 2, 3...) -->
            </div>

            <div class="palette-footer-stats">
              <div class="palette-progress-label">
                <span>Tiến độ:</span>
                <strong id="paletteProgressText">0 / 40 (0%)</strong>
              </div>
              <div class="palette-progress-track">
                <div class="palette-progress-fill" id="paletteProgressFill" style="width: 0%;"></div>
              </div>
            </div>
          </aside>
        </div>
      </div>

      <!-- SCORE BOARD MODAL / POPUP -->
      <div class="exam-score-modal" id="examScoreModal" style="display: none;">
        <div class="exam-score-dialog">
          <div class="score-dialog-header">
            <div class="score-trophy-badge" id="scoreTrophyIcon">🏆</div>
            <h3 class="score-dialog-title" id="scoreDialogTitle">Kết Quả Bài Thi Thử</h3>
            <p class="score-dialog-subtitle" id="scoreDialogSubtitle">Chúc mừng bạn đã hoàn thành bài thi thử tuyển sinh!</p>
          </div>

          <div class="score-summary-grid">
            <div class="score-stat-card primary-card">
              <span class="stat-card-label">ĐIỂM SỐ (THANG 10)</span>
              <div class="stat-card-value" id="scoreTotalTen">8.5</div>
              <span class="stat-card-sub" id="scoreCorrectCount">Đúng 34 / 40 câu</span>
            </div>
            <div class="score-stat-card">
              <span class="stat-card-label">TỶ LỆ CHÍNH XÁC</span>
              <div class="stat-card-value text-accent" id="scoreAccuracyPercent">85%</div>
              <span class="stat-card-sub" id="scoreGradeRank">Xếp loại: Giỏi</span>
            </div>
            <div class="score-stat-card">
              <span class="stat-card-label">THỜI GIAN LÀM BÀI</span>
              <div class="stat-card-value" id="scoreTimeTaken">42:15</div>
              <span class="stat-card-sub">Thời gian tối đa: 60:00</span>
            </div>
          </div>

          <!-- SKILLS BREAKDOWN CHART -->
          <div class="score-skills-breakdown">
            <h4 class="skills-breakdown-title">📊 Đánh Giá Năng Lực Theo 4 Trụ Cột</h4>
            <div class="skill-bar-row">
              <div class="skill-info">
                <span class="skill-name">🔊 Ngữ âm & Trọng âm</span>
                <span class="skill-pct" id="skillPhoneticsPct">100%</span>
              </div>
              <div class="skill-track"><div class="skill-fill fill-green" id="skillPhoneticsFill" style="width: 100%;"></div></div>
            </div>
            <div class="skill-bar-row">
              <div class="skill-info">
                <span class="skill-name">📖 Ngữ pháp & Từ vựng</span>
                <span class="skill-pct" id="skillGrammarPct">85%</span>
              </div>
              <div class="skill-track"><div class="skill-fill fill-blue" id="skillGrammarFill" style="width: 85%;"></div></div>
            </div>
            <div class="skill-bar-row">
              <div class="skill-info">
                <span class="skill-name">📑 Kỹ năng Đọc hiểu</span>
                <span class="skill-pct" id="skillReadingPct">80%</span>
              </div>
              <div class="skill-track"><div class="skill-fill fill-amber" id="skillReadingFill" style="width: 80%;"></div></div>
            </div>
            <div class="skill-bar-row">
              <div class="skill-info">
                <span class="skill-name">✍️ Viết & Biến đổi câu</span>
                <span class="skill-pct" id="skillWritingPct">75%</span>
              </div>
              <div class="skill-track"><div class="skill-fill fill-purple" id="skillWritingFill" style="width: 75%;"></div></div>
            </div>
          </div>

          <!-- PEDAGOGICAL ADVICE BOX -->
          <div class="pedagogical-advice-box" id="pedagogicalAdviceBox">
            <div class="advice-header">💡 Lời Khuyên Sư Phạm & Định Hướng Ôn Tập:</div>
            <div class="advice-body" id="pedagogicalAdviceText">
              Em đã nắm rất vững ngữ âm và trọng âm. Cần rèn luyện thêm các cấu trúc viết lại câu với câu điều kiện loại 2, 3 và mệnh đề quan hệ để đạt điểm tuyệt đối 10.0!
            </div>
          </div>

          <div class="score-dialog-actions">
            <button type="button" class="score-action-btn primary" onclick="reviewExamAnswers()">
              🔍 Xem Lại Bài Làm & Lời Giải Chi Tiết
            </button>
            <button type="button" class="score-action-btn secondary" onclick="retakeCurrentExam()">
              🔄 Làm Lại Đề Này
            </button>
            <button type="button" class="score-action-btn outline" onclick="closeScoreModal()">
              📋 Về Danh Sách Đề Thi
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- INLINE EXAM DATABASE JSON IN SCRIPT -->
    <script>
      window.GLOBAL_EXAMS_DATABASE = {exam_db_raw};
    </script>
    

    </main>
  </div>

  <!-- FLOATING QUICK ACTIONS -->
  <div class="floating-tools-dock">
    <button type="button" class="float-tool-btn" onclick="scrollToTop()" title="Lên đầu trang">⬆</button>
    <button type="button" class="float-tool-btn" onclick="resetAllProgress()" title="Đặt lại toàn bộ tiến độ">🔄</button>
  </div>

  <!-- CLIENT-SIDE JS APPLICATION ENGINE -->
  <script>
    // ==============================================================================
    // 1. STATE MANAGEMENT & LOCAL STORAGE
    // ==============================================================================
    const APP_STORAGE_KEY = 'AnhVan10_Master_Progress_v2';
    
    let appState = {{
      theme: 'light',
      globalMode: 'practice', // 'practice' or 'exam'
      soundEnabled: true,
      answers: {{}},          // qid -> user_selected_option
      examSubmitted: {{}},   // mod_id -> boolean
      examScores: {{}},      // mod_id -> score
      activeSection: null
    }};

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
        updateTocBadges();
      }} catch (e) {{
        console.warn('Cannot save state:', e);
      }}
    }}

    // ==============================================================================
    // 2. WEB AUDIO API SYNTHESIZER (NATIVE SOUND EFFECTS - 100% OFFLINE)
    // ==============================================================================
    let audioCtx = null;
    let soundEnabled = true;

    function getAudioContext() {{
      if (!audioCtx) {{
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) audioCtx = new AudioContext();
      }}
      if (audioCtx && audioCtx.state === 'suspended') {{
        audioCtx.resume();
      }}
      return audioCtx;
    }}

    function playSuccessTone() {{
      if (!soundEnabled) return;
      const ctx = getAudioContext();
      if (!ctx) return;
      
      const now = ctx.currentTime;
      const osc1 = ctx.createOscillator();
      const gain1 = ctx.createGain();
      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(523.25, now);
      gain1.gain.setValueAtTime(0.12, now);
      gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
      osc1.connect(gain1);
      gain1.connect(ctx.destination);
      osc1.start(now);
      osc1.stop(now + 0.16);
      
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = 'sine';
      osc2.frequency.setValueAtTime(783.99, now + 0.08);
      gain2.gain.setValueAtTime(0.14, now + 0.08);
      gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
      osc2.connect(gain2);
      gain2.connect(ctx.destination);
      osc2.start(now + 0.08);
      osc2.stop(now + 0.38);
    }}

    function playWrongTone() {{
      if (!soundEnabled) return;
      const ctx = getAudioContext();
      if (!ctx) return;
      
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.setValueAtTime(180, now + 0.08);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.26);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.26);
    }}

    function toggleSound() {{
      soundEnabled = !soundEnabled;
      const btn = document.getElementById('sound_toggle_btn');
      if (btn) {{
        btn.innerHTML = soundEnabled ? '🔊 <span class="btn-text-label">Âm thanh: Bật</span>' : '🔇 <span class="btn-text-label">Âm thanh: Tắt</span>';
      }}
      appState.soundEnabled = soundEnabled;
      saveState();
    }}

    // ==============================================================================
    // 3. THEME ENGINE & UI TOGGLES
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
      const backdrop = document.getElementById('sidebar_backdrop');
      if (window.innerWidth <= 1024) {{
        const isOpen = sb?.classList.toggle('open');
        if (isOpen) {{
          backdrop?.classList.add('active');
        }} else {{
          backdrop?.classList.remove('active');
        }}
      }} else {{
        document.body.classList.toggle('sidebar-collapsed');
      }}
      requestAnimationFrame(normalizeMermaidDiagrams);
    }}

    function normalizeMermaidDiagrams() {{
      document.querySelectorAll('.mermaid-content .mermaid svg').forEach(svg => {{
        if (!svg.getAttribute('preserveAspectRatio')) {{
          svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
        }}
        const styleMaxW = svg.style.maxWidth;
        if (styleMaxW && parseInt(styleMaxW) > 640) {{
          svg.style.maxWidth = 'min(100%, 640px)';
        }}
        svg.style.width = 'auto';
        svg.style.height = 'auto';
        svg.style.display = 'block';
        svg.style.margin = '0 auto';
      }});
    }}

    function scrollToTop() {{
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // ==============================================================================
    // 3.5. MERMAID DIAGRAM ZOOM & PAN CONTROLLER
    // ==============================================================================
    const mermaidStates = {{}};

    function zoomMermaid(diagId, factor) {{
      if (!mermaidStates[diagId]) {{
        mermaidStates[diagId] = {{ scale: 1.0, panX: 0, panY: 0 }};
      }}
      const state = mermaidStates[diagId];
      state.scale = Math.min(2.5, Math.max(0.5, state.scale * factor));
      applyMermaidTransform(diagId);
    }}

    function resetMermaidZoom(diagId) {{
      mermaidStates[diagId] = {{ scale: 1.0, panX: 0, panY: 0 }};
      applyMermaidTransform(diagId);
    }}

    function applyMermaidTransform(diagId) {{
      const content = document.getElementById('content_' + diagId);
      if (!content) return;
      const state = mermaidStates[diagId] || {{ scale: 1.0, panX: 0, panY: 0 }};
      content.style.transform = `translate(${{state.panX}}px, ${{state.panY}}px) scale(${{state.scale}})`;
    }}

    function initMermaidInteractions() {{
      normalizeMermaidDiagrams();
      setTimeout(normalizeMermaidDiagrams, 300);
      setTimeout(normalizeMermaidDiagrams, 800);

      // Auto close sidebar on mobile when navigating
      document.querySelectorAll('.toc-link').forEach(link => {{
        link.addEventListener('click', () => {{
          if (window.innerWidth <= 1024) {{
            document.getElementById('app_sidebar')?.classList.remove('open');
            document.getElementById('sidebar_backdrop')?.classList.remove('active');
          }}
        }});
      }});

      document.querySelectorAll('.mermaid-viewport').forEach(vp => {{
        const diagId = vp.id.replace('viewport_', '');
        let isDragging = false;
        let startX = 0, startY = 0;
        
        vp.addEventListener('mousedown', e => {{
          if (e.target.closest('.mermaid-zoom-toolbar')) return;
          isDragging = true;
          startX = e.clientX;
          startY = e.clientY;
          vp.style.cursor = 'grabbing';
        }});
        
        window.addEventListener('mousemove', e => {{
          if (!isDragging) return;
          if (!mermaidStates[diagId]) {{
            mermaidStates[diagId] = {{ scale: 1.0, panX: 0, panY: 0 }};
          }}
          const state = mermaidStates[diagId];
          const dx = e.clientX - startX;
          const dy = e.clientY - startY;
          startX = e.clientX;
          startY = e.clientY;
          state.panX += dx;
          state.panY += dy;
          applyMermaidTransform(diagId);
        }});
        
        window.addEventListener('mouseup', () => {{
          if (isDragging) {{
            isDragging = false;
            vp.style.cursor = 'grab';
          }}
        }});

        vp.addEventListener('wheel', e => {{
          if (e.ctrlKey) {{
            e.preventDefault();
            const factor = e.deltaY < 0 ? 1.15 : 0.85;
            zoomMermaid(diagId, factor);
          }}
        }}, {{ passive: false }});
      }});
    }}

    // ==============================================================================
    // 4. QUIZ ENGINE (PRACTICE VS EXAM)
    // ==============================================================================
    function handleOptionSelect(qid, optKey) {{
      const card = document.getElementById('card_' + qid);
      if (!card) return;
      
      const correctKey = (card.getAttribute('data-correct') || '').toUpperCase();
      const wrapper = card.closest('.interactive-quiz-wrapper');
      const modId = wrapper?.getAttribute('data-mod-id') || '';
      
      appState.answers[qid] = optKey;
      saveState();
      
      card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
        btn.classList.remove('selected');
        if (btn.getAttribute('data-opt') === optKey) {{
          btn.classList.add('selected');
        }}
      }});
      
      const statusBadge = card.querySelector('.question-status-badge');
      
      if (appState.globalMode === 'practice') {{
        const isCorrect = (optKey.toUpperCase() === correctKey);
        
        if (isCorrect) {{
          playSuccessTone();
        }} else {{
          playWrongTone();
        }}
        
        card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
          const bOpt = btn.getAttribute('data-opt');
          const feedbackIcon = btn.querySelector('.opt-feedback-icon');
          btn.classList.remove('correct-choice', 'wrong-choice');
          if (feedbackIcon) feedbackIcon.textContent = '';
          
          if (bOpt === correctKey) {{
            btn.classList.add('correct-choice');
            if (feedbackIcon) feedbackIcon.textContent = '✓';
          }} else if (bOpt === optKey && !isCorrect) {{
            btn.classList.add('wrong-choice');
            if (feedbackIcon) feedbackIcon.textContent = '✕';
          }}
        }});
        
        if (statusBadge) {{
          statusBadge.textContent = isCorrect ? '✓ Chính xác' : '✗ Chưa đúng';
          statusBadge.className = 'question-status-badge ' + (isCorrect ? 'status-correct' : 'status-incorrect');
        }}
        
        const exp = document.getElementById('exp_' + qid);
        if (exp) exp.classList.remove('hidden');
      }} else {{
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
        const feedbackIcon = btn.querySelector('.opt-feedback-icon');
        if (feedbackIcon) feedbackIcon.textContent = '';
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
      
      updateTocBadges();
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
        
        card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
          const bOpt = btn.getAttribute('data-opt');
          const feedbackIcon = btn.querySelector('.opt-feedback-icon');
          btn.classList.remove('correct-choice', 'wrong-choice');
          if (feedbackIcon) feedbackIcon.textContent = '';
          
          if (bOpt === correct) {{
            btn.classList.add('correct-choice');
            if (feedbackIcon) feedbackIcon.textContent = '✓';
          }} else if (bOpt === userChoice && !isRight) {{
            btn.classList.add('wrong-choice');
            if (feedbackIcon) feedbackIcon.textContent = '✕';
          }}
        }});
        
        const badge = card.querySelector('.question-status-badge');
        if (badge) {{
          badge.textContent = isRight ? '✓ Đúng' : (userChoice ? '✗ Sai' : 'Chưa chọn');
          badge.className = 'question-status-badge ' + (isRight ? 'status-correct' : 'status-incorrect');
        }}
        
        const exp = document.getElementById('exp_' + qid);
        if (exp) exp.classList.remove('hidden');
      }});
      
      appState.examSubmitted[modId] = true;
      appState.examScores[modId] = score;
      saveState();
      
      if (score >= Math.round(total * 0.8)) {{
        playSuccessTone();
      }} else {{
        playWrongTone();
      }}
      
      const banner = document.getElementById('result_' + modId);
      const scoreNum = document.getElementById('score_num_' + modId);
      const comment = document.getElementById('comment_' + modId);
      const pctTag = document.getElementById('pct_' + modId);
      
      if (banner && scoreNum) {{
        scoreNum.textContent = score;
        const pct = Math.round((score / total) * 100);
        if (pctTag) pctTag.textContent = 'Tỉ lệ đúng: ' + pct + '%';
        if (comment) {{
          if (pct >= 90) comment.textContent = '🌟 Xuất sắc! Bạn đã nắm rất vững kiến thức của chuyên đề này.';
          else if (pct >= 70) comment.textContent = '👍 Khá tốt! Hãy xem lại phần giải thích chi tiết của các câu làm sai để củng cố thêm.';
          else comment.textContent = '📖 Cần ôn tập lại! Hãy đọc lại phần lý thuyết và ví dụ minh họa ở trên trước khi làm lại.';
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
        card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
          btn.classList.remove('selected', 'correct-choice', 'wrong-choice');
          const feedbackIcon = btn.querySelector('.opt-feedback-icon');
          if (feedbackIcon) feedbackIcon.textContent = '';
        }});
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

    function updateTocBadges() {{
      document.querySelectorAll('.interactive-quiz-wrapper').forEach(wrapper => {{
        const modId = wrapper.getAttribute('data-mod-id');
        if (!modId) return;
        
        const total = parseInt(wrapper.getAttribute('data-total') || '0', 10);
        let answered = 0;
        wrapper.querySelectorAll('.quiz-question-card').forEach(card => {{
          const qid = card.getAttribute('data-qid');
          if (appState.answers[qid]) answered++;
        }});
        
        const badge = document.getElementById('toc_badge_' + modId);
        const dot = document.getElementById('toc_dot_' + modId);
        if (badge && total > 0) {{
          badge.textContent = answered + '/' + total;
          if (answered === total) {{
            badge.classList.add('completed');
            badge.textContent = '✓ ' + answered + '/' + total;
            if (dot) dot.style.background = 'var(--success)';
          }} else {{
            badge.classList.remove('completed');
            if (dot) dot.style.background = '';
          }}
        }}
      }});
    }}

    // ==============================================================================
    // 5. PRONUNCIATION INTERACTIVE WIZARDS (ED & S/ES)
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
      
      playSpeech(clean);
      
      const exceptions = ['naked', 'wicked', 'sacred', 'beloved', 'crooked', 'ragged', 'hatred', 'wretched', 'learned', 'blessed'];
      if (exceptions.includes(clean)) {{
        badge.textContent = '/ɪd/ (TRƯỜNG HỢP NGOẠI LỆ)';
        rule.textContent = 'Từ này là tính từ đặc biệt, luôn phát âm đuôi -ed là /ɪd/.';
        badge.style.color = '#dc2626';
        return;
      }}
      
      let stem = clean;
      if (stem.endsWith('ed')) stem = stem.slice(0, -2);
      else if (stem.endsWith('d')) stem = stem.slice(0, -1);
      
      if (stem.endsWith('t') || stem.endsWith('te') || stem.endsWith('d') || stem.endsWith('de')) {{
        badge.textContent = '/ɪd/';
        rule.textContent = 'Âm cuối là /t/ hoặc /d/ ➔ Phát âm là /ɪd/ (Mẹo nhớ: "Tiền - Đô")';
        badge.style.color = '#2563eb';
      }}
      else if (stem.endsWith('k') || stem.endsWith('ke') || stem.endsWith('s') || stem.endsWith('ss') || 
               stem.endsWith('sh') || stem.endsWith('p') || stem.endsWith('pe') || stem.endsWith('ch') || 
               stem.endsWith('gh') || stem.endsWith('ph') || stem.endsWith('f') || stem.endsWith('x') || stem.endsWith('ce')) {{
        badge.textContent = '/t/';
        rule.textContent = 'Tận cùng bằng các phụ âm vô thanh (/p, k, f, s, ʃ, tʃ/) ➔ Phát âm là /t/ (Mẹo nhớ: "Khi Sang Sông Phải Chờ Phà")';
        badge.style.color = '#16a34a';
      }}
      else {{
        badge.textContent = '/d/';
        rule.textContent = 'Tận cùng bằng các âm hữu thanh còn lại và nguyên âm ➔ Phát âm là /d/.';
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
      
      playSpeech(clean);
      
      if (clean === 'houses') {{
        badge.textContent = '/ˈhaʊ.zɪz/ (TRƯỜNG HỢP ĐẶC BIỆT)';
        rule.textContent = 'Danh từ house /haʊs/ khi thêm -es biến âm thành /ˈhaʊ.zɪz/.';
        badge.style.color = '#dc2626';
        return;
      }}
      
      let stem = clean;
      if (stem.endsWith('es')) stem = stem.slice(0, -2);
      else if (stem.endsWith('s')) stem = stem.slice(0, -1);
      
      if (stem.endsWith('s') || stem.endsWith('ss') || stem.endsWith('ch') || stem.endsWith('sh') || 
          stem.endsWith('x') || stem.endsWith('z') || stem.endsWith('ge') || stem.endsWith('ce') || stem.endsWith('se')) {{
        badge.textContent = '/ɪz/';
        rule.textContent = 'Tận cùng bằng âm xuýt/âm gió (/s, z, ʃ, ʒ, tʃ, dʒ/) ➔ Phát âm là /ɪz/ (Mẹo nhớ: "Sáu Chạy Xe SH Zui Zẻ")';
        badge.style.color = '#2563eb';
      }}
      else if (stem.endsWith('p') || stem.endsWith('k') || stem.endsWith('f') || stem.endsWith('ph') || 
               stem.endsWith('gh') || stem.endsWith('t') || stem.endsWith('th')) {{
        badge.textContent = '/s/';
        rule.textContent = 'Tận cùng bằng phụ âm vô thanh (/p, k, f, θ, t/) ➔ Phát âm là /s/ (Mẹo nhớ: "Thời Phong Kiến Phương Tây")';
        badge.style.color = '#16a34a';
      }}
      else {{
        badge.textContent = '/z/';
        rule.textContent = 'Tận cùng bằng các âm hữu thanh còn lại và nguyên âm ➔ Phát âm là /z/.';
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
    // 6. INTERACTIVE GRAMMAR TIMELINE
    // ==============================================================================
    const TENSE_DATA = {{
      past_simple: {{
        name: 'Quá khứ đơn (Past Simple)',
        feynman: 'Diễn tả hành động đã kết thúc hoàn toàn trong quá khứ, có thời gian xác định cụ thể.',
        formula: 'S + V2/ed (Khẳng định) | S + did not + V-inf (Phủ định) | Did + S + V-inf? (Nghi vấn)',
        signals: 'yesterday, ago, last (night/week/year), in 2020, when I was young.',
        trap: 'Lưu ý: Khi câu có trạng từ thời gian quá khứ cụ thể, dùng Quá khứ đơn, không dùng Hiện tại hoàn thành.'
      }},
      past_cont: {{
        name: 'Quá khứ tiếp diễn (Past Continuous)',
        feynman: 'Diễn tả hành động đang diễn ra tại một thời điểm cụ thể trong quá khứ, hoặc đang diễn ra thì có hành động khác xen vào.',
        formula: 'S + was/were + V-ing',
        signals: 'at 8 p.m last night, at this time yesterday, while, when + S + V2/ed.',
        trap: 'Quy tắc kết hợp: Hành động đang diễn ra dùng was/were + V-ing; hành động xen vào dùng V2/ed.'
      }},
      past_perf: {{
        name: 'Quá khứ hoàn thành (Past Perfect)',
        feynman: 'Diễn tả hành động xảy ra và hoàn tất trước một hành động khác trong quá khứ.',
        formula: 'S + had + V3/ed',
        signals: 'by the time, before, after, as soon as.',
        trap: 'Quy tắc trước - sau: After + Had V3/ed, V2/ed | Before + V2/ed, Had V3/ed.'
      }},
      pres_simple: {{
        name: 'Hiện tại đơn (Present Simple)',
        feynman: 'Diễn đạt chân lý, sự thật hiển nhiên, thói quen lặp đi lặp lại hoặc lịch trình cố định.',
        formula: 'S + V(s/es) | S + do/does not + V-inf',
        signals: 'always, usually, often, sometimes, never, every day/week, once a month.',
        trap: 'Lịch trình tàu xe, máy bay cố định trong tương lai vẫn dùng Hiện tại đơn (The train leaves at 7 a.m tomorrow).'
      }},
      pres_cont: {{
        name: 'Hiện tại tiếp diễn (Present Continuous)',
        feynman: 'Diễn tả hành động đang xảy ra ngay lúc nói, hoặc phàn nàn về một thói quen xấu (đi kèm always).',
        formula: 'S + am/is/are + V-ing',
        signals: 'now, right now, at the moment, at present, Look!, Listen!, Be quiet!.',
        trap: 'Lưu ý: Không dùng với các động từ chỉ nhận thức, tri giác hoặc sở hữu (know, understand, have, like, love).'
      }},
      pres_perf: {{
        name: 'Hiện tại hoàn thành (Present Perfect - Trọng tâm)',
        feynman: 'Diễn tả hành động bắt đầu trong quá khứ, kéo dài đến hiện tại và có thể tiếp diễn trong tương lai.',
        formula: 'S + have/has + V3/ed',
        signals: 'since (mốc thời gian), for (khoảng thời gian), already, yet, just, ever, never, recently, so far.',
        trap: 'Mẫu chuyển đổi câu thường gặp: started + V-ing ... ago ➔ have/has + V3/ed for ...'
      }},
      fut_simple: {{
        name: 'Tương lai đơn (Future Simple)',
        feynman: 'Diễn tả quyết định tức thời tại thời điểm nói, lời hứa, đề nghị hoặc dự đoán không có căn cứ.',
        formula: 'S + will + V-inf',
        signals: 'tomorrow, next week, in the future, think, hope, promise.',
        trap: 'Trong mệnh đề trạng ngữ chỉ thời gian (sau when, as soon as, before), dùng Hiện tại đơn thay cho will.'
      }},
      near_fut: {{
        name: 'Tương lai gần (Be going to)',
        feynman: 'Diễn tả kế hoạch, dự định đã sắp xếp từ trước hoặc dự đoán có bằng chứng, căn cứ cụ thể ở hiện tại.',
        formula: 'S + am/is/are + going to + V-inf',
        signals: 'Look at those dark clouds!, plan, intend to.',
        trap: 'Phân biệt: Khi có dấu hiệu trực tiếp trước mắt (như mây đen kéo đến), dùng is going to thay vì will.'
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
          <h4 style="font-size: 1.25rem; color: var(--primary); margin-bottom: 8px;">${{data.name}}</h4>
          <p style="font-size: 0.98rem; margin-bottom: 12px; color: var(--text-main);"><strong>Bản chất và ngữ cảnh sử dụng:</strong> ${{data.feynman}}</p>
          <div style="background: var(--bg-surface); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: var(--radius-sm); margin-bottom: 10px;">
            <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-soft); display: block; margin-bottom: 4px;">CẤU TRÚC:</span>
            <code style="font-family: var(--font-mono); font-weight: 700; color: var(--primary); font-size: 1.05rem;">${{data.formula}}</code>
          </div>
          <div style="margin-bottom: 8px; font-size: 0.92rem; color: var(--text-muted);">
            <strong>📌 Dấu hiệu nhận biết:</strong> <span style="color: var(--accent-teal); font-weight: 600;">${{data.signals}}</span>
          </div>
          <div style="font-size: 0.92rem; color: #dc2626; font-weight: 600; padding: 6px 10px; background: rgba(220, 38, 38, 0.08); border-radius: var(--radius-sm);">
            ${{data.trap}}
          </div>
        `;
      }}
    }}

    // ==============================================================================
    // 7. AUDIO SPEECH SYNTHESIS (100% OFFLINE)
    // ==============================================================================
    function playSpeech(word) {{
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      const clean = (word || '').replace(/[^a-zA-Z\\s]/g, '').trim();
      if (!clean) return;
      
      const utter = new SpeechSynthesisUtterance(clean);
      utter.lang = 'en-US';
      utter.rate = 0.9;
      
      const voices = window.speechSynthesis.getVoices();
      const enVoice = voices.find(v => v.lang.startsWith('en'));
      if (enVoice) utter.voice = enVoice;
      
      window.speechSynthesis.speak(utter);
    }}

    // ==============================================================================
    // 8. REAL-TIME SEARCH & SCROLLSPY
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

    document.addEventListener('click', (e) => {{
      const searchBox = document.querySelector('.header-center');
      const dropdown = document.getElementById('search_dropdown');
      if (searchBox && !searchBox.contains(e.target) && dropdown) {{
        dropdown.style.display = 'none';
      }}
    }});

    document.addEventListener('keydown', (e) => {{
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
        e.preventDefault();
        const searchInput = document.getElementById('global_search');
        searchInput?.focus();
      }}
    }});

    function initScrollSpy() {{
      const sections = document.querySelectorAll('.module-card-section');
      const navItems = document.querySelectorAll('.toc-item');
      
      window.addEventListener('scroll', () => {{
        let current = '';
        const scrollY = window.pageYOffset + 140;
        
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
    // EXAM HUB & ARENA CLIENT ENGINE
    // ==============================================================================
    function formatExamPrompt(txt) {{
      if (!txt) return '';
      return String(txt).split(String.fromCharCode(10)).join('<br>');
    }}

    let currentExamSession = {{
      exam: null,
      mode: 'practice', // 'practice' | 'exam'
      answers: {{}},      // qid -> selected key (A/B/C/D)
      textAnswers: {{}},  // qid -> string
      flagged: new Set(),
      secondsElapsed: 0,
      secondsTotal: 3600,
      timerId: null,
      isSubmitted: false
    }};

    const EXAM_STORAGE_KEY = 'AnhVan10_Exam_Records_v1';

    function getExamRecords() {{
      try {{
        const raw = localStorage.getItem(EXAM_STORAGE_KEY);
        return raw ? JSON.parse(raw) : {{}};
      }} catch(e) {{
        return {{}};
      }}
    }}

    function saveExamRecord(examId, record) {{
      try {{
        const data = getExamRecords();
        if (!data[examId] || record.score > (data[examId].score || 0)) {{
          data[examId] = record;
          localStorage.setItem(EXAM_STORAGE_KEY, JSON.stringify(data));
        }}
      }} catch(e) {{}}
    }}

    function initExamHub() {{
      renderExamCards('all');
    }}

    function filterExams(category) {{
      document.querySelectorAll('.exam-filter-btn').forEach(b => {{
        b.classList.toggle('active', b.getAttribute('data-filter') === category);
      }});
      renderExamCards(category);
    }}

    function renderExamCards(category) {{
      const container = document.getElementById('examCardsGrid');
      if (!container || !window.GLOBAL_EXAMS_DATABASE) return;

      const records = getExamRecords();
      let exams = window.GLOBAL_EXAMS_DATABASE;

      if (category === 'quangngai') {{
        exams = exams.filter(e => e.region === 'Quảng Ngãi');
      }} else if (category === 'danang') {{
        exams = exams.filter(e => e.region === 'Đà Nẵng');
      }} else if (category === 'semester') {{
        exams = exams.filter(e => e.category === 'semester');
      }} else if (category === 'practice') {{
        exams = exams.filter(e => e.category === 'practice');
      }}

      let html = '';
      exams.forEach(ex => {{
        const best = records[ex.id];
        const bestScoreHtml = best 
          ? `<div class="card-best-score-row">
               <span>Điểm thi cao nhất:</span>
               <span class="best-score-badge">⭐ ${{best.score.toFixed(1)}}/10.0</span>
             </div>`
          : `<div class="card-best-score-row">
               <span>Trạng thái:</span>
               <span style="color:var(--text-muted);">Chưa thi thử</span>
             </div>`;

        html += `
        <div class="exam-card-item">
          <div>
            <div class="card-top-badges">
              <span class="card-badge ${{ex.badgeClass || 'badge-official'}}">${{ex.badge || 'Thi Tuyển Sinh'}}</span>
              <span class="card-year-tag">${{ex.year || ''}}</span>
            </div>
            <h3 class="card-exam-title">${{ex.title}}</h3>
            <p class="card-exam-subtitle">${{ex.subtitle || ex.description}}</p>
            <div class="card-meta-chips">
              <span class="card-chip">⏱️ ${{ex.durationMinutes}} phút</span>
              <span class="card-chip">❓ ${{ex.totalQuestions}} câu hỏi</span>
              <span class="card-chip">💯 Thang điểm 10</span>
              <span class="card-chip">📍 ${{ex.region}}</span>
            </div>
          </div>
          <div>
            ${{bestScoreHtml}}
            <div class="card-action-buttons">
              <button type="button" class="card-btn practice" onclick="startExam('${{ex.id}}', 'practice')">
                🎯 Luyện Từng Câu
              </button>
              <button type="button" class="card-btn exam" onclick="startExam('${{ex.id}}', 'exam')">
                ⏱️ Phòng Thi Thử
              </button>
            </div>
          </div>
        </div>
        `;
      }});

      container.innerHTML = html;
    }}

    function startExam(examId, mode) {{
      const exam = (window.GLOBAL_EXAMS_DATABASE || []).find(e => e.id === examId);
      if (!exam) return;

      currentExamSession = {{
        exam: exam,
        mode: mode,
        answers: {{}},
        textAnswers: {{}},
        flagged: new Set(),
        secondsElapsed: 0,
        secondsTotal: (exam.durationMinutes || 60) * 60,
        timerId: null,
        isSubmitted: false
      }};

      // Switch views
      document.getElementById('examCardsGrid').style.display = 'none';
      document.getElementById('examFiltersBar').style.display = 'none';
      document.getElementById('examPlayerWrapper').style.display = 'block';

      // Header Meta
      document.getElementById('playerExamTitle').textContent = exam.title;
      document.getElementById('playerModePill').textContent = (mode === 'practice') ? '🎯 Chế Độ: Luyện Tập Từng Câu' : '⏱️ Chế Độ: Phòng Thi Bấm Giờ';
      document.getElementById('playerModePill').style.background = (mode === 'practice') ? '#eff6ff' : '#fef2f2';
      document.getElementById('playerModePill').style.color = (mode === 'practice') ? '#2563eb' : '#dc2626';
      document.getElementById('playerDurationPill').textContent = `⏱️ ${{exam.durationMinutes}} phút`;
      document.getElementById('playerQCountPill').textContent = `❓ ${{exam.totalQuestions}} câu`;

      // Render Questions
      renderPlayerQuestions(exam, mode);

      // Render Palette
      renderPaletteGrid(exam);

      // Start Timer
      startTimer(mode);

      // Scroll into view
      document.getElementById('examPlayerWrapper').scrollIntoView({{ behavior: 'smooth' }});
    }}

    function renderPlayerQuestions(exam, mode) {{
      const container = document.getElementById('examQuestionsInner');
      if (!container) return;

      let html = '';
      (exam.sections || []).forEach((sec, sIdx) => {{
        html += `
        <div class="exam-section-block" id="sec_${{sIdx}}">
          <div class="exam-section-header-banner">
            <h4>${{sec.sectionTitle}}</h4>
            ${{sec.sectionDesc ? `<p>${{sec.sectionDesc}}</p>` : ''}}
          </div>
        `;

        (sec.questions || []).forEach(q => {{
          const qid = q.id;
          const isFlagged = currentExamSession.flagged.has(qid);

          html += `
          <div class="exam-question-card ${{isFlagged ? 'flagged' : ''}}" id="exam_card_${{qid}}">
            <div class="exam-q-top-row">
              <div class="exam-q-num-badge">
                <span class="q-num-circle">${{q.num}}</span>
                <span>Câu ${{q.num}}</span>
              </div>
              <div class="exam-q-actions">
                <button type="button" class="q-audio-btn" onclick="speakExamPrompt('${{qid}}')" title="Phát âm câu hỏi">🔊</button>
                <button type="button" class="q-flag-btn ${{isFlagged ? 'active' : ''}}" id="flag_btn_${{qid}}" onclick="toggleFlag('${{qid}}')" title="Đánh dấu xem lại">🚩</button>
              </div>
            </div>

            <div class="exam-q-prompt-text" id="prompt_${{qid}}">
              ${{formatExamPrompt(q.text)}}
            </div>
          `;

          if (q.type === 'mcq' && q.options) {{
            html += `<div class="exam-options-grid">`;
            q.options.forEach(opt => {{
              html += `
              <div class="quiz-option-btn" role="button" tabindex="0" data-qid="${{qid}}" data-opt="${{opt.k}}" onclick="onSelectExamOpt('${{qid}}', '${{opt.k}}')">
                <span class="opt-label">${{opt.k}}</span>
                <span class="opt-text">${{opt.t}}</span>
              </div>
              `;
            }});
            html += `</div>`;
          }} else {{
            // Text or rewrite question
            html += `
            <div class="exam-text-input-wrap">
              <input type="text" class="exam-text-input" id="input_${{qid}}" placeholder="Gõ câu trả lời của em tại đây..." oninput="onInputExamText('${{qid}}', this.value)">
            </div>
            `;
          }}

          // Explanation box (hidden initially or shown in review/practice)
          html += `
            <div class="exam-exp-box" id="exp_${{qid}}" style="display: none;">
              <strong>💡 Lời Giải Chi Tiết:</strong> ${{q.explanation || ''}}
              ${{q.correct ? `<br><strong>Đáp án chuẩn:</strong> <span style="color:var(--success);font-weight:700;">${{q.correct}}</span>` : ''}}
            </div>
          </div>
          `;
        }});

        html += `</div>`;
      }});

      container.innerHTML = html;
    }}

    function renderPaletteGrid(exam) {{
      const grid = document.getElementById('paletteGrid');
      if (!grid) return;

      let html = '';
      let qIndex = 1;
      (exam.sections || []).forEach(sec => {{
        (sec.questions || []).forEach(q => {{
          html += `
          <button type="button" class="palette-btn" id="pal_btn_${{q.id}}" onclick="jumpToExamQuestion('${{q.id}}')">
            ${{q.num}}
          </button>
          `;
        }});
      }});

      grid.innerHTML = html;
      updatePaletteStats();
    }}

    function jumpToExamQuestion(qid) {{
      const el = document.getElementById('exam_card_' + qid);
      if (el) {{
        el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        el.style.boxShadow = '0 0 0 3px rgba(37, 99, 235, 0.4)';
        setTimeout(() => {{
          el.style.boxShadow = '';
        }}, 1200);
      }}
    }}

    function onSelectExamOpt(qid, optKey) {{
      if (currentExamSession.isSubmitted) return;

      currentExamSession.answers[qid] = optKey;

      // Update card option selected
      const card = document.getElementById('exam_card_' + qid);
      if (card) {{
        card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
          btn.classList.toggle('selected', btn.getAttribute('data-opt') === optKey);
        }});
      }}

      // Update palette button
      const palBtn = document.getElementById('pal_btn_' + qid);
      if (palBtn) {{
        palBtn.classList.add('answered');
      }}

      // If Practice Mode: Instant feedback
      if (currentExamSession.mode === 'practice') {{
        const question = findQuestionById(qid);
        if (question) {{
          const isCorrect = (optKey.trim().toUpperCase() === (question.correct || '').trim().toUpperCase());
          card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
            const k = btn.getAttribute('data-opt');
            if (k === question.correct) btn.classList.add('correct');
            else if (k === optKey) btn.classList.add('incorrect');
          }});

          // Play Sound
          if (typeof playSoundEffect === 'function') {{
            playSoundEffect(isCorrect ? 'correct' : 'incorrect');
          }}

          // Show explanation
          const expBox = document.getElementById('exp_' + qid);
          if (expBox) {{
            expBox.style.display = 'block';
            expBox.className = 'exam-exp-box ' + (isCorrect ? 'correct-box' : 'incorrect-box');
          }}
        }}
      }}

      updatePaletteStats();
    }}

    function onInputExamText(qid, val) {{
      if (currentExamSession.isSubmitted) return;
      currentExamSession.textAnswers[qid] = val;

      const palBtn = document.getElementById('pal_btn_' + qid);
      if (palBtn) {{
        if (val.trim()) {{
          palBtn.classList.add('answered');
        }} else {{
          palBtn.classList.remove('answered');
        }}
      }}
      updatePaletteStats();
    }}

    function toggleFlag(qid) {{
      const card = document.getElementById('exam_card_' + qid);
      const flagBtn = document.getElementById('flag_btn_' + qid);
      const palBtn = document.getElementById('pal_btn_' + qid);

      if (currentExamSession.flagged.has(qid)) {{
        currentExamSession.flagged.delete(qid);
        if (card) card.classList.remove('flagged');
        if (flagBtn) flagBtn.classList.remove('active');
        if (palBtn) palBtn.classList.remove('flagged');
      }} else {{
        currentExamSession.flagged.add(qid);
        if (card) card.classList.add('flagged');
        if (flagBtn) flagBtn.classList.add('active');
        if (palBtn) palBtn.classList.add('flagged');
      }}
    }}

    function updatePaletteStats() {{
      const exam = currentExamSession.exam;
      if (!exam) return;

      let answeredCount = 0;
      let totalCount = 0;

      (exam.sections || []).forEach(s => {{
        (s.questions || []).forEach(q => {{
          totalCount++;
          if (q.type === 'mcq') {{
            if (currentExamSession.answers[q.id]) answeredCount++;
          }} else {{
            if (currentExamSession.textAnswers[q.id] && currentExamSession.textAnswers[q.id].trim()) answeredCount++;
          }}
        }});
      }});

      const pct = Math.round((answeredCount / totalCount) * 100);
      const textEl = document.getElementById('paletteProgressText');
      const fillEl = document.getElementById('paletteProgressFill');
      if (textEl) textEl.textContent = `${{answeredCount}} / ${{totalCount}} (${{pct}}%)`;
      if (fillEl) fillEl.style.width = pct + '%';
    }}

    function startTimer(mode) {{
      if (currentExamSession.timerId) clearInterval(currentExamSession.timerId);

      const digitsEl = document.getElementById('timerDigits');
      const progressFill = document.getElementById('timerProgressFill');

      currentExamSession.timerId = setInterval(() => {{
        currentExamSession.secondsElapsed++;

        if (mode === 'exam') {{
          const remain = currentExamSession.secondsTotal - currentExamSession.secondsElapsed;
          if (remain <= 0) {{
            clearInterval(currentExamSession.timerId);
            alert('⏱️ ĐÃ HẾT GIỜ LÀM BÀI! Hệ thống sẽ tự động nộp bài thi của bạn.');
            submitExamFinal();
            return;
          }}

          const mins = Math.floor(remain / 60);
          const secs = remain % 60;
          if (digitsEl) {{
            digitsEl.textContent = `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
            if (remain <= 300) {{
              digitsEl.className = 'timer-digits danger';
            }} else if (remain <= 600) {{
              digitsEl.className = 'timer-digits warning';
            }} else {{
              digitsEl.className = 'timer-digits';
            }}
          }}

          if (progressFill) {{
            const p = (remain / currentExamSession.secondsTotal) * 100;
            progressFill.style.width = p + '%';
          }}
        }} else {{
          // Practice mode: count up
          const mins = Math.floor(currentExamSession.secondsElapsed / 60);
          const secs = currentExamSession.secondsElapsed % 60;
          if (digitsEl) {{
            digitsEl.textContent = `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
          }}
        }}
      }}, 1000);
    }}

    function confirmSubmitExam() {{
      const exam = currentExamSession.exam;
      if (!exam) return;

      let answeredCount = 0;
      let totalCount = 0;
      (exam.sections || []).forEach(s => {{
        (s.questions || []).forEach(q => {{
          totalCount++;
          if (q.type === 'mcq') {{
            if (currentExamSession.answers[q.id]) answeredCount++;
          }} else {{
            if (currentExamSession.textAnswers[q.id] && currentExamSession.textAnswers[q.id].trim()) answeredCount++;
          }}
        }});
      }});

      const remainCount = totalCount - answeredCount;
      let msg = "Em đã làm được " + answeredCount + "/" + totalCount + " câu hỏi.";
      if (remainCount > 0) {{
        msg += String.fromCharCode(10) + "⚠️ Còn " + remainCount + " câu chưa trả lời! Em có chắc chắn muốn nộp bài ngay không?";
      }} else {{
        msg += String.fromCharCode(10) + "🎉 Em đã hoàn thành tất cả câu hỏi! Em có muốn nộp bài để xem điểm số không?";
      }}

      if (confirm(msg)) {{
        submitExamFinal();
      }}
    }}

    function submitExamFinal() {{
      if (currentExamSession.timerId) clearInterval(currentExamSession.timerId);
      currentExamSession.isSubmitted = true;

      const exam = currentExamSession.exam;
      let totalQuestions = 0;
      let correctCount = 0;

      // Kỹ năng
      const skills = {{
        phonetics: {{ total: 0, correct: 0 }},
        grammar_vocab: {{ total: 0, correct: 0 }},
        reading: {{ total: 0, correct: 0 }},
        writing: {{ total: 0, correct: 0 }}
      }};

      (exam.sections || []).forEach(sec => {{
        (sec.questions || []).forEach(q => {{
          totalQuestions++;
          const skillKey = q.skill || 'grammar_vocab';
          if (!skills[skillKey]) skills[skillKey] = {{ total: 0, correct: 0 }};
          skills[skillKey].total++;

          let isCorrect = false;
          if (q.type === 'mcq') {{
            const ans = currentExamSession.answers[q.id];
            if (ans && ans.trim().toUpperCase() === (q.correct || '').trim().toUpperCase()) {{
              correctCount++;
              skills[skillKey].correct++;
              isCorrect = true;
            }}
          }} else {{
            const userTxt = (currentExamSession.textAnswers[q.id] || '').trim().toLowerCase();
            const correctTxt = (q.correct || '').trim().toLowerCase();
            // Basic matching or give credit if contains main keywords
            if (userTxt && correctTxt.includes(userTxt) && userTxt.length > 3) {{
              correctCount++;
              skills[skillKey].correct++;
              isCorrect = true;
            }}
          }}

          // Mark palette button
          const palBtn = document.getElementById('pal_btn_' + q.id);
          if (palBtn) {{
            palBtn.className = 'palette-btn ' + (isCorrect ? 'review-correct' : 'review-incorrect');
          }}
        }});
      }});

      // Calculate Scores
      const scoreTen = Math.round((correctCount / totalQuestions) * 10 * 10) / 10;
      const accuracyPct = Math.round((correctCount / totalQuestions) * 100);

      // Save to LocalStorage
      saveExamRecord(exam.id, {{
        score: scoreTen,
        accuracy: accuracyPct,
        date: new Date().toISOString()
      }});

      // Show Score Modal
      showScoreModal(scoreTen, correctCount, totalQuestions, accuracyPct, skills);
    }}

    function showScoreModal(scoreTen, correctCount, totalCount, accuracyPct, skills) {{
      const modal = document.getElementById('examScoreModal');
      if (!modal) return;

      document.getElementById('scoreTotalTen').textContent = scoreTen.toFixed(1);
      document.getElementById('scoreCorrectCount').textContent = `Đúng ${{correctCount}} / ${{totalCount}} câu`;
      document.getElementById('scoreAccuracyPercent').textContent = accuracyPct + '%';

      let rank = 'Trung Bình';
      let trophy = '🥉';
      if (scoreTen >= 9.0) {{ rank = 'Xuất Sắc'; trophy = '🏆'; }}
      else if (scoreTen >= 8.0) {{ rank = 'Giỏi'; trophy = '🥇'; }}
      else if (scoreTen >= 6.5) {{ rank = 'Khá'; trophy = '🥈'; }}
      document.getElementById('scoreGradeRank').textContent = 'Xếp loại: ' + rank;
      document.getElementById('scoreTrophyIcon').textContent = trophy;

      // Time taken
      const mins = Math.floor(currentExamSession.secondsElapsed / 60);
      const secs = currentExamSession.secondsElapsed % 60;
      document.getElementById('scoreTimeTaken').textContent = `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;

      // Skills Bar
      const calcPct = (s) => (s && s.total > 0) ? Math.round((s.correct / s.total) * 100) : 100;
      const phPct = calcPct(skills.phonetics);
      const grPct = calcPct(skills.grammar_vocab);
      const rdPct = calcPct(skills.reading);
      const wrPct = calcPct(skills.writing);

      document.getElementById('skillPhoneticsPct').textContent = phPct + '%';
      document.getElementById('skillPhoneticsFill').style.width = phPct + '%';

      document.getElementById('skillGrammarPct').textContent = grPct + '%';
      document.getElementById('skillGrammarFill').style.width = grPct + '%';

      document.getElementById('skillReadingPct').textContent = rdPct + '%';
      document.getElementById('skillReadingFill').style.width = rdPct + '%';

      document.getElementById('skillWritingPct').textContent = wrPct + '%';
      document.getElementById('skillWritingFill').style.width = wrPct + '%';

      // Advice Text
      let advice = '';
      if (scoreTen >= 9.0) {{
        advice = '🌟 Tuyệt vời! Em có phong độ xuất sắc và nắm rất chắc kiến thức trọng tâm. Hãy duy trì tốc độ và sự cẩn thận để giữ vững số điểm 10 tuyệt đối trong kỳ thi chính thức nhé!';
      }} else if (scoreTen >= 7.5) {{
        advice = '👍 Kết quả rất tốt! Em đã nắm vững ngữ âm và từ vựng cơ bản. Hãy xem lại các câu sai ở phần Biến đổi câu (Writing) và Đọc hiểu nâng cao trong cẩm nang để nâng điểm lên mức Xuất sắc nhé!';
      }} else {{
        advice = '💪 Hãy cố gắng lên nhé! Em nên mở lại Chuyên đề 01 (Phát âm -ed, -s), Chuyên đề 07 (Câu điều kiện) và Chuyên đề 09 (Câu tường thuật) trong cẩm nang để củng cố lại các nền tảng còn yếu!';
      }}
      document.getElementById('pedagogicalAdviceText').textContent = advice;

      modal.style.display = 'flex';
    }}

    function reviewExamAnswers() {{
      document.getElementById('examScoreModal').style.display = 'none';

      // Reveal all answers & explanations
      const exam = currentExamSession.exam;
      if (!exam) return;

      (exam.sections || []).forEach(sec => {{
        (sec.questions || []).forEach(q => {{
          const card = document.getElementById('exam_card_' + q.id);
          const expBox = document.getElementById('exp_' + q.id);
          if (expBox) expBox.style.display = 'block';

          if (q.type === 'mcq' && card) {{
            const userOpt = currentExamSession.answers[q.id];
            card.querySelectorAll('.quiz-option-btn').forEach(btn => {{
              const k = btn.getAttribute('data-opt');
              if (k === q.correct) {{
                btn.classList.add('correct');
              }} else if (k === userOpt) {{
                btn.classList.add('incorrect');
              }}
            }});
          }}
        }});
      }});

      // Scroll to top
      document.getElementById('examQuestionsScrollArea').scrollTop = 0;
    }}

    function retakeCurrentExam() {{
      document.getElementById('examScoreModal').style.display = 'none';
      if (currentExamSession.exam) {{
        startExam(currentExamSession.exam.id, currentExamSession.mode);
      }}
    }}

    function closeScoreModal() {{
      document.getElementById('examScoreModal').style.display = 'none';
      exitExamPlayer();
    }}

    function exitExamPlayer() {{
      if (currentExamSession.timerId) clearInterval(currentExamSession.timerId);
      document.getElementById('examPlayerWrapper').style.display = 'none';
      document.getElementById('examCardsGrid').style.display = 'grid';
      document.getElementById('examFiltersBar').style.display = 'flex';
      renderExamCards('all');
    }}

    function toggleQuestionPalette() {{
      const palette = document.getElementById('examPaletteSidebar');
      if (palette) {{
        palette.classList.toggle('mobile-open');
      }}
    }}

    function speakExamPrompt(qid) {{
      const p = document.getElementById('prompt_' + qid);
      if (p && 'speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        const text = p.innerText || p.textContent;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
      }}
    }}

    function findQuestionById(qid) {{
      if (!currentExamSession.exam) return null;
      for (const s of currentExamSession.exam.sections || []) {{
        for (const q of s.questions || []) {{
          if (q.id === qid) return q;
        }}
      }}
      return null;
    }}
    

    // ==============================================================================
    // 9. INITIALIZATION
    // ==============================================================================
    window.addEventListener('DOMContentLoaded', () => {{
      loadSavedState();
      applyTheme(appState.theme || 'light');
      setGlobalMode(appState.globalMode || 'practice');
      soundEnabled = (appState.soundEnabled !== false);
      const sBtn = document.getElementById('sound_toggle_btn');
      if (sBtn) {{
        sBtn.innerHTML = soundEnabled ? '🔊 <span class="btn-text-label">Âm thanh: Bật</span>' : '🔇 <span class="btn-text-label">Âm thanh: Tắt</span>';
      }}
      
      selectTimelineTense('pres_perf');
      initScrollSpy();
      initMermaidInteractions();
      if (typeof initExamHub === 'function') initExamHub();
      
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
      updateTocBadges();
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
