function ChatWindow() {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "12px",
        height: "600px",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#ffffff",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "15px",
          borderBottom: "1px solid #ddd",
          fontWeight: "bold",
          fontSize: "18px",
        }}
      >
        AI Medical Assistant
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          padding: "15px",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "10px",
        }}
      >
        {/* AI Message */}
        <div
          style={{
            alignSelf: "flex-start",
            backgroundColor: "#e5e7eb",
            padding: "12px",
            borderRadius: "12px",
            maxWidth: "75%",
          }}
        >
          Hello! Upload a CT scan to begin analysis.
        </div>

        {/* User Message */}
        <div
          style={{
            alignSelf: "flex-end",
            backgroundColor: "#2563eb",
            color: "white",
            padding: "12px",
            borderRadius: "12px",
            maxWidth: "75%",
          }}
        >
          What is pneumonia?
        </div>

        {/* AI Reply */}
        <div
          style={{
            alignSelf: "flex-start",
            backgroundColor: "#e5e7eb",
            padding: "12px",
            borderRadius: "12px",
            maxWidth: "75%",
          }}
        >
          Pneumonia is an infection that inflames the air sacs in one or both lungs.
        </div>
      </div>

      {/* Input Area */}
      <div
        style={{
          borderTop: "1px solid #ddd",
          padding: "15px",
          display: "flex",
          gap: "10px",
        }}
      >
        <input
          type="text"
          placeholder="Ask about lung diseases..."
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />

        <button
          style={{
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            padding: "10px 20px",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;