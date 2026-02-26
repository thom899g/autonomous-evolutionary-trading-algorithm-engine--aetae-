"""
Master Agent - Orchestrates the evolutionary trading ecosystem
Coordinates all sub-agents and manages the evolutionary loop
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import uuid

from google.cloud import firestore
from google.cloud.firestore_v1 import Client as FirestoreClient

from config import config
from core.data_agent import DataAgent
from core.strategy_agent import StrategyAgent
from core.backtest_agent import BacktestAgent
from core.live_agent import LiveAgent

logger = logging.getLogger(__name__)

@dataclass
class EvolutionState:
    """Current state of evolutionary process"""
    generation: int = 0
    best_fitness: float = 0.0
    active_strategies: List[str] = None
    last_evolution: Optional[datetime] = None
    
    def __post_init__(self):
        if self.active_strategies is None:
            self.active_strategies = []

class MasterAgent:
    """Main orchestrator agent"""
    
    def __init__(self):
        self.agent_id = f"master_{uuid.uuid4().hex[:8]}"
        self.db: Optional[FirestoreClient] = None
        self.evolution_state = EvolutionState()
        
        # Initialize sub-agents
        self.data_agent = DataAgent()
        self.strategy_agent = Strategy