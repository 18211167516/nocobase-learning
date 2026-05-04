import axios from 'axios'

const getBaseURL = () => {
  // 优先使用环境变量
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // 生产环境 - 直接指向 Render 后端
  if (import.meta.env.PROD) {
    return 'https://nocobase-learning.onrender.com'
  }
  
  // 开发环境
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return '/api'
  }
  
  // 生产环境默认
  return 'https://nocobase-learning.onrender.com'
}

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 60000
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const getProgress = () => api.get('/progress')
export const getDayProgress = (day) => api.get(`/progress/${day}`)
export const updateProgress = (data) => api.post('/progress', data)
export const getAnswers = (day) => api.get(`/answers/${day}`)
export const getWrongAnswers = () => api.get('/wrong-answers')
export const submitAnswer = (data) => api.post('/answers', data)
export const getStats = () => api.get('/stats')
export const getLearningStats = () => api.get('/learning-stats')

export const createNote = (data) => api.post('/notes', data)
export const getNotes = (day) => api.get(`/notes${day ? `?day=${day}` : ''}`)
export const updateNote = (data) => api.put('/notes', data)
export const deleteNote = (noteId) => api.delete(`/notes/${noteId}`)

export const createFavorite = (data) => api.post('/favorites', data)
export const getFavorites = (params) => {
  const query = new URLSearchParams(params).toString()
  return api.get(`/favorites${query ? `?${query}` : ''}`)
}
export const deleteFavorite = (favId) => api.delete(`/favorites/${favId}`)

export const getBadges = () => api.get('/badges')
export const getRecommendations = () => api.get('/recommendations')
export const search = (query) => api.get(`/search?query=${encodeURIComponent(query)}`)
export const chat = (data) => api.post('/chat', data)
export const speechToText = (data) => api.post('/speech-to-text', data, { timeout: 60000 })

export default api