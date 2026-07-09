"""
PLATO ActiveLedger Agent — Activity/Investment Tracking for activeledger.ai

Ledger of activities, investments, trades, and resource tracking.
Every transaction logged to PLATO as a functional tile.
"""

import time
import requests
from fleet_agent import BaseAgent
from fleet_agent.fleet_math import EmergenceDetector, HolonomyConsensus

from typing import Optional, List, Dict, Any
from dataclasses import dataclass

DEFAULT_PLATO_URL = "http://localhost:8847"
ROOM = "activeledger-ai"

@dataclass
class LedgerEntry:
    """A ledger entry tile."""
    entry_type: str  # "activity" | "investment" | "trade" | "expense" | "income"
    amount: float
    category: str
    description: str
    timestamp: float

class ActiveLedgerAgent(BaseAgent):
    """
    Activity/investment ledger agent.
    
    Logs financial activities, investments, trades to PLATO.
    Tracks resource flow over time through vessel accumulation.
    """
    
        
    def detect_emergence(self, events: list) -> dict:
        """Detect emergence via H1 cohomology."""
        detector = EmergenceDetector()
        edges = [(events[i], events[i+1]) for i in range(len(events)-1)]
        detector.update(events, edges)
        return {"emergence_detected": detector.emergence_detected, "h1_cohomology": detector.h1, "confidence": detector.confidence}

    def check_consensus(self, tile_ids: list[int]) -> bool:
        """Check holonomy consensus across tiles."""
        hc = HolonomyConsensus()
        for tid in tile_ids:
            hc.add_tile(tid)
        return hc.check_consensus([tile_ids])

    def __init__(self, vessel: str = "activeledger-agent", domain: str = ROOM, plato_url: str = "http://localhost:8847"):
        super().__init__(vessel=vessel, domain=domain, plato_url=plato_url)
        self.room = domain
        self.ledger_id = vessel

    def _write(self, entry_type: str, data: Dict[str, Any]) -> bool:
        tile = {
            "question": f"ledger:{entry_type}",
            "answer": str(data),
            "confidence": 0.9,
            "metadata": {
                "ledger_id": self.ledger_id,
                "entry_type": entry_type,
                "timestamp": time.time(),
                **data
            }
        }
        try:
            resp = requests.post(f"{self.plato_url}/room/{self.room}", json=tile, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def log_activity(self, activity: str, duration_minutes: int, energy_level: str = "medium") -> bool:
        """Log a general activity."""
        return self._write("activity", {
            "activity": activity,
            "duration_minutes": duration_minutes,
            "energy_level": energy_level,
        })
    
    def log_investment(self, asset: str, amount: float, purchase_price: float) -> bool:
        """Log an investment."""
        return self._write("investment", {
            "asset": asset,
            "amount": amount,
            "purchase_price": purchase_price,
        })
    
    def log_trade(self, asset: str, action: str, amount: float, price: float) -> bool:
        """Log a trade."""
        return self._write("trade", {
            "asset": asset,
            "action": action,  # "buy" | "sell"
            "amount": amount,
            "price": price,
        })
    
    def ask(self, question: str) -> str:
        """Query ledger from PLATO."""
        try:
            resp = requests.get(f"{self.plato_url}/room/{self.room}?limit=20", timeout=5)
            if resp.status_code == 200:
                tiles = resp.json().get("tiles", [])
                relevant = [t for t in tiles if any(w in str(t).lower() for w in question.lower().split()[:3])]
                if relevant:
                    return f"Found {len(relevant)} ledger entries: {relevant[-1].get('answer', '')[:200]}"
        except:
            pass
        return "Ledger system unavailable."


# Alias for test/import compatibility (matches the package's lowercase spelling).
ActiveledgerAgent = ActiveLedgerAgent
