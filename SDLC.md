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
3. Patch functions to RlCard ws & Redis to Supabase
    1. Assume every casino-server variables are needed for a normal functionality
    2. Reduce the variables for rlcard integration
    3. Patch new RlCard games from casino-server if need be
    4. test new patched rl-card server  

- Future DEVs
1. Each socket execution should runs on one game instance
2. Try Multi-threading or Multi-processing as last resort

#### C. RlCard python REST w/ DB

NB: REST DB Server Error
- Cannot create a single instance of a game for one express server. Trying WebSockets
