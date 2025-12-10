import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * A UI component for selecting export format and triggering textbook export.
 */
function ExportOptions({ textbookId, onExport, disabled = false }) {
  const [selectedFormat, setSelectedFormat] = useState('pdf'); // Default to PDF

  const handleFormatChange = (event) => {
    setSelectedFormat(event.target.value);
  };

  const handleExportClick = () => {
    if (onExport && textbookId) {
      onExport(textbookId, selectedFormat);
    }
  };

  return (
    <div className="export-options">
      <h3>Export Textbook</h3>
      <div className="form-group">
        <label>Select Format:</label>
        <div className="radio-group">
          <label>
            <input
              type="radio"
              value="pdf"
              checked={selectedFormat === 'pdf'}
              onChange={handleFormatChange}
              disabled={disabled}
            />
            PDF
          </label>
          <label>
            <input
              type="radio"
              value="epub"
              checked={selectedFormat === 'epub'}
              onChange={handleFormatChange}
              disabled={disabled}
            />
            ePub
          </label>
        </div>
      </div>
      <button
        type="button"
        onClick={handleExportClick}
        disabled={disabled || !textbookId}
        className="export-btn"
      >
        Export
      </button>
    </div>
  );
}

ExportOptions.propTypes = {
  /**
   * The ID of the textbook to be exported.
   */
  textbookId: PropTypes.string.isRequired,
  /**
   * Callback function to be called when the export button is clicked.
   * Receives (textbookId, selectedFormat) as arguments.
   */
  onExport: PropTypes.func.isRequired,
  /**
   * Whether the export options should be disabled.
   */
  disabled: PropTypes.bool,
};

export default ExportOptions;
