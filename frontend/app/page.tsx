'use client'

import React, { useState, useEffect, useRef } from 'react'
import { 
  Send, RotateCcw, MessageCircle, CreditCard, Phone, FileText, 
  Fingerprint, Sun, Moon, History, Globe, 
  Clock, User, Bot, Archive, Settings, Wifi, WifiOff
} from 'lucide-react'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

interface ChatState {
  current_state: string
}

interface Suggestion {
  text: string
  value: string
  icon: string
}

interface ChatSession {
  id: string
  name: string
  messages: Message[]
  state: string
  timestamp: Date
}

// Client-side only check
const isClient = typeof window !== 'undefined'
const API_BASE_URL = isClient ? 'http://localhost:5000/api' : ''

export default function Home() {
  // Core states
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string>('')
  const [chatState, setChatState] = useState<ChatState>({ current_state: 'wait' })
  const [suggestions, setSuggestions] = useState<Suggestion[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Theme states - initialize with default to avoid hydration mismatch
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [themeInitialized, setThemeInitialized] = useState(false)

  // Language states
  const [currentLanguage, setCurrentLanguage] = useState<'vi' | 'en'>('vi')

  // Chat history states
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [currentSessionName, setCurrentSessionName] = useState('')

  // Backend connection states
  const [isConnected, setIsConnected] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('connecting')

  // Auto-generated session name
  useEffect(() => {
    const now = new Date()
    const sessionName = `Phiên trò chuyện ${now.getDate()}/${now.getMonth() + 1} ${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`
    setCurrentSessionName(sessionName)
  }, [])

  // Initialize session ID safely for hydration
  useEffect(() => {
    if (!sessionId) {
      const newSessionId = Math.random().toString(36).substring(7)
      setSessionId(newSessionId)
    }
  }, [])

  // Check backend connection
  const checkBackendConnection = async () => {
    if (!isClient || !API_BASE_URL) {
      setConnectionStatus('disconnected')
      setIsConnected(false)
      return
    }

    try {
      setConnectionStatus('connecting')
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(5000)
      })
      
      if (response.ok) {
        setIsConnected(true)
        setConnectionStatus('connected')
      } else {
        throw new Error('Backend not healthy')
      }
    } catch (error) {
      console.log('Backend connection failed:', error)
      setIsConnected(false)
      setConnectionStatus('error')
    }
  }

  // Initialize backend connection check
  useEffect(() => {
    if (isClient) {
      checkBackendConnection()
      
      // Check connection every 30 seconds
      const interval = setInterval(checkBackendConnection, 30000)
      
      return () => clearInterval(interval)
    }
  }, [isClient])

  // Initialize theme safely for hydration
  useEffect(() => {
    if (isClient && !themeInitialized) {
      const savedTheme = localStorage.getItem('theme')
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      const shouldUseDark = savedTheme === 'dark' || (!savedTheme && prefersDark)
      
      setIsDarkMode(shouldUseDark)
      setThemeInitialized(true)
      
      // Apply theme immediately
      if (shouldUseDark) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  }, [themeInitialized])

  // Initialize language safely for hydration
  useEffect(() => {
    if (isClient) {
      const savedLanguage = localStorage.getItem('language')
      if (savedLanguage === 'en' || savedLanguage === 'vi') {
        setCurrentLanguage(savedLanguage)
      }
    }
  }, [])

  // Theme effect - only update after initialization
  useEffect(() => {
    if (themeInitialized && isClient) {
      if (isDarkMode) {
        document.documentElement.classList.add('dark')
        localStorage.setItem('theme', 'dark')
      } else {
        document.documentElement.classList.remove('dark')
        localStorage.setItem('theme', 'light')
      }
    }
  }, [isDarkMode, themeInitialized, isClient])

  // Auto-save session to history
  useEffect(() => {
    if (messages.length > 0 && sessionId && isClient) {
      const session: ChatSession = {
        id: sessionId,
        name: currentSessionName,
        messages: [...messages],
        state: chatState.current_state,
        timestamp: new Date()
      }
      
      const existingIndex = chatSessions.findIndex(s => s.id === sessionId)
      if (existingIndex >= 0) {
        const updatedSessions = [...chatSessions]
        updatedSessions[existingIndex] = session
        setChatSessions(updatedSessions)
      } else {
        setChatSessions(prev => [session, ...prev.slice(0, 9)]) // Keep only 10 recent sessions
      }
      
      localStorage.setItem('chatHistory', JSON.stringify([session, ...chatSessions.slice(0, 9)]))
    }
  }, [messages, chatState, sessionId, currentSessionName, isClient])

  // Load history on mount
  useEffect(() => {
    if (isClient) {
      const savedHistory = localStorage.getItem('chatHistory')
      if (savedHistory) {
        try {
          const history = JSON.parse(savedHistory)
          setChatSessions(history.map((session: any) => ({
            ...session,
            timestamp: new Date(session.timestamp)
          })))
        } catch (error) {
          console.error('Error loading chat history:', error)
        }
      }
    }
  }, [isClient])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Gửi tin nhắn chào mừng khi component mount và sessionId đã sẵn sàng
    if (sessionId && isClient) {
      handleWelcomeMessage()
    }
  }, [sessionId, isClient])

  // Translations
  const translations = {
    vi: {
      title: 'Trợ Lý Ảo Bank-Soft BaSo',
      subtitle: 'Hỗ trợ khách hàng ngân hàng 24/7',
      placeholder: 'Nhập tin nhắn của bạn...',
      send: 'Gửi',
      loading: 'Đang xử lý...',
      quickReplies: 'Gợi ý trả lời:',
      reset: 'Bắt đầu lại',
      theme: 'Chế độ',
      history: 'Lịch sử',
      settings: 'Cài đặt',
      language: 'Ngôn ngữ',
      vietnamese: 'Tiếng Việt',
      english: 'English',
      chatHistory: 'Nhật ký trò chuyện',
      newChat: 'Trò chuyện mới',
      noHistory: 'Chưa có lịch sử trò chuyện',
      backToChat: 'Quay lại trò chuyện',
      saveSession: 'Đã lưu',
      currentSession: 'Phiên hiện tại',
      recentChats: 'Các phiên gần đây',
      connected: 'Đã kết nối',
      connecting: 'Đang kết nối...',
      disconnected: 'Mất kết nối',
      connectionError: 'Lỗi kết nối server',
      statusConnected: 'Đang hoạt động - Phản hồi trong vài giây',
      statusConnecting: 'Đang kết nối tới server...',
      statusDisconnected: 'Không có kết nối với máy chủ',
      statusError: 'Lỗi kết nối với máy chủ',
      retryConnection: 'Thử kết nối lại',
      serverOffline: 'Máy chủ đang offline',
      noBackendConnection: 'Không thể kết nối với backend. Vui lòng kiểm tra kết nối mạng.'
    },
    en: {
      title: 'Bank-Soft BaSo Assistant',
      subtitle: '24/7 Banking Customer Support',
      placeholder: 'Enter your message...',
      send: 'Send',
      loading: 'Processing...',
      quickReplies: 'Quick replies:',
      reset: 'Start over',
      theme: 'Theme',
      history: 'History',
      settings: 'Settings',
      language: 'Language',
      vietnamese: 'Tiếng Việt',
      english: 'English',
      chatHistory: 'Chat History',
      newChat: 'New Chat',
      noHistory: 'No chat history yet',
      backToChat: 'Back to Chat',
      saveSession: 'Saved',
      currentSession: 'Current Session',
      recentChats: 'Recent Sessions',
      connected: 'Connected',
      connecting: 'Connecting...',
      disconnected: 'Disconnected',
      connectionError: 'Server connection error',
      statusConnected: 'Active - Responding in seconds',
      statusConnecting: 'Connecting to server...',
      statusDisconnected: 'No server connection',
      statusError: 'Server connection error',
      retryConnection: 'Retry connection',
      serverOffline: 'Server is offline',
      noBackendConnection: 'Unable to connect to backend. Please check your network connection.'
    }
  }

  const t = translations[currentLanguage]

  const handleWelcomeMessage = async () => {
    if (!isClient || !sessionId) {
      console.log('Waiting for client initialization...')
      return
    }
    
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: 'Hi',
          session_id: sessionId,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        addBotMessage(data.response)
        setChatState({ current_state: data.state })
        setSuggestions(data.suggestions || [])
      } else {
        throw new Error('Failed to send message')
      }
    } catch (error) {
      console.error('Error:', error)
      // Show appropriate error message based on connection status
      if (!isConnected) {
        addBotMessage(t.noBackendConnection)
      } else {
        addBotMessage(currentLanguage === 'vi' ? 'Xin lỗi, có lỗi xảy ra. Vui lòng thử lại!' : 'Sorry, an error occurred. Please try again!')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const addBotMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'bot',
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, newMessage])
  }

  const addUserMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, newMessage])
  }

  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || inputValue.trim()
    if (!textToSend || isLoading) return

    setInputValue('')
    addUserMessage(textToSend)
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: textToSend,
          session_id: sessionId,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setTimeout(() => {
          addBotMessage(data.response)
          setChatState({ current_state: data.state })
          setSuggestions(data.suggestions || [])
        }, 500)
      } else {
        throw new Error('Failed to send message')
      }
    } catch (error) {
      console.error('Error:', error)
      setTimeout(() => {
        if (!isConnected) {
          addBotMessage(t.noBackendConnection)
        } else {
          addBotMessage(currentLanguage === 'vi' ? 'Xin lỗi, có lỗi xảy ra. Vui lòng thử lại!' : 'Sorry, an error occurred. Please try again!')
        }
      }, 500)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const resetChat = async () => {
    try {
      await fetch(`${API_BASE_URL}/reset`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
        }),
      })
    } catch (error) {
      console.error('Error resetting session:', error)
    } finally {
      setMessages([])
      setChatState({ current_state: 'wait' })
      setSuggestions([])
      setTimeout(() => {
        handleWelcomeMessage()
      }, 100)
    }
  }

  const loadSession = (session: ChatSession) => {
    setMessages(session.messages)
    setChatState({ current_state: session.state })
    setShowHistory(false)
    // Clear suggestions until next message
    setSuggestions([])
  }

  const clearHistory = () => {
    if (isClient) {
      setChatSessions([])
      localStorage.removeItem('chatHistory')
    }
  }

  const handleSuggestionClick = (suggestion: Suggestion) => {
    if (suggestion.value === 'main_menu') {
      sendMessage('Hi')
    } else if (suggestion.value === 'Hi') {
      sendMessage('Hi')
    } else if (suggestion.value.includes('_menu')) {
      // Handle menu navigation
      sendMessage(suggestion.value.replace('_menu', ''))
    } else {
      sendMessage(suggestion.value)
    }
  }

  // Language toggle function with state management
  const toggleLanguage = () => {
    const newLang = currentLanguage === 'vi' ? 'en' : 'vi'
    setCurrentLanguage(newLang)
    if (isClient) {
      localStorage.setItem('language', newLang)
    }
  }

  // Get connection status display
  const getConnectionStatusInfo = () => {
    switch (connectionStatus) {
      case 'connecting':
        return {
          text: t.statusConnecting,
          color: 'text-yellow-600 dark:text-yellow-400',
          bgColor: 'bg-yellow-100 dark:bg-yellow-900/20',
          icon: <Clock className="w-2 h-2" />
        }
      case 'connected':
        return {
          text: t.statusConnected,
          color: 'text-green-600 dark:text-green-400',
          bgColor: 'bg-green-100 dark:bg-green-900/20',
          icon: <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        }
      case 'disconnected':
        return {
          text: t.statusDisconnected,
          color: 'text-red-600 dark:text-red-400',
          bgColor: 'bg-red-100 dark:bg-red-900/20',
          icon: <WifiOff className="w-2 h-2" />
        }
      case 'error':
        return {
          text: t.statusError,
          color: 'text-red-600 dark:text-red-400',
          bgColor: 'bg-red-100 dark:bg-red-900/20',
          icon: <WifiOff className="w-2 h-2" />
        }
      default:
        return {
          text: t.statusConnecting,
          color: 'text-gray-600 dark:text-gray-400',
          bgColor: 'bg-gray-100 dark:bg-gray-900/20',
          icon: <Clock className="w-2 h-2" />
        }
    }
  }

  const connectionInfo = getConnectionStatusInfo()

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto main-chat-container transition-all duration-500 rounded-3xl overflow-hidden shadow-2xl">
      
      {/* Header */}
      <div className="chat-header p-6 shadow-lg transition-all duration-300 relative overflow-hidden">
        {/* Gradient background overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-purple-600/5 to-green-600/10 dark:from-blue-900/20 dark:via-purple-900/10 dark:to-green-900/20"></div>
        
        <div className="flex items-center justify-between relative z-10">
          <div className="flex items-center space-x-4">
            {/* Enhanced Vietcombank Logo */}
            <div className="relative">
              <div className="w-14 h-14 bg-gradient-to-br from-green-500 via-green-600 to-green-700 rounded-2xl flex items-center justify-center shadow-xl transform hover:scale-105 transition-all duration-300">
                <span className="text-white font-bold text-xl">
                <img 
                  src="/favicon.ico"
                  alt="Bank-Soft Logo"
                  className="w-16 h-16 object-contain rounded-xl" 
                />                 
                 </span>
                {/* Glow effect */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-green-400 to-green-600 opacity-30 blur-md"></div>
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-green-800 dark:from-green-400 dark:to-green-600 bg-clip-text text-transparent">
                {t.title}
              </h1>
              <div className="flex items-center space-x-3">
                <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${connectionInfo.bgColor}`}>
                  {connectionInfo.icon}
                  <p className={`text-sm font-medium ${connectionInfo.color}`}>
                    {connectionInfo.text}
                  </p>
                </div>
                {/* Connection indicator */}
                <button 
                  onClick={checkBackendConnection}
                  className={`p-1 rounded-full transition-all duration-200 hover:scale-110 ${
                    isConnected 
                      ? 'text-green-500 hover:text-green-600' 
                      : 'text-red-500 hover:text-red-600'
                  }`}
                  title={t.retryConnection}
                >
                  {isConnected ? <Wifi className="w-4 h-4" /> : <WifiOff className="w-4 h-4" />}
                </button>
              </div>
            </div>
          </div>
          
          {/* Enhanced Header Controls */}
          <div className="flex items-center space-x-3">
            
            {/* Language Toggle - Enhanced */}
            <button
              onClick={toggleLanguage}
              className={`p-3 rounded-2xl transition-all duration-200 hover:scale-105 hover:shadow-lg ${
                isDarkMode 
                  ? 'hover:bg-gray-700/80 bg-gray-800/50' 
                  : 'hover:bg-white/80 bg-white/50'
              } backdrop-blur-sm border border-white/20 dark:border-gray-700/20`}
              title={t.language}
            >
              <div className="flex items-center space-x-2">
                <Globe className="w-5 h-5 text-gray-600 dark:text-gray-300" />
                <span className="text-sm font-bold text-gray-700 dark:text-gray-300 bg-gradient-to-r from-green-600 to-green-700 dark:from-green-400 dark:to-green-500 bg-clip-text text-transparent">
                  {currentLanguage === 'vi' ? 'VI' : 'EN'}
                </span>
              </div>
            </button>

            {/* History Button - Enhanced */}
            <button
              onClick={() => setShowHistory(!showHistory)}
              className={`p-3 rounded-2xl transition-all duration-200 hover:scale-105 hover:shadow-lg ${
                isDarkMode 
                  ? 'hover:bg-gray-700/80 bg-gray-800/50' 
                  : 'hover:bg-white/80 bg-white/50'
              } backdrop-blur-sm border border-white/20 dark:border-gray-700/20`}
              title={t.history}
            >
              <History className="w-5 h-5 text-gray-600 dark:text-gray-300" />
            </button>

            {/* Theme Toggle - Enhanced */}
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className={`p-3 rounded-2xl transition-all duration-200 hover:scale-105 hover:shadow-lg ${
                isDarkMode 
                  ? 'hover:bg-gray-700/80 bg-gray-800/50' 
                  : 'hover:bg-white/80 bg-white/50'
              } backdrop-blur-sm border border-white/20 dark:border-gray-700/20`}
              title={t.theme}
            >
              {isDarkMode ? <Sun className="w-5 h-5 text-yellow-500" /> : <Moon className="w-5 h-5 text-blue-600" />}
            </button>

            {/* Reset Button - Enhanced */}
            <button
              onClick={resetChat}
              className={`p-3 rounded-2xl transition-all duration-200 hover:scale-105 hover:shadow-lg ${
                isDarkMode 
                  ? 'hover:bg-gray-700/80 bg-gray-800/50' 
                  : 'hover:bg-white/80 bg-white/50'
              } backdrop-blur-sm border border-white/20 dark:border-gray-700/20`}
              title={t.reset}
            >
              <RotateCcw className="w-5 h-5 text-gray-600 dark:text-gray-300" />
            </button>
          </div>
        </div>
      </div>

      {/* Enhanced History Sidebar */}
      {showHistory && (
        <div className={`border-b transition-all duration-300 ${
          isDarkMode ? 'bg-gray-800/90 border-gray-700/50' : 'bg-white/90 border-gray-200/50'
        } backdrop-blur-sm`}>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className={`font-bold text-lg ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                {t.chatHistory}
              </h3>
              <button
                onClick={clearHistory}
                className={`text-sm px-3 py-1.5 rounded-xl transition-all duration-200 hover:scale-105 ${
                  isDarkMode 
                    ? 'text-red-400 hover:bg-red-900/30' 
                    : 'text-red-600 hover:bg-red-50'
                }`}
              >
                Xóa tất cả
              </button>
            </div>
            
            {chatSessions.length === 0 ? (
              <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                {t.noHistory}
              </p>
            ) : (
              <div className="space-y-3 max-h-48 overflow-y-auto custom-scrollbar">
                {chatSessions.map((session) => (
                  <div
                    key={session.id}
                    onClick={() => loadSession(session)}
                    className={`p-4 rounded-2xl cursor-pointer transition-all duration-200 hover:scale-[1.02] ${
                      isDarkMode 
                        ? 'bg-gray-700/80 hover:bg-gray-600/80 border border-gray-600/20' 
                        : 'bg-gray-50/80 hover:bg-gray-100/80 border border-gray-200/50'
                    } backdrop-blur-sm shadow-sm hover:shadow-md`}
                  >
                    <div className="flex items-center justify-between">
                      <span className={`font-semibold text-sm ${
                        isDarkMode ? 'text-white' : 'text-gray-900'
                      }`}>
                        {session.name}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        isDarkMode 
                          ? 'text-gray-300 bg-gray-600/50' 
                          : 'text-gray-600 bg-gray-200/50'
                      }`}>
                        {session.messages.length} tin nhắn
                      </span>
                    </div>
                    <div className={`text-xs mt-2 ${
                      isDarkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>
                      {session.timestamp.toLocaleString('vi-VN')}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Enhanced Messages Container */}
      <div className="flex-1 overflow-y-auto chat-area p-6 space-y-4 transition-all duration-300 custom-scrollbar bg-gradient-to-br from-white/50 to-gray-50/30 dark:from-gray-800/50 dark:to-gray-900/30">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
          >
            <div
              className={`max-w-xs lg:max-w-md xl:max-w-lg px-6 py-4 rounded-3xl shadow-lg transition-all duration-200 hover:shadow-xl ${
                message.sender === 'user'
                  ? isDarkMode 
                    ? 'bg-gradient-to-br from-green-600 to-green-700 text-white ml-auto border border-green-500/30' 
                    : 'bg-gradient-to-br from-green-600 to-green-700 text-white ml-auto border border-green-500/30'
                  : isDarkMode
                    ? 'bg-gray-700/90 backdrop-blur-sm text-gray-100 border border-gray-600/30'
                    : 'bg-white/90 backdrop-blur-sm text-gray-800 border border-gray-200/50'
              }`}
            >
              <div className="flex items-start space-x-3">
                {message.sender === 'bot' && (
                  <div className={`p-2 rounded-full ${
                    isDarkMode ? 'bg-gray-600/50' : 'bg-gray-100'
                  }`}>
                    <Bot className={`w-5 h-5 ${
                      isDarkMode ? 'text-gray-400' : 'text-gray-500'
                    }`} />
                  </div>
                )}
                {message.sender === 'user' && (
                  <div className="p-2 rounded-full bg-green-500/20">
                    <User className="w-5 h-5 text-green-200" />
                  </div>
                )}
                <div className="flex-1">
                  <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.text}</p>
                  <p className={`text-xs mt-2 opacity-70 ${
                    message.sender === 'user' ? 'text-green-200' : ''
                  }`}>
                    {message.timestamp.toLocaleTimeString('vi-VN', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start animate-fade-in">
            <div className={`max-w-xs lg:max-w-md xl:max-w-lg px-6 py-4 rounded-3xl shadow-lg ${
              isDarkMode ? 'bg-gray-700/90 backdrop-blur-sm border border-gray-600/30' : 'bg-white/90 backdrop-blur-sm border border-gray-200/50'
            }`}>
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-gray-100 dark:bg-gray-600">
                  <Bot className={`w-5 h-5 ${
                    isDarkMode ? 'text-gray-400' : 'text-gray-500'
                  }`} />
                </div>
                <div className="loading-dots">
                  <div style={{ '--delay': '0ms' } as React.CSSProperties}></div>
                  <div style={{ '--delay': '200ms' } as React.CSSProperties}></div>
                  <div style={{ '--delay': '400ms' } as React.CSSProperties}></div>
                </div>
                <span className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                  {t.loading}
                </span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Enhanced Quick Suggestions */}
      {suggestions.length > 0 && (
        <div className="quick-actions px-6 py-6 transition-all duration-300 bg-gradient-to-r from-gray-50/50 to-white/50 dark:from-gray-800/50 dark:to-gray-900/50 backdrop-blur-sm border-t border-gray-200/30 dark:border-gray-700/30">
          <p className={`text-sm mb-4 font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            {t.quickReplies}
          </p>
          <div className="flex flex-wrap gap-3">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="quick-action-btn flex items-center space-x-3 px-4 py-3 rounded-2xl transition-all duration-200 hover:scale-105 hover:shadow-lg"
              >
                <span className="text-lg">{suggestion.icon}</span>
                <span className="text-sm font-medium">{suggestion.text}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Enhanced Input Form */}
      <div className="input-area p-6 transition-all duration-300 bg-gradient-to-r from-white/80 to-gray-50/80 dark:from-gray-800/80 dark:to-gray-900/80 backdrop-blur-sm border-t border-gray-200/50 dark:border-gray-700/50">
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={t.placeholder}
              className="input-field w-full px-6 py-4 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 rounded-3xl text-lg"
              disabled={isLoading}
            />
            {/* Subtle glow effect when focused */}
            <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-green-400/20 to-green-600/20 opacity-0 focus-within:opacity-100 transition-opacity duration-200 pointer-events-none"></div>
          </div>
          <button
            onClick={() => sendMessage()}
            disabled={!inputValue.trim() || isLoading}
            className={`p-4 rounded-3xl transition-all duration-200 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:scale-105 ${
              !inputValue.trim() || isLoading
                ? 'bg-gray-300 dark:bg-gray-600 cursor-not-allowed'
                : 'bg-gradient-to-br from-green-500 via-green-600 to-green-700 hover:from-green-600 hover:via-green-700 hover:to-green-800 shadow-xl hover:shadow-2xl'
            }`}
          >
            <Send className="w-6 h-6 text-white" />
          </button>
        </div>
        
        {/* Enhanced Session Info */}
        <div className={`flex items-center justify-between mt-6 text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          <div className="flex items-center space-x-4">
            <span>{messages.length} tin nhắn</span>
            <span>{new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}</span>
          </div>
          <div className={`px-3 py-1 rounded-full text-xs ${
            isConnected 
              ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' 
              : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
          }`}>
            {isConnected ? t.connected : t.disconnected}
          </div>
        </div>
      </div>
    </div>
  )
}