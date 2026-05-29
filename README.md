# activeledger-agent

PLATO domain agent for [activeledger.ai](https://activeledger.ai) — writes transactions to PLATO, queries ledger state, and learns over time.

## What This Gives You

- **Ledger tile writes** — record transactions as PLATO tiles in the `activeledger` room
- **Query interface** — retrieve and aggregate ledger data from PLATO
- **Fleet integration** — connects to the PLATO tile server at `localhost:8847`

## Installation

```bash
pip install activeledger-agent
```

## Quick Start

```python
from activeledger_agent import write_tile, query_ledger

# Record a transaction
write_tile({
    "type": "credit",
    "amount": 12500.00,
    "source": "Acme Corp",
    "category": "revenue",
})

# Query recent entries
entries = query_ledger(room="activeledger", limit=50)
```

## Configuration

Set the PLATO tile server URL via environment variable:

```bash
export PLATO_TILE_URL=http://localhost:8847
```

## Testing

```bash
pip install -e .
pytest
```

## How It Fits

Domain agent in the Cocapn Fleet. Writes to the same PLATO instance as `businesslog-agent`, `capitaine-agent`, and other fleet agents.

## License

MIT
