import { render, screen } from '@testing-library/react';
import RoutinePage from '../Workout/page';

describe('Routine Recommendation Page', () => {
  it('renders Routine Recommendation heading', () => {
    render(<RoutinePage />);
    expect(screen.getByRole('heading', { name: /routine recommendation/i })).toBeInTheDocument();
  });
});
