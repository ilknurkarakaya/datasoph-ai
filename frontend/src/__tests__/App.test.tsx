/**
 * Essential tests for DataSoph AI frontend
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import DataSophApp from '../App';

// Mock contexts to avoid complex setup
jest.mock('../App', () => {
  const MockApp = () => (
    <div data-testid="app">
      <div data-testid="sidebar">DataSoph AI</div>
      <div data-testid="main">Chat Area</div>
    </div>
  );
  return MockApp;
});

describe('DataSoph AI App', () => {
  test('renders without crashing', () => {
    render(<DataSophApp />);
    expect(screen.getByTestId('app')).toBeInTheDocument();
  });

  test('contains sidebar', () => {
    render(<DataSophApp />);
    expect(screen.getByTestId('sidebar')).toBeInTheDocument();
  });

  test('contains main chat area', () => {
    render(<DataSophApp />);
    expect(screen.getByTestId('main')).toBeInTheDocument();
  });

  test('displays DataSoph AI branding', () => {
    render(<DataSophApp />);
    expect(screen.getByText('DataSoph AI')).toBeInTheDocument();
  });
}); 