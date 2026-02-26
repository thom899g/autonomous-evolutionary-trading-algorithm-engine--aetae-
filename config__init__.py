"""
Configuration management for AETAE
Centralized config with environment variable fallbacks
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
import logging
from pathlib import Path

@dataclass
class ExchangeConfig:
    """Exchange-specific configuration"""
    name: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    sandbox: bool = True
    rate_limit: int = 10
    supported_pairs: list = None
    
    def __post_init__(self):
        if self.supported_pairs is None:
            self.supported_pairs = ["BTC/USDT", "ETH/USDT"]

@dataclass
class FirestoreConfig:
    """Firestore configuration"""
    project_id: str
    collection_prefix: str = "aetae"
    enable_real_time: bool = True
    batch_size: int = 500

@dataclass
class EvolutionConfig:
    """Evolutionary algorithm parameters"""
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.15
    crossover_rate: float = 0.7
    elite_size: int = 5
    min_fitness: float = 0.6

@dataclass 
class RiskConfig:
    """Risk management parameters"""
    max_position_size: float = 0.1  # 10% of portfolio
    max_daily_loss: float = 0.02   # 2% max daily loss
    stop_loss_pct: float = 0.02    # 2% stop loss
    take_profit_pct: float = 0.05  # 5% take profit
    max_open_positions: int = 5

class AETAEConfig:
    """Main configuration class"""
    
    def __init__(self):
        self.exchange = self._load_exchange_config()
        self.firestore = self._load_firestore_config()
        self.evolution = EvolutionConfig()
        self.risk = RiskConfig()
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
    def _load_exchange_config(self) -> ExchangeConfig:
        """Load exchange configuration with environment fallbacks"""
        return ExchangeConfig(
            name=os.getenv("EXCHANGE_NAME", "binance"),
            api_key=os.getenv("EXCHANGE_API_KEY"),
            api_secret=os.getenv("EXCHANGE_API_SECRET"),
            sandbox=os.getenv("EXCHANGE_SANDBOX", "true").lower() == "true"
        )
    
    def _load_firestore_config(self) -> FirestoreConfig:
        """Load Firestore configuration"""
        # Firebase Admin SDK uses GOOGLE_APPLICATION_CREDENTIALS
        return FirestoreConfig(
            project_id=os.getenv("FIRESTORE_PROJECT_ID", "aetae-production")
        )
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        if not self.exchange.name:
            errors.append("Exchange name must be specified")
            
        if not self.firestore.project_id:
            errors.append("Firestore project ID must be specified")
            
        if self.evolution.mutation_rate <= 0 or self.evolution.mutation_rate >= 1:
            errors.append("Mutation rate must be between 0 and 1")
            
        if errors:
            logging.error(f"Configuration errors: {errors}")
            return False
            
        return True

# Global configuration instance
config = AETAEConfig()