import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TranslateButton from '../TranslateButton';

// Mock the alert function
global.alert = jest.fn();

describe('TranslateButton', () => {
  beforeEach(() => {
    global.alert.mockClear();
  });

  it('renders the button with the initial text', () => {
    render(<TranslateButton />);
    expect(screen.getByRole('button', { name: /Translate to Urdu/i })).toBeInTheDocument();
  });

  it('shows loading text and is disabled during the async operation', async () => {
    render(<TranslateButton />);
    const button = screen.getByRole('button', { name: /Translate to Urdu/i });
    
    fireEvent.click(button);
    
    expect(button).toBeDisabled();
    expect(screen.getByText(/Translating.../i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Translate to Urdu/i })).not.toBeDisabled();
    }, { timeout: 1500 });

    expect(screen.queryByText(/Translating.../i)).not.toBeInTheDocument();
  });

  it('calls the alert function after the async operation completes', async () => {
    render(<TranslateButton />);
    const button = screen.getByRole('button', { name: /Translate to Urdu/i });
    
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(global.alert).toHaveBeenCalledTimes(1);
    }, { timeout: 1500 });
    
    expect(global.alert).toHaveBeenCalledWith('Translate to Urdu button clicked! (Operation successful)');
  });
});
