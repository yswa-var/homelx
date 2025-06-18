import React, { useState, useRef } from "react";
import "./App.css";

// Configurable API base URL - can be overridden for global deployment
const API_BASE = process.env.REACT_APP_API_BASE || "https://yash-backend.loca.lt";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [recording, setRecording] = useState(false);
  const [micAccessible, setMicAccessible] = useState(true);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const chatboxRef = useRef(null);

  // Fetch user info on mount
  React.useEffect(() => {
    fetch(`${API_BASE}/api/user_info`)
      .then(res => res.json())
      .then(setUserInfo)
      .catch(() => {});
    
    // Test API connectivity
    fetch(`${API_BASE}/api/test`)
      .then(res => res.json())
      .then(data => console.log("API test:", data))
      .catch(err => console.error("API test failed:", err));
  }, []);

  // Scroll to bottom on new messages
  React.useEffect(() => {
    if (chatboxRef.current) {
      chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
    }
  }, [messages]);

  // Check mic access on mount
  React.useEffect(() => {
    const checkMicAccess = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(t => t.stop());
        setMicAccessible(true);
      } catch (error) {
        console.log("Microphone access error:", error);
        setMicAccessible(false);
        
        // Check if it's a protocol issue (HTTP vs HTTPS)
        if (window.location.protocol === 'http:' && window.location.hostname !== 'localhost') {
          console.warn("Microphone access blocked: HTTPS required for network access");
        }
      }
    };
    checkMicAccess();
  }, []);

  const sendText = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages(msgs => [...msgs, { role: "user", content: input.trim() }]);
    setInput("");
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: input, input_type: "text" })
      });
      const data = await res.json();
      setMessages(msgs => [...msgs, { role: "assistant", content: data.answer || "Sorry, I couldn't process that request." }]);
      setAudioUrl(data.audio_url ? `${API_BASE}${data.audio_url}` : null);
    } catch (e) {
      console.error("Text Error:", e);
      setMessages(msgs => [...msgs, { role: "assistant", content: "Error communicating with server." }]);
    }
    setLoading(false);
  };

  const sendVoiceBlob = async (blob) => {
    setLoading(true);
    // Add a placeholder for the user's voice message
    setMessages(msgs => [...msgs, { role: "user", content: "🎙️ Processing voice..." }]);
    const formData = new FormData();
    formData.append("file", blob, "recording.wav");
    try {
      const res = await fetch(`${API_BASE}/api/voice`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      // Update the last user message with the transcribed text
      setMessages(msgs => {
        const updated = [...msgs];
        // Find the last user message with the placeholder
        for (let i = updated.length - 1; i >= 0; i--) {
          if (updated[i].role === "user" && updated[i].content === "🎙️ Processing voice...") {
            updated[i] = { ...updated[i], content: data.question ? data.question.split('\n')[0] : "[Voice message]" };
            break;
          }
        }
        // Add the assistant's response
        return [...updated, { role: "assistant", content: data.answer || "Sorry, I couldn't process that voice message." }];
      });
      setAudioUrl(data.audio_url ? `${API_BASE}${data.audio_url}` : null);
    } catch (e) {
      console.error("Voice Error:", e);
      setMessages(msgs => {
        const updated = [...msgs];
        // Find the last user message with the placeholder and update it
        for (let i = updated.length - 1; i >= 0; i--) {
          if (updated[i].role === "user" && updated[i].content === "🎙️ Processing voice...") {
            updated[i] = { ...updated[i], content: "[Voice message - Error processing]" };
            break;
          }
        }
        return [...updated, { role: "assistant", content: "Error communicating with server." }];
      });
    }
    setLoading(false);
  };

  const startRecording = async () => {
    if (!navigator.mediaDevices) {
      alert("Media devices not supported in this browser.");
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new window.MediaRecorder(stream);
      audioChunksRef.current = [];
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        sendVoiceBlob(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      setMicAccessible(false);
      alert("Could not start recording: " + err.message);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const clearChat = async () => {
    await fetch(`${API_BASE}/api/clear`, { method: "POST" });
    setMessages([]);
    setAudioUrl(null);
  };

  const deleteAudioFiles = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/delete_audio_files`, { method: "POST" });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      alert("All audio files deleted.");
    } catch (error) {
      console.error("Error deleting audio files:", error);
      alert("Failed to delete audio files. Please try again.");
    }
  };

  return (
    <div className="app-root">
      <div className="sidebar-userinfo dark-sidebar">
        <h3>Contact Info</h3>
        <div><b style={{ color: '#7ecfff' }}>Email:</b> <a href="mailto:yswa.var@icloud.com">yswa.var@icloud.com</a></div>
        <div><b style={{ color: '#7ecfff' }}>Phone:</b> <a href="tel:+916396300355">+91 6396300355</a></div>
        <div><b style={{ color: '#7ecfff' }}>LinkedIn:</b> <a href="https://linkedin.com/in/yashaswa-varshney" target="_blank" rel="noopener noreferrer">linkedin.com/in/yashaswa-varshney</a></div>
        <div><b style={{ color: '#7ecfff' }}>GitHub:</b> <a href="https://github.com/yswa-var" target="_blank" rel="noopener noreferrer">github.com/yswa-var</a></div>
      </div>
      <div className="container dark-container">
        <h2>Yash's Chatbot</h2>
        {userInfo && (
          <div className="userinfo">
            <b>{userInfo.name}</b> | {userInfo.current_role}
          </div>
        )}
        <div className="chatbox dark-chatbox" ref={chatboxRef}>
          {messages.map((msg, i) => (
            <div key={i} className={`message-row ${msg.role}`}> 
              <div className="message-bubble">
                <b style={{ fontWeight: 500 }}>{msg.role === "user" ? "You" : "Yash"}:</b><br />
                {(msg.content || "").split('\n').map((line, idx) => <div key={idx}>{line}</div>)}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message-row assistant">
              <div className="message-bubble">
                <span className="typing-indicator">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </span>
              </div>
            </div>
          )}
        </div>
        {audioUrl && (
          <audio controls src={audioUrl} style={{ margin: '16px 0 0 0', background: '#232323', borderRadius: 6 }}>
            Your browser does not support the audio element.
          </audio>
        )}
        <div className="input-row">
          <input
            type="text"
            value={input}
            disabled={loading}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && sendText()}
            placeholder="Type your message..."
          />
          <button onClick={sendText} disabled={loading || !input.trim()}>Send</button>
          <button
            onClick={recording ? stopRecording : startRecording}
            disabled={loading || !micAccessible}
            style={{ background: recording ? '#d9534f' : undefined }}
            title={!micAccessible ? 
              (window.location.protocol === 'http:' && window.location.hostname !== 'localhost' 
                ? "Microphone access blocked: HTTPS required for network access" 
                : "Microphone access denied") 
              : undefined}
          >
            {recording ? "Stop" : "Record"}
          </button>
          {recording && <span className="recording-indicator">● Recording...</span>}
          <button onClick={clearChat} disabled={loading}>Clear</button>
          <button onClick={deleteAudioFiles} disabled={loading} title="Delete all audio files">🗑️🔊</button>
        </div>
      </div>
    </div>
  );
}

export default App;
