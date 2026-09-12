"""
Multi-Window Analyzer

Combines multiple moving averages (short-term, medium-term, long-term) to confirm
trends and reduce false signals. Validates signals across multiple time windows.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
from src.sma_calculator import SMACalculator
from src.ema_calculator import EMACalculator
from src.momentum_detector import MomentumDetector


class MultiWindowAnalyzer:
    """
    Analyzes price trends using multiple moving averages simultaneously.
    
    Combines short-term, medium-term, and long-term moving averages to:
    - Confirm trends across multiple timeframes
    - Reduce false signals through alignment detection
    - Provide confidence scores based on indicator alignment
    
    Time Complexity: O(n * m) where n is price count and m is number of windows
    Space Complexity: O(n * m) for storing all moving averages
    """
    
    def __init__(self):
        """
        Initialize the multi-window analyzer.
        """
        self.prices: List[float] = []
        self.dates: Optional[List[datetime]] = None
        self.sma_calculator = SMACalculator()
        self.ema_calculator = EMACalculator()
        self.momentum_detector = MomentumDetector()
        
        self.short_ma: List[float] = []
        self.medium_ma: List[float] = []
        self.long_ma: List[float] = []
        
        self.confirmed_signals: List[Dict] = []
        self.alignment_scores: List[float] = []
    
    def analyze(self, prices: List[float],
               short_window: int = 10,
               medium_window: int = 20,
               long_window: int = 50,
               dates: Optional[List[datetime]] = None,
               use_ema: bool = True) -> Dict:
        """
        Perform multi-window analysis on price data.
        
        Args:
            prices (List[float]): List of price values.
            short_window (int): Window size for short-term MA (default: 10).
            medium_window (int): Window size for medium-term MA (default: 20).
            long_window (int): Window size for long-term MA (default: 50).
            dates (Optional[List[datetime]]): List of dates for each price.
            use_ema (bool): Use EMA instead of SMA (default: True).
            
        Returns:
            Dict: Analysis results containing:
                - short_ma: Short-term moving average values
                - medium_ma: Medium-term moving average values
                - long_ma: Long-term moving average values
                - signals: Detected signals with confidence scores
                - confirmed_signals: Signals confirmed by multiple indicators
                - alignment_scores: Alignment score for each price point
                
        Raises:
            ValueError: If prices list is empty or window sizes are invalid.
        """
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if short_window <= 0 or medium_window <= 0 or long_window <= 0:
            raise ValueError("All window sizes must be positive")
        
        if short_window >= medium_window or medium_window >= long_window:
            raise ValueError("Window sizes must be in ascending order: short < medium < long")
        
        if long_window > len(prices):
            raise ValueError(f"Long window size ({long_window}) cannot exceed prices length ({len(prices)})")
        
        self.prices = prices
        self.dates = dates
        
        # Calculate moving averages
        if use_ema:
            self.short_ma = self.ema_calculator.calculate_with_padding(prices, short_window)
            self.medium_ma = self.ema_calculator.calculate_with_padding(prices, medium_window)
            self.long_ma = self.ema_calculator.calculate_with_padding(prices, long_window)
        else:
            self.short_ma = self.sma_calculator.calculate_with_padding(prices, short_window)
            self.medium_ma = self.sma_calculator.calculate_with_padding(prices, medium_window)
            self.long_ma = self.sma_calculator.calculate_with_padding(prices, long_window)
        
        # Detect signals using short-term MA
        signals = self.momentum_detector.detect_signals(prices, self.short_ma, dates)
        
        # Calculate alignment scores and confirm signals
        self._calculate_alignment_scores()
        self._confirm_signals(signals)
        
        return {
            'prices': prices,
            'short_ma': self.short_ma,
            'medium_ma': self.medium_ma,
            'long_ma': self.long_ma,
            'short_window': short_window,
            'medium_window': medium_window,
            'long_window': long_window,
            'signals': signals,
            'confirmed_signals': self.confirmed_signals,
            'alignment_scores': self.alignment_scores,
        }
    
    def _calculate_alignment_scores(self) -> None:
        """
        Calculate alignment scores for each price point.
        
        Alignment score measures how well the three moving averages align:
        - 1.0: All three MAs are aligned (bullish or bearish)
        - 0.5: Mixed signals
        - 0.0: Conflicting signals
        """
        self.alignment_scores = []
        
        for i in range(len(self.prices)):
            short = self.short_ma[i]
            medium = self.medium_ma[i]
            long = self.long_ma[i]
            price = self.prices[i]
            
            # Skip if any MA is None (not enough data)
            if short is None or medium is None or long is None:
                self.alignment_scores.append(None)
                continue
            
            # Count bullish and bearish signals
            bullish_count = 0
            bearish_count = 0
            
            # Check price vs short MA
            if price > short:
                bullish_count += 1
            elif price < short:
                bearish_count += 1
            
            # Check short vs medium MA
            if short > medium:
                bullish_count += 1
            elif short < medium:
                bearish_count += 1
            
            # Check medium vs long MA
            if medium > long:
                bullish_count += 1
            elif medium < long:
                bearish_count += 1
            
            # Calculate alignment score
            total_signals = bullish_count + bearish_count
            if total_signals == 0:
                alignment_score = 0.5  # Neutral
            else:
                # Score based on how aligned the signals are
                max_aligned = max(bullish_count, bearish_count)
                alignment_score = max_aligned / total_signals
            
            self.alignment_scores.append(alignment_score)
    
    def _confirm_signals(self, signals: List[Dict]) -> None:
        """
        Confirm signals based on alignment with multiple moving averages.
        
        A signal is confirmed if:
        - The price is on the correct side of all three moving averages
        - The moving averages are properly ordered (short > medium > long for bullish)
        
        Args:
            signals (List[Dict]): List of detected signals.
        """
        self.confirmed_signals = []
        
        for signal in signals:
            idx = signal['index']
            price = signal['price']
            signal_type = signal['signal']
            
            short = self.short_ma[idx]
            medium = self.medium_ma[idx]
            long = self.long_ma[idx]
            
            # Skip if any MA is None
            if short is None or medium is None or long is None:
                continue
            
            # Check if signal is confirmed
            is_confirmed = False
            confirmation_strength = 0.0
            
            if signal_type == MomentumDetector.SIGNAL_BULLISH:
                # Bullish confirmation: price > short > medium > long
                if price > short and short > medium and medium > long:
                    is_confirmed = True
                    confirmation_strength = 1.0
                # Partial confirmation: price > short and short > medium
                elif price > short and short > medium:
                    is_confirmed = True
                    confirmation_strength = 0.7
                # Weak confirmation: price > short
                elif price > short:
                    is_confirmed = True
                    confirmation_strength = 0.4
            
            elif signal_type == MomentumDetector.SIGNAL_BEARISH:
                # Bearish confirmation: price < short < medium < long
                if price < short and short < medium and medium < long:
                    is_confirmed = True
                    confirmation_strength = 1.0
                # Partial confirmation: price < short and short < medium
                elif price < short and short < medium:
                    is_confirmed = True
                    confirmation_strength = 0.7
                # Weak confirmation: price < short
                elif price < short:
                    is_confirmed = True
                    confirmation_strength = 0.4
            
            if is_confirmed:
                confirmed_signal = signal.copy()
                confirmed_signal['confirmation_strength'] = confirmation_strength
                confirmed_signal['alignment_score'] = self.alignment_scores[idx]
                self.confirmed_signals.append(confirmed_signal)
    
    def get_confirmed_signals(self) -> List[Dict]:
        """
        Get all confirmed signals.
        
        Returns:
            List[Dict]: List of confirmed signal records.
        """
        return self.confirmed_signals.copy()
    
    def get_alignment_scores(self) -> List[float]:
        """
        Get all alignment scores.
        
        Returns:
            List[float]: List of alignment scores.
        """
        return self.alignment_scores.copy()
    
    def get_moving_averages(self) -> Dict[str, List[float]]:
        """
        Get all calculated moving averages.
        
        Returns:
            Dict: Dictionary with keys 'short', 'medium', 'long'.
        """
        return {
            'short': self.short_ma.copy(),
            'medium': self.medium_ma.copy(),
            'long': self.long_ma.copy(),
        }
    
    def get_trend_at_index(self, index: int) -> Dict:
        """
        Get trend information at a specific index.
        
        Args:
            index (int): The index to analyze.
            
        Returns:
            Dict: Trend information including:
                - price: Price at the index
                - short_ma: Short-term MA
                - medium_ma: Medium-term MA
                - long_ma: Long-term MA
                - trend: Overall trend (BULLISH, BEARISH, or NEUTRAL)
                - alignment_score: Alignment score
                
        Raises:
            IndexError: If index is out of range.
        """
        if index < 0 or index >= len(self.prices):
            raise IndexError(f"Index {index} out of range")
        
        price = self.prices[index]
        short = self.short_ma[index]
        medium = self.medium_ma[index]
        long = self.long_ma[index]
        alignment = self.alignment_scores[index]
        
        # Determine trend
        if short is None or medium is None or long is None:
            trend = 'UNKNOWN'
        elif price > short and short > medium and medium > long:
            trend = 'STRONG_BULLISH'
        elif price > short and short > medium:
            trend = 'BULLISH'
        elif price > short:
            trend = 'WEAK_BULLISH'
        elif price < short and short < medium and medium < long:
            trend = 'STRONG_BEARISH'
        elif price < short and short < medium:
            trend = 'BEARISH'
        elif price < short:
            trend = 'WEAK_BEARISH'
        else:
            trend = 'NEUTRAL'
        
        return {
            'index': index,
            'price': price,
            'short_ma': short,
            'medium_ma': medium,
            'long_ma': long,
            'trend': trend,
            'alignment_score': alignment,
        }
