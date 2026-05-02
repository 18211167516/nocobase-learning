<template>
  <div class="ai-assistant">
    <!-- 悬浮按钮 -->
    <div 
      class="ai-float-btn" 
      @click="toggleChat"
      :class="{ active: isOpen }"
    >
      <span>🤖</span>
    </div>

    <!-- 聊天窗口 -->
    <transition name="slide-up">
      <div v-if="isOpen" class="ai-chat-window">
        <div class="ai-header">
          <h3>🤖 NocoBase 学习助手</h3>
          <div class="ai-header-actions">
            <button @click="clearChat" class="clear-btn" title="清空对话">🗑️</button>
            <button @click="toggleTTS" class="tts-btn" :class="{ active: ttsEnabled }" title="语音播报">
              {{ ttsEnabled ? '🔊' : '🔇' }}
            </button>
            <button @click="toggleChat" class="close-btn" title="关闭">✕</button>
          </div>
        </div>

        <div class="ai-messages" ref="messagesContainer">
          <div 
            v-for="(msg, index) in messages" 
            :key="index"
            :class="['message', msg.role]"
          >
            <div class="message-avatar">
              {{ msg.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <div v-html="formatMessage(msg.content)"></div>
              <div class="message-time">{{ msg.time }}</div>
            </div>
          </div>
          <div v-if="isLoading" class="message assistant loading">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>

        <div class="ai-quick-actions">
          <button @click="askQuestion('NocoBase 是什么？')" class="quick-btn">❓ NocoBase 是什么</button>
          <button @click="askQuestion('给我出一道练习题')" class="quick-btn">📝 出一道题</button>
          <button @click="askQuestion('解释一下数据源的概念')" class="quick-btn">💡 数据源解释</button>
        </div>

        <div class="ai-input-area">
          <button 
            @click="toggleVoiceInput" 
            class="voice-btn"
            :class="{ recording: isRecording }"
            :title="isRecording ? '点击停止录音' : '点击开始语音输入'"
          >
            {{ isRecording ? '⏹️' : '🎤' }}
          </button>
          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage"
            placeholder="输入问题或点击麦克风语音输入..."
            class="ai-input"
            :disabled="isLoading"
          />
          <button @click="sendMessage" class="send-btn" :disabled="!inputMessage.trim() || isLoading">
            发送
          </button>
        </div>

        <div v-if="isRecording" class="recording-indicator">
          <div class="recording-wave">
            <span></span><span></span><span></span><span></span><span></span>
          </div>
          <span>正在录音...点击麦克风停止</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const isRecording = ref(false)
const ttsEnabled = ref(true)
const messagesContainer = ref(null)

let recognition = null
let synthesis = window.speechSynthesis

const initMessages = () => {
  messages.value = [
    {
      role: 'assistant',
      content: '你好！我是 NocoBase 学习助手 🤖\n\n我可以帮你：\n• 解答 NocoBase 相关问题\n• 出练习题帮你巩固知识\n• 解释概念和最佳实践\n\n有什么想问的吗？',
      time: new Date().toLocaleTimeString()
    }
  ]
}

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && messages.value.length === 0) {
    initMessages()
  }
}

const clearChat = () => {
  initMessages()
}

const toggleTTS = () => {
  ttsEnabled.value = !ttsEnabled.value
  if (!ttsEnabled.value) {
    synthesis.cancel()
  }
}

const formatMessage = (content) => {
  return content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const speak = (text) => {
  if (!ttsEnabled.value || !synthesis) return
  
  synthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text.replace(/<[^>]*>/g, '').replace(/[🤖👤📝💡❓🔊🔇🗑️✕]/g, ''))
  utterance.lang = 'zh-CN'
  utterance.rate = 1
  utterance.pitch = 1
  synthesis.speak(utterance)
}

const sendMessage = async () => {
  const message = inputMessage.value.trim()
  if (!message || isLoading.value) return

  messages.value.push({
    role: 'user',
    content: message,
    time: new Date().toLocaleTimeString()
  })

  inputMessage.value = ''
  isLoading.value = true
  await scrollToBottom()

  try {
    const response = await axios.post('/api/chat', {
      message: message,
      context: messages.value.slice(-6)
    })

    const assistantMessage = response.data.response
    
    messages.value.push({
      role: 'assistant',
      content: assistantMessage,
      time: new Date().toLocaleTimeString()
    })

    await scrollToBottom()
    speak(assistantMessage)

  } catch (error) {
    console.error('Chat error:', error)
    
    const fallbackResponse = generateLocalResponse(message)
    messages.value.push({
      role: 'assistant',
      content: fallbackResponse,
      time: new Date().toLocaleTimeString()
    })
    await scrollToBottom()
    speak(fallbackResponse)
  }

  isLoading.value = false
}

const askQuestion = (question) => {
  inputMessage.value = question
  sendMessage()
}

const generateLocalResponse = (message) => {
  const lowerMessage = message.toLowerCase()
  
  if (lowerMessage.includes('nocobase') && (lowerMessage.includes('是什么') || lowerMessage.includes('介绍'))) {
    return '**NocoBase** 是一个开源的 AI 无代码开发平台！\n\n**核心特点：**\n• 数据模型驱动\n• 所见即所得\n• 一切皆插件\n• AI 融入业务\n• 开源 + 私有部署\n\n非常适合快速搭建业务系统！'
  }
  
  if (lowerMessage.includes('出题') || lowerMessage.includes('练习题')) {
    return generateQuiz()
  }
  
  if (lowerMessage.includes('数据源')) {
    return '**数据源（Data Source）** 是存放数据的地方！\n\n**作用：**\n• 定义数据结构和存储位置\n• 可以是数据库、API等\n• 默认使用 PostgreSQL\n\n**配置路径：** 设置 → 数据源配置'
  }
  
  if (lowerMessage.includes('区块')) {
    return '**区块（Block）** 是页面上展示数据的方式！\n\n**常见类型：**\n• 表格区块 - 展示数据列表\n• 表单区块 - 输入和编辑数据\n• 详情区块 - 展示单条记录\n• 看板区块 - 任务进度展示\n• 图表区块 - 数据可视化'
  }
  
  if (lowerMessage.includes('操作')) {
    return '**操作（Action）** 是对数据进行处理的动作！\n\n**常见操作：**\n• 新增（Create）\n• 查看（View）\n• 编辑（Edit）\n• 删除（Delete）\n• 批量操作'
  }
  
  if (lowerMessage.includes('安装') || lowerMessage.includes('部署')) {
    return '**Docker 快速安装：**\n\n```bash\nmkdir my-nocobase && cd my-nocobase\ncurl -fsSL https://static-docs.nocobase.com/docker-compose/cn/latest-postgres.yml -o docker-compose.yml\ndocker compose up -d\n```\n\n**默认登录：**\n• 地址：http://localhost:13000\n• 账号：admin@nocobase.com\n• 密码：admin123'
  }
  
  return '这是个好问题！🤔\n\n你可以：\n• 查看官方文档：https://docs.nocobase.com/cn/\n• 点击"出一道题"测试你的知识\n• 或者问我关于 NocoBase 的具体问题\n\n我会尽力帮助你的！'
}

const generateQuiz = () => {
  const quizzes = [
    {
      question: 'NocoBase 的五个核心理念是什么？',
      hint: '提示：数据模型驱动、所见即所得、一切皆插件...'
    },
    {
      question: 'Collection 和 Field 有什么区别？',
      hint: '提示：Collection 是数据表，Field 是字段...'
    },
    {
      question: '如何给表格区块添加"新增"操作？',
      hint: '提示：进入配置模式 → 选择区块 → 配置操作...'
    },
    {
      question: '数据源、区块、操作三者的关系是什么？',
      hint: '提示：数据源定义存什么，区块定义怎么展示，操作定义怎么用...'
    },
    {
      question: 'NocoBase 支持哪些数据库？',
      hint: '提示：PostgreSQL、MySQL、MariaDB...'
    }
  ]
  
  const quiz = quizzes[Math.floor(Math.random() * quizzes.length)]
  
  return `📝 **练习题来了！**\n\n**问题：** ${quiz.question}\n\n${quiz.hint}\n\n想看答案吗？输入"答案"我就告诉你！`
}

const toggleVoiceInput = () => {
  if (isRecording.value) {
    stopVoiceInput()
  } else {
    startVoiceInput()
  }
}

const startVoiceInput = () => {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    alert('您的浏览器不支持语音识别，请使用 Chrome 浏览器')
    return
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  recognition = new SpeechRecognition()
  recognition.lang = 'zh-CN'
  recognition.continuous = false
  recognition.interimResults = false

  recognition.onstart = () => {
    isRecording.value = true
  }

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript
    inputMessage.value = transcript
    isRecording.value = false
    
    setTimeout(() => {
      sendMessage()
    }, 500)
  }

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error)
    isRecording.value = false
    if (event.error === 'not-allowed') {
      alert('请允许麦克风权限')
    }
  }

  recognition.onend = () => {
    isRecording.value = false
  }

  recognition.start()
}

const stopVoiceInput = () => {
  if (recognition) {
    recognition.stop()
    isRecording.value = false
  }
}

onMounted(() => {
  initMessages()
})

onUnmounted(() => {
  if (recognition) {
    recognition.stop()
  }
  synthesis.cancel()
})
</script>

<style scoped>
.ai-assistant {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 9999;
}

.ai-float-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  user-select: none;
}

.ai-float-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6);
}

.ai-float-btn.active {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.ai-chat-window {
  position: absolute;
  bottom: 70px;
  right: 0;
  width: 380px;
  height: 550px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ai-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.ai-header-actions {
  display: flex;
  gap: 8px;
}

.clear-btn, .tts-btn, .close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.clear-btn:hover, .tts-btn:hover, .close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.tts-btn.active {
  background: rgba(255, 255, 255, 0.4);
}

.close-btn {
  background: rgba(245, 87, 108, 0.6);
}

.close-btn:hover {
  background: rgba(245, 87, 108, 0.8);
}

.ai-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  background: #f8f9fa;
}

.message {
  display: flex;
  margin-bottom: 15px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message.user .message-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.message.assistant .message-avatar {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.message-content {
  max-width: 260px;
  margin: 0 10px;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message-content code {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}

.message.user .message-content code {
  background: rgba(255, 255, 255, 0.2);
}

.message-time {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 5px;
  text-align: right;
}

.message.assistant .message-time {
  color: #999;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 5px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #667eea;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.ai-quick-actions {
  padding: 10px 15px;
  display: flex;
  gap: 8px;
  overflow-x: auto;
  background: white;
  border-top: 1px solid #eee;
}

.quick-btn {
  background: #f0f2ff;
  border: none;
  border-radius: 20px;
  padding: 8px 14px;
  font-size: 12px;
  color: #667eea;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.quick-btn:hover {
  background: #667eea;
  color: white;
}

.ai-input-area {
  padding: 15px;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
  align-items: center;
}

.voice-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #f0f2ff;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.voice-btn:hover {
  background: #667eea;
}

.voice-btn.recording {
  background: #f5576c;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.ai-input {
  flex: 1;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  padding: 10px 18px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.ai-input:focus {
  border-color: #667eea;
}

.send-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.recording-indicator {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.recording-wave {
  display: flex;
  gap: 3px;
  align-items: center;
}

.recording-wave span {
  width: 4px;
  height: 15px;
  background: #f5576c;
  border-radius: 2px;
  animation: wave 0.5s infinite ease-in-out alternate;
}

.recording-wave span:nth-child(1) { animation-delay: 0s; }
.recording-wave span:nth-child(2) { animation-delay: 0.1s; }
.recording-wave span:nth-child(3) { animation-delay: 0.2s; }
.recording-wave span:nth-child(4) { animation-delay: 0.3s; }
.recording-wave span:nth-child(5) { animation-delay: 0.4s; }

@keyframes wave {
  0% { height: 5px; }
  100% { height: 20px; }
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 480px) {
  .ai-chat-window {
    width: calc(100vw - 40px);
    right: -10px;
  }
}
</style>
