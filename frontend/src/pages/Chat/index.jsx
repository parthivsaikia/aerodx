import { useState, useRef, useEffect } from "react";
import "./Chat.css";

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "assistant",
      content:
        "Hello! I'm your AI medical assistant. I can help you understand your CT scan results, explain lung conditions, and answer health-related questions. How can I help you today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        role: "assistant",
        content: getSimulatedResponse(userMessage.content),
      };
      setMessages((prev) => [...prev, aiResponse]);
      setLoading(false);
    }, 1500);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="page chat-page">
      <div className="container">
        <div className="chat-layout">
          {/* Sidebar */}
          <aside className="chat-sidebar">
            <h3>AI Medical Assistant</h3>
            <p className="sidebar-desc">
              Ask questions about your scan results, lung conditions, or
              treatment options.
            </p>
            <div className="quick-questions">
              <h4>Quick Questions</h4>
              <button onClick={() => setInput("What is pneumonia?")}>
                What is pneumonia?
              </button>
              <button onClick={() => setInput("Explain my scan results")}>
                Explain my scan results
              </button>
              <button onClick={() => setInput("What treatment options are available?")}>
                Treatment options
              </button>
              <button onClick={() => setInput("Should I see a specialist?")}>
                Should I see a specialist?
              </button>
            </div>
          </aside>

          {/* Chat Window */}
          <div className="chat-window">
            <div className="chat-header">
              <div className="chat-header-info">
                <div className="chat-avatar">🤖</div>
                <div>
                  <h4>AeroDx Assistant</h4>
                  <span className="status-indicator">
                    <span className="status-pulse"></span>
                    Online
                  </span>
                </div>
              </div>
            </div>

            <div className="chat-messages">
              {messages.map((msg) => (
                <div key={msg.id} className={`message ${msg.role} msg-enter`}>
                  {msg.role === "assistant" && (
                    <div className="message-avatar">🤖</div>
                  )}
                  <div className="message-bubble">
                    <p>{msg.content}</p>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message assistant msg-enter">
                  <div className="message-avatar">🤖</div>
                  <div className="message-bubble typing">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-area">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about lung diseases..."
                disabled={loading}
                aria-label="Chat message input"
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className="send-btn"
                aria-label="Send message"
              >
                ➤
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function getSimulatedResponse(question) {
  const q = question.toLowerCase();
  if (q.includes("pneumonia")) {
    return "Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm, fever, chills, and difficulty breathing. It can be caused by bacteria, viruses, or fungi.";
  }
  if (q.includes("results") || q.includes("scan")) {
    return "Based on your latest scan analysis, the AI detected signs consistent with pneumonia with 94% confidence. The affected areas show characteristic ground-glass opacities in the lower lobes. I recommend discussing these findings with your pulmonologist.";
  }
  if (q.includes("treatment")) {
    return "Treatment depends on the type and severity. Bacterial pneumonia is typically treated with antibiotics. Viral pneumonia may require antiviral medications. Rest, fluids, and fever reducers are generally recommended. Severe cases may require hospitalization.";
  }
  if (q.includes("specialist")) {
    return "Given the AI findings, it would be advisable to consult a pulmonologist (lung specialist) who can review the full clinical picture including your symptoms, medical history, and these imaging results for a definitive diagnosis.";
  }
  return "That's a great question. While I can provide general medical information, please remember that this AI assistant is for educational purposes and should not replace professional medical advice. Would you like me to explain anything specific about lung conditions or your scan results?";
}

export default ChatPage;
