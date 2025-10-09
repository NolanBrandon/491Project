import { render, screen } from '@testing-library/react';
import MyLogPage from '../mylog/page';

describe('My Log Page', () => {
  it('renders My Log heading', () => {
    render(<MyLogPage />);
    expect(screen.getByRole('heading', { name: /my log/i })).toBeInTheDocument();
  });
});
