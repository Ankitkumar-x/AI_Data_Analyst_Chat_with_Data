import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useState } from "react";

import { sendChatMessage } from "../services/api";
import ChartRenderer from "./ChartRenderer";

function cleanAssistantContent(content) {
  if (!content) {
    return "";
  }

  return content
    .replace(
      /!\[[^\]]*\]\([^)]*\)/g,
      ""
    )
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function ChatPanel() {

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  const handleSendMessage = async () => {

    const trimmedMessage = message.trim();

    if (!trimmedMessage || loading) {
      return;
    }

    setError("");

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: trimmedMessage,
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);

    setMessage("");

    setLoading(true);


    try {

        const conversationHistory = messages.map(
            (item) => ({
                role: item.role,
                content: item.content,
            })
        );

        const result = await sendChatMessage(
            trimmedMessage,
            conversationHistory
        );

        const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: result.answer,
        chart: result.chart,
        };

        
      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage,
      ]);

    } catch (error) {

      setError(error.message);

    } finally {

      setLoading(false);

    }
  };


  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      handleSendMessage();
    }
  };


  return (
    <main className="chat-panel">

      <div className="chat-header">

        <div>
          <h2>AI Analyst</h2>

          <p>
            Ask questions about your dataset
          </p>
        </div>

        <button
          className="new-chat-button"
          onClick={() => {
            setMessages([]);
            setError("");
            setMessage("");
          }}
          disabled={loading}
        >
          New Analysis
        </button>

      </div>


      <div className="chat-messages">

        {messages.length === 0 ? (

          <div className="welcome-message">

            <div className="welcome-icon">
              ✦
            </div>

            <h2>
              Welcome to AI Data Analyst
            </h2>

            <p>
              Upload a dataset and ask questions
              about your data in natural language.
            </p>

          </div>

        ) : (

          <div className="messages-list">

            {messages.map((item) => (

              <div
                key={item.id}
                className={`message ${
                  item.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >

                <div className="message-label">
                  {item.role === "user"
                    ? "You"
                    : "AI Analyst"}
                </div>

                <div className="message-content">

                  {item.role === "assistant" ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {cleanAssistantContent(item.content)}
                    </ReactMarkdown>
                  ) : (
                    item.content
                  )}

                  {item.chart && (
                    <ChartRenderer
                      chart={item.chart}
                      />
                )}

              </div>

              </div>

            ))}


            {loading && (

              <div className="message assistant-message">

                <div className="message-label">
                  AI Analyst
                </div>

                <div className="message-content typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

              </div>

            )}

          </div>

        )}

      </div>


      {error && (
        <div className="chat-error">
          <div className="chat-error-icon">
            ⚠
          </div>

          <div className="chat-error-content">
            <strong>Unable to complete the request</strong>
            <span>{error}</span>
          </div>

          <button
            className="chat-error-close"
            onClick={() => setError("")}
            type="button"
          >
            ×
          </button>
        </div>
      )}


      <div className="chat-input-area">

        <input
          type="text"
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask your data..."
          disabled={loading}
        />

        <button
          onClick={handleSendMessage}
          disabled={
            loading || !message.trim()
          }
        >
          {loading ? "..." : "Send"}
        </button>

      </div>

    </main>
  );
}


export default ChatPanel;