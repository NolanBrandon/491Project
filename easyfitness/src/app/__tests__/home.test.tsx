import { render, screen } from '@testing-library/react';
import Home from '../page';

describe('Home Page', () => {
  it('renders the EasyFitness title', () => {
    render(<Home />);
    expect(screen.getByRole('heading', { name: /easyfitness/i })).toBeInTheDocument();
  });
});
