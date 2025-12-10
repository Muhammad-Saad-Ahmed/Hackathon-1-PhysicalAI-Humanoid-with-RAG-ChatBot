import React, { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import './ChatWidget.css'; // Assuming a CSS file for styling

/**
 * A UI component for interacting with the RAG chatbot.
 * Displays chat messages, allows user input, and shows source attributions.
 */
function ChatWidget({ textbookId }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleInputChange = (event) => {
    setInputMessage(event.target.value);
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputMessage };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const requestBody = {
        query: userMessage.content,
        textbook_id: textbookId,
        session_id: sessionId,
      };

      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const assistantMessage = {
        role: 'assistant',
        content: data.response,
        sources: data.sources,
      };

      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
      setSessionId(data.session_id); // Update session ID if a new one was created
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'assistant', content: `Error: ${error.message}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="chat-widget">
      <div className="chat-header">
        <h4>Textbook Chatbot</h4>
        {textbookId && <small>Textbook ID: {textbookId}</small>}
      </div>
      <div className="chat-messages">
        {messages.length === 0 && !isLoading && (
            <div className="chat-welcome">
                <p>Hello! Ask me anything about this textbook.</p>
            </div>
        )}
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <div className="message-bubble">
              <p>{msg.content}</p>
              {msg.sources && msg.sources.length > 0 && (
                <div className="message-sources">
                  <strong>Sources:</strong>
                  <ul>
                    {msg.sources.map((source, sIndex) => (
                      <li key={sIndex}>
                        {source.title} (Relevance: {source.relevance_score.toFixed(2)})
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="chat-message assistant loading">
            <div className="message-bubble">
              <p>...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={inputMessage}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question..."
          disabled={isLoading || !textbookId}
        />
        <button onClick={sendMessage} disabled={isLoading || !inputMessage.trim() || !textbookId}>
          Send
        </button>
      </div>
    </div>
  );
}

ChatWidget.propTypes = {
  /**
   * The ID of the textbook the chatbot is associated with.
   */
  textbookId: PropTypes.string.isRequired,
};

export default ChatWidget;
