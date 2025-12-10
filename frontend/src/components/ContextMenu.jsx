import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import './ContextMenu.css'; // Assuming a CSS file for styling

/**
 * A UI component for displaying a context menu near selected text.
 */
function ContextMenu({ selectedText, position, onAskChatbot, onClose }) {
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  const handleAskChatbot = () => {
    onAskChatbot(selectedText);
    onClose();
  };

  if (!selectedText || !position) {
    return null;
  }

  return (
    <div
      ref={menuRef}
      className="context-menu"
      style={{
        top: position.y,
        left: position.x,
      }}
    >
      <button onClick={handleAskChatbot} className="context-menu-item">
        Ask Chatbot about "{selectedText.substring(0, 30)}..."
      </button>
    </div>
  );
}

ContextMenu.propTypes = {
  /**
   * The text that was selected by the user.
   */
  selectedText: PropTypes.string,
  /**
   * The position (x, y) where the context menu should appear.
   */
  position: PropTypes.shape({
    x: PropTypes.number.isRequired,
    y: PropTypes.number.isRequired,
  }),
  /**
   * Callback function to be called when "Ask Chatbot" is clicked.
   * Receives the selectedText as an argument.
   */
  onAskChatbot: PropTypes.func.isRequired,
  /**
   * Callback function to be called when the context menu should be closed.
   */
  onClose: PropTypes.func.isRequired,
};

export default ContextMenu;
