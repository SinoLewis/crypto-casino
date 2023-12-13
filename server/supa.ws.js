// Initialize the JS client
const { createClient } = require('@supabase/supabase-js')
require('dotenv').config();

const supa_url = process.env.SUPABASE_URL;
const supa_key = process.env.SUPABASE_KEY;
const supabase = createClient(supa_url, supa_key)

// Create a function to handle inserts
const handleInserts = (payload) => {
  console.log('Change received!', payload)
}

// Listen to inserts
supabase
  .channel('todos')
  .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'limitholdem' }, handleInserts)
  .subscribe()
