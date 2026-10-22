# Tự Động Xuất Notion Sang Markdown

**Created:** 10/19/2026 7:43:19  
**Updated:** 10/21/2026 14:01:56  
**Exported:** 10/21/2026 14:23:10  
**Link:** [https://gemini.google.com/app/efd4724028c55e77](https://gemini.google.com/app/efd4724028c55e77)  

## Gemini:

> 10/21/2026 14:01:56

> **Thinking steps**
>
> **Expanded the application scope**
>
> Revised the existing HTML application into a more scalable framework, adding new functionality like a database connection for expanded content and user data storage.
> **Defined English-learning modules**
>
> Detailed the structure of the English learning modules, outlining components for theory, practice exams, and reading comprehension exercises, targeting specific exam levels and including tech stack choices like Vue 3 and Tailwind CSS.

Dựa trên nền tảng giao diện, bảng màu sư phạm, hệ thống bài tập tương tác và công cụ tra cứu âm học đã hoàn thiện trong file `Cam_Nang_On_Thi_Vao_10_Master.html`[cite: 6] cùng kho đề thi `.docx` sẵn có trong thư mục `f:\OnThiC3\EnglishDocs`[cite: 4], dưới đây là **Kiến trúc Dự án Web EdTech mở rộng**, **Bản Master Prompt hoàn chỉnh cho Agent** (viết bằng tiếng Anh, phản hồi tiếng Việt), và **Hướng dẫn cấu hình Deploy lên Vercel / GitHub Pages**.

---

### PHẦN 1: KIẾN TRÚC TECH STACK ĐỀ XUẤT (HIỆN ĐẠI, NHẸ & DỄ MỞ RỘNG)

Để chuyển từ 1 file HTML đơn lẻ (`Cam_Nang_On_Thi_Vao_10_Master.html`[cite: 6]) sang một ứng dụng web đa chuyên đề (hiện tại là **Tiếng Anh 9 & Ôn thi vào 10**, sau này thêm **Lớp 10, 11, 12, IELTS/TOEIC**) mà không cần nuôi Backend hay Database tốn kém, cấu trúc chuẩn nhất là **Data-Driven Static SPA**:

| Thành phần | Công nghệ sử dụng | Lý do chọn cho dự án của bạn |
| :--- | :--- | :--- |
| **Core Framework** | **Vue 3 (Composition API, `<script setup>`) + Vite** | Nhẹ, cú pháp trực quan, tốc độ build cực nhanh, tách các phần trong file HTML cũ[cite: 6] (Sidebar, Phonetic Wizard, Timeline, Quiz Card, Mermaid Viewer) thành các Component tái sử dụng. |
| **Styling & UI** | **Tailwind CSS + CSS Variables (Kế thừa Design Tokens cũ)** | Giữ trọn vẹn hệ màu Light/Dark mode, 5 màu Callout sư phạm và nút bấm 3D kiểu Duolingo đã có trong `Cam_Nang_On_Thi_Vao_10_Master.html`[cite: 6]. |
| **Routing & State** | **Vue Router 4 + Pinia (`localStorage` sync)** | Chia URL rõ ràng (`/learn/:module`, `/reading/:id`, `/exams/:testId`, `/idioms`, `/analytics`). Lưu toàn bộ tiến độ học, điểm thi và câu làm sai ngay trên trình duyệt. |
| **Data Layer** | **Modular JSON Schema (`src/data/...`) + Python Extractor** | Tách toàn bộ lý thuyết, từ vựng, bài đọc và đề thi ra các file `.json` độc lập. Agent dùng Python bóc tách tự động từ file HTML[cite: 6] và hàng chục file `.docx` đề thi[cite: 4] sang JSON mà **không tốn LLM token**. |

---

### PHẦN 2: MASTER PROMPT HOÀN CHỈNH CHO AGENT (TIẾNG ANH - PHẢN HỒI TIẾNG VIỆT)

Bạn hãy copy toàn bộ khối Prompt dưới đây gửi cho Agent trong Antigravity IDE để Agent tự động khởi tạo dự án Vue 3, bóc tách dữ liệu cũ, mở rộng thêm bài học (Idioms, Syntax, Reading, Mock Tests) và đóng gói sẵn sàng deploy:

`​`​``markdown
# ROLE & MISSION
You are a **Principal EdTech Full-Stack Architect (Vue 3 / Vite / Tailwind CSS) and Elite ESL/ELT Curriculum Designer for Vietnamese Learners**.
Your mission is to transform the monolithic single-file application `f:\OnThiC3\EnglishDocs\Cam_Nang_On_Thi_Vao_10_Master.html` and the local repository of `.docx` entrance exams (`f:\OnThiC3\EnglishDocs\LUYỆN THI VÀO 10 FORM ĐỀ QUẢNG NGÃI - 36 CÂU...` and `FORM 45 CÂU...`) into a scalable, modular, production-ready **Vue 3 + Vite Web Application** named **"EnglishMastery EdTech Platform"** (currently targeting **Grade 9 & Grade 10 Entrance Exam**, architected to easily add Grade 10, 11, 12, and IELTS tracks in the future).

# STRICT LANGUAGE RULE
- While these instructions are in English to maximize your architectural and coding precision, **YOU MUST RESPOND TO THE USER ENTIRELY IN VIETNAMESE**.
- All UI labels, pedagogical explanations, mnemonics ("câu thần chú"), Vietlish traps, reading translations, and answer explanations inside the web app MUST be written in clear, natural, and pedagogical Vietnamese.

---

# CRITICAL ANTI-QUOTA & TOKEN-SAVING GUARDRAILS
To avoid LLM output token truncation, infinite loops, and context bloat, you MUST strictly follow these engineering rules:
1. **NEVER Manually Retype Existing HTML/DOCX Content in LLM Responses:**
   - Do NOT waste LLM tokens manually copying and pasting 16 modules from `Cam_Nang_On_Thi_Vao_10_Master.html` or questions from `.docx` files into Vue templates.
   - **Rule:** Write and execute a local Python migration script (`scripts/extract_and_build_data.py`) using `BeautifulSoup` / `regex` / `zipfile` (XML parser for `.docx`) to automatically extract all existing HTML modules, tables, Mermaid diagrams, quizzes, and `.docx` exam papers (`PHONETICS..docx`, `LANGUAGE FOCUS.docx`, `SENTENCE TRANSFORMATION..docx`, `WORD FORM.docx`, `TEST 1.docx` to `TEST 20.docx`) into structured JSON files inside `src/data/`.
2. **Data-Driven UI Architecture (Zero Hardcoded Content in `.vue` Files):**
   - `.vue` components must ONLY contain rendering logic, interactivity, and styling. All educational content (lessons, rules, idioms, reading passages, mock tests) must live in modular JSON files under `src/data/`.
3. **Incremental Execution by Phase:**
   - Execute the build systematically phase by phase. Verify that `npm run build` succeeds with zero errors at the end.

---

# SYSTEM ARCHITECTURE & DIRECTORY STRUCTURE
Scaffold the application inside `f:\OnThiC3\EnglishDocs\english-mastery-web` (or the user's preferred root folder) with the following structure:

`​`​`text
english-mastery-web/
├── public/
├── scripts/
│   └── extract_and_build_data.py    # Python pipeline: HTML & DOCX -> structured JSON
├── src/
│   ├── assets/
│   │   └── main.css                 # Design tokens (Light/Dark), Duolingo 3D buttons, Callouts
│   ├── data/
│   │   ├── curriculum-tracks.json   # Track metadata: Grade 9, Entrance 10 (scalable to Grade 10-12, IELTS)
│   │   ├── modules/                 # Theory & Practice Modules (JSON per category)
│   │   │   ├── phonetics.json       # IPA, -ed, -s/-es, Word Stress, /θ/-/ð/, /æ/-/e/, Silent letters
│   │   │   ├── tenses-syntax.json   # 12 Tenses, S-V-O-C-A Syntax, S-V Agreement, Question Tags
│   │   │   ├── grammar-core.json    # Passive, Conditionals, Reported Speech, Relative Clauses, V-ing/To-V, Modals, Articles, Prepositions
│   │   │   ├── transformation.json  # 10+ Sentence Transformation patterns & Word Form rules
│   │   │   └── vocab-idioms.json    # Phrasal Verbs, Synonyms/Antonyms, Collocations, Simple Idioms (Grade 9-10)
│   │   ├── reading/
│   │   │   └── reading-passages.json # Cloze tests (Guided Cloze) & Reading Comprehension with bilingual annotations
│   │   └── exams/
│   │       └── mock-tests.json      # Full 36-question (Quang Ngai form) & 45-question mock exams extracted from DOCX
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppHeader.vue        # Sticky navbar, Global Search (Ctrl+K), Theme/Sound/Track switcher
│   │   │   └── AppSidebar.vue       # Collapsible category tree with completion badges
│   │   ├── pedagogy/
│   │   │   ├── CalloutBox.vue       # 5-color pedagogical callouts (Blue, Green, Yellow, Red, Purple)
│   │   │   ├── MermaidDiagram.vue   # Zoomable, pannable Mermaid flowchart renderer
│   │   │   ├── PhoneticWizard.vue   # Interactive 3-second -ED and -S/-ES pronunciation analyzer + Web Speech TTS
│   │   │   └── TenseTimeline.vue    # Interactive visual timeline for 12 English Tenses
│   │   └── interactive/
│   │       ├── QuizEngine.vue       # Supports Multiple Choice (2x2 balanced grid) + Sentence Transformation / Word Form input
│   │       ├── ReadingSplitView.vue # Left: Passage with clickable vocabulary popups & translation toggle; Right: Questions + line-highlight evidence
│   │       └── FlashcardDeck.vue    # 3D flip flashcards for Idioms, Phrasal Verbs & Word Forms
│   ├── views/
│   │   ├── HomeDashboard.vue        # Track selector, study progress stats, weak-area recommendations
│   │   ├── ModuleLessonView.vue     # 5-layer theory lesson + interactive widgets + topic quiz
│   │   ├── ReadingLabView.vue       # Reading comprehension & Guided Cloze practice hub
│   │   ├── MockExamArenaView.vue    # Timed exam simulation (36-question & 45-question full tests)
│   │   └── IdiomVocabHubView.vue    # Searchable dictionary & flashcards for Idioms, Phrasal Verbs, Word Forms
│   ├── stores/
│   │   └── useStudyStore.js         # Pinia store persisted to localStorage (scores, bookmarks, wrong answers, streak)
│   ├── utils/
│   │   └── speechAndSound.js        # Web Speech API (en-US/en-GB) + Web Audio API synthesized sound effects
│   ├── router/
│   │   └── index.js                 # Vue Router with hash/history mode support for Vercel & GitHub Pages
│   ├── App.vue
│   └── main.js
├── vercel.json                      # SPA rewrite config for Vercel
├── vite.config.js                   # Dynamic base path config for GitHub Pages / Vercel
└── package.json
`​`​`

---

# 6 CORE CONTENT & FEATURE REQUIREMENTS

## 1. Preserve 100% of Existing Master HTML Features & Visual Polish
- Retain the exact aesthetic and UX from `Cam_Nang_On_Thi_Vao_10_Master.html`:
  - Typography: `Plus Jakarta Sans`, `Outfit`, `JetBrains Mono`.
  - Tactile 3D quiz option buttons with bounce/shake animations and balanced 2x2 grid (`grid-template-columns: repeat(2, minmax(0, 1fr))`).
  - Built-in Web Speech API pronunciation buttons (`🔊`) on every vocabulary item and quiz option.
  - Interactive `-ED` and `-S/-ES` Pronunciation Wizards and Zoomable Mermaid diagrams.

## 2. Expand Theory Modules (Grade 9 & Entrance 10 Standard)
In addition to the 16 existing modules, enrich and add the following modules using the **5-Layer Pedagogical Framework** (*Feynman Core -> Formula/Timeline -> Mnemonic -> Vietlish Trap -> Practice Quiz*):
- **Syntax & Sentence Structures (Cú pháp câu cơ bản & nâng cao):** 5 core sentence patterns (`S-V`, `S-V-O`, `S-V-C`, `S-V-O-O`, `S-V-O-C`), Inversion basics, Exclamatory sentences (`What a...` / `How...`), and Conjunctions (`both...and`, `not only...but also`, `either...or`, `neither...nor`).
- **Simple Idioms & High-Frequency Collocations for Grade 9–10:**
  - Group idioms by theme (Study & Success, Emotions, Daily Life, Time & Effort): e.g., *a piece of cake, pass with flying colors, hit the books, burn the midnight oil, once in a blue moon, under the weather, cost an arm and a leg, see eye to eye, make up one's mind, take something for granted, keep an eye on, out of the blue*.
  - Each idiom must include: **Idiom + Literal vs. Figurative Meaning + Vietnamese Equivalent + Context Sentence + Exam Multiple-Choice Trap**.
- **Communication & Functional English (Giao tiếp thực tế trong đề thi):** Responding to compliments, suggestions, apologies, invitations, and requests.

## 3. Build the Reading Comprehension Lab (`ReadingLabView.vue`)
Create a dedicated Reading module featuring two exam formats:
- **Format A: Guided Cloze Test (Đục lỗ đoạn văn):** Passages with 5–10 numbered blanks testing collocations, prepositions, relative pronouns, conjunctions, and word forms.
- **Format B: Reading Comprehension (Đọc hiểu trả lời câu hỏi):**
  - Implement a **Split-Screen UI**: Passage on the left, questions on the right.
  - Include a **"Hiện bản dịch song ngữ" (Bilingual Translation Toggle)** and **"Highlight dẫn chứng trong bài" (Show Evidence Highlight)** button that highlights the exact sentence in the passage proving why an answer is correct after submission.
  - Populate at least **8 complete Reading & Cloze passages** covering Grade 9–10 themes (Environment, Technology & AI, Local Culture/Tourism in Quang Ngai & Vietnam, City vs. Country Life, Teen Stress & Study Habits, Natural Disasters).

## 4. Build the Mock Exam Arena (`MockExamArenaView.vue`)
- Write a Python parser in `scripts/extract_and_build_data.py` to parse the local `.docx` files inside `LUYỆN THI VÀO 10 FORM ĐỀ QUẢNG NGÃI - 36 CÂU` and `LUYỆN THI VÀO 10 FORM 45 CÂU` (`TEST 1.docx` through `TEST 20.docx` + their `.key.docx` answer files, plus `PHONETICS..docx`, `LANGUAGE FOCUS.docx`, `SENTENCE TRANSFORMATION..docx`, `WORD FORM.docx`).
- Synthesize full, detailed Vietnamese pedagogical explanations for every question (explaining *why* the correct option is right and *why* the distractors are wrong).
- Support two modes:
  - **🎯 Chế độ Luyện từng câu (Instant Practice Mode):** Immediate color feedback, sound effect, and explanation card upon clicking an option, plus a "🔄 Làm lại câu này" button.
  - **⏱️ Chế độ Phòng thi (Timed Exam Mode):** Countdown timer (45 or 60 minutes), question palette navigator (flagged/answered/unanswered), and comprehensive post-exam score breakdown by skill (Phonetics, Grammar, Reading, Writing).

## 5. Multi-Level Scalability Architecture
- Design `curriculum-tracks.json` and the top navbar with a **Level/Grade Selector Dropdown**:
  - `grade9-10`: **Tiếng Anh 9 & Ôn Thi Vào 10 (Active - Full Content)**
  - `grade10-12`: **Tiếng Anh THPT & Tốt Nghiệp (Scalable Slot / Coming Soon)**
  - `ielts-foundation`: **IELTS & Giao Tiếp Thực Chiến (Scalable Slot / Coming Soon)**

## 6. Deployment Readiness (Vercel & GitHub Pages)
- Generate `vercel.json` for zero-config Vercel deployment.
- Generate `.github/workflows/deploy.yml` for automated GitHub Pages deployment.
- Ensure all asset paths and router configurations work seamlessly in both root domain (`vercel.app`) and subpath (`username.github.io/repo-name/`) environments.

---

# STEP-BY-STEP EXECUTION PLAN
1. **Step 1 (Data Extraction & Expansion Pipeline):** Create and run `scripts/extract_and_build_data.py` to extract all 16 modules from `Cam_Nang_On_Thi_Vao_10_Master.html` and parse questions/keys from the `.docx` folders into `src/data/*.json`, enriching them with new Syntax, Idioms, Reading passages, and detailed explanations.
2. **Step 2 (Project Scaffolding):** Initialize the Vite + Vue 3 + Tailwind CSS + Pinia + Vue Router project and configure `vite.config.js` and `vercel.json`.
3. **Step 3 (Core Pedagogical & Interactive Components):** Build `CalloutBox.vue`, `MermaidDiagram.vue`, `PhoneticWizard.vue`, `TenseTimeline.vue`, `QuizEngine.vue`, `ReadingSplitView.vue`, and `FlashcardDeck.vue`.
4. **Step 4 (Views & State Management):** Implement `useStudyStore.js` and the 5 main views (`HomeDashboard`, `ModuleLessonView`, `ReadingLabView`, `MockExamArenaView`, `IdiomVocabHubView`).
5. **Step 5 (Verification & Build Test):** Run `npm install` and `npm run build` to verify zero compilation or runtime errors, and provide a concise Vietnamese summary report to the user.
`​`​``

---

### PHẦN 3: HƯỚNG DẪN CẤU HÌNH TỰ HOST TRÊN VERCEL & GITHUB PAGES

Sau khi Agent khởi tạo xong dự án `english-mastery-web`, bạn có thể đưa web lên mạng hoàn toàn miễn phí chỉ trong 2 phút theo một trong hai cách sau:

#### Cách 1: Host trên Vercel (Khuyên dùng – Nhanh nhất, tự động có HTTPS & tên miền `.vercel.app`)

1. **Cấu hình file `vercel.json` ở thư mục gốc của web** *(Agent sẽ tự tạo sẵn theo Prompt trên)*:
   `​`​`json
   {
     "rewrites": [
       { "source": "/(.*)", "destination": "/index.html" }
     ]
   }
   `​`​`
   *(Cấu hình này giúp khi học sinh F5 lại trang ở đường dẫn con như `/reading` hay `/exams/test-1`, Vercel không báo lỗi 404).*
2. **Đẩy code lên GitHub và kết nối Vercel:**
   * Đẩy thư mục `english-mastery-web` lên một Repository trên GitHub của bạn.
   * Đăng nhập [vercel.com](https://vercel.com/) bằng tài khoản GitHub $\rightarrow$ bấm **Add New...** $\rightarrow$ **Project** $\rightarrow$ chọn Repo vừa tạo.
   * Tại mục **Framework Preset**, Vercel sẽ tự nhận diện là **Vite** (`Build Command: npm run build`, `Output Directory: dist`).
   * Bấm **Deploy**. Mỗi khi bạn hoặc Agent cập nhật thêm bài học mới và `git push`, Vercel sẽ tự động build lại trong ~20 giây.

---

#### Cách 2: Host trực tiếp trên GitHub Pages (Không cần tài khoản bên thứ ba)

1. **Cấu hình `vite.config.js` hỗ trợ đường dẫn động:**
   `​`​`javascript
   import { defineConfig } from 'vite'
   import vue from '@vitejs/plugin-vue'

   export default defineConfig({
     plugins: [vue()],
     // Tự động nhận diện nếu chạy trên GitHub Actions thì lấy tên repo, còn trên Vercel/Local thì dùng '/'
     base: process.env.GITHUB_REPOSITORY
       ? `/${process.env.GITHUB_REPOSITORY.split('/')[1]}/`
       : '/',
   })
   `​`​`
2. **Sử dụng `createWebHashHistory()` hoặc cấu hình GitHub Actions (`.github/workflows/deploy.yml`):**
   * Tạo file `.github/workflows/deploy.yml` trong dự án:
   `​`​`yaml
   name: Deploy Vue App to GitHub Pages

   on:
     push:
       branches: [ main, master ]
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   jobs:
     build-and-deploy:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout
           uses: actions/checkout@v4

         - name: Setup Node.js
           uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: 'npm'

         - name: Install & Build
           run: |
             npm ci
             npm run build

         - name: Copy index.html to 404.html for SPA Routing
           run: cp dist/index.html dist/404.html

         - name: Upload Pages Artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: ./dist

         - name: Deploy to GitHub Pages
           uses: actions/deploy-pages@v4
   `​`​`
3. **Bật GitHub Pages trên Repo:**
   * Vào **Settings** của Repository trên GitHub $\rightarrow$ mục **Pages** (cột bên trái) $\rightarrow$ tại phần **Build and deployment > Source**, chọn **GitHub Actions**.

Bạn có muốn mình viết sẵn luôn script Python `extract_and_build_data.py` để bóc tách tự động toàn bộ 16 chuyên đề trong `Cam_Nang_On_Thi_Vao_10_Master.html`[cite: 6] cùng bộ đề `.docx` Quảng Ngãi[cite: 4] thành các file JSON chuẩn cho dự án Vue không?

Powered by Gemini Exporter (https://www.ai-chat-exporter.com)
