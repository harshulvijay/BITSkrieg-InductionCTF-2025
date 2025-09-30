# Mines CTF Challenge

A web-based minesweeper gambling game with a predictable RNG vulnerability.

## Challenge Goal

Accumulate **$1,000,000** to get the flag.

## Vulnerability

The game uses `server_time` (Unix timestamp) as the RNG seed, which is exposed to the client in the game start response.

## Solution

1. Start a game and capture the `server_time` value from the response
2. Use the same seed to predict mine positions:
   ```python
   import random
   random.seed(server_time)
   mine_positions = random.sample(range(25), 10)
   ```
3. Only click on safe tiles (positions not in `mine_positions`)
4. Cash out after revealing several safe tiles
5. Repeat until balance reaches $1,000,000

## Quick Start

```bash
docker-compose up --build
```

Access the game at: http://localhost:8080
