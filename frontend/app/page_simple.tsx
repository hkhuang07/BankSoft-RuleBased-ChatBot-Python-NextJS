'use client'

import React, { useState, useEffect, useRef } from 'react'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

interface ChatState {
  current_state: string
}

const API_BASE_URL = 'http://localhost:5000/api'

// Icon components sử dụng Unicode symbols
const Icon = {
  Send: () => <span className="text-lg">📤</span>,
  RotateCcw: () => <span className="text-lg">🔄</span>,
  MessageCircle: () => <span className="text-2xl">💬</span>,
  CreditCard: () => <span className="text-lg">💳</span>,
  Phone: () => <span className="text-lg">📱</span>,
  FileText: () => <span className="text-lg">📋</span>,
  Fingerprint: () => <span className="text-lg">👆</span>,
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => Math.random().toString(36).substring(7))
  const [chatState, setChatState] = useState<ChatState>({ current_state: 'wait' })
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Gửi tin nhắn chào mừng khi component mount
    handleWelcomeMessage()
  }, [])

  const handleWelcomeMessage = async () => {
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
      } else {
        throw new Error('Failed to send message')
      }
    } catch (error) {
      console.error('Error:', error)
      addBotMessage('Xin lỗi, có lỗi xảy ra. Vui lòng thử lại!')
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

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage = inputValue.trim()
    setInputValue('')
    addUserMessage(userMessage)
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setTimeout(() => {
          addBotMessage(data.response)
          setChatState({ current_state: data.state })
        }, 500) // Thêm delay để tạo cảm giác tự nhiên hơn
      } else {
        throw new Error('Failed to send message')
      }
    } catch (error) {
      console.error('Error:', error)
      setTimeout(() => {
        addBotMessage('Xin lỗi, có lỗi xảy ra. Vui lòng thử lại!')
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
      setTimeout(() => {
        handleWelcomeMessage()
      }, 100)
    }
  }

  const quickReplies = [
    { icon: <Icon.CreditCard />, text: 'Chuyển tiền', value: 'chuyển tiền' },
    { icon: <Icon.Phone />, text: 'Nạp tiền điện thoại', value: 'nạp tiền điện thoại' },
    { icon: <Icon.FileText />, text: 'Thanh toán hóa đơn', value: 'thanh toán hóa đơn' },
    { icon: <Icon.Fingerprint />, text: 'Cập nhật sinh trắc học', value: 'cập nhật sinh trắc học' },
  ]

  const handleQuickReply = (value: string) => {
    setInputValue(value)
  }

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto bg-white shadow-xl">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Icon.MessageCircle />
            <div>
              <h1 className="text-xl font-bold">Bank-SoftAI</h1>
              <p className="text-blue-100 text-sm">Hỗ trợ khách hàng ngân hàng</p>
            </div>
          </div>
          <button
            onClick={resetChat}
            className="p-2 hover:bg-blue-700 rounded-full transition-colors"
            title="Bắt đầu lại"
          >
            <Icon.RotateCcw />
          </button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow-sm ${
                message.sender === 'user' 
                  ? 'bg-blue-500 text-white ml-auto' 
                  : 'bg-white text-gray-800 border border-gray-200'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.text}</p>
              <p className="text-xs opacity-70 mt-1">
                {message.timestamp.toLocaleTimeString('vi-VN', {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start animate-fade-in">
            <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow-sm bg-white text-gray-800 border border-gray-200">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{animationDelay: '0ms'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{animationDelay: '200ms'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{animationDelay: '400ms'}}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Replies */}
      {chatState.current_state === 'main_menu' && (
        <div className="px-4 py-2 bg-white border-t border-gray-200">
          <p className="text-sm text-gray-600 mb-2">Phản hồi nhanh:</p>
          <div className="flex flex-wrap gap-2">
            {quickReplies.map((reply, index) => (
              <button
                key={index}
                onClick={() => handleQuickReply(reply.value)}
                className="flex items-center space-x-2 px-3 py-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-lg transition-colors text-sm"
              >
                {reply.icon}
                <span>{reply.text}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Form */}
      <div className="p-4 bg-white border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Nhập tin nhắn của bạn..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center space-x-2"
          >
            <Icon.Send />
            <span className="hidden sm:inline">Gửi</span>
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Nhấn Enter để gửi tin nhắn. Gõ "Hi" để bắt đầu lại.
        </p>
      </div>
    </div>
  )
}