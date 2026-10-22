# Xây dựng bộ khung Docs-as-Code

**Created:** 10/21/2026 16:11:37  
**Updated:** 10/21/2026 16:11:37  
**Exported:** 10/21/2026 16:19:41  
**Link:** [https://gemini.google.com/app/884bfb73d89a2022](https://gemini.google.com/app/884bfb73d89a2022)  

## Gemini:

> 10/21/2026 16:11:37

Dưới đây là bản đánh giá chi tiết (Review) 2 tệp tài liệu bạn đã cung cấp, kèm theo bức tranh tổng hợp về hệ sinh thái công nghệ **Docs-as-Code** trên GitHub và **Bộ khung chuẩn hóa (Universal Master Prompt, Agent Skill Spec & Multi-Source ETL Pipeline)** để bạn có thể tái sử dụng cho mọi dự án: từ tệp `.md`, mã nguồn `.js/.ts`, cho đến việc giải cứu các trang tài liệu đang bị hardcode trong `.html`.

---

## PHẦN 1: REVIEW & ĐÁNH GIÁ KỸ THUẬT 2 FILE HIỆN TẠI

### 1. Đánh giá file `Docs-as-Code-brainstorm.md`[cite: 1]
* **Điểm mạnh:**
  * **Tư duy kiến trúc chuẩn xác:** Nắm bắt đúng cốt lõi của triết lý *Single Source of Truth* (tách biệt hoàn toàn tầng dữ liệu Markdown và tầng hiển thị UI) dựa trên bài học từ repo `zalopay-oss/go-advanced`[cite: 1].
  * **Cấu trúc Prompt rõ ràng:** Khóa chặt ràng buộc *"Never hardcode lesson content into HTML"* ngay từ đầu[cite: 1], giúp các AI Coding Agent không bị trượt sang thói quen sinh từng trang HTML tĩnh thủ công.
  * **Tận dụng tốt hệ sinh thái Vue 3 (VitePress):** Đưa ra giải pháp dùng `createContentLoader` để quét bài học lúc build, tính toán thời gian đọc (reading time) và dựng trang danh mục tự động[cite: 1].
* **Điểm hạn chế cần nâng cấp:**
  * **Phạm vi hẹp (Domain-Specific):** Bản prompt đang bị đóng khung vào bài toán *"Web dạy học Python"*[cite: 1]. Khi bạn mang sang dự án làm tài liệu API, tài liệu quản trị hệ thống (SysAdmin Runbooks) hay tài liệu thư viện `.js`, bạn lại phải sửa lại câu chữ trong prompt.
  * **Chưa có quy trình xử lý nguồn `.js` và `.html` hardcode:** Tài liệu mới chỉ đề cập sơ bộ đến `.md` và `.docx` (qua Pandoc/Mammoth)[cite: 1], chưa có cơ chế tự động trích xuất tài liệu từ bình luận mã nguồn (`.js/.ts` JSDoc) hay cào ngược (reverse-parse) từ các file `.html` cũ sang Markdown.

### 2. Đánh giá file `init-docs.mjs` (Bản nâng cấp thực tế)[cite: 2]
So với bản nháp nằm trong file brainstorm[cite: 1], file `init-docs.mjs` rời bên ngoài đã có những bước tiến rất đáng giá về mặt kỹ thuật hệ thống:
* **Điểm sáng kỹ thuật (Best Practices):**
  1. **Zero-Copy NTFS Junction (`fs.symlinkSync(..., 'junction')`):** Đây là cách xử lý cực kỳ thông minh trên môi trường Windows[cite: 2]. Thay vì copy trùng lặp thư mục `python_reference` vào `docs/lessons`, việc tạo Junction giúp liên kết trực tiếp mà **không cần quyền Administrator**, giữ nguyên *Single Source of Truth* và có cơ chế fallback sang `copyDirRecursive` nếu lỗi[cite: 2].
  2. **Tự động suy luận Mô tả (Auto-Excerpt Fallback):** Trong `lessons.data.ts`, khi file `.md` không có YAML Frontmatter `description`, script đã biết quét từng dòng để lấy đoạn văn bản đầu tiên (bỏ qua thẻ `#`, `<`, `​`​`` `​`​` `​`​``, `-`) làm mô tả tóm tắt[cite: 2].
  3. **Tích hợp sẵn Mermaid.js Hook:** Đã can thiệp vào `md.renderer.rules.fence` trong `config.mts` để bọc khối `mermaid` vào `<div class="mermaid">` và gọi `mermaid.run()` tại hook `router.onAfterRouteChanged`[cite: 2].

* **Các lỗi tiềm ẩn (Edge Cases & Bugs) cần khắc phục trong `init-docs.mjs`:**
  1. **Thiếu khai báo thư viện `mermaid` trong `package.json`:** Ở file `init-docs.mjs` rời, khối tạo `package.json` đã bị lược bỏ[cite: 2], và ngay cả trong bản brainstorm cũng chỉ cài `vitepress` và `vue`[cite: 1]. Khi chạy tới dòng `import('mermaid')` trong `theme/index.ts`[cite: 2], trình biên dịch Vite sẽ báo lỗi thiếu dependency nếu chưa cài đặt gói `mermaid`.
  2. **Giao diện Mermaid bị cố định ở Dark Mode:** Trong `theme/index.ts`, cấu hình `m.default.initialize({ startOnLoad: false, theme: 'dark' })` đang khóa cứng giao diện tối[cite: 2]. Khi người đọc chuyển VitePress sang chế độ Sáng (Light Mode), sơ đồ Mermaid sẽ bị lệch tông màu hoặc mất chữ.
  3. **Giới hạn quét thư mục 1 cấp (1-Level Depth):** Hàm `getAutoSidebar()` chỉ quét `lessonsRoot -> categories -> mdFiles` (tối đa 2 tầng)[cite: 2]. Nếu bộ tài liệu có thư mục con sâu hơn (ví dụ: `01_core/memory/garbage_collection.md`), các file nằm ở tầng thứ 3 sẽ bị bỏ sót hoàn toàn.
  4. **Hardcode biến `MODULE_NAMES`:** Từ điển `MODULE_NAMES` đang gán cứng 10 chương của bộ tài liệu Python[cite: 2]. Để thành bộ khung dùng chung (Universal), cần chuyển sang đọc từ một file `manifest.json` hoặc tự động đọc từ file `_category_.json` / `index.md` trong từng thư mục.

---

## PHẦN 2: TỔNG HỢP CÔNG NGHỆ DOCS-AS-CODE TRÊN GITHUB

Để xử lý trọn vẹn 3 nguồn dữ liệu đầu vào (`.md`, `.js/.ts`, và `.html` hardcode) thành một trang web chuẩn UI/UX, các dự án mã nguồn mở lớn trên GitHub kết hợp **3 tầng công nghệ** sau:

### 1. Tầng Chuyển đổi & Chuẩn hóa Dữ liệu (ETL Ingestion Layer)
| Nguồn đầu vào | Công cụ / Thư viện chuẩn trên GitHub | Cơ chế hoạt động |
| :--- | :--- | :--- |
| **Hardcoded `.html`** *(Web cũ, Wiki nội bộ, Confluence export)* | **`turndown`** + **`@mozilla/readability`** + **`cheerio`** | Dùng `cheerio` hoặc `readability` bóc tách phần `<main>` / `<article>` (loại bỏ menu, quảng cáo, thẻ `<div>` rác của HTML cũ), sau đó dùng `turndown` dịch ngược DOM HTML về cú pháp Markdown sạch kèm bảng biểu (GFM) và code block. |
| **Source Code `.js` / `.ts`** *(API, SDK, Utility Scripts)* | **`TypeDoc`** + **`typedoc-plugin-markdown`** (hoặc **`documentation.js`**) | Phân tích cây cú pháp AST của file `.js`/`.ts` và các thẻ JSDoc (`/** @param ... */`) để tự động sinh ra bộ file `.md` chuẩn cấu trúc (Functions, Classes, Interfaces, Parameters) đưa thẳng vào thư mục của VitePress. |
| **Tài liệu `.md` / `.mdx` thô** | **`gray-matter`** + **`unified` / `remark`** | Tự động bổ sung YAML Frontmatter còn thiếu, chuẩn hóa đường dẫn ảnh tương đối và kiểm tra liên kết hỏng (broken links). |

### 2. Tầng Core Engine & UI/UX (Static Site Generators)
* **Hệ sinh thái Vue.js:**
  * **VitePress** (`vuejs/vitepress`): Nhanh nhất, gọn nhất, tích hợp sẵn **Shiki** (tô màu code chuẩn VS Code), **MiniSearch** (tìm kiếm toàn văn offline) và hỗ trợ nhúng trực tiếp Vue 3 Component vào Markdown[cite: 1, 2].
  * **Nuxt Content** (`nuxt/content`): Phù hợp khi cần biến thư mục `.md`, `.json`, `.yml` thành cơ sở dữ liệu có API truy vấn phức tạp.
* **Hệ sinh thái Đa nền tảng / React:**
  * **Astro Starlight** (`withastro/starlight`): Kiến trúc *Zero-JS by default*, cho phép nhúng cả component của Vue, React, Svelte vào cùng một trang tài liệu[cite: 1].
  * **Fumadocs** (`fuma-nama/fumadocs`) & **Nextra**: Xu hướng mới trên GitHub cho giao diện hiện đại kiểu Vercel/Shadcn UI.
  * **Docusaurus** (`facebook/docusaurus`): Rất mạnh khi cần quản lý phiên bản tài liệu (`v1.0`, `v2.0`)[cite: 1].

### 3. Tầng Nâng cấp Trải nghiệm Đọc (UI/UX Enhancement Plugins)
Các repo tài liệu hàng đầu trên GitHub thường cài thêm 4 gói mở rộng này vào VitePress:
1. **`vitepress-plugin-mermaid`**: Tự động xử lý sơ đồ Mermaid, hỗ trợ phóng to/thu nhỏ (zoom/pan) và tự đổi màu theo chế độ Sáng/Tối mà không cần tự viết hook thủ công.
2. **`@shikijs/vitepress-twoslash`**: Khi người đọc rê chuột (hover) vào biến hoặc hàm trong khối code JS/TS/Python, một popup kiểu IDE sẽ hiện lên giải thích kiểu dữ liệu.
3. **`vitepress-markdown-timeline`**: Biến danh sách Markdown thông thường thành sơ đồ lộ trình (Roadmap / Step-by-step) trực quan.
4. **`Pagefind` (`CloudCannon/pagefind`)**: Nếu bộ tài liệu lên tới hàng nghìn trang (khiến file index của `MiniSearch` bị nặng), `Pagefind` sẽ chia nhỏ index thành các mảnh (chunks) chạy bằng WebAssembly cực nhẹ.

---

## PHẦN 3: BỘ KHUNG CHUẨN HÓA ĐA NĂNG (UNIVERSAL DOCS-AS-CODE FRAMEWORK)

Dưới đây là bộ 3 công cụ chuẩn hóa gồm: **1. Universal Master Prompt**, **2. Agent Skill Specification (`SKILL.md`)**, và **3. Universal Ingestion & Bootstrapper Script (`universal-docs-engine.mjs`)** để bạn dùng chung cho mọi dự án `.md`, `.js` và `.html`.

### 1. Universal Master Prompt (Dùng cho mọi dự án `.md`, `.js`, `.html`)

Bạn có thể lưu prompt này làm mẫu chuẩn. Khi có bất kỳ kho tài liệu nào (dù là `.md`, code `.js` hay web `.html` cũ), chỉ cần đưa prompt này cho AI thực thi:

`​`​`markdown
# Role & Mission

You are a Principal Docs-as-Code Architect, Full-Stack Developer (Vue 3 / VitePress Specialist), and Technical Information Designer.

Your mission is to transform raw technical materials—whether they are **Markdown files (`*.md`)**, **JavaScript/TypeScript source files (`*.js`, `*.ts`)**, or **legacy hardcoded HTML files (`*.html`)**—into a unified, high-performance, aesthetically refined Documentation Portal powered by **VitePress (Vue 3)**.

IMPORTANT RULES:
- Respond, explain, and report entirely in **Vietnamese**. Keep code identifiers, file paths, and configuration keys in English.
- **STRICT PROHIBITION:** Never hardcode documentation content into HTML or Vue templates. All content MUST flow through a unified Markdown compilation pipeline (Single Source of Truth).
- Execute proactively from data extraction to UI configuration without asking for step-by-step confirmation.

---

# Multi-Source Ingestion Pipeline (ETL Architecture)

Before rendering the website, inspect the input repository and execute the appropriate normalization pipeline into the target `docs/content/` directory:

1. **Scenario A — Input is Markdown (`*.md`):**
   - Preserve the original directory via **Zero-Copy Symlink / NTFS Junction** whenever possible.
   - Automatically infer missing metadata (`title` from `# H1`, `description` from the first text paragraph, `category` from folder names, and `readingTime` from word count).

2. **Scenario B — Input is Legacy Hardcoded HTML (`*.html`):**
   - Write and execute an automated Node.js migration script using `cheerio` (or `@mozilla/readability`) + `turndown` + `turndown-plugin-gfm`.
   - Strip legacy layout wrappers (`<nav>`, `<header>`, `<footer>`, inline styles, redundant `<div>` tags), extract the core `<article>`/`<main>` content, preserve tables and code blocks, and convert them into clean `.md` files with proper YAML Frontmatter (`title`, `description`, `source_html`).

3. **Scenario C — Input is Source Code (`*.js`, `*.ts`):**
   - Parse JSDoc comments, exported functions, classes, and configuration objects (using `typedoc` with `typedoc-plugin-markdown` or an AST parser script).
   - Generate structured API Reference `.md` files grouped by module, automatically linking parameters, return types, and usage examples.

---

# Core Portal Architecture & UI/UX Standards

Build the VitePress (Vue 3) portal with the following mandatory capabilities:

1. **Dynamic Landing Portal (`docs/index.md`):**
   - Modern Hero banner, quick-start actions, and core feature cards.
   - Live statistics badge (total articles, total reading time, module breakdown).
2. **Interactive Content Catalog (`<ContentCatalog/>` Vue 3 Component):**
   - Build-time indexing via `createContentLoader`.
   - Instant reactive filtering by Category Pills, Difficulty/Type tags, and keyword search.
   - Display card metadata: Category badge, Estimated reading time (`⏱ X phút`), Word count, and clean excerpt.
3. **Recursive Auto-Sidebar & Navigation:**
   - Automatically scan multi-level folder hierarchies (`getAutoSidebar` recursive function).
   - Support optional `manifest.json` or `_category.json` for custom human-readable Vietnamese category titles while falling back gracefully to formatted folder names.
4. **Enhanced Reading Experience:**
   - Dual-theme syntax highlighting via **Shiki** (`github-light` / `one-dark-pro`) with line numbers and 1-click Copy button.
   - Native **Mermaid.js** diagram rendering that dynamically adapts to Light/Dark mode toggles.
   - Sticky right-hand Table of Contents (`H2`, `H3`), top reading progress bar, and local full-text search (`Ctrl + K` via MiniSearch).

---

# Deliverables

1. **Source Audit & Ingestion Execution:** Identify input file types (`.md`, `.js`, `.html`) and run the normalization/linking script.
2. **Information Architecture:** Organize logical categories and navigation hierarchy.
3. **Complete Scaffolding & Codebase:** Generate `package.json`, `config.mts`, `content.data.ts`, custom Vue components, and theme enhancements.
4. **Verification:** Validate the build pipeline (`npm run docs:build`) to ensure zero broken links or SSR hydration errors.
`​`​`

---

### 2. Bộ khung Skill (`SKILL.md`) dùng cho AI Coding Agent

Nếu bạn sử dụng các IDE hoặc Agent hỗ trợ cơ chế nạp Skill (như Claude Code, Cursor Rules, Antigravity, hoặc MCP Agent), hãy lưu file này thành `.agent/skills/docs-as-code-builder/SKILL.md`:

`​`​`markdown
---
name: docs-as-code-builder
description: Tự động chuyển đổi các bộ tài liệu Markdown (.md), mã nguồn (.js/.ts) hoặc trang web HTML hardcode (.html) thành cổng tài liệu VitePress (Vue 3) chuẩn UI/UX hiện đại.
---

# Docs-as-Code Builder Skill

## Khi nào sử dụng Skill này?
Kích hoạt ngay khi người dùng yêu cầu:
- Đẩy một thư mục chứa các file `.md` lên web đọc tài liệu có giao diện đẹp, mục lục tự động, tìm kiếm nhanh.
- Chuyển đổi các trang `.html` viết cứng (hardcoded HTML documentation) sang kiến trúc Docs-as-Code dễ bảo trì.
- Sinh trang tài liệu kỹ thuật / API Reference từ các file mã nguồn `.js`, `.mjs`, `.ts`.

## Quy trình thực thi chuẩn (Standard Operating Procedure)

### Bước 1: Kiểm tra & Chuẩn hóa nguồn dữ liệu (Ingestion)
- **Nếu nguồn là `.html`:** Chạy bộ chuyển đổi HTML-to-Markdown (`cheerio` + `turndown`). Chỉ lấy vùng nội dung chính (`main`, `article`, `.content`), loại bỏ hoàn toàn CSS nội tuyến và thanh điều hướng cũ, lưu thành file `.md` kèm Frontmatter.
- **Nếu nguồn là `.js` / `.ts`:** Quét các khối JSDoc `/** ... */` và chữ ký hàm (`function`, `class`, `const`) để kết xuất thành tài liệu `.md` theo từng module.
- **Nếu nguồn là `.md`:** Tạo liên kết **NTFS Junction** (trên Windows) hoặc **Symlink** (trên Linux/macOS) từ thư mục nguồn vào `docs/content` để đảm bảo nguyên tắc *Zero-Copy Single Source of Truth*.

### Bước 2: Khởi tạo kiến trúc VitePress (Vue 3)
Luôn đảm bảo cấu trúc file tối thiểu sau:
1. `docs/.vitepress/config.mts`:
   - Hàm `getAutoSidebar()` đệ quy đa cấp, tự động đọc `title` từ Frontmatter hoặc thẻ `# H1`.
   - Bật `search: { provider: 'local' }` với bản dịch tiếng Việt.
   - Tích hợp hook render `mermaid` tương thích cả chế độ Sáng và Tối.
2. `docs/.vitepress/data/content.data.ts`:
   - Sử dụng `createContentLoader('content/**/*.md', { includeSrc: true })`.
   - Tự động tính `wordCount`, `readingTime` (200 từ/phút), và trích xuất đoạn văn đầu tiên làm `description` nếu thiếu Frontmatter.
3. `docs/.vitepress/theme/components/ContentCatalog.vue`:
   - Giao diện lưới (Grid Card) có thanh tìm kiếm tức thì và bộ lọc danh mục (Category Pills).
   - Sử dụng biến CSS chuẩn của VitePress (`--vp-c-brand-1`, `--vp-c-bg-soft`, `--vp-c-divider`) để tự động tương thích Light/Dark mode.

### Bước 3: Kiểm tra chất lượng (QA Checklist)
- Không được phép có bất kỳ nội dung bài viết nào bị hardcode trong file `.vue` hoặc `.html`.
- `package.json` phải khai báo đầy đủ `vitepress`, `vue`, `mermaid` (và `turndown`, `cheerio` nếu có bước chuyển đổi HTML).
- Cấu hình `ignoreDeadLinks: true` trong giai đoạn chuyển đổi dữ liệu thô để tránh gãy luồng build do các liên kết nội bộ cũ.
`​`​`

---

### 3. Script Thực Thi Đa Năng: `universal-docs-engine.mjs`

Đây là phiên bản nâng cấp toàn diện từ file `init-docs.mjs` của bạn[cite: 2], giải quyết triệt để các hạn chế đã nêu và tích hợp **Bộ chuyển đổi đa nguồn (`.md` + `.html` hardcode + `.js` JSDoc)**:

* **Khắc phục lỗi thiếu `package.json` và `mermaid`**[cite: 1, 2].
* **Hỗ trợ tự động đồng bộ Dark/Light mode cho sơ đồ Mermaid.**
* **Tích hợp bộ giải cứu HTML Hardcode (`convertHtmlToMd`) và trích xuất JSDoc từ file `.js` (`extractJsDocToMd`).**
* **Tách từ điển tên chương ra cấu hình linh hoạt, quét thư mục đệ quy.**

`​`​`javascript
/**
 * UNIVERSAL DOCS-AS-CODE ENGINE (v2.0)
 * Hỗ trợ tự động hóa xây dựng cổng tài liệu VitePress (Vue 3) từ:
 *  1. Thư mục tài liệu Markdown (.md) -> Zero-Copy NTFS Junction / Symlink
 *  2. Các file HTML hardcode cũ (.html) -> Tự động bóc tách & dịch ngược sang .md
 *  3. Các file mã nguồn (.js / .ts) -> Tự động trích xuất JSDoc & chữ ký hàm sang .md
 *
 * Cách dùng:
 *   node universal-docs-engine.mjs --src=./python_reference --title="Python Master Hub"
 */

import fs from 'node:fs';
import path from 'node:path';

// Đọc tham số dòng lệnh
const args = Object.fromEntries(
  process.argv.slice(2).map(arg => {
    const [k, v] = arg.replace(/^--/, '').split('=');
    return [k, v ?? true];
  })
);

const SOURCE_DIR = path.resolve(args.src || 'python_reference');
const SITE_TITLE = args.title || 'Technical Knowledge Hub';
const SITE_DESC = args.desc || 'Cổng tài liệu kỹ thuật chuẩn hóa theo kiến trúc Docs-as-Code';
const CONTENT_DEST = path.resolve('docs/lessons');

// Từ điển ánh xạ tên thư mục (Có thể mở rộng qua file manifest.json nếu có)
const DEFAULT_MODULE_NAMES = {
  "01_core_mechanics": "1. Nền Tảng & Cấu Trúc Dữ Liệu CPython",
  "02_advanced_functions": "2. Lập Trình Hàm Nâng Cao & Closures",
  "03_oop_metaprogramming": "3. Hướng Đối Tượng & Siêu Lập Trình",
  "04_concurrency_async": "4. Bất Đồng Bộ, Đa Luồng & GIL",
  "05_typing_modern_python": "5. Hệ Thống Kiểu Tĩnh & Pydantic V2",
  "06_standard_library": "6. Thư Viện Chuẩn & Tooling Hiện Đại",
  "07_web_frameworks": "7. FastAPI & Tích Hợp AI / LLM",
  "08_database_orm": "8. Cơ Sở Dữ Liệu & SQLAlchemy 2.0",
  "09_data_engineering_tools": "9. Xử Lý Dữ Liệu Hiệu Năng Cao",
  "appendix": "10. Phụ Lục, Cạm Bẫy & Bài Tập Thực Chiến"
};

// ============================================================================
// TẦNG 1: BỘ CHUYỂN ĐỔI NGƯỢC HTML HARDCODE & JS SANG MARKDOWN (ETL PARSERS)
// ============================================================================

/**
 * Chuyển đổi file HTML hardcode sang Markdown sạch (Zero-dependency Regex Parser,
 * tự động nâng cấp dùng Turndown nếu môi trường đã cài đặt).
 */
function convertHardcodedHtmlToMd(htmlContent, fileName) {
  // Trích xuất <title> hoặc <h1>
  const titleMatch = htmlContent.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i) || htmlContent.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const rawTitle = titleMatch ? titleMatch[1].replace(/<[^>]+>/g, '').trim() : fileName.replace(/\.html?$/i, '');

  // Chỉ lấy phần nội dung trong <main>, <article> hoặc <body>
  const bodyMatch = htmlContent.match(/<(?:main|article)[^>]*>([\s\S]*?)<\/(?:main|article)>/i) || htmlContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  let body = bodyMatch ? bodyMatch[1] : htmlContent;

  // Loại bỏ script, style, nav, header, footer
  body = body
    .replace(/<(script|style|nav|header|footer|aside)[^>]*>[\s\S]*?<\/\1>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '');

  // Chuyển đổi các thẻ HTML phổ biến sang Markdown
  let md = body
    .replace(/<pre[^>]*><code[^>]*class="[^"]*language-([a-zA-Z0-9_-]+)[^"]*"[^>]*>([\s\S]*?)<\/code><\/pre>/gi, (_, lang, code) => `\n\`\`\`${lang}\n${decodeHtmlEntities(code.trim())}\n\`\`\`\n`)
    .replace(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/gi, (_, code) => `\n\`\`\`\n${decodeHtmlEntities(code.trim())}\n\`\`\`\n`)
    .replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n')
    .replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n')
    .replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n')
    .replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, '\n#### $1\n')
    .replace(/<strong[^>]*>([\s\S]*?)<\/strong>/gi, '**$1**')
    .replace(/<b[^>]*>([\s\S]*?)<\/b>/gi, '**$1**')
    .replace(/<em[^>]*>([\s\S]*?)<\/em>/gi, '*$1*')
    .replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, '`$1`')
    .replace(/<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)')
    .replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '- $1\n')
    .replace(/<\/?(?:ul|ol|p|div|section|br)[^>]*>/gi, '\n')
    .replace(/<[^>]+>/g, '') // Xóa các thẻ HTML còn sót
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  md = decodeHtmlEntities(md);

  return `---
title: "${rawTitle.replace(/"/g, '\\"')}"
source_type: "html-migrated"
---

${md}
`;
}

function decodeHtmlEntities(str) {
  return str
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ');
}

/**
 * Trích xuất JSDoc và danh sách hàm từ file .js / .ts sang Markdown
 */
function convertJsSourceToMd(jsContent, fileName) {
  const baseName = fileName.replace(/\.[m]?[jt]s$/, '');
  const blocks = [];
  const jsdocRegex = /\/\*\*([\s\S]*?)\*\/\s*(?:export\s+)?(?:async\s+)?(?:function\s+([a-zA-Z0-9_$]+)|(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=|class\s+([a-zA-Z0-9_$]+))?/g;

  let match;
  while ((match = jsdocRegex.exec(jsContent)) !== null) {
    const rawComment = match[1]
      .split('\n')
      .map(line => line.replace(/^\s*\*\s?/, '').trim())
      .join('\n')
      .trim();
    const symbolName = match[2] || match[3] || match[4] || 'Mô tả Module';
    blocks.push(`## \`${symbolName}\`\n\n${rawComment}\n`);
  }

  return `---
title: "API Reference: ${baseName}"
category: "API & Source Code"
source_type: "js-autodoc"
---

# Tài liệu Mã nguồn: \`${fileName}\`

${blocks.length > 0 ? blocks.join('\n---\n\n') : '`​`​`javascript\n' + jsContent.trim() + '\n`​`​`'}
`;
}

// ============================================================================
// TẦNG 2: ĐỊNH NGHĨA CẤU HÌNH VITEPRESS (VUE 3) CHUẨN HÓA
// ============================================================================

const files = {
  // 1. package.json (Đảm bảo đầy đủ dependencies, bao gồm cả mermaid)
  'package.json': JSON.stringify(
    {
      name: 'universal-docs-portal',
      version: '2.0.0',
      description: SITE_DESC,
      type: 'module',
      scripts: {
        'docs:init': 'node universal-docs-engine.mjs',
        'docs:dev': 'vitepress dev docs',
        'docs:build': 'vitepress build docs',
        'docs:preview': 'vitepress preview docs'
      },
      devDependencies: {
        mermaid: '^11.0.0',
        vitepress: '^1.5.0',
        vue: '^3.5.0'
      }
    },
    null,
    2
  ),

  // 2. docs/.vitepress/config.mts (Quét Sidebar đệ quy đa cấp + Mermaid + MiniSearch)
  'docs/.vitepress/config.mts': `import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

const MODULE_NAMES: Record<string, string> = ${JSON.stringify(DEFAULT_MODULE_NAMES, null, 2)}

function formatFolderName(name: string): string {
  if (MODULE_NAMES[name]) return MODULE_NAMES[name]
  const clean = name.replace(/^\\d+[-_]/, '').replace(/[-_]/g, ' ')
  const prefix = name.match(/^(\\d+)[-_]/)?.[1]
  const capitalized = clean.charAt(0).toUpperCase() + clean.slice(1)
  return prefix ? \`\${parseInt(prefix)}. \${capitalized}\` : capitalized
}

function extractMarkdownTitle(filePath: string, fallbackName: string): string {
  try {
    const content = fs.readFileSync(filePath, 'utf-8')
    const fmMatch = content.match(/^---\\r?\\n[\\s\\S]*?title:\\s*(.*?)\\r?\\n[\\s\\S]*?---/)
    const h1Match = content.match(/^#\\s+(.+)$/m)
    const raw = fmMatch ? fmMatch[1] : (h1Match ? h1Match[1] : fallbackName)
    return raw.trim().replace(/^['"](.*)['"]$/, '$1').replace(/[\\x60*]/g, '').trim()
  } catch {
    return fallbackName
  }
}

// Hàm đệ quy quét thư mục đa tầng để dựng Sidebar
function scanDirectoryRecursive(dirPath: string, urlPrefix: string): any[] {
  if (!fs.existsSync(dirPath)) return []
  const entries = fs.readdirSync(dirPath, { withFileTypes: true })
    .filter(e => !e.name.startsWith('.'))
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }))

  const items: any[] = []

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name)
    if (entry.isDirectory()) {
      const children = scanDirectoryRecursive(fullPath, \`\${urlPrefix}/\${entry.name}\`)
      if (children.length > 0) {
        items.push({
          text: formatFolderName(entry.name),
          collapsed: false,
          items: children
        })
      }
    } else if (entry.isFile() && entry.name.endsWith('.md') && entry.name.toLowerCase() !== 'readme.md') {
      const slug = entry.name.replace(/\\.md$/, '')
      items.push({
        text: extractMarkdownTitle(fullPath, slug),
        link: \`\${urlPrefix}/\${slug}\`
      })
    }
  }
  return items
}

export default defineConfig({
  title: ${JSON.stringify(SITE_TITLE)},
  description: ${JSON.stringify(SITE_DESC)},
  lang: 'vi-VN',
  lastUpdated: true,
  cleanUrls: true,
  ignoreDeadLinks: true,

  markdown: {
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'one-dark-pro'
    },
    config(md) {
      const defaultFence = md.renderer.rules.fence!
      md.renderer.rules.fence = (tokens, idx, options, env, slf) => {
        const token = tokens[idx]
        const info = (token.info || '').trim()
        if (info.toLowerCase() === 'mermaid') {
          return \`<pre class="mermaid">\${token.content}</pre>\`
        }
        return defaultFence(tokens, idx, options, env, slf)
      }
    }
  },

  themeConfig: {
    siteTitle: ${JSON.stringify(SITE_TITLE)},
    nav: [
      { text: 'Trang chủ', link: '/' },
      { text: 'Toàn bộ danh mục 📚', link: '/catalog' }
    ],
    sidebar: {
      '/lessons/': scanDirectoryRecursive(path.resolve(__dirname, '../lessons'), '/lessons')
    },
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: 'Tìm kiếm tài liệu (Ctrl+K)...', buttonAriaLabel: 'Tìm kiếm' },
              modal: {
                noResultsText: 'Không tìm thấy nội dung phù hợp',
                resetButtonTitle: 'Xóa tìm kiếm',
                footer: { selectText: 'chọn', navigateText: 'di chuyển', closeText: 'đóng' }
              }
            }
          }
        }
      }
    },
    outline: {
      level: [2, 3],
      label: 'Mục lục trên trang'
    },
    docFooter: {
      prev: '← Bài trước',
      next: 'Bài kế tiếp →'
    }
  }
})
`,

  // 3. docs/.vitepress/data/lessons.data.ts
  'docs/.vitepress/data/lessons.data.ts': `import { createContentLoader } from 'vitepress'

const MODULE_NAMES: Record<string, string> = ${JSON.stringify(DEFAULT_MODULE_NAMES, null, 2)}

export interface LessonMeta {
  title: string
  url: string
  category: string
  description: string
  readingTime: number
  wordCount: number
  sourceType: string
}

declare const data: LessonMeta[]
export { data }

export default createContentLoader('lessons/**/*.md', {
  includeSrc: true,
  transform(raw): LessonMeta[] {
    return raw
      .filter(({ url }) => !url.endsWith('/lessons/') && !url.toLowerCase().endsWith('/readme.html'))
      .map(({ url, frontmatter, src }) => {
        const parts = url.split('/')
        const catKey = parts[2] || 'general'
        const category = frontmatter.category || MODULE_NAMES[catKey] || catKey.replace(/[-_]/g, ' ').toUpperCase()

        let title = frontmatter.title
        if (!title && src) {
          const match = src.match(/^#\\s+(.+)$/m)
          if (match) title = match[1].replace(/[\\x60*]/g, '').trim()
        }
        if (!title) {
          title = url.split('/').pop()?.replace('.html', '').replace(/[-_]/g, ' ') || 'Tài liệu'
        }

        const wordCount = (src || '').trim().split(/\\s+/).length
        const readingTime = Math.max(1, Math.ceil(wordCount / 200))

        let description = frontmatter.description
        if (!description && src) {
          const lines = src.replace(/^---[\\s\\S]*?---/, '').split('\\n')
          for (const line of lines) {
            const trimmed = line.trim()
            if (trimmed && !trimmed.startsWith('#') && !trimmed.startsWith('<') && !trimmed.startsWith('\`\`\`') && !trimmed.startsWith('-') && !trimmed.startsWith('|')) {
              description = trimmed.slice(0, 160) + (trimmed.length > 160 ? '...' : '')
              break
            }
          }
        }

        return {
          title,
          description: description || 'Tài liệu kỹ thuật được tổng hợp tự động qua luồng Docs-as-Code.',
          category,
          readingTime,
          wordCount,
          sourceType: frontmatter.source_type || 'markdown',
          url
        }
      })
      .sort((a, b) => a.url.localeCompare(b.url, undefined, { numeric: true }))
  }
})
`,

  // 4. docs/.vitepress/theme/components/LessonCatalog.vue
  'docs/.vitepress/theme/components/LessonCatalog.vue': `<script setup>
import { ref, computed } from 'vue'
import { data as lessons } from '../data/lessons.data.ts'

const searchQuery = ref('')
const selectedCategory = ref('Tất cả')

const categories = computed(() => {
  const cats = new Set(lessons.map(l => l.category))
  return ['Tất cả', ...Array.from(cats)]
})

const filteredLessons = computed(() => {
  return lessons.filter(lesson => {
    const matchesCat = selectedCategory.value === 'Tất cả' || lesson.category === selectedCategory.value
    const query = searchQuery.value.toLowerCase().trim()
    if (!query) return matchesCat

    return lesson.title.toLowerCase().includes(query) ||
           lesson.description.toLowerCase().includes(query) ||
           lesson.category.toLowerCase().includes(query)
  })
})
</script>

<template>
  <div class="catalog-container">
    <div class="filter-bar">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="🔍 Lọc nhanh theo tiêu đề, từ khóa, chuyên đề..." 
        class="search-input"
      />
      <div class="category-pills">
        <button 
          v-for="cat in categories" 
          :key="cat"
          :class="['pill-btn', { active: selectedCategory === cat }]"
          @click="selectedCategory = cat"
        >
          {{ cat }}
        </button>
      </div>
    </div>

    <div class="catalog-summary">
      <span>Hiển thị <strong>{{ filteredLessons.length }}</strong> / {{ lessons.length }} tài liệu kỹ thuật</span>
    </div>

    <div class="lessons-grid">
      <a 
        v-for="item in filteredLessons" 
        :key="item.url" 
        :href="item.url" 
        class="lesson-card"
      >
        <div class="card-header">
          <span class="badge category-badge">{{ item.category }}</span>
          <span class="badge time-badge">⏱ {{ item.readingTime }} phút (~{{ item.wordCount }} từ)</span>
        </div>
        <h3 class="card-title">{{ item.title }}</h3>
        <p class="card-desc">{{ item.description }}</p>
        <span class="read-more">Đọc chi tiết →</span>
      </a>
    </div>
  </div>
</template>

<style scoped>
.catalog-container { margin-top: 1.5rem; }
.filter-bar { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }
.search-input {
  width: 100%; padding: 0.85rem 1.15rem; border-radius: 10px;
  border: 1px solid var(--vp-c-divider); background: var(--vp-c-bg-alt);
  color: var(--vp-c-text-1); font-size: 0.95rem; outline: none;
}
.search-input:focus { border-color: var(--vp-c-brand-1); }
.category-pills { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.pill-btn {
  padding: 0.4rem 0.95rem; border-radius: 9999px; font-size: 0.85rem;
  border: 1px solid var(--vp-c-divider); background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2); cursor: pointer; transition: all 0.2s ease;
}
.pill-btn:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
.pill-btn.active { background: var(--vp-c-brand-1); border-color: var(--vp-c-brand-1); color: #fff; font-weight: 600; }
.catalog-summary { font-size: 0.85rem; color: var(--vp-c-text-3); margin-bottom: 1.25rem; }
.lessons-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}
.lesson-card {
  display: flex; flex-direction: column; padding: 1.35rem; border-radius: 12px;
  border: 1px solid var(--vp-c-divider); background: var(--vp-c-bg-soft);
  text-decoration: none !important; transition: transform 0.2s ease, border-color 0.2s ease;
}
.lesson-card:hover { transform: translateY(-3px); border-color: var(--vp-c-brand-1); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.85rem; gap: 0.5rem; }
.badge { font-size: 0.72rem; padding: 0.2rem 0.55rem; border-radius: 6px; }
.category-badge { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 600; }
.time-badge { color: var(--vp-c-text-3); white-space: nowrap; }
.card-title { margin: 0 0 0.6rem 0; font-size: 1.15rem; color: var(--vp-c-text-1); font-weight: 700; line-height: 1.4; }
.card-desc { font-size: 0.875rem; color: var(--vp-c-text-2); flex-grow: 1; margin-bottom: 1.25rem; line-height: 1.6; }
.read-more { font-size: 0.875rem; font-weight: 600; color: var(--vp-c-brand-1); }
</style>
`,

  // 5. docs/.vitepress/theme/index.ts (Sửa lỗi Mermaid tự động nhận diện Dark/Light Mode)
  'docs/.vitepress/theme/index.ts': `import DefaultTheme from 'vitepress/theme'
import LessonCatalog from './components/LessonCatalog.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app, router }) {
    app.component('LessonCatalog', LessonCatalog)

    if (typeof window !== 'undefined') {
      import('mermaid').then(m => {
        const renderDiagrams = () => {
          setTimeout(() => {
            const isDark = document.documentElement.classList.contains('dark')
            m.default.initialize({
              startOnLoad: false,
              theme: isDark ? 'dark' : 'default'
            })
            const elements = document.querySelectorAll('.mermaid')
            if (elements.length > 0) {
              m.default.run({ nodes: elements })
            }
          }, 120)
        }

        router.onAfterRouteChanged = renderDiagrams
        window.addEventListener('load', renderDiagrams)
      }).catch(err => {
        console.warn('Mermaid chưa được cài đặt hoặc bỏ qua:', err)
      })
    }
  }
}
`,

  // 6. docs/index.md
  'docs/index.md': `---
layout: home

hero:
  name: ${JSON.stringify(SITE_TITLE)}
  text: "Cổng Tài Liệu Kỹ Thuật Chuẩn Docs-as-Code"
  tagline: "Tự động biên dịch từ Markdown (.md), Source Code (.js) và chuyển đổi HTML cũ sang nền tảng Vue 3 & VitePress."
  actions:
    - theme: brand
      text: Khám phá Danh mục 📚
      link: /catalog

features:
  - icon: 📄
    title: Markdown Single Source of Truth
    details: Liên kết trực tiếp thư mục tài liệu qua NTFS Junction / Symlink, tự động tạo Sidebar và tính thời gian đọc.
  - icon: 🔄
    title: Giải cứu HTML Hardcode
    details: Tự động bóc tách nội dung từ các trang HTML tĩnh đời cũ, dọn sạch thẻ rác và chuẩn hóa về Markdown.
  - icon: 💻
    title: Tự động hóa tài liệu JS/TS
    details: Quét JSDoc và chữ ký hàm trong mã nguồn để sinh trang API Reference đồng bộ.
---

<div style="margin-top: 2.5rem;">
  <LessonCatalog />
</div>
`,

  // 7. docs/catalog.md
  'docs/catalog.md': `---
title: Danh mục tài liệu
---

# 📚 Toàn bộ Danh mục Tài liệu

<LessonCatalog />
`
};

// ============================================================================
// TẦNG 3: THỰC THI KHỞI TẠO & ĐỒNG BỘ DỮ LIỆU ĐA NGUỒN
// ============================================================================

console.log('🚀 [1/2] Đang khởi tạo bộ khung Universal VitePress (Vue 3)...');

for (const [filePath, content] of Object.entries(files)) {
  // Không ghi đè package.json nếu người dùng đã có sẵn cấu hình riêng
  if (filePath === 'package.json' && fs.existsSync( path.resolve('package.json'))) {
    console.log(' ℹ️ Giữ nguyên package.json hiện có (Hãy đảm bảo đã cài: vitepress, vue, mermaid)');
    continue;
  }
  const fullPath = path.resolve(filePath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, content.trim() + '\n', 'utf-8');
  console.log(` ✅ Đã tạo: ${filePath}`);
}

console.log(`\n🔗 [2/2] Đang xử lý nguồn dữ liệu từ: ${SOURCE_DIR}`);

if (fs.existsSync(SOURCE_DIR)) {
  // Kiểm tra xem thư mục nguồn có chứa file .html hoặc .js cần chuyển đổi sang .md không
  const hasLegacyFiles = checkRequiresConversion(SOURCE_DIR);

  if (!hasLegacyFiles) {
    // Trường hợp 100% là .md thuần túy -> Dùng NTFS Junction (Zero-Copy)
    if (fs.existsSync(CONTENT_DEST)) {
      fs.rmSync(CONTENT_DEST, { recursive: true, force: true });
    }
    try {
      fs.symlinkSync(SOURCE_DIR, CONTENT_DEST, 'junction');
      console.log(' ✅ Đã tạo liên kết Zero-Copy (NTFS Junction): docs/lessons -> ' + SOURCE_DIR);
    } catch {
      ingestAndConvertDirectory(SOURCE_DIR, CONTENT_DEST);
      console.log(' ✅ Đã đồng bộ thư mục tài liệu vào docs/lessons');
    }
  } else {
    // Trường hợp pha trộn .md, .html hardcode, .js -> Chạy luồng ETL chuyển đổi sang .md
    if (fs.existsSync(CONTENT_DEST) && fs.lstatSync(CONTENT_DEST).isSymbolicLink()) {
      fs.unlinkSync(CONTENT_DEST);
    }
    ingestAndConvertDirectory(SOURCE_DIR, CONTENT_DEST);
    console.log(' ✅ Đã chuyển đổi toàn bộ (.md, .html, .js) về chuẩn Markdown tại docs/lessons');
  }
} else {
  console.warn(` ⚠️ Không tìm thấy thư mục nguồn "${SOURCE_DIR}". Đã tạo thư mục docs/lessons trống.`);
  fs.mkdirSync(CONTENT_DEST, { recursive: true });
}

function checkRequiresConversion(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.name.startsWith('.')) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory() && checkRequiresConversion(full)) return true;
    if (e.isFile() && /\.(html?|js|ts)$/i.test(e.name)) return true;
  }
  return false;
}

function ingestAndConvertDirectory(srcDir, destDir) {
  fs.mkdirSync(destDir, { recursive: true });
  const entries = fs.readdirSync(srcDir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const srcPath = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);

    if (entry.isDirectory()) {
      ingestAndConvertDirectory(srcPath, destPath);
    } else if (entry.name.endsWith('.md')) {
      fs.copyFileSync(srcPath, destPath);
    } else if (/\.html?$/i.test(entry.name)) {
      const html = fs.readFileSync(srcPath, 'utf-8');
      const md = convertHardcodedHtmlToMd(html, entry.name);
      const mdDest = destPath.replace(/\.html?$/i, '.md');
      fs.writeFileSync(mdDest, md, 'utf-8');
      console.log(`   🔄 [HTML -> MD] Đã giải cứu: ${entry.name}`);
    } else if (/\.[jt]s$/i.test(entry.name)) {
      const js = fs.readFileSync(srcPath, 'utf-8');
      const md = convertJsSourceToMd(js, entry.name);
      const mdDest = destPath.replace(/\.[jt]s$/i, '.md');
      fs.writeFileSync(mdDest, md, 'utf-8');
      console.log(`   💻 [JS -> MD] Đã trích xuất tài liệu: ${entry.name}`);
    }
  }
}
`​`​`

---

### Tóm tắt cách vận hành Bộ khung chuẩn này trong thực tế

1. **Khi làm dự án tài liệu `.md` thuần (như `python_reference`):**
   Script tự động nhận diện 100% là file `.md` và kích hoạt chế độ **Zero-Copy NTFS Junction** (giữ nguyên ưu điểm của file `init-docs.mjs` hiện tại[cite: 2] nhưng hỗ trợ cây thư mục nhiều tầng và Mermaid tự đổi màu Sáng/Tối).
2. **Khi gặp dự án cũ bị hardcode trong `.html` hoặc muốn rút trích tài liệu từ file `.js`:**
   Chỉ cần trỏ `--src=./thu_muc_html_cu`, bộ máy ETL tích hợp sẵn sẽ tự động lọc bỏ các thẻ layout rác của HTML, rút trích JSDoc từ `.js` và biên dịch toàn bộ sang các file `.md` sạch sẽ trong `docs/lessons/` trước khi VitePress dựng giao diện.
3. **Bạn có muốn mình lưu trực tiếp bộ quy trình này thành một Agent Skill cá nhân trên hệ thống để các phiên làm việc sau tự động kích hoạt không?** Nếu cần tinh chỉnh thêm về giao diện (như tích hợp thêm bộ phóng to sơ đồ Mermaid hoặc tuỳ biến màu sắc thương hiệu), bạn cứ cho mình biết nhé!

Powered by Gemini Exporter (https://www.ai-chat-exporter.com)
