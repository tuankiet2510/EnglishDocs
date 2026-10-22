import { createContentLoader } from 'vitepress'

const MODULE_NAMES: Record<string, string> = {
  "chuyen_de_1": "Chuyên đề 1: Ngữ Âm & Trọng Âm",
  "chuyen_de_2": "Chuyên đề 2: Ngữ Pháp & Cấu Trúc",
  "chuyen_de_3": "Chuyên đề 3: Từ Vựng Chọn Lọc",
  "chuyen_de_4": "Chuyên đề 4: Biển Báo & Giao Tiếp",
  "chuyen_de_5": "Chuyên đề 5: Viết Luận & Đoạn Văn",
  "chuyen_de_6": "Chuyên đề 6: 12 Units SGK Lớp 9",
  "guide": "Cẩm Nang Phương Pháp",
  "exams": "Bộ Đề Tuyển Sinh Vào 10"
}

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

export default createContentLoader(['lessons/**/*.md', 'exams/**/*.md'], {
  includeSrc: true,
  transform(raw): LessonMeta[] {
    return raw
      .filter(({ url }) => {
        if (!url || url.endsWith('/lessons/') || url.endsWith('/exams/') || url.toLowerCase().endsWith('/readme.html')) return false
        // Lọc bỏ các thư mục tạm / UUID Notion / superpowers
        if (url.includes('c674a7bc') || url.includes('ExportBlock') || url.includes('superpowers')) return false
        return true
      })
      .map(({ url, frontmatter, src }) => {
        const parts = url.split('/')
        const fileName = parts[parts.length - 1] || ''

        let catKey = 'general'
        if (fileName.startsWith('chuyen_de_1')) catKey = 'chuyen_de_1'
        else if (fileName.startsWith('chuyen_de_2')) catKey = 'chuyen_de_2'
        else if (fileName.startsWith('chuyen_de_3')) catKey = 'chuyen_de_3'
        else if (fileName.startsWith('chuyen_de_4')) catKey = 'chuyen_de_4'
        else if (fileName.startsWith('chuyen_de_5')) catKey = 'chuyen_de_5'
        else if (fileName.startsWith('chuyen_de_6')) catKey = 'chuyen_de_6'
        else if (fileName.startsWith('guide')) catKey = 'guide'
        else if (fileName.includes('exam') || fileName.includes('de_thi') || fileName.includes('qng') || fileName.includes('36_cau') || fileName.includes('45_cau')) catKey = 'exams'

        const category = frontmatter.category || MODULE_NAMES[catKey] || 'Tài Liệu Chung'

        let title = frontmatter.title
        if (!title && src) {
          const match = src.match(/^#\s+(.+)$/m)
          if (match) title = match[1].replace(/[\x60*]/g, '').trim()
        }
        if (!title) {
          title = fileName.replace('.html', '').replace(/[-_]/g, ' ') || 'Tài liệu'
        }

        const wordCount = (src || '').trim().split(/\s+/).length
        const readingTime = Math.max(1, Math.ceil(wordCount / 200))

        let description = frontmatter.description
        if (!description && src) {
          const cleanSrc = src.replace(/^---[\s\S]*?---/, '')
          const lines = cleanSrc.split('\n')
          for (const rawLine of lines) {
            let line = rawLine.trim()
            if (!line || line.startsWith('#') || line.startsWith('```') || line.startsWith('|') || line.startsWith('---')) continue

            // Làm sạch cú pháp Notion / Callout
            line = line.replace(/^>\s*(\[![\w-]+\])?\s*/i, '')
            line = line.replace(/\*\*([^*]+)\*\*/g, '$1')
            line = line.replace(/\*([^*]+)\*/g, '$1')
            line = line.replace(/`([^`]+)`/g, '$1')
            line = line.replace(/^[-*]\s+/, '')
            line = line.trim()

            if (line.length > 25) {
              description = line.slice(0, 160) + (line.length > 160 ? '...' : '')
              break
            }
          }
        }

        return {
          title,
          description: description || 'Tài liệu luyện thi chuyên sâu vào lớp 10 theo chuẩn chương trình GDPT mới.',
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
