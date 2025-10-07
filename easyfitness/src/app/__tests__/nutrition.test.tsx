import { render, screen } from '@testing-library/react';
import CalorieTrack from '../Nutrition/page';

describe('Nutrition Page', () => {
  it('renders Nutrition heading', () => {
    render(<CalorieTrack />);
    expect(screen.getByRole('heading', { name: /nutrition/i })).toBeInTheDocument();
  });
});
