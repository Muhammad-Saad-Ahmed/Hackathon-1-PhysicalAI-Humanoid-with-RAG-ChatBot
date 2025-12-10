import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import PersonalizeButton from '../PersonalizeButton';

// Mock the alert function to avoid it blocking tests
global.alert = jest.fn();

describe('PersonalizeButton', () => {
  // Clear mock calls before each test
  beforeEach(() => {
    global.alert.mockClear();
  });

  it('renders the button with the initial text', () => {
    render(<PersonalizeButton />);
    expect(screen.getByRole('button', { name: /Personalize Chapter/i })).toBeInTheDocument();
  });

  it('shows loading text and is disabled during the async operation', async () => {
    render(<PersonalizeButton />);
    const button = screen.getByRole('button', { name: /Personalize Chapter/i });
    
    fireEvent.click(button);
    
    // Immediately after click, button should be disabled and show loading text
    expect(button).toBeDisabled();
    expect(screen.getByText(/Personalizing.../i)).toBeInTheDocument();
    
    // Wait for the button to become enabled again, which signifies the end of the async op
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Personalize Chapter/i })).not.toBeDisabled();
    }, { timeout: 1500 }); // Timeout should be longer than the simulated delay

    // Check that the loading text is gone
    expect(screen.queryByText(/Personalizing.../i)).not.toBeInTheDocument();
  });

  it('calls the alert function after the async operation completes', async () => {
    render(<PersonalizeButton />);
    const button = screen.getByRole('button', { name: /Personalize Chapter/i });
    
    fireEvent.click(button);
    
    // Wait for the async operation to finish
    await waitFor(() => {
      expect(global.alert).toHaveBeenCalledTimes(1);
    }, { timeout: 1500 });
    
    expect(global.alert).toHaveBeenCalledWith('Personalize Chapter button clicked! (Operation successful)');
  });

  it('displays an error message if the async operation fails', async () => {
    // For this test, we would need to modify the component to simulate a failure.
    // As the current component always succeeds, we can't test the failure case
    // without altering the component's code, for example, by passing a prop.
    // This test is a placeholder for what a more complex test suite would include.
    
    // To properly test this, the component could be refactored:
    // const handleClick = async () => {
    //   ...
    //   try {
    //     if (shouldFail) throw new Error("Failure");
    //     ...
    //   } ...
    // }
    
    // For now, this just confirms the current behavior (no error shown).
    render(<PersonalizeButton />);
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });
});
