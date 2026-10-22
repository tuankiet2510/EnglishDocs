<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useData } from 'vitepress'

const { frontmatter } = useData()
const route = useRoute()

const isSidebarHidden = ref(false)
const isAsideHidden = ref(false)
const hasAsideElement = ref(false)

const checkAside = () => {
  if (typeof window === 'undefined') return
  setTimeout(() => {
    const asideEl = document.querySelector('.VPDoc .aside')
    hasAsideElement.value = !!asideEl && frontmatter.value.aside !== false
  }, 120)
}

const toggleSidebar = () => {
  isSidebarHidden.value = !isSidebarHidden.value
  if (typeof window !== 'undefined') {
    if (isSidebarHidden.value) {
      document.documentElement.classList.add('hide-sidebar')
      localStorage.setItem('englishdocs_sidebar_hidden', 'true')
    } else {
      document.documentElement.classList.remove('hide-sidebar')
      localStorage.setItem('englishdocs_sidebar_hidden', 'false')
    }
  }
}

const toggleAside = () => {
  isAsideHidden.value = !isAsideHidden.value
  if (typeof window !== 'undefined') {
    if (isAsideHidden.value) {
      document.documentElement.classList.add('hide-aside')
      localStorage.setItem('englishdocs_aside_hidden', 'true')
    } else {
      document.documentElement.classList.remove('hide-aside')
      localStorage.setItem('englishdocs_aside_hidden', 'false')
    }
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  // Ctrl+B or Cmd+B to toggle sidebar
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b' && !e.shiftKey) {
    e.preventDefault()
    toggleSidebar()
  }
  // Ctrl+Shift+O to toggle outline/aside
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'o') {
    e.preventDefault()
    toggleAside()
  }
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    const savedSidebar = localStorage.getItem('englishdocs_sidebar_hidden')
    if (savedSidebar === 'true') {
      isSidebarHidden.value = true
      document.documentElement.classList.add('hide-sidebar')
    }
    const savedAside = localStorage.getItem('englishdocs_aside_hidden')
    if (savedAside === 'true') {
      isAsideHidden.value = true
      document.documentElement.classList.add('hide-aside')
    }
    checkAside()
    window.addEventListener('keydown', handleKeydown)
  }
})

watch(() => route.path, () => {
  checkAside()
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('keydown', handleKeydown)
  }
})
</script>

<template>
  <div v-if="frontmatter.layout !== 'home'" class="layout-toggle-controls">
    <!-- Sidebar Toggle Button (Desktop Left Edge) -->
    <button
      class="layout-toggle-btn sidebar-toggle-btn"
      :class="{ 'is-collapsed': isSidebarHidden }"
      :title="isSidebarHidden ? 'Hiện danh mục bài học (Ctrl+B)' : 'Ẩn danh mục bài học (Ctrl+B)'"
      :aria-label="isSidebarHidden ? 'Hiện danh mục bài học' : 'Ẩn danh mục bài học'"
      @click="toggleSidebar"
    >
      <svg v-if="!isSidebarHidden" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="18" height="18" x="3" y="3" rx="2" />
        <path d="M9 3v18" />
        <path d="m14 9-3 3 3 3" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="18" height="18" x="3" y="3" rx="2" />
        <path d="M9 3v18" />
        <path d="m13 15 3-3-3-3" />
      </svg>
      <span class="btn-label" v-if="isSidebarHidden">Menu</span>
    </button>

    <!-- Outline Toggle Button (Desktop Right Edge) -->
    <button
      v-if="hasAsideElement"
      class="layout-toggle-btn aside-toggle-btn"
      :class="{ 'is-collapsed': isAsideHidden }"
      :title="isAsideHidden ? 'Hiện mục lục bài học (Ctrl+Shift+O)' : 'Ẩn mục lục bài học (Ctrl+Shift+O)'"
      :aria-label="isAsideHidden ? 'Hiện mục lục bài học' : 'Ẩn mục lục bài học'"
      @click="toggleAside"
    >
      <svg v-if="!isAsideHidden" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="18" height="18" x="3" y="3" rx="2" />
        <path d="M15 3v18" />
        <path d="m10 9 3 3-3 3" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="18" height="18" x="3" y="3" rx="2" />
        <path d="M15 3v18" />
        <path d="m11 15-3-3 3-3" />
      </svg>
      <span class="btn-label" v-if="isAsideHidden">Mục lục</span>
    </button>
  </div>
</template>

<style scoped>
.layout-toggle-controls {
  position: relative;
  z-index: 40;
  pointer-events: none;
}

.layout-toggle-btn {
  position: fixed;
  top: calc(var(--vp-nav-height) + 12px);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 8px;
  border-radius: 8px;
  background: var(--vp-c-bg-elv);
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  pointer-events: auto;
  font-size: 0.82rem;
  font-weight: 600;
  font-family: var(--vp-font-family-base);
  transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.layout-toggle-btn:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
  transform: translateY(-1px);
}

/* Sidebar button position */
.sidebar-toggle-btn {
  left: calc(var(--vp-sidebar-width, 280px) + 12px);
}

.sidebar-toggle-btn.is-collapsed {
  left: 14px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  border-color: rgba(37, 99, 235, 0.3);
  padding: 0 10px;
}

/* Aside button position */
.aside-toggle-btn {
  right: calc(256px + 12px);
}

.aside-toggle-btn.is-collapsed {
  right: 14px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  border-color: rgba(37, 99, 235, 0.3);
  padding: 0 10px;
}

.btn-label {
  font-size: 0.78rem;
  letter-spacing: 0.02em;
}

/* Desktop Only: hide on mobile because VitePress has mobile drawer */
@media (max-width: 959px) {
  .sidebar-toggle-btn {
    display: none !important;
  }
}

@media (max-width: 1279px) {
  .aside-toggle-btn {
    display: none !important;
  }
}
</style>
