// Initialize the JS client
const { createClient } = require('@supabase/supabase-js')
require('dotenv').config();

const supa_url = process.env.SUPABASE_URL;
const supa_key = process.env.SUPABASE_KEY;
const supabase = createClient(supa_url, supa_key)

// Join a room/topic. Can be anything except for 'realtime'.

// Simple function to log any messages we receive
function gameAction(payload) {
  console.log(payload)
}

function createBroadcastChannel(channel, event) {
  const callback = supabase.channel(channel)
  // Init RlCard game
  // Payload is passed as action to Game obj; return state
  // Subscribe to the Channel
  callback
    .on(
      'broadcast',
      { event: event },
      (payload) => gameAction(payload, game)
    )
    .subscribe()
}


createBroadcastChannel("first-off", "trill")