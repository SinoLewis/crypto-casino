# Crypto Casino

## 1. Requirements

1. RlCard Server
    1. RlCard Node Supabase realtime
    2. RlCard python Web Socket
    3. RlCard python REST w/ DB
2. React Client App
2. Web3 Wallet functions

## 2. Sys Design

### 2.1 RlCard Server

#### A. RlCard Node Supabase realtime

1. ReCode RLCard to Node
2. Each channel has a unique name & event;Thus A channel can hold a single game execution
3. SERVER: Create Postgres Realtime for listening for new game rooms, each new game spawns a new broadcast realtime channel for that game room 
4. CLIENT: Game stores are subcribed to database change or Sends broadcast message to its specific channel


#### B. RlCard python Web Socket

1. Create Dynamic Socket client json parsed data for each game stored in a dictonary.
2. Enumerate Casino production functonality from [floatinghotpot casino-server](https://github.com/floatinghotpot/casino-server)
3. Patch functions to RlCard ws & Redis API's to Supabase API's
    1. Test env for Redis & Supabase's API to match data types of Params & return

- Future DEVs
1. Each socket execution should runs on one game instance
2. Try Multi-threading or Multi-processing as last resort

#### C. RlCard python REST w/ DB

NB: REST DB Server Error
- Cannot create a single instance of a game for one express server. Trying WebSockets

### 2.2 RlCard Client

> Svelte & React Apps

1. Create a Test env for Jquery & Svelte
2. Patch Jquery Client API's w/ Svelte API's
    1. Svelte new funcs will use params: Events & HTML var Bindings API for jquery var DOM element
    2. The new functions will be export for svelte components
    3. Add Casino UI Compos
3. Create a new reatc app from the new Svlete app
