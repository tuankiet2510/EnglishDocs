<script setup lang="ts">
import { ref, computed } from 'vue'
import { useExam } from '../composables/useExamStore'

const props = withDefaults(
  defineProps<{
    total?: number
    title?: string
  }>(),
  {
    total: 36,
    title: 'Bảng Điểm Thực Chiến Phòng Thi'
  }
)

const { examStore, total, answeredCount, correctCount, score10, percentage, rank, submit, reset } = useExam(props.total)
const showResultModal = ref(false)

const progressPercent = computed(() => {
  if (total.value === 0) return 0
  return Math.min(100, Math.round((answeredCount.value / total.value) * 100))
})

function handleSubmit() {
  submit()
  showResultModal.value = true
}

function handleResetExam() {
  if (confirm('Bạn có chắc chắn muốn xóa bài làm và thi lại từ đầu?')) {
    reset()
    showResultModal.value = false
    // Cuộn lên đầu trang
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}
</script>

<template>
  <div class="exam-scoreboard-wrapper">
    <!-- KHỐI THANH TIẾN ĐỘ THỜI GIAN THỰC (STICKY/INLINE BAR) -->
    <div class="scoreboard-bar">
      <div class="bar-left">
        <span class="bar-icon">📊</span>
        <div class="progress-details">
          <div class="progress-label-row">
            <span class="p-text">Tiến độ làm bài: <strong>{{ answeredCount }} / {{ total }} câu</strong></span>
            <span class="p-percent">({{ progressPercent }}%)</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="bar-center">
        <div class="score-chip">
          <span class="chip-label">Điểm tạm tính:</span>
          <span class="chip-val">{{ score10 }} <small>/ 10.0</small></span>
        </div>
        <div class="correct-badge">
          ✅ Đúng: <strong>{{ correctCount }}</strong> / {{ answeredCount }}
        </div>
      </div>

      <div class="bar-right">
        <button class="submit-exam-btn" @click="handleSubmit">
          🎯 Nộp Bài & Xem Điểm
        </button>
      </div>
    </div>

    <!-- MODAL / POPUP BẢNG TỔNG KẾT ĐIỂM (STUDY4 ARENA STYLE) -->
    <div v-if="showResultModal" class="result-modal-backdrop" @click.self="showResultModal = false">
      <div class="result-modal-card">
        <button class="modal-close-btn" @click="showResultModal = false">✕</button>

        <div class="result-header">
          <div class="result-badge-top">KẾT QUẢ PHÒNG THI THỬ</div>
          <h2 class="result-title">{{ title }}</h2>
        </div>

        <div class="score-showcase">
          <div class="score-circle">
            <span class="big-score">{{ score10 }}</span>
            <span class="score-scale">/ 10.0</span>
          </div>
          <div class="rank-box">
            <div :class="['rank-badge', rank.class]">{{ rank.title }}</div>
            <p class="rank-advice">{{ rank.msg }}</p>
          </div>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-icon">🎯</span>
            <div class="stat-info">
              <span class="stat-num">{{ correctCount }} / {{ total }}</span>
              <span class="stat-desc">Số câu trả lời đúng</span>
            </div>
          </div>

          <div class="stat-card">
            <span class="stat-icon">❌</span>
            <div class="stat-info">
              <span class="stat-num">{{ answeredCount - correctCount }}</span>
              <span class="stat-desc">Số câu trả lời sai</span>
            </div>
          </div>

          <div class="stat-card">
            <span class="stat-icon">📈</span>
            <div class="stat-info">
              <span class="stat-num">{{ percentage }}%</span>
              <span class="stat-desc">Tỉ lệ chính xác</span>
            </div>
          </div>

          <div class="stat-card">
            <span class="stat-icon">⏳</span>
            <div class="stat-info">
              <span class="stat-num">{{ total - answeredCount }}</span>
              <span class="stat-desc">Số câu chưa làm</span>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button class="modal-btn review-btn" @click="showResultModal = false">
            🔍 Xem Lại Toàn Bộ Đáp Án & Lời Giải
          </button>
          <button class="modal-btn retry-btn" @click="handleResetExam">
            ↺ Làm Lại Đề Này
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.exam-scoreboard-wrapper {
  margin: 2rem 0;
}

.scoreboard-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.25rem;
  padding: 1.15rem 1.45rem;
  border-radius: 14px;
  background: var(--vp-c-bg-soft);
  border: 1.5px solid var(--vp-c-divider);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
  flex-wrap: wrap;
}

.bar-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex: 1 1 240px;
}

.bar-icon {
  font-size: 1.6rem;
}

.progress-details {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  width: 100%;
}

.progress-label-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.86rem;
  color: var(--vp-c-text-2);
}

.progress-track {
  width: 100%;
  height: 8px;
  background: var(--vp-c-divider);
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #10b981);
  border-radius: 9999px;
  transition: width 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.bar-center {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.score-chip {
  display: flex;
  align-items: baseline;
  gap: 0.35rem;
  background: var(--vp-c-bg);
  padding: 0.4rem 0.85rem;
  border-radius: 10px;
  border: 1px solid var(--vp-c-divider);
}

.chip-label {
  font-size: 0.78rem;
  color: var(--vp-c-text-3);
  font-weight: 500;
}

.chip-val {
  font-family: var(--vp-font-family-mono);
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--vp-c-brand-1);
}

.chip-val small {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.correct-badge {
  font-size: 0.85rem;
  font-weight: 600;
  color: #10b981;
  background: rgba(16, 185, 129, 0.08);
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  white-space: nowrap;
}

.bar-right {
  display: flex;
  align-items: center;
}

.submit-exam-btn {
  padding: 0.65rem 1.35rem;
  border-radius: 10px;
  background: var(--vp-c-brand-1);
  color: #fff;
  border: none;
  font-weight: 700;
  font-size: 0.92rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
  white-space: nowrap;
}

.submit-exam-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
}

/* MODAL RESULT */
.result-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1.5rem;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.result-modal-card {
  position: relative;
  width: 100%;
  max-width: 580px;
  background: var(--vp-c-bg);
  border: 1.5px solid var(--vp-c-divider);
  border-radius: 20px;
  padding: 2.2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-close-btn {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: all 0.2s;
}

.modal-close-btn:hover {
  color: var(--vp-c-text-1);
  transform: scale(1.1);
}

.result-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.result-badge-top {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  margin-bottom: 0.5rem;
}

.result-title {
  margin: 0 !important;
  font-family: 'Outfit', var(--vp-font-family-base);
  font-size: 1.45rem !important;
  color: var(--vp-c-text-1);
  border: none !important;
  padding: 0 !important;
}

.score-showcase {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--vp-c-bg-soft);
  border-radius: 16px;
  border: 1px solid var(--vp-c-divider);
  margin-bottom: 1.5rem;
}

.score-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #10b981);
  color: #fff;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.3);
  flex-shrink: 0;
}

.big-score {
  font-family: var(--vp-font-family-mono);
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
}

.score-scale {
  font-size: 0.75rem;
  opacity: 0.85;
}

.rank-box {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.rank-badge {
  font-size: 1.15rem;
  font-weight: 800;
  font-family: 'Outfit', var(--vp-font-family-base);
}

.rank-excellent {
  color: #10b981;
}

.rank-good {
  color: #2563eb;
}

.rank-average {
  color: #f59e0b;
}

.rank-needs-work {
  color: #ef4444;
}

.rank-advice {
  margin: 0;
  font-size: 0.88rem;
  color: var(--vp-c-text-2);
  line-height: 1.5;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.85rem;
  margin-bottom: 1.6rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
}

.stat-icon {
  font-size: 1.35rem;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-num {
  font-family: var(--vp-font-family-mono);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.stat-desc {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
}

.modal-btn {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.review-btn {
  background: var(--vp-c-brand-1);
  color: #fff;
  border: none;
}

.review-btn:hover {
  opacity: 0.92;
}

.retry-btn {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
}

.retry-btn:hover {
  color: var(--vp-c-text-1);
  border-color: var(--vp-c-text-3);
}

@media (max-width: 640px) {
  .scoreboard-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .bar-center {
    justify-content: space-between;
  }
  .score-showcase {
    flex-direction: column;
    text-align: center;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .modal-actions {
    flex-direction: column;
  }
}
</style>
