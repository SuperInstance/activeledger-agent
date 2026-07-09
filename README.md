# activeledger-agent

A Python client that writes activity, investment, and trade entries to a [PLATO](https://github.com/SuperInstance) tile server and queries them back. Built on the `fleet-agent` base class.

## Status

- ✅ **Ledger writes** — record activities, investments, and trades as PLATO tiles via `ActiveLedgerAgent`
- ✅ **Query interface** — `ask()` retrieves recent ledger tiles from PLATO
- ⚠️ **Conditional on a running PLATO server** — writes and queries talk to the PLATO tile server (default `http://localhost:8847`). With no server reachable, write methods return `False` and `ask()` returns a fallback string. Construction itself needs no network.
- 🔮 **Later phase** — aggregation, richer query semantics, and persistence beyond PLATO are not implemented yet.

## Installation

```bash
pip install activeledger-agent
```

## Quick Start

```python
from activeledger_agent import ActiveLedgerAgent

agent = ActiveLedgerAgent()  # defaults: vessel="activeledger-agent", domain="activeledger-ai"

agent.log_activity("running", duration_minutes=30, energy_level="high")
agent.log_investment(asset="AAPL", amount=10, purchase_price=180.50)
agent.log_trade(asset="AAPL", action="buy", amount=10, price=180.50)

print(agent.ask("recent activity"))
```

## API

`ActiveLedgerAgent(vessel="activeledger-agent", domain="activeledger-ai", plato_url="http://localhost:8847")`

| Method | Returns | Notes |
|--------|---------|-------|
| `log_activity(activity, duration_minutes, energy_level="medium")` | `bool` | energy_level: low/medium/high |
| `log_investment(asset, amount, purchase_price)` | `bool` | |
| `log_trade(asset, action, amount, price)` | `bool` | action: `"buy"` or `"sell"` |
| `ask(question)` | `str` | fetches up to 20 tiles from PLATO, filters by the first three words of `question`, and returns a summary. Returns `"Ledger system unavailable."` if PLATO is unreachable. |

Each write method POSTs a tile to `{plato_url}/room/{domain}` and returns `True` on HTTP 200, `False` otherwise.

The lowercase alias `ActiveledgerAgent` is also exported. A `LedgerEntry` dataclass is available for structuring entries.

## Configuration

Point the agent at your PLATO server via the constructor:

```python
agent = ActiveLedgerAgent(plato_url="http://my-plato:8847")
```

## Requirements

- Python 3.10+
- `fleet-agent` >= 0.2.0
- `requests` >= 2.28
- A reachable PLATO server for writes and queries

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
