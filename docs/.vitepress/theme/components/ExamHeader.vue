<script setup lang="ts">
import { ref, onUnmounted, computed } from 'vue'

const props = withDefaults(
  defineProps<{
    title: string
    province?: string
    year?: string
    duration?: number
    total?: number
    grade?: string
  }>(),
  {
    province: 'Sở GD&ĐT Quảng Ngãi',
    year: '2026 - 2027',
    duration: 60,
    total: 36,
    grade: 'Lớp 10 THPT'
  }
)

const isTimerRunning = ref(false)
const secondsLeft = ref(props.duration * 60)
let timerInterval: any = null

const formattedTime = computed(() => {
  const m = Math.floor(secondsLeft.value / 60)
  const s = secondsLeft.value % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

const isTimeLow = computed(() => secondsLeft.value <= 300 && isTimerRunning.value)

function toggleTimer() {
  if (isTimerRunning.value) {
    clearInterval(timerInterval)
    isTimerRunning.value = false
  } else {
    isTimerRunning.value = true
    timerInterval = setInterval(() => {
      if (secondsLeft.value > 0) {
        secondsLeft.value--
      } else {
        clearInterval(timerInterval)
        isTimerRunning.value = false
        alert('⏰ Đã hết thời gian làm bài thi!')
      }
    }, 1000)
  }
}

function resetTimer() {
  clearInterval(timerInterval)
  isTimerRunning.value = false
  secondsLeft.value = props.duration * 60
}

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})
</script>

<template>
  <div class="exam-header-card">
    <div class="exam-top-row">
      <div class="exam-authority">
        <span class="province-badge">🏛️ {{ province }}</span>
        <span class="exam-grade">Kỳ Thi Tuyển Sinh {{ grade }}</span>
      </div>
      <div class="exam-year-tag">{{ year }}</div>
    </div>

    <h1 class="exam-main-title">{{ title }}</h1>

    <div class="exam-meta-grid">
      <div class="meta-item">
        <span class="meta-icon">🎯</span>
        <div class="meta-text">
          <span class="meta-label">Số lượng câu hỏi</span>
          <span class="meta-val">{{ total }} câu</span>
        </div>
      </div>

      <div class="meta-item">
        <span class="meta-icon">⏱️</span>
        <div class="meta-text">
          <span class="meta-label">Thời gian làm bài</span>
          <span class="meta-val">{{ duration }} phút</span>
        </div>
      </div>

      <div class="meta-item">
        <span class="meta-icon">📘</span>
        <div class="meta-text">
          <span class="meta-label">Chương trình</span>
          <span class="meta-val">Chuẩn GDPT 2018</span>
        </div>
      </div>

      <!-- ĐỒNG HỒ BẤM GIỜ THỰC CHIẾN -->
      <div :class="['timer-box', { 'is-running': isTimerRunning, 'is-low': isTimeLow }]">
        <div class="timer-display">
          <span class="timer-icon">⏳</span>
          <span class="timer-digits">{{ formattedTime }}</span>
        </div>
        <div class="timer-controls">
          <button class="timer-btn toggle-btn" @click="toggleTimer">
            {{ isTimerRunning ? '⏸ Tạm dừng' : '▶ Bắt đầu tính giờ' }}
          </button>
          <button v-if="secondsLeft < duration * 60" class="timer-btn reset-btn" @click="resetTimer">
            ↺ Đặt lại
          </button>
        </div>
      </div>
    </div>

    <div class="exam-instructions-alert">
      <span class="alert-icon">💡</span>
      <div class="alert-text">
        <strong>Hướng dẫn phòng thi:</strong> Học sinh click vào từng phương án A, B, C, D để làm bài và kiểm tra kiến thức tức thì. Đối với dạng tự luận viết lại câu, hãy nhập câu trả lời vào ô trống trước khi đối chiếu đáp án mẫu chuẩn barem chấm điểm của Sở GD&ĐT.
      </div>
    </div>
  </div>
</template>

<style scoped>
.exam-header-card {
  margin: 1.5rem 0 2rem 0;
  padding: 1.6rem 1.85rem;
  border-radius: 16px;
  background: var(--vp-c-bg-soft);
  border: 1.5px solid var(--vp-c-divider);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.exam-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.85rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.exam-authority {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.85rem;
}

.province-badge {
  font-weight: 700;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  padding: 0.25rem 0.65rem;
  border-radius: 8px;
}

.exam-grade {
  color: var(--vp-c-text-2);
  font-weight: 600;
}

.exam-year-tag {
  font-size: 0.82rem;
  font-weight: 700;
  color: #fff;
  background: var(--vp-c-brand-1);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  letter-spacing: 0.03em;
}

.exam-main-title {
  margin: 0.5rem 0 1.25rem 0 !important;
  font-family: 'Outfit', var(--vp-font-family-base);
  font-size: 1.85rem !important;
  line-height: 1.35 !important;
  color: var(--vp-c-text-1);
  border: none !important;
  padding: 0 !important;
}

.exam-meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--vp-c-divider);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
}

.meta-icon {
  font-size: 1.5rem;
}

.meta-text {
  display: flex;
  flex-direction: column;
}

.meta-label {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
  font-weight: 500;
}

.meta-val {
  font-size: 0.98rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

/* TIMER BOX */
.timer-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.65rem 1rem;
  border-radius: 12px;
  background: var(--vp-c-bg);
  border: 1.5px solid var(--vp-c-brand-1);
  gap: 0.75rem;
}

.timer-box.is-running {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.timer-box.is-low {
  border-color: #ef4444 !important;
  background: rgba(239, 68, 68, 0.08) !important;
  animation: pulse 1s infinite alternate;
}

@keyframes pulse {
  from { opacity: 0.85; }
  to { opacity: 1; }
}

.timer-display {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.timer-digits {
  font-family: var(--vp-font-family-mono);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--vp-c-brand-1);
}

.timer-box.is-running .timer-digits {
  color: #10b981;
}

.timer-box.is-low .timer-digits {
  color: #ef4444;
}

.timer-controls {
  display: flex;
  gap: 0.4rem;
}

.timer-btn {
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
  white-space: nowrap;
}

.toggle-btn {
  background: var(--vp-c-brand-1);
  color: #fff;
}

.timer-box.is-running .toggle-btn {
  background: #f59e0b;
}

.reset-btn {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
}

/* INSTRUCTIONS ALERT */
.exam-instructions-alert {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.85rem 1.15rem;
  border-radius: 10px;
  background: rgba(37, 99, 235, 0.06);
  border-left: 4px solid var(--vp-c-brand-1);
  font-size: 0.88rem;
  line-height: 1.6;
  color: var(--vp-c-text-1);
}

.alert-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}
</style>
