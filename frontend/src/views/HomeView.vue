<template>
  <div class="main-content">
    <div v-if="loading" class="loading">
      加载中...
    </div>
    
    <div v-else>
      <div class="progress-section">
        <h2>📊 学习进度</h2>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: stats.progress_percent + '%' }"></div>
        </div>
        <p style="text-align: center; color: #666;">
          已完成 {{ stats.completed_days }} / {{ stats.total_days }} 天 ({{ stats.progress_percent }}%)
        </p>
      </div>
      
      <div class="stats">
        <div class="stat-card">
          <div class="number">{{ stats.completed_days }}</div>
          <div class="label">已完成天数</div>
        </div>
        <div class="stat-card">
          <div class="number">{{ stats.remaining_days }}</div>
          <div class="label">剩余天数</div>
        </div>
        <div class="stat-card">
          <div class="number">{{ stats.total_answers }}</div>
          <div class="label">已回答问题</div>
        </div>
        <div class="stat-card">
          <div class="number">{{ stats.average_score }}</div>
          <div class="label">平均分数</div>
        </div>
        <div class="stat-card">
          <div class="number">{{ stats.current_day }}</div>
          <div class="label">当前学习</div>
        </div>
      </div>

      <button @click="goToLearningCenter" class="learning-center-btn">
        📊 前往学习中心
      </button>
      
      <h2 style="margin-top: 30px;">📚 学习计划</h2>
      
      <div class="days-grid">
        <div 
          v-for="day in days" 
          :key="day.day"
          class="day-card"
          :class="{ 
            'completed': day.completed, 
            'current': day.day === stats.current_day && !day.completed 
          }"
          @click="goToDay(day.day)"
        >
          <div class="day-number">Day {{ day.day }}</div>
          <div class="day-title">{{ getDayTitle(day.day) }}</div>
          <span 
            v-if="day.completed" 
            class="status completed"
          >✓ 已完成</span>
          <span 
            v-else-if="day.day === stats.current_day" 
            class="status current"
          >当前</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProgress, getStats } from '../api'

const router = useRouter()
const loading = ref(true)
const days = ref([])
const stats = ref({
  total_days: 15,
  completed_days: 0,
  remaining_days: 15,
  progress_percent: 0,
  total_answers: 0,
  average_score: 0,
  current_day: 1
})

const dayTitles = {
  1: '认识 NocoBase',
  2: 'Docker 安装部署',
  3: '基础功能概览',
  4: '数据建模基础',
  5: '数据建模进阶',
  6: '界面搭建',
  7: '用户与权限',
  8: '工作流',
  9: '部署与运维',
  10: '常见问题排查（一）',
  11: '常见问题排查（二）',
  12: '高级功能了解',
  13: '插件开发基础',
  14: '售后实战模拟',
  15: '毕业考核'
}

const getDayTitle = (day) => {
  return dayTitles[day] || ''
}

const goToDay = (day) => {
  router.push(`/day/${day}`)
}

const goToLearningCenter = () => {
  router.push('/learning-center')
}

onMounted(async () => {
  try {
    const [progressRes, statsRes] = await Promise.all([
      getProgress(),
      getStats()
    ])
    
    days.value = progressRes.data
    stats.value = statsRes.data
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 60px;
  color: #666;
}

.progress-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.progress-bar {
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin: 16px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  transition: width 0.5s ease;
}

.stats {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.stat-card .number {
  font-size: 36px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-card .label {
  font-size: 14px;
  color: #666;
}

.learning-center-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.learning-center-btn:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.day-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 2px solid transparent;
}

.day-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  border-color: #667eea;
}

.day-card.completed {
  background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
  border-color: #38a169;
}

.day-card.current {
  background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%);
  border-color: #3182ce;
}

.day-number {
  font-size: 24px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 8px;
}

.day-card.completed .day-number {
  color: #38a169;
}

.day-title {
  font-size: 16px;
  color: #333;
  margin-bottom: 12px;
}

.status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status.completed {
  background: #38a169;
  color: white;
}

.status.current {
  background: #3182ce;
  color: white;
}

@media (max-width: 768px) {
  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .days-grid {
    grid-template-columns: 1fr;
  }
}
</style>
