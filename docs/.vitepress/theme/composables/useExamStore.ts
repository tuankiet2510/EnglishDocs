import { reactive, computed } from 'vue'

export interface QuestionRecord {
  number: number | string
  answered: boolean
  isCorrect: boolean
  skill?: string
}

// Global reactive exam state
export const examStore = reactive({
  questions: {} as Record<string, QuestionRecord>,
  isSubmitted: false,

  reset() {
    this.questions = {}
    this.isSubmitted = false
  },

  recordAnswer(number: number | string, isCorrect: boolean, skill?: string) {
    this.questions[String(number)] = {
      number,
      answered: true,
      isCorrect,
      skill: skill || 'General'
    }
  },

  submit() {
    this.isSubmitted = true
  }
})

export function useExam(totalQuestions: number = 36) {
  const total = computed(() => totalQuestions)
  
  const answeredCount = computed(() => {
    return Object.values(examStore.questions).filter(q => q.answered).length
  })

  const correctCount = computed(() => {
    return Object.values(examStore.questions).filter(q => q.isCorrect).length
  })

  const score10 = computed(() => {
    if (total.value === 0) return '0.0'
    const sc = (correctCount.value / total.value) * 10
    return sc.toFixed(1)
  })

  const percentage = computed(() => {
    if (total.value === 0) return 0
    return Math.round((correctCount.value / total.value) * 100)
  })

  const rank = computed(() => {
    const sc = parseFloat(score10.value)
    if (sc >= 8.5) return { title: 'Xuất Sắc 🏆', class: 'rank-excellent', msg: 'Kiến thức rất vững vàng! Sẵn sàng chinh phục trường chuyên / lớp chọn.' }
    if (sc >= 7.0) return { title: 'Giỏi ⭐', class: 'rank-good', msg: 'Kết quả rất tốt! Hãy soát kỹ các câu bẫy từ vựng để đạt điểm 9+.' }
    if (sc >= 5.0) return { title: 'Khá 👍', class: 'rank-average', msg: 'Đã nắm được ngữ pháp cơ bản. Cần luyện thêm kỹ năng đọc hiểu và viết lại câu.' }
    return { title: 'Cần Cố Gắng 📚', class: 'rank-needs-work', msg: 'Nên xem lại các chuyên đề lý thuyết trọng tâm trước khi làm lại đề.' }
  })

  return {
    examStore,
    total,
    answeredCount,
    correctCount,
    score10,
    percentage,
    rank,
    recordAnswer: examStore.recordAnswer.bind(examStore),
    submit: examStore.submit.bind(examStore),
    reset: examStore.reset.bind(examStore)
  }
}
