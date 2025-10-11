import { render, screen } from '@testing-library/react';
import Home from '../page';

describe('Home Page', () => {
  it('renders the EasyFitness title', () => {
    render(<Home />);
    expect(screen.getByRole('heading', { name: /easyfitness/i })).toBeInTheDocument();
  });

  it('renders without crashing', () => {
    const { container } = render(<Home />);
    expect(container).toBeInTheDocument();
  });

  it('has proper page structure', () => {
    render(<Home />);
    
    // Check for main content area
    const main = screen.getByRole('main');
    expect(main).toBeInTheDocument();
  });

  it('contains navigation links', () => {
    render(<Home />);
    
    // Test for common navigation elements
    const links = screen.getAllByRole('link');
    expect(links.length).toBeGreaterThan(0);
  });

  it('is accessible', () => {
    const { container } = render(<Home />);
    
    // Basic accessibility checks
    expect(container.querySelector('h1')).toBeInTheDocument();
  });
});
