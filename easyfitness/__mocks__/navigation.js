// __mocks__/next/navigation.js
export const useRouter = () => ({
  push: jest.fn(),
  replace: jest.fn(),
  prefetch: jest.fn(),
});

export const usePathname = () => '/';
export const useSearchParams = () => new URLSearchParams();
