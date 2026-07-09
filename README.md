# activeledger-agent

Activity / investment / trade ledger agent that writes entries to a [PLATO](https://github.com/SuperInstance) tile server and queries them back. Built on the `fleet-agent` base class.

## What This Gives You

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

agent = ActiveLedgerAgent()  # defaults: vessel="activeledger-agent", room="activeledger-ai"

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
| `ask(question)` | `str` | queries recent tiles from PLATO |

The lowercase alias `ActiveledgerAgent` is also exported. A `LedgerEntry` dataclass is available for structuring entries.

## Configuration

Point the agent at your PLATO server via the constructor:

```python
agent = ActiveLedgerAgent(plato_url="http://my-plato:8847")
```

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
