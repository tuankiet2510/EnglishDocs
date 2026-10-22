import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import LessonCatalog from './components/LessonCatalog.vue'
import QuizItem from './components/QuizItem.vue'
import ExamHeader from './components/ExamHeader.vue'
import ExamScoreboard from './components/ExamScoreboard.vue'
import LayoutToggles from './components/LayoutToggles.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'layout-bottom': () => h(LayoutToggles)
    })
  },
  enhanceApp({ app, router }) {
    app.component('LessonCatalog', LessonCatalog)
    app.component('QuizItem', QuizItem)
    app.component('ExamHeader', ExamHeader)
    app.component('ExamScoreboard', ExamScoreboard)
    app.component('LayoutToggles', LayoutToggles)

    if (typeof window !== 'undefined') {
      import('mermaid').then(m => {
        let isRendering = false
        let observerAttached = false

        const renderDiagrams = (force = false) => {
          if (isRendering) return
          isRendering = true

          setTimeout(() => {
            try {
              const isDark = document.documentElement.classList.contains('dark')
              m.default.initialize({
                startOnLoad: false,
                theme: 'base',
                flowchart: {
                  curve: 'basis',
                  nodeSpacing: 16,
                  rankSpacing: 24,
                  padding: 10,
                  useMaxWidth: true
                },
                themeVariables: isDark ? {
                  darkMode: true,
                  background: '#111827',
                  primaryColor: '#1e293b',
                  primaryTextColor: '#f8fafc',
                  primaryBorderColor: '#3b82f6',
                  lineColor: '#64748b',
                  secondaryColor: '#0f172a',
                  secondaryTextColor: '#f8fafc',
                  secondaryBorderColor: '#10b981',
                  tertiaryColor: '#1e1b4b',
                  tertiaryTextColor: '#f8fafc',
                  tertiaryBorderColor: '#8b5cf6',
                  textColor: '#f8fafc',
                  mainBkg: '#1e293b',
                  nodeBorder: '#3b82f6',
                  nodeTextColor: '#f8fafc',
                  edgeLabelBackground: '#1e293b',
                  fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
                  fontSize: '13px'
                } : {
                  darkMode: false,
                  background: '#f8fafc',
                  primaryColor: '#eff6ff',
                  primaryTextColor: '#0f172a',
                  primaryBorderColor: '#2563eb',
                  lineColor: '#94a3b8',
                  secondaryColor: '#f0fdf4',
                  secondaryTextColor: '#065f46',
                  secondaryBorderColor: '#10b981',
                  tertiaryColor: '#fffbeb',
                  tertiaryTextColor: '#92400e',
                  tertiaryBorderColor: '#f59e0b',
                  textColor: '#0f172a',
                  mainBkg: '#ffffff',
                  nodeBorder: '#cbd5e1',
                  nodeTextColor: '#0f172a',
                  edgeLabelBackground: '#ffffff',
                  fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
                  fontSize: '13px'
                }
              })

              const elements = document.querySelectorAll('.mermaid')
              if (elements.length > 0) {
                elements.forEach(el => {
                  if (!el.getAttribute('data-original-code')) {
                    el.setAttribute('data-original-code', el.textContent || '')
                  } else if (force) {
                    el.removeAttribute('data-processed')
                    el.innerHTML = el.getAttribute('data-original-code') || ''
                  }
                })

                m.default.run({ nodes: elements }).then(() => {
                  document.querySelectorAll('.mermaid svg').forEach(svg => {
                    svg.style.maxWidth = 'min(100%, 750px)'
                    svg.style.height = 'auto'
                    svg.style.margin = '0 auto'
                    svg.style.display = 'block'
                  })
                }).catch(err => {
                  console.warn('Mermaid rendering error:', err)
                }).finally(() => {
                  isRendering = false
                })
              } else {
                isRendering = false
              }
            } catch (e) {
              isRendering = false
            }
          }, 80)
        }

        router.onAfterRouteChanged = () => renderDiagrams(false)
        window.addEventListener('load', () => renderDiagrams(false))

        if (!observerAttached) {
          observerAttached = true
          const observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
              if (mutation.attributeName === 'class') {
                renderDiagrams(true)
                break
              }
            }
          })
          observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
          })
        }
      }).catch(err => {
        console.warn('Mermaid chưa được cài đặt hoặc bỏ qua:', err)
      })
    }
  }
}

