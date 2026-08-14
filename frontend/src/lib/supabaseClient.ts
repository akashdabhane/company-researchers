import { createClient } from "@supabase/supabase-js";

let url = process.env.NEXT_PUBLIC_SUPABASE_URL || "https://placeholder.supabase.co";
let anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "placeholder-anon-key";

if (!url.startsWith("http://") && !url.startsWith("https://")) {
  url = "https://placeholder.supabase.co";
}

export const supabase = createClient(url, anonKey);
