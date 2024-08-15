import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import Login from './Login';

test('renders login form', () => {
  const { getByLabelText, getByText } = render(<Login />);
  expect(getByLabelText(/username/i)).toBeInTheDocument();
  expect(getByLabelText(/password/i)).toBeInTheDocument();
  expect(getByText(/sign in/i)).toBeInTheDocument();
});

test('submits form with username and password', async () => {
  const mockLogin = jest.fn();
  const { getByLabelText, getByText } = render(<Login onLogin={mockLogin} />);
  fireEvent.change(getByLabelText(/username/i), { target: { value: 'testuser' } });
  fireEvent.change(getByLabelText(/password/i), { target: { value: 'testpass' } });
  fireEvent.click(getByText(/sign in/i));
  await waitFor(() => expect(mockLogin).toHaveBeenCalled());
});