import { createClient } from '@supabase/supabase-js'

const supabaseUrl = "https://wzgxtvqkivbiinkoewmf.supabase.co"
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6Z3h0dnFraXZiaWlua29ld21mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc0NTM4MDEsImV4cCI6MjA3MzAyOTgwMX0.N4EcHLKB1EXyUVUTf3OhlJ6P-bss2C0A5xPvt7GQ3VE"

export const supabase = createClient(supabaseUrl, supabaseKey)
