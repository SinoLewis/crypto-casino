// Initialize the JS client
const { createClient } = require('@supabase/supabase-js')
require('dotenv').config();

const supa_url = process.env.SUPABASE_URL;
const supa_key = process.env.SUPABASE_KEY;
const supabase = createClient(supa_url, supa_key)

// Join a room/topic. Can be anything except for 'realtime'.
const channelB = supabase.channel('first-off')

channelB.send({
  type: 'broadcast',
  event: 'trill',
  payload: { message: `Never worked in the gym, \n but I weighed it` },
})
// channelB.subscribe((status) => {
//   // Wait for successful connection
//   if (status !== 'SUBSCRIBED') {
//     return null
//   }

//   // Send a message once the client is subscribed
//   channelB.send({
//     type: 'broadcast',
//     event: 'test',
//     payload: { message: 'hello, world' },
//   })
// })
