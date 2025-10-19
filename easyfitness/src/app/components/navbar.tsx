'use client';

import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Link } from "@heroui/react";
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function Nav() {
  const router = useRouter();
  const { logout, isAuthenticated, loading } = useAuth();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <Navbar className="nav-root">
      {/* Left: Brand/Logo centered in left section */}
      <NavbarContent justify="center" className="nav-left">
        <NavbarBrand>
          <Link href="/dashboard" className="nav-link">Home</Link>
        </NavbarBrand>
      </NavbarContent>

      {/* Center: Navigation Headers */}
      <NavbarContent className="nav-center" justify="center">
        <NavbarItem>
          <Link href="/mylog" color="foreground" className="nav-link">
            My Log
          </Link>
        </NavbarItem>

        <NavbarItem isActive>
          <Link
            aria-current="page"
            href="/workout-plan-generator"
            className="nav-link text-black font-semibold"
          >
            Workout
          </Link>
        </NavbarItem>

        <NavbarItem>
          <Link color="foreground" href="/Nutrition" className="nav-link">
            Nutrition
          </Link>
        </NavbarItem>

        <NavbarItem>
          <Link color="foreground" href="/Progress" className="nav-link">
            Goals
          </Link>
        </NavbarItem>

        {/* Show logout when authenticated */}
        {!loading && isAuthenticated && (
          <NavbarItem>
            <button
              onClick={handleLogout}
              className="nav-link cursor-pointer bg-transparent border-none text-black"
            >
              Logout
            </button>
          </NavbarItem>
        )}

        {/* Show login link when not authenticated */}
        {!loading && !isAuthenticated && (
          <NavbarItem>
            <Link href="/login" className="nav-link text-black">
              Login
            </Link>
          </NavbarItem>
        )}
      </NavbarContent>
    </Navbar>
  );
}
