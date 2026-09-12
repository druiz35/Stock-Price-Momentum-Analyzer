"""
Stock Price Momentum Analyzer

A financial analysis tool that identifies momentum patterns in stock price movements
using sliding window techniques and array manipulation.
"""

__version__ = '1.0.0'
__author__ = 'Financial Analysis Team'

from src.data_loader import DataLoader
from src.sma_calculator import SMACalculator
from src.ema_calculator import EMACalculator
from src.momentum_detector import MomentumDetector
from src.volatility_calculator import VolatilityCalculator
from src.multi_window_analyzer import MultiWindowAnalyzer

__all__ = [
    'DataLoader',
    'SMACalculator',
    'EMACalculator',
    'MomentumDetector',
    'VolatilityCalculator',
    'MultiWindowAnalyzer',
]
