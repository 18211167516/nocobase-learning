<template>
  <div class="learning-center" :class="{ 'dark-mode': isDarkMode }">
    <div class="header-actions">
      <button @click="toggleDarkMode" class="theme-toggle">
        {{ isDarkMode ? '☀️' : '🌙' }}
      </button>
    </div>

    <h2 class="page-title">📊 学习中心</h2>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.completed_days }}/{{ stats.total_days }}</div>
          <div class="stat-label">完成天数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_answers }}</div>
          <div class="stat-label">答题数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.average_score }}</div>
          <div class="stat-label">平均分</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🎖️</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_badges }}</div>
          <div class="stat-label">徽章数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📒</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_notes }}</div>
          <div class="stat-label">笔记数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">❤️</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_favorites }}</div>
          <div class="stat-label">收藏数</div>
        </div>
      </div>
    </div>

    <div class="progress-section">
      <h3>📈 学习进度</h3>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: stats.progress_percent + '%' }"></div>
      </div>
      <p class="progress-text">{{ stats.progress_percent }}% 完成，剩余 {{ stats.remaining_days }} 天</p>
    </div>

    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.icon }} {{ tab.name }}
      </button>
    </div>

    <div class="tab-content">
      <div v-if="activeTab === 'recommendations'" class="recommendations">
        <h3>🎯 AI 学习推荐</h3>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else>
          <div v-for="rec in recommendations" :key="rec.type" class="recommendation-card" :class="rec.priority">
            <div class="rec-header">
              <span class="rec-type">{{ getRecTypeName(rec.type) }}</span>
              <span class="rec-priority">{{ getPriorityName(rec.priority) }}</span>
            </div>
            <p class="rec-message">{{ rec.message }}</p>
            <p class="rec-reason">{{ rec.reason }}</p>
          </div>
          <div v-if="recommendations.length === 0" class="empty-state">
            <p>开始学习后，我会给你推荐学习内容哦！</p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'wrong-answers'" class="wrong-answers">
        <h3>❌ 错题本</h3>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else>
          <div v-for="item in wrongAnswers" :key="item.id" class="wrong-answer-card">
            <div class="wrong-header">
              <span class="day-badge">Day {{ item.day }} - Q{{ item.question }}</span>
              <span class="score-badge low">{{ item.score }}分</span>
            </div>
            <p class="question">{{ getQuestionText(item.day, item.question) }}</p>
            <p class="answer"><strong>我的答案：</strong>{{ item.answer }}</p>
            <p class="feedback">{{ item.feedback }}</p>
            <button @click="retryQuestion(item)" class="retry-btn">重新答题</button>
          </div>
          <div v-if="wrongAnswers.length === 0" class="empty-state">
            <p>🎉 太棒了！没有错题！</p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'notes'" class="notes">
        <h3>📒 我的笔记</h3>
        <div class="note-input">
          <select v-model="noteDay" class="day-select">
            <option v-for="day in 15" :key="day" :value="day">Day {{ day }}</option>
          </select>
          <textarea v-model="noteContent" placeholder="写下今天的学习心得..." rows="3"></textarea>
          <button @click="addNote" class="add-btn">添加笔记</button>
        </div>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else class="notes-list">
          <div v-for="note in notes" :key="note.id" class="note-card">
            <div class="note-header">
              <span class="note-day">Day {{ note.day }}</span>
              <span class="note-date">{{ formatDate(note.updated_at) }}</span>
              <button @click="deleteNote(note.id)" class="delete-btn">🗑️</button>
            </div>
            <p class="note-content">{{ note.content }}</p>
          </div>
          <div v-if="notes.length === 0" class="empty-state">
            <p>还没有笔记，开始记录你的学习心得吧！</p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'favorites'" class="favorites">
        <h3>❤️ 我的收藏</h3>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else class="favorites-list">
          <div v-for="fav in favorites" :key="fav.id" class="favorite-card">
            <div class="fav-header">
              <span class="fav-type">{{ fav.type }}</span>
              <span class="fav-day">Day {{ fav.day }}</span>
              <button @click="deleteFavorite(fav.id)" class="delete-btn">🗑️</button>
            </div>
            <p class="fav-content">{{ fav.content }}</p>
          </div>
          <div v-if="favorites.length === 0" class="empty-state">
            <p>还没有收藏，在学习时收藏感兴趣的知识点吧！</p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'badges'" class="badges">
        <h3>🏆 学习徽章</h3>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else class="badges-grid">
          <div 
            v-for="badge in badges" 
            :key="badge.name" 
            class="badge-card"
            :class="{ earned: badge.earned }"
          >
            <div class="badge-icon">{{ badge.icon }}</div>
            <div class="badge-name">{{ badge.name }}</div>
            <div class="badge-desc">{{ badge.description }}</div>
            <div v-if="badge.earned" class="badge-earned">
              ✓ 已获得
            </div>
            <div v-else class="badge-locked">
              🔒 未获得
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'search'" class="search">
        <h3>🔍 知识搜索</h3>
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            @input="doSearch"
            placeholder="搜索知识点..."
            class="search-input"
          />
        </div>
        <div v-if="searchResults.length > 0" class="search-results">
          <div v-for="result in searchResults" :key="result.keyword" class="search-result-card">
            <h4>{{ result.keyword }}</h4>
            <p>{{ result.answer }}</p>
          </div>
        </div>
        <div v-else-if="searchQuery" class="empty-state">
          <p>没有找到相关结果</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  getStats, 
  getWrongAnswers, 
  getNotes, 
  getFavorites, 
  getBadges, 
  getRecommendations,
  createNote,
  deleteNote as apiDeleteNote,
  deleteFavorite as apiDeleteFavorite,
  search
} from '../api'

const router = useRouter()

const stats = ref({
  total_days: 15,
  completed_days: 0,
  remaining_days: 15,
  progress_percent: 0,
  total_answers: 0,
  average_score: 0,
  current_day: 1,
  total_notes: 0,
  total_favorites: 0,
  total_badges: 0
})

const wrongAnswers = ref([])
const notes = ref([])
const favorites = ref([])
const badges = ref([])
const recommendations = ref([])
const searchResults = ref([])

const activeTab = ref('recommendations')
const loading = ref(false)
const noteDay = ref(1)
const noteContent = ref('')
const searchQuery = ref('')
const isDarkMode = ref(false)

const tabs = [
  { id: 'recommendations', name: '推荐', icon: '🎯' },
  { id: 'wrong-answers', name: '错题本', icon: '❌' },
  { id: 'notes', name: '笔记', icon: '📒' },
  { id: 'favorites', name: '收藏', icon: '❤️' },
  { id: 'badges', name: '徽章', icon: '🏆' },
  { id: 'search', name: '搜索', icon: '🔍' }
]

const questionTexts = {
  1: { 1: 'NocoBase 的五个核心理念是什么？', 2: '配置模式和使用模式有什么区别？', 3: '数据源、区块、操作三者的关系是什么？' },
  2: { 1: '如何查看 NocoBase 的运行日志？', 2: '默认的登录账号密码是什么？', 3: '如何解决端口被占用的问题？' },
  3: { 1: 'Collection 和 Field 分别是什么？有什么区别？', 2: '常用的区块类型有哪些？它们各自的用途是什么？', 3: '如何给表格区块添加「新增」操作？请描述具体步骤。' }
}

const getQuestionText = (day, question) => {
  return questionTexts[day]?.[question] || `Day ${day} Q${question}`
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('darkMode', isDarkMode.value)
}

const loadStats = async () => {
  try {
    const res = await getStats()
    stats.value = res.data
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const loadWrongAnswers = async () => {
  loading.value = true
  try {
    const res = await getWrongAnswers()
    wrongAnswers.value = res.data
  } catch (error) {
    console.error('Failed to load wrong answers:', error)
  } finally {
    loading.value = false
  }
}

const loadNotes = async () => {
  loading.value = true
  try {
    const res = await getNotes()
    notes.value = res.data
  } catch (error) {
    console.error('Failed to load notes:', error)
  } finally {
    loading.value = false
  }
}

const loadFavorites = async () => {
  loading.value = true
  try {
    const res = await getFavorites()
    favorites.value = res.data
  } catch (error) {
    console.error('Failed to load favorites:', error)
  } finally {
    loading.value = false
  }
}

const loadBadges = async () => {
  loading.value = true
  try {
    const res = await getBadges()
    badges.value = res.data
  } catch (error) {
    console.error('Failed to load badges:', error)
  } finally {
    loading.value = false
  }
}

const loadRecommendations = async () => {
  loading.value = true
  try {
    const res = await getRecommendations()
    recommendations.value = res.data
  } catch (error) {
    console.error('Failed to load recommendations:', error)
  } finally {
    loading.value = false
  }
}

const addNote = async () => {
  if (!noteContent.value.trim()) return
  
  try {
    await createNote({
      day: noteDay.value,
      content: noteContent.value.trim()
    })
    noteContent.value = ''
    await loadNotes()
    await loadStats()
  } catch (error) {
    console.error('Failed to add note:', error)
  }
}

const deleteNote = async (id) => {
  if (!confirm('确定要删除这条笔记吗？')) return
  
  try {
    await apiDeleteNote(id)
    await loadNotes()
    await loadStats()
  } catch (error) {
    console.error('Failed to delete note:', error)
  }
}

const deleteFavorite = async (id) => {
  if (!confirm('确定要取消收藏吗？')) return
  
  try {
    await apiDeleteFavorite(id)
    await loadFavorites()
    await loadStats()
  } catch (error) {
    console.error('Failed to delete favorite:', error)
  }
}

const retryQuestion = (item) => {
  router.push(`/day/${item.day}`)
}

const doSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }
  
  try {
    const res = await search(searchQuery.value)
    searchResults.value = res.data.results || []
  } catch (error) {
    console.error('Failed to search:', error)
  }
}

const getRecTypeName = (type) => {
  const names = {
    next_step: '下一步',
    review: '复习',
    practice: '练习',
    explore: '探索'
  }
  return names[type] || type
}

const getPriorityName = (priority) => {
  const names = {
    high: '高优先级',
    medium: '中优先级',
    low: '低优先级'
  }
  return names[priority] || priority
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

onMounted(async () => {
  isDarkMode.value = localStorage.getItem('darkMode') === 'true'
  await loadStats()
  await loadRecommendations()
})
</script>

<style scoped>
.learning-center {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
  transition: all 0.3s;
}

.learning-center.dark-mode {
  background: #1a1a2e;
  color: #fff;
}

.header-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.theme-toggle {
  background: white;
  border: 2px solid #ddd;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.dark-mode .theme-toggle {
  background: #2d2d44;
  border-color: #4a4a6a;
  color: #fff;
}

.theme-toggle:hover {
  transform: scale(1.1);
}

.page-title {
  font-size: 32px;
  margin-bottom: 30px;
  color: #333;
}

.dark-mode .page-title {
  color: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
}

.dark-mode .stat-card {
  background: #2d2d44;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.stat-icon {
  font-size: 40px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2ff;
  border-radius: 12px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
}

.dark-mode .stat-value {
  color: #a8b4ff;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.dark-mode .stat-label {
  color: #aaa;
}

.progress-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.dark-mode .progress-section {
  background: #2d2d44;
}

.progress-section h3 {
  margin: 0 0 16px 0;
  color: #333;
}

.dark-mode .progress-section h3 {
  color: #fff;
}

.progress-bar {
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  transition: width 0.5s ease;
}

.progress-text {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.dark-mode .progress-text {
  color: #aaa;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 12px 20px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.dark-mode .tab-btn {
  background: #2d2d44;
  border-color: #4a4a6a;
  color: #aaa;
}

.tab-btn:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.tab-content {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.dark-mode .tab-content {
  background: #2d2d44;
}

.tab-content h3 {
  margin: 0 0 20px 0;
  color: #333;
}

.dark-mode .tab-content h3 {
  color: #fff;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.dark-mode .loading {
  color: #aaa;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.dark-mode .empty-state {
  color: #aaa;
}

.recommendation-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  border-left: 4px solid #ddd;
}

.dark-mode .recommendation-card {
  background: #1a1a2e;
}

.recommendation-card.high {
  border-left-color: #f5576c;
}

.recommendation-card.medium {
  border-left-color: #f5a623;
}

.recommendation-card.low {
  border-left-color: #667eea;
}

.rec-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.rec-type {
  font-weight: 600;
  color: #333;
}

.dark-mode .rec-type {
  color: #fff;
}

.rec-priority {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 12px;
  background: #e0e0e0;
  color: #666;
}

.dark-mode .rec-priority {
  background: #4a4a6a;
  color: #aaa;
}

.rec-message {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #667eea;
}

.dark-mode .rec-message {
  color: #a8b4ff;
}

.rec-reason {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.dark-mode .rec-reason {
  color: #aaa;
}

.wrong-answer-card {
  background: #fff5f5;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  border: 2px solid #fecaca;
}

.dark-mode .wrong-answer-card {
  background: #2d1f1f;
  border-color: #5c3a3a;
}

.wrong-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.day-badge {
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.score-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.score-badge.low {
  background: #fee2e2;
  color: #dc2626;
}

.dark-mode .score-badge.low {
  background: #5c3a3a;
  color: #fca5a5;
}

.question {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #333;
}

.dark-mode .question {
  color: #fff;
}

.answer {
  font-size: 14px;
  margin: 0 0 8px 0;
  color: #666;
}

.dark-mode .answer {
  color: #aaa;
}

.feedback {
  font-size: 14px;
  color: #f5576c;
  margin: 0 0 12px 0;
}

.retry-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.retry-btn:hover {
  transform: scale(1.05);
}

.note-input {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.day-select {
  padding: 10px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  color: #333;
}

.dark-mode .day-select {
  background: #1a1a2e;
  color: #fff;
  border-color: #4a4a6a;
}

.note-input textarea {
  flex: 1;
  min-width: 200px;
  padding: 10px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
}

.dark-mode .note-input textarea {
  background: #1a1a2e;
  color: #fff;
  border-color: #4a4a6a;
}

.add-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.add-btn:hover {
  transform: scale(1.05);
}

.note-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}

.dark-mode .note-card {
  background: #1a1a2e;
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.note-day {
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.note-date {
  font-size: 12px;
  color: #999;
}

.delete-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 4px 8px;
  transition: transform 0.2s;
}

.delete-btn:hover {
  transform: scale(1.2);
}

.note-content {
  margin: 0;
  color: #333;
  line-height: 1.6;
}

.dark-mode .note-content {
  color: #fff;
}

.favorite-card {
  background: #fff5f8;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  border: 2px solid #fecdd3;
}

.dark-mode .favorite-card {
  background: #2d1f2d;
  border-color: #5c3a5c;
}

.fav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.fav-type {
  background: #f5576c;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.fav-day {
  font-size: 12px;
  color: #999;
}

.fav-content {
  margin: 0;
  color: #333;
  line-height: 1.6;
}

.dark-mode .fav-content {
  color: #fff;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.badge-card {
  background: #f8f9fa;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  border: 2px solid #e0e0e0;
  transition: all 0.3s;
}

.dark-mode .badge-card {
  background: #1a1a2e;
  border-color: #4a4a6a;
}

.badge-card.earned {
  border-color: #667eea;
  background: #f0f2ff;
}

.dark-mode .badge-card.earned {
  background: #2d2d44;
}

.badge-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.badge-name {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #333;
}

.dark-mode .badge-name {
  color: #fff;
}

.badge-desc {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
}

.dark-mode .badge-desc {
  color: #aaa;
}

.badge-earned {
  font-size: 12px;
  color: #667eea;
  font-weight: 600;
}

.badge-locked {
  font-size: 12px;
  color: #999;
}

.search-box {
  margin-bottom: 24px;
}

.search-input {
  width: 100%;
  padding: 12px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  background: white;
  color: #333;
  transition: all 0.3s;
}

.dark-mode .search-input {
  background: #1a1a2e;
  color: #fff;
  border-color: #4a4a6a;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.search-result-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}

.dark-mode .search-result-card {
  background: #1a1a2e;
}

.search-result-card h4 {
  margin: 0 0 8px 0;
  color: #667eea;
}

.dark-mode .search-result-card h4 {
  color: #a8b4ff;
}

.search-result-card p {
  margin: 0;
  color: #333;
  line-height: 1.6;
}

.dark-mode .search-result-card p {
  color: #fff;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 10px;
  }
  
  .tab-btn {
    white-space: nowrap;
  }
  
  .badges-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
