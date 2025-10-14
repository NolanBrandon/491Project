'use client';

import { useState, useEffect } from 'react';
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button } from "@heroui/react";
import { supabase } from '../../lib/supabaseClient';
import { useRouter } from 'next/navigation';

export default function Nav() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

  // Track user session
  useEffect(() => {
    // Fetch current session (async)
    const fetchSession = async () => {
      const { data } = await supabase.auth.getSession();
      setUser(data.session?.user ?? null);
    };
    fetchSession();

    // Listen to auth state changes
    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => {
      listener.subscription.unsubscribe();
    };
  }, []);

  // Logout handler
  const handleLogout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) {
      alert('Logout failed: ' + error.message);
    } else {
      router.push('/signup'); // redirect to signup after logout
    }
  };

  return (
    <Navbar className="nav-root">
      {/* Left: Brand/Logo */}
      <NavbarContent justify="center" className="nav-left">
        <NavbarBrand>
          <Link href="/" className="nav-brand">Home</Link>
        </NavbarBrand>
      </NavbarContent>

      {/* Center: Navigation Links */}
      <NavbarContent className="nav-center" justify="center">
        <NavbarItem>
          <Link href="/mylog" className="nav-link">My Log</Link>
        </NavbarItem>
        <NavbarItem>
          <Link href="/routines" className="nav-link">Routines</Link>
        </NavbarItem>
        <NavbarItem>
          <Link href="/Nutrition" className="nav-link">Nutrition</Link>
        </NavbarItem>
        <NavbarItem>
          <Link href="/Progress" className="nav-link">Progress</Link>
        </NavbarItem>

        {/* Conditional Auth Links */}
        <NavbarItem>
          {user ? (
            <Button variant="destructive" size="sm" onClick={handleLogout}>
              Logout
            </Button>
          ) : (
            <div className="flex gap-4">
              <Link href="/signup" className="nav-link">Sign Up</Link>
              <Link href="/signup" className="nav-link">Sign In</Link>
            </div>
          )}
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}
