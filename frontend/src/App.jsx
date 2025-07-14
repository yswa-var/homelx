import { useState, useRef, useEffect } from 'react'
import Recorder from './components/Recorder'
import Player from './components/Player'
import './App.css'

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [currentAudioBlob, setCurrentAudioBlob] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleTranscription = async (transcribedText) => {
    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: transcribedText,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Send to GPT and get response
    await sendToGPT(transcribedText);
  };

  const sendToGPT = async (message) => {
    setIsLoading(true);
    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          conversationId
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add assistant message to chat
      const assistantMessage = {
        id: Date.now() + 1,
        text: data.reply,
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      setConversationId(data.conversationId);

      // Convert response to speech
      await textToSpeech(data.reply);
      
    } catch (error) {
      console.error('Error sending message to GPT:', error);
      alert('Error communicating with GPT. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const textToSpeech = async (text) => {
    try {
      const response = await fetch('/tts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const audioBlob = await response.blob();
      setCurrentAudioBlob(audioBlob);
      
    } catch (error) {
      console.error('Error converting text to speech:', error);
      // Don't show alert for TTS errors as it's not critical
    }
  };

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const message = formData.get('message').trim();
    
    if (message) {
      e.target.reset();
      await sendToGPT(message);
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🎙️ Voice Chat with GPT</h1>
          <p>Use voice or text to chat with AI</p>
        </div>
        
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <p>Start a conversation by recording your voice or typing a message!</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender === 'user' ? 'user-message' : 'assistant-message'}`}
              >
                <div className="message-content">
                  <p>{message.text}</p>
                  <span className="timestamp">{message.timestamp}</span>
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="message assistant-message">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="input-section">
          <Recorder onTranscription={handleTranscription} />
          
          <form onSubmit={handleTextSubmit} className="text-input-form">
            <input
              type="text"
              name="message"
              placeholder="Or type your message here..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              Send
            </button>
          </form>
          
          {currentAudioBlob && (
            <Player audioBlob={currentAudioBlob} />
          )}
        </div>
      </div>
    </div>
  )
}

export default App
