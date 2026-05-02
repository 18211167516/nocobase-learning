import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DayView from '../views/DayView.vue'
import LearningCenter from '../views/LearningCenter.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/day/:id',
    name: 'day',
    component: DayView
  },
  {
    path: '/learning-center',
    name: 'learning-center',
    component: LearningCenter
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router