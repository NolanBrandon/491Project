// src/app/ClientWrapper.tsx
'use client';

import { SessionContextProvider } from '@supabase/auth-helpers-react';
import { supabase } from '../lib/supabaseClient';
import Nav from './components/navbar';
import Footer from './components/footer';

export default function ClientWrapper({ children }: { children: React.ReactNode }) {
  return (
    <SessionContextProvider supabaseClient={supabase}>
      <div className="page-container blur-bg">
        <Nav />
        {children}
        <Footer />
      </div>
    </SessionContextProvider>
  );
}
