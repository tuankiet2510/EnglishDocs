<script setup>
import { ref, computed } from 'vue'
import { withBase } from 'vitepress'
import { data as lessons } from '../../data/lessons.data.ts'

const searchQuery = ref('')
const selectedCategory = ref('Tất cả')

const CATEGORY_ORDER = [
  'Tất cả',
  'Bộ Đề Tuyển Sinh Vào 10',
  'Chuyên đề 1: Ngữ Âm & Trọng Âm',
  'Chuyên đề 2: Ngữ Pháp & Cấu Trúc',
  'Chuyên đề 3: Từ Vựng Chọn Lọc',
  'Chuyên đề 4: Biển Báo & Giao Tiếp',
  'Chuyên đề 5: Viết Luận & Đoạn Văn',
  'Chuyên đề 6: 12 Units SGK Lớp 9',
  'Cẩm Nang Phương Pháp'
]

const categories = computed(() => {
  const cats = new Set(lessons.map(l => l.category))
  const foundCats = Array.from(cats)
  
  // Sắp xếp danh mục theo thứ tự logic học tập
  return CATEGORY_ORDER.filter(c => c === 'Tất cả' || foundCats.includes(c)).concat(
    foundCats.filter(c => !CATEGORY_ORDER.includes(c))
  )
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
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Tìm kiếm chuyên đề, bài học, ngữ pháp, phát âm..." 
          class="search-input"
        />
        <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''">✕</button>
      </div>
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
      <span>Hiển thị <strong>{{ filteredLessons.length }}</strong> / {{ lessons.length }} bài giảng & chuyên đề trọng tâm</span>
    </div>

    <div class="lessons-grid">
      <a 
        v-for="item in filteredLessons" 
        :key="item.url" 
        :href="withBase(item.url)" 
        class="lesson-card"
      >
        <div class="card-header">
          <span class="badge category-badge">{{ item.category }}</span>
          <span class="badge time-badge">⏱ {{ item.readingTime }} phút đọc</span>
        </div>
        <h3 class="card-title">{{ item.title }}</h3>
        <p class="card-desc">{{ item.description }}</p>
        <div class="card-footer">
          <span class="read-more">Bắt đầu học <span class="arrow">→</span></span>
          <span class="word-count">{{ item.wordCount }} từ</span>
        </div>
      </a>
    </div>
  </div>
</template>

<style scoped>
.catalog-container {
  margin-top: 1.5rem;
}

.filter-bar {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
  margin-bottom: 1.5rem;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 1.1rem;
  font-size: 1rem;
  opacity: 0.6;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.85rem 2.5rem 0.85rem 2.85rem;
  border-radius: 12px;
  border: 1.5px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 0.95rem;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 3px var(--vp-c-brand-soft);
  background: var(--vp-c-bg);
}

.clear-btn {
  position: absolute;
  right: 1rem;
  background: transparent;
  border: none;
  font-size: 0.9rem;
  color: var(--vp-c-text-3);
  cursor: pointer;
  padding: 0.2rem 0.4rem;
}

.clear-btn:hover {
  color: var(--vp-c-text-1);
}

.category-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.pill-btn {
  padding: 0.45rem 1.05rem;
  border-radius: 9999px;
  font-size: 0.86rem;
  border: 1.5px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  font-weight: 500;
}

.pill-btn:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}

.pill-btn.active {
  background: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  color: #fff;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.catalog-summary {
  font-size: 0.88rem;
  color: var(--vp-c-text-3);
  margin-bottom: 1.35rem;
}

.lessons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.35rem;
}

.lesson-card {
  display: flex;
  flex-direction: column;
  padding: 1.45rem;
  border-radius: 14px;
  border: 1.5px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  text-decoration: none !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.02);
}

.lesson-card:hover {
  transform: translateY(-4px);
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.08);
  background: var(--vp-c-bg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.85rem;
  gap: 0.5rem;
}

.badge {
  font-size: 0.72rem;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-weight: 600;
}

.category-badge {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  max-width: 65%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.time-badge {
  color: var(--vp-c-text-3);
  font-weight: 500;
  white-space: nowrap;
}

.card-title {
  margin: 0 0 0.65rem 0;
  font-family: 'Outfit', var(--vp-font-family-base);
  font-size: 1.15rem;
  color: var(--vp-c-text-1);
  font-weight: 700;
  line-height: 1.45;
}

.card-desc {
  font-size: 0.88rem;
  color: var(--vp-c-text-2);
  flex-grow: 1;
  margin-bottom: 1.25rem;
  line-height: 1.65;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 0.85rem;
}

.read-more {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.arrow {
  transition: transform 0.2s ease;
}

.lesson-card:hover .arrow {
  transform: translateX(4px);
}

.word-count {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}
</style>
