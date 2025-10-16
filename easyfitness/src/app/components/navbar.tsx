'use client';

import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button } from "@heroui/react";
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function Nav() {
  const router = useRouter();
  const { logout, isAuthenticated, user, loading } = useAuth();

  // Logout handler
  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <Navbar className="nav-root">
      {/* Left: Brand/Logo centered in left section */}
      <NavbarContent justify="center" className="nav-left">
        <NavbarBrand>
          <Link href="/" className="nav-brand">Home</Link>
        </NavbarBrand>
      </NavbarContent>

      {/* Center: Navigation Headers */}
      <NavbarContent className="nav-center" justify="center">
        <NavbarItem>
          <Link as={Link} href="/mylog" color="foreground" className="nav-link">
            My Log
          </Link>
        </NavbarItem>
        <NavbarItem isActive>
          <Link aria-current="page" href="/routines" className="nav-link">
            Routines
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/Nutrition" className="nav-link">
            Nutrition
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="/Progress" className="nav-link">
            Progress
          </Link>
        </NavbarItem>
        
        {/* Show user info and logout when authenticated */}
        {!loading && isAuthenticated && user && (
          <>
            <NavbarItem>
              <span className="text-sm text-foreground">
                Welcome, {user.username}
              </span>
            </NavbarItem>
            <NavbarItem>
              <Button
                color="danger"
                size="sm"
                onClick={handleLogout}
              >
                Logout
              </Button>
            </NavbarItem>
          </>
        )}
        
        {/* Show login link when not authenticated */}
        {!loading && !isAuthenticated && (
          <NavbarItem>
            <Button
              as={Link}
              href="/login"
              color="primary"
              size="sm"
            >
              Login
            </Button>
          </NavbarItem>
        )}
      </NavbarContent>
    </Navbar>
  );
}
