import { render, screen } from '@testing-library/react';
import CalculationPage from '../Progress/page';

describe('Progress Page', () => {
  it('renders Progress heading', () => {
    render(<CalculationPage />);
    expect(screen.getByRole('heading', { name: /progress/i })).toBeInTheDocument();
  });
});
