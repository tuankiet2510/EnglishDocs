<script setup lang="ts">
import { ref, computed } from 'vue'
import { examStore } from '../composables/useExamStore'

export interface OptionItem {
  key: string
  text: string
  ipa?: string
}

const props = withDefaults(
  defineProps<{
    number: number | string
    question?: string
    type?: 'choice' | 'transform'
    options?: (OptionItem | string)[] | string
    correct?: string
    explanation?: string
    targetPrompt?: string
    sampleAnswer?: string
    skill?: string
  }>(),
  {
    type: 'choice',
    question: '',
    explanation: '',
    targetPrompt: '',
    sampleAnswer: '',
    skill: 'General'
  }
)

const selectedKey = ref<string | null>(null)
const showExplanation = ref(false)
const userTransformText = ref('')
const showTransformAnswer = ref(false)

// Format markdown bold/underline cho chữ cái trọng tâm phát âm
function formatInlineMarkdown(raw: string): string {
  if (!raw) return ''
  return raw
    .replace(/\*\*([^*]+)\*\*/g, '<u class="quiz-target-char"><strong>$1</strong></u>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code class="quiz-inline-code">$1</code>')
}

// Chuẩn hóa danh sách Options từ nhiều định dạng đầu vào (mảng object, mảng string, chuỗi "A. x | B. y")
const parsedOptions = computed<OptionItem[]>(() => {
  if (!props.options) return []

  if (typeof props.options === 'string') {
    // Parse chuỗi dạng: "A. bad | B. man | C. pan | D. bed"
    const parts = props.options.split('|').map(s => s.trim())
    return parts.map((part, idx) => {
      const match = part.match(/^([A-D])\.\s*(.+)$/i)
      if (match) {
        return { key: match[1].toUpperCase(), text: formatInlineMarkdown(match[2].trim()) }
      }
      const defaultKey = String.fromCharCode(65 + idx)
      return { key: defaultKey, text: formatInlineMarkdown(part) }
    })
  }

  if (Array.isArray(props.options)) {
    return props.options.map((item, idx) => {
      if (typeof item === 'string') {
        const match = item.match(/^([A-D])\.\s*(.+)$/i)
        if (match) {
          return { key: match[1].toUpperCase(), text: formatInlineMarkdown(match[2].trim()) }
        }
        return { key: String.fromCharCode(65 + idx), text: formatInlineMarkdown(item) }
      }
      return { ...item, text: formatInlineMarkdown(item.text) }
    })
  }

  return []
})

const isAnswered = computed(() => selectedKey.value !== null)
const isCorrect = computed(() => {
  if (!selectedKey.value || !props.correct) return false
  return selectedKey.value.trim().toUpperCase() === props.correct.trim().toUpperCase()
})

function handleSelect(key: string) {
  selectedKey.value = key
  // Khi học sinh chọn, tự động mở phần giải thích để học tập hiệu quả
  showExplanation.value = true
  const correctMatch = props.correct ? key.trim().toUpperCase() === props.correct.trim().toUpperCase() : false
  examStore.recordAnswer(props.number, correctMatch, props.skill)
}

function handleReset() {
  selectedKey.value = null
  showExplanation.value = false
  userTransformText.value = ''
  showTransformAnswer.value = false
  if (examStore.questions[String(props.number)]) {
    delete examStore.questions[String(props.number)]
  }
}

// Phát âm từ vựng tiếng Anh bằng Web Speech API
function playAudio(text: string, event?: Event) {
  if (event) event.stopPropagation()
  if (typeof window === 'undefined' || !window.speechSynthesis) return

  window.speechSynthesis.cancel() // Dừng câu đang đọc dở nếu có
  const cleanWord = text.replace(/[*_`]/g, '').trim()
  const utterance = new SpeechSynthesisUtterance(cleanWord)
  utterance.lang = 'en-US'
  utterance.rate = 0.88 // Tốc độ hơi chậm một chút để nghe rõ ngữ âm
  window.speechSynthesis.speak(utterance)
}
</script>

<template>
  <div :class="['study4-quiz-card', { 'is-answered': isAnswered, 'is-correct': isCorrect, 'is-wrong': isAnswered && !isCorrect }]">
    <!-- Header của câu hỏi -->
    <div class="card-top-bar">
      <div class="badge-group">
        <span class="quiz-num-badge">Câu {{ number }}</span>
        <span v-if="type === 'choice'" class="quiz-type-tag">Trắc nghiệm</span>
        <span v-else class="quiz-type-tag transform-tag">Viết lại câu</span>
      </div>
      <div class="card-actions">
        <button v-if="isAnswered || showTransformAnswer" class="action-btn reset-btn" title="Làm lại câu này" @click="handleReset">
          ↺ Làm lại
        </button>
      </div>
    </div>

    <!-- Nội dung đề bài -->
    <div v-if="question" class="quiz-question-stem">
      <span class="stem-text" v-html="formatInlineMarkdown(question)"></span>
    </div>

    <!-- DẠNG 1: TRẮC NGHIỆM 4 LỰA CHỌN (A, B, C, D) -->
    <div v-if="type === 'choice'" class="options-grid">
      <div
        v-for="opt in parsedOptions"
        :key="opt.key"
        :class="[
          'option-pill',
          {
            'selected': selectedKey === opt.key,
            'correct-answer': (selectedKey === opt.key && isCorrect) || (isAnswered && !isCorrect && opt.key === correct),
            'wrong-answer': selectedKey === opt.key && !isCorrect
          }
        ]"
        @click="handleSelect(opt.key)"
      >
        <div class="opt-label-circle">{{ opt.key }}</div>
        <div class="opt-content">
          <span class="opt-text" v-html="opt.text"></span>
          <span v-if="opt.ipa" class="opt-ipa">{{ opt.ipa }}</span>
        </div>
        <!-- Nút loa phát âm độc lập cho từng từ -->
        <button
          class="audio-speaker-btn"
          title="Nghe phát âm chuẩn"
          @click="playAudio(opt.text, $event)"
        >
          🔊
        </button>
      </div>
    </div>

    <!-- DẠNG 2: VIẾT LẠI CÂU (SENTENCE TRANSFORMATION) -->
    <div v-else class="transform-container">
      <div v-if="targetPrompt" class="prompt-guide">
        <span class="prompt-icon">✍️</span>
        <span class="prompt-label">Gợi ý bắt đầu:</span>
        <code class="prompt-code">{{ targetPrompt }}</code>
      </div>
      <div class="transform-input-row">
        <input
          v-model="userTransformText"
          type="text"
          class="transform-input"
          placeholder="Nhập câu viết lại hoàn chỉnh của bạn..."
        />
        <button
          class="show-answer-btn"
          @click="showTransformAnswer = !showTransformAnswer"
        >
          {{ showTransformAnswer ? 'Ẩn đáp án' : 'Xem đáp án mẫu' }}
        </button>
      </div>

      <div v-if="showTransformAnswer && sampleAnswer" class="sample-answer-box">
        <div class="sample-label">✅ Câu viết lại chuẩn cấu trúc:</div>
        <div class="sample-text">{{ sampleAnswer }}</div>
      </div>
    </div>

    <!-- Trạng thái phản hồi nhanh sau khi chọn -->
    <div v-if="isAnswered && type === 'choice'" class="feedback-status-banner">
      <div v-if="isCorrect" class="feedback-badge correct">
        <span class="feedback-icon">🎉</span>
        <span>Chính xác! Đáp án <strong>{{ correct }}</strong> là câu trả lời đúng.</span>
      </div>
      <div v-else class="feedback-badge wrong">
        <span class="feedback-icon">💡</span>
        <span>Chưa chính xác! Bạn đã chọn <strong>{{ selectedKey }}</strong>. Đáp án đúng là <strong>{{ correct }}</strong>.</span>
      </div>
    </div>

    <!-- ACCORDION GIẢI THÍCH CHI TIẾT (STUDY4 STYLE) -->
    <div v-if="explanation || $slots.explanation" class="explanation-accordion">
      <button class="toggle-explanation-btn" @click="showExplanation = !showExplanation">
        <span class="exp-title">
          <span class="bulb-icon">📘</span>
          <span>Phân tích đáp án & Cạm bẫy phòng thi</span>
        </span>
        <span :class="['chevron-icon', { 'open': showExplanation }]">▼</span>
      </button>

      <div v-show="showExplanation" class="explanation-body">
        <div v-if="explanation" class="exp-text" v-html="formatInlineMarkdown(explanation)"></div>
        <slot name="explanation"></slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
:deep(.quiz-target-char) {
  text-decoration: underline 2.5px var(--vp-c-brand-1);
  text-underline-offset: 3px;
  color: var(--vp-c-brand-1);
  font-weight: 700;
}

:deep(.quiz-inline-code) {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  padding: 0.12rem 0.38rem;
  border-radius: 5px;
  font-size: 0.88em;
  font-family: var(--vp-font-family-mono);
}

.study4-quiz-card {
  margin: 1.5rem 0;
  padding: 1.25rem 1.4rem;
  border-radius: 14px;
  background: var(--vp-c-bg-soft);
  border: 1.5px solid var(--vp-c-divider);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.03);
}

.study4-quiz-card:hover {
  border-color: var(--vp-c-brand-1);
}

.study4-quiz-card.is-correct {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.04);
}

.study4-quiz-card.is-wrong {
  border-color: #f59e0b;
  background: rgba(245, 158, 11, 0.04);
}

.card-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.85rem;
}

.badge-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quiz-num-badge {
  font-size: 0.8rem;
  font-weight: 700;
  color: #fff;
  background: var(--vp-c-brand-1);
  padding: 0.25rem 0.65rem;
  border-radius: 8px;
  letter-spacing: 0.02em;
}

.quiz-type-tag {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
}

.transform-tag {
  color: #8b5cf6;
  background: rgba(139, 92, 246, 0.12);
}

.action-btn {
  font-size: 0.78rem;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
}

.quiz-question-stem {
  font-size: 1.02rem;
  font-weight: 600;
  line-height: 1.6;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
}

/* GRID TÙY CHỌN A, B, C, D */
.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1rem;
}

@media (max-width: 640px) {
  .options-grid {
    grid-template-columns: 1fr;
  }
}

.option-pill {
  display: flex;
  align-items: center;
  padding: 0.65rem 0.85rem;
  border-radius: 10px;
  background: var(--vp-c-bg);
  border: 1.5px solid var(--vp-c-divider);
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  gap: 0.75rem;
}

.option-pill:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1.5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.opt-label-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--vp-c-bg-soft);
  border: 1.5px solid var(--vp-c-divider);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--vp-c-text-2);
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.opt-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.opt-text {
  font-size: 0.95rem;
  color: var(--vp-c-text-1);
  font-weight: 500;
}

.opt-ipa {
  font-size: 0.75rem;
  color: var(--vp-c-brand-1);
  font-family: var(--vp-font-family-mono);
}

.audio-speaker-btn {
  background: transparent;
  border: none;
  font-size: 0.95rem;
  cursor: pointer;
  padding: 0.2rem 0.35rem;
  border-radius: 6px;
  opacity: 0.6;
  transition: all 0.15s ease;
}

.audio-speaker-btn:hover {
  opacity: 1;
  background: var(--vp-c-bg-soft);
  transform: scale(1.15);
}

/* ĐÁP ÁN ĐÚNG / SAI */
.option-pill.correct-answer {
  border-color: #10b981 !important;
  background: rgba(16, 185, 129, 0.12) !important;
}

.option-pill.correct-answer .opt-label-circle {
  background: #10b981;
  color: #fff;
  border-color: #10b981;
}

.option-pill.wrong-answer {
  border-color: #ef4444 !important;
  background: rgba(239, 68, 68, 0.12) !important;
}

.option-pill.wrong-answer .opt-label-circle {
  background: #ef4444;
  color: #fff;
  border-color: #ef4444;
}

/* FEEDBACK BANNER */
.feedback-status-banner {
  margin-bottom: 0.85rem;
}

.feedback-badge {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 0.95rem;
  border-radius: 9px;
  font-size: 0.88rem;
  font-weight: 500;
}

.feedback-badge.correct {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.feedback-badge.wrong {
  background: rgba(245, 158, 11, 0.12);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

/* DẠNG BÀI VIẾT LẠI CÂU */
.transform-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.prompt-guide {
  font-size: 0.88rem;
  color: var(--vp-c-text-2);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.prompt-code {
  background: var(--vp-c-bg);
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  color: var(--vp-c-brand-1);
  font-weight: 600;
}

.transform-input-row {
  display: flex;
  gap: 0.6rem;
}

.transform-input {
  flex-grow: 1;
  padding: 0.65rem 0.95rem;
  border-radius: 9px;
  border: 1.5px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.92rem;
  outline: none;
}

.transform-input:focus {
  border-color: var(--vp-c-brand-1);
}

.show-answer-btn {
  padding: 0.65rem 1rem;
  border-radius: 9px;
  background: var(--vp-c-brand-1);
  color: #fff;
  border: none;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s ease;
}

.show-answer-btn:hover {
  opacity: 0.9;
}

.sample-answer-box {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-left: 4px solid #10b981;
  padding: 0.75rem 0.95rem;
  border-radius: 8px;
}

.sample-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #10b981;
  margin-bottom: 0.25rem;
}

.sample-text {
  font-size: 0.92rem;
  color: var(--vp-c-text-1);
  font-weight: 500;
}

/* ACCORDION GIẢI THÍCH CHI TIẾT */
.explanation-accordion {
  border-top: 1px dashed var(--vp-c-divider);
  padding-top: 0.85rem;
  margin-top: 0.5rem;
}

.toggle-explanation-btn {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: transparent;
  border: none;
  padding: 0.4rem 0;
  cursor: pointer;
  color: var(--vp-c-text-2);
  font-size: 0.88rem;
  font-weight: 600;
  transition: color 0.2s ease;
}

.toggle-explanation-btn:hover {
  color: var(--vp-c-brand-1);
}

.exp-title {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.chevron-icon {
  font-size: 0.7rem;
  transition: transform 0.25s ease;
}

.chevron-icon.open {
  transform: rotate(180deg);
}

.explanation-body {
  margin-top: 0.75rem;
  padding: 0.95rem 1.15rem;
  background: var(--vp-c-bg);
  border-radius: 10px;
  border: 1px solid var(--vp-c-divider);
  font-size: 0.9rem;
  line-height: 1.65;
  color: var(--vp-c-text-1);
}
</style>
