import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * A UI component for customizing textbook format preferences.
 * Allows users to select font size and layout.
 */
function FormatCustomizer({ initialPreferences, onPreferencesChange }) {
  const [fontSize, setFontSize] = useState(initialPreferences.font_size || 'medium');
  const [layout, setLayout] = useState(initialPreferences.layout || 'standard');

  useEffect(() => {
    // Call the callback when preferences change
    if (onPreferencesChange) {
      onPreferencesChange({ font_size: fontSize, layout: layout });
    }
  }, [fontSize, layout, onPreferencesChange]);

  const handleFontSizeChange = (event) => {
    setFontSize(event.target.value);
  };

  const handleLayoutChange = (event) => {
    setLayout(event.target.value);
  };

  return (
    <div className="format-customizer">
      <h3>Format Preferences</h3>
      <div className="form-group">
        <label htmlFor="font-size-select">Font Size:</label>
        <select id="font-size-select" value={fontSize} onChange={handleFontSizeChange}>
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="large">Large</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="layout-select">Layout:</label>
        <select id="layout-select" value={layout} onChange={handleLayoutChange}>
          <option value="standard">Standard</option>
          <option value="compact">Compact</option>
          <option value="spacious">Spacious</option>
        </select>
      </div>
    </div>
  );
}

FormatCustomizer.propTypes = {
  /**
   * Initial format preferences to pre-fill the component.
   */
  initialPreferences: PropTypes.shape({
    font_size: PropTypes.oneOf(['small', 'medium', 'large']),
    layout: PropTypes.oneOf(['standard', 'compact', 'spacious']),
  }),
  /**
   * Callback function to be called when preferences change.
   * Receives an object with the updated preferences: { font_size, layout }.
   */
  onPreferencesChange: PropTypes.func,
};

FormatCustomizer.defaultProps = {
  initialPreferences: {
    font_size: 'medium',
    layout: 'standard',
  },
  onPreferencesChange: () => {},
};

export default FormatCustomizer;
