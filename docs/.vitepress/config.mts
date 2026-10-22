import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

const MODULE_NAMES: Record<string, string> = {
  "chuyen_de_1": "Phần 1: Ngữ Âm & Trọng Âm",
  "chuyen_de_2": "Phần 2: Ngữ Pháp & Cấu Trúc Trọng Tâm",
  "chuyen_de_3": "Phần 3: Từ Vựng Chọn Lọc",
  "guide": "Cẩm Nang Phương Pháp",
  "exams": "Bộ Đề Tuyển Sinh Vào 10"
}

function formatFolderName(name: string): string {
  if (MODULE_NAMES[name]) return MODULE_NAMES[name]
  const clean = name.replace(/^\d+[-_]/, '').replace(/[-_]/g, ' ')
  const prefix = name.match(/^(\d+)[-_]/)?.[1]
  const capitalized = clean.charAt(0).toUpperCase() + clean.slice(1)
  return prefix ? `${parseInt(prefix)}. ${capitalized}` : capitalized
}

function extractMarkdownTitle(filePath: string, fallbackName: string): string {
  try {
    const content = fs.readFileSync(filePath, 'utf-8')
    const fmMatch = content.match(/^---\r?\n[\s\S]*?title:\s*(.*?)\r?\n[\s\S]*?---/)
    const h1Match = content.match(/^#\s+(.+)$/m)
    const raw = fmMatch ? fmMatch[1] : (h1Match ? h1Match[1] : fallbackName)
    return raw.trim().replace(/^['"](.*)['"]$/, '$1').replace(/[\x60*]/g, '').trim()
  } catch {
    return fallbackName
  }
}

// Hàm đệ quy quét thư mục đa tầng để dựng Sidebar
function scanDirectoryRecursive(dirPath: string, urlPrefix: string): any[] {
  if (!fs.existsSync(dirPath)) return []
  const entries = fs.readdirSync(dirPath, { withFileTypes: true })
    .filter(e => !e.name.startsWith('.') && !e.name.includes('c674a7bc') && !e.name.includes('ExportBlock') && e.name !== 'superpowers')
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }))

  const items: any[] = []
  const flatFiles: any[] = []

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name)
    if (entry.isDirectory()) {
      const children = scanDirectoryRecursive(fullPath, `${urlPrefix}/${entry.name}`)
      if (children.length > 0) {
        items.push({
          text: formatFolderName(entry.name),
          collapsed: false,
          items: children
        })
      }
    } else if (entry.isFile() && entry.name.endsWith('.md') && entry.name.toLowerCase() !== 'readme.md') {
      const slug = entry.name.replace(/\.md$/, '')
      flatFiles.push({
        text: extractMarkdownTitle(fullPath, slug),
        link: `${urlPrefix}/${slug}`,
        rawName: entry.name
      })
    }
  }

  // Tự động gom nhóm chuyên đề theo tiền tố nếu tài liệu ở cùng cấp
  if (flatFiles.length > 0) {
    const groups: Record<string, any[]> = {}
    for (const f of flatFiles) {
      let gKey = 'Tài liệu bổ trợ'
      if (f.rawName.startsWith('chuyen_de_1')) gKey = 'Phần 1: Ngữ Âm & Trọng Âm'
      else if (f.rawName.startsWith('chuyen_de_2')) gKey = 'Phần 2: Ngữ Pháp & Cấu Trúc'
      else if (f.rawName.startsWith('chuyen_de_3')) gKey = 'Phần 3: Từ Vựng Chọn Lọc'
      else if (f.rawName.startsWith('chuyen_de_4')) gKey = 'Phần 4: Biển Báo & Giao Tiếp Thực Tế'
      else if (f.rawName.startsWith('chuyen_de_5')) gKey = 'Phần 5: Kỹ Năng Viết Luận & Đoạn Văn'
      else if (f.rawName.startsWith('chuyen_de_6')) gKey = 'Phần 6: Trọng Tâm 12 Units SGK Lớp 9'
      else if (f.rawName.startsWith('guide')) gKey = 'Cẩm Nang Phương Pháp'
      else if (f.rawName.includes('quang_ngai') || f.rawName.includes('da_nang')) gKey = '🏛️ Đề Thi Chính Thức Sở GD&ĐT'
      else if (f.rawName.includes('hoc_ky')) gKey = '📖 Đề Thi Học Kỳ Lớp 9'
      else if (f.rawName.includes('36_cau')) gKey = '📚 Bộ Đề Form 36 Câu (Quảng Ngãi)'
      else if (f.rawName.includes('45_cau')) gKey = '📝 Bộ Đề Form 45 Câu Tuyển Sinh'

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
  base: process.env.GITHUB_ACTIONS ? '/EnglishDocs/' : '/',
  title: "Cẩm Nang Tiếng Anh Vào 10",
  description: "Cổng tài liệu kỹ thuật chuẩn hóa theo kiến trúc Docs-as-Code",
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
          return `<pre class="mermaid">${token.content}</pre>`
        }
        return defaultFence(tokens, idx, options, env, slf)
      }
    }
  },

  themeConfig: {
    siteTitle: "Cẩm Nang Tiếng Anh Vào 10",
    nav: [
      { text: 'Trang chủ', link: '/' },
      { text: 'Toàn bộ danh mục 📚', link: '/catalog' },
      { text: 'Luyện đề thi thử 🎯', link: '/exams/' }
    ],
    sidebar: {
      '/lessons/': scanDirectoryRecursive(path.resolve(__dirname, '../lessons'), '/lessons'),
      '/exams/': scanDirectoryRecursive(path.resolve(__dirname, '../exams'), '/exams')
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
