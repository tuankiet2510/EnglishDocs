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
  "chuyen_de_1": "Phần 1: Ngữ Âm & Trọng Âm",
  "chuyen_de_2": "Phần 2: Ngữ Pháp & Cấu Trúc Trọng Tâm",
  "chuyen_de_3": "Phần 3: Từ Vựng Chọn Lọc",
  "guide": "Cẩm Nang Phương Pháp",
  "exams": "Bộ Đề Tuyển Sinh Vào 10"
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

${blocks.length > 0 ? blocks.join('\n---\n\n') : '```javascript\n' + jsContent.trim() + '\n```'}
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
  const flatFiles: any[] = []

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
      flatFiles.push({
        text: extractMarkdownTitle(fullPath, slug),
        link: \`\${urlPrefix}/\${slug}\`,
        rawName: entry.name
      })
    }
  }

  // Tự động gom nhóm chuyên đề theo tiền tố nếu tài liệu ở cùng cấp
  if (flatFiles.length > 0) {
    const groups: Record<string, any[]> = {}
    for (const f of flatFiles) {
      let gKey = 'Tài liệu khác'
      if (f.rawName.startsWith('chuyen_de_1')) gKey = 'Phần 1: Ngữ Âm & Trọng Âm'
      else if (f.rawName.startsWith('chuyen_de_2')) gKey = 'Phần 2: Ngữ Pháp & Cấu Trúc'
      else if (f.rawName.startsWith('chuyen_de_3')) gKey = 'Phần 3: Từ Vựng Chọn Lọc'

      if (!groups[gKey]) groups[gKey] = []
      groups[gKey].push({ text: f.text, link: f.link })
    }

    if (Object.keys(groups).length > 1) {
      for (const [gTitle, gItems] of Object.entries(groups)) {
        items.push({
          text: gTitle,
          collapsed: false,
          items: gItems
        })
      }
    } else {
      items.push(...flatFiles.map(f => ({ text: f.text, link: f.link })))
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
import { data as lessons } from '../../data/lessons.data.ts'

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
              theme: isDark ? 'dark' : 'default',
              flowchart: {
                curve: 'basis',
                nodeSpacing: 14,
                rankSpacing: 20,
                padding: 8,
                useMaxWidth: true
              },
              themeVariables: {
                fontSize: '13px'
              }
            })
            const elements = document.querySelectorAll('.mermaid')
            if (elements.length > 0) {
              m.default.run({ nodes: elements }).then(() => {
                document.querySelectorAll('.mermaid svg').forEach(svg => {
                  svg.style.maxWidth = 'min(100%, 650px)';
                  svg.style.height = 'auto';
                  svg.style.margin = '0 auto';
                  svg.style.display = 'block';
                });
              });
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
    title: Chuyển đổi tài liệu HTML cũ
    details: Tự động trích xuất nội dung từ các trang HTML tĩnh, làm sạch mã nguồn và chuẩn hóa về định dạng Markdown.
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

const IGNORED_NAMES = new Set([
  'node_modules',
  '.git',
  '.gemini',
  '.agents',
  'docs',
  'docs-as-code-builder',
  'scratch',
  'dist',
  '.system_generated'
]);

console.log(`\n🔗 [2/2] Đang xử lý nguồn dữ liệu từ: ${SOURCE_DIR}`);

if (fs.existsSync(SOURCE_DIR)) {
  const isSelfOrParent = path.resolve(CONTENT_DEST).startsWith(path.resolve(SOURCE_DIR));
  const hasLegacyFiles = checkRequiresConversion(SOURCE_DIR);

  if (!hasLegacyFiles && !isSelfOrParent) {
    // Trường hợp thư mục nguồn nằm độc lập bên ngoài và 100% .md -> Dùng NTFS Junction (Zero-Copy)
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
    // Trường hợp nguồn là thư mục gốc (.) hoặc có file cần chuyển đổi -> Copy và xử lý an toàn
    if (fs.existsSync(CONTENT_DEST) && fs.lstatSync(CONTENT_DEST).isSymbolicLink()) {
      fs.unlinkSync(CONTENT_DEST);
    }
    ingestAndConvertDirectory(SOURCE_DIR, CONTENT_DEST);
    console.log(' ✅ Đã chuyển đổi và đồng bộ toàn bộ tài liệu về chuẩn Markdown tại docs/lessons');
  }
} else {
  console.warn(` ⚠️ Không tìm thấy thư mục nguồn "${SOURCE_DIR}". Đã tạo thư mục docs/lessons trống.`);
  fs.mkdirSync(CONTENT_DEST, { recursive: true });
}

console.log('\n======================================================================');
console.log('🎉 KHỞI TẠO THÀNH CÔNG BỘ KHUNG DOCS-AS-CODE VITEPRESS (VUE 3)!');
console.log('👉 Các bước tiếp theo để chạy web:');
console.log('   1. npm install       (Cài đặt VitePress và Vue)');
console.log('   2. npm run docs:dev  (Khởi động local server tại http://localhost:5173)');
console.log('======================================================================\n');

function checkRequiresConversion(dir) {
  const abs = path.resolve(dir);
  if (abs === CONTENT_DEST || abs === path.resolve('docs') || abs.startsWith(CONTENT_DEST)) return false;

  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.name.startsWith('.') || IGNORED_NAMES.has(e.name.toLowerCase())) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory() && checkRequiresConversion(full)) return true;
    if (e.isFile() && /\.(html?|js|ts)$/i.test(e.name)) {
      if (/Master\.html$/i.test(e.name) || /universal-docs-engine/i.test(e.name)) continue;
      return true;
    }
  }
  return false;
}

function ingestAndConvertDirectory(srcDir, destDir) {
  const absSrc = path.resolve(srcDir);
  const absDest = path.resolve(destDir);
  const absDocs = path.resolve('docs');
  // Chặn tuyệt đối đệ quy vào thư mục docs hoặc chính thư mục đích
  if (absSrc === absDest || absSrc === absDocs || absSrc.startsWith(absDest)) return;

  fs.mkdirSync(destDir, { recursive: true });
  const entries = fs.readdirSync(srcDir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.name.startsWith('.') || IGNORED_NAMES.has(entry.name.toLowerCase())) continue;
    const srcPath = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);

    if (path.resolve(srcPath) === absDocs || path.resolve(srcPath) === absDest) continue;

    if (entry.isDirectory()) {
      ingestAndConvertDirectory(srcPath, destPath);
    } else if (entry.name.endsWith('.md')) {
      // Khi nguồn là thư mục gốc, chỉ lấy các tệp bài học chuyên đề và hướng dẫn
      if (absSrc === path.resolve('.') && !entry.name.startsWith('chuyen_de_') && entry.name !== 'guide.md') {
        continue;
      }
      fs.copyFileSync(srcPath, destPath);
      console.log(`   📄 [MD] Đã sao chép: ${entry.name}`);
    } else if (/\.html?$/i.test(entry.name)) {
      if (/Master\.html$/i.test(entry.name)) {
        continue; // Bỏ qua tệp xuất bản Master HTML
      }
      const html = fs.readFileSync(srcPath, 'utf-8');
      const md = convertHardcodedHtmlToMd(html, entry.name);
      const mdDest = destPath.replace(/\.html?$/i, '.md');
      fs.writeFileSync(mdDest, md, 'utf-8');
      console.log(`   🔄 [HTML -> MD] Đã chuyển đổi: ${entry.name}`);
    } else if (/\.[jt]s$/i.test(entry.name)) {
      if (entry.name.includes('engine') || entry.name.endsWith('.config.js')) continue;
      const js = fs.readFileSync(srcPath, 'utf-8');
      const md = convertJsSourceToMd(js, entry.name);
      const mdDest = destPath.replace(/\.[jt]s$/i, '.md');
      fs.writeFileSync(mdDest, md, 'utf-8');
      console.log(`   💻 [JS -> MD] Đã trích xuất tài liệu: ${entry.name}`);
    }
  }
}