<template>
  <div class="app">
    <header class="header">
      <h1>🔧 NocoBase 学习平台</h1>
      <p>15 天成为 NocoBase 售后技术支持</p>
    </header>
    
    <main class="container">
      <router-view />
    </main>
    
    <footer class="footer">
      <p>© 2026 NocoBase 学习平台 | 基于 Vue3 + FastAPI</p>
    </footer>
    
    <!-- AI 助手悬浮组件 -->
    <AIAssistant />
  </div>
</template>

<script setup>
import AIAssistant from './components/AIAssistant.vue'
</script>
