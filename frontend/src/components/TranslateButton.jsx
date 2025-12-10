import React, { useState } from 'react';

export default function TranslateButton() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleClick = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Simulate an async operation
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('Translate to Urdu button clicked! (Operation successful)');
    } catch (err) {
      setError('Failed to translate. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button onClick={handleClick} disabled={isLoading} style={{marginLeft: '10px'}}>
      {isLoading ? 'Translating...' : 'Translate to Urdu'}
      {error && <span role="alert" aria-live="assertive" style={{ color: 'red', marginLeft: '10px' }}>{error}</span>}
      {isLoading && <span aria-live="polite" className="sr-only">Loading...</span>}
    </button>
  );
}
