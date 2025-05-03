/*
Messages page for doctors and patients to send and receive messages.
*/

import './Messages.css';
import React, { useState, useRef } from 'react'; 
import Navbar from './Navbar';

function Messages({ role }) {
  const [userMessage, setUserMessage] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const handleSendMessage = async () => {
    if (!userMessage.trim()) return // Don't send empty messages

    // Add user's message to chat
    const newMessages = [...messages, { sender: "You", text: userMessage }]
    setMessages(newMessages)
    setUserMessage("") 
    setLoading(true) 

    try {
      const response = await fetch("http://localhost:5000/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      })

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`)
      }

      const data = await response.json()

      if (data.response) {
        setMessages([...newMessages, { sender: "Sender", text: data.response }])
      } else {
        setMessages([...newMessages, { sender: "Sender", text: "Error: Could not get response." }])
      }
    } catch (error) {
      console.error("Error:", error)
      setMessages([
        ...newMessages,
        { sender: "Sender", text: `Error: ${error.message || "Could not reach server."}` },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="app">
    <Navbar role={role} />
      <h1>Messages</h1>
      <div className="chat-box">
        <div className="messages">
          {messages.length === 0 && <div className="empty-state">Start a chat...</div>}
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender === "You" ? "user" : "sender"}`}>
              <strong>{msg.sender}:</strong> {msg.text}
            </div>
          ))}
          {loading && <div className="loading">✨Awaiting Response</div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="input-container">
          <textarea className="input-texts"
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a message..."
            rows={2}
            disabled={loading}
          />
          <button className="send-button" onClick={handleSendMessage} disabled={loading}>
            {loading ? "..." :"Send"}
          </button>
        </div>
      </div>
    </div>
  )
}

export default Messages