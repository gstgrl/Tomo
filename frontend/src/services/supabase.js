import { createClient } from "@supabase/supabase-js";

const supabaseUrl = 'https://cedjdxzadrzxurbvtrmm.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNlZGpkeHphZHJ6eHVyYnZ0cm1tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkxMjI0MzEsImV4cCI6MjA2NDY5ODQzMX0.gxQ_noZFo4Uhw9FF36VFZ0Su7zbhygFK51ogK2xwFaE'

export const supabase = createClient(supabaseUrl, supabaseKey);
        