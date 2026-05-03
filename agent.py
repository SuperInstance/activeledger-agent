#!/usr/bin/env python3
"""activeledger-agent — Activity and fitness tracking for fleet agents"""
import json, time
from typing import List, Dict

class ActiveLedgerAgent:
    def __init__(self, plato_url="http://147.224.38.131:8847"):
        self.plato_url = plato_url
        self.activities: List[Dict] = []
    
    def log_activity(self, activity_type: str, duration_min: int, intensity: int, calories: Optional[int]=None, notes: str=""):
        act = {"type": activity_type, "duration": duration_min, "intensity": intensity, "calories": calories, "notes": notes, "time": time.time()}
        self.activities.append(act)
        self._submit(f"Activity: {activity_type}", f"{duration_min}min at intensity {intensity}/10. {notes}")
        return act
    
    def get_weekly_summary(self) -> Dict:
        if not self.activities: return {"error": "No activities"}
        total_time = sum(a["duration"] for a in self.activities)
        types = {}
        for a in self.activities: types[a["type"]] = types.get(a["type"], 0) + a["duration"]
        return {"total_activities": len(self.activities), "total_hours": round(total_time/60, 1), "by_type": types, "avg_intensity": round(sum(a["intensity"] for a in self.activities)/len(self.activities), 1)}
    
    def _submit(self, q: str, a: str):
        try:
            import urllib.request
            urllib.request.urlopen(urllib.request.Request(f"{self.plato_url}/submit", data=json.dumps({"question": q, "answer": a, "agent": "activeledger-agent", "room": "activeledger"}).encode(), headers={"Content-Type": "application/json"}), timeout=5)
        except: pass

def demo():
    a = ActiveLedgerAgent()
    a.log_activity("run", 30, 7, 350, "Morning run, felt good")
    a.log_activity("weights", 45, 8, 200, "Leg day")
    a.log_activity("swim", 20, 6, 180, "Cooldown")
    print(a.get_weekly_summary())

if __name__ == "__main__": demo()
