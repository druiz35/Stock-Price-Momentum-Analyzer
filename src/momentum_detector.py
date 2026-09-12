"""
Momentum Detector

Detects bullish and bearish trading signals by comparing current prices to moving
averages and identifying crossover points where price crosses above or below key
moving averages.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime


class MomentumDetector:
    """
    Detects price momentum signals using moving average comparisons.
    
    Signals:
    - BULLISH: Price crosses above moving average (upward momentum)
    - BEARISH: Price crosses below moving average (downward momentum)
    - NEUTRAL: Price is stable relative to moving average
    """
    
    SIGNAL_BULLISH = 'BULLISH'
    SIGNAL_BEARISH = 'BEARISH'
    SIGNAL_NEUTRAL = 'NEUTRAL'
    
    def __init__(self):
        """
        Initialize the momentum detector.
        """
        self.prices: List[float] = []
        self.moving_averages: List[float] = []
        self.signals: List[Dict] = []
        self.crossovers: List[Dict] = []
    
    def detect_signals(self, prices: List[float], moving_averages: List[float],
                      dates: Optional[List[datetime]] = None) -> List[Dict]:
        """
        Detect bullish and bearish signals by comparing prices to moving averages.
        
        Args:
            prices (List[float]): List of price values.
            moving_averages (List[float]): List of moving average values.
            dates (Optional[List[datetime]]): List of dates corresponding to prices.
            
        Returns:
            List[Dict]: List of signal dictionaries with keys:
                - index: Position in the price array
                - date: Date of the signal (if provided)
                - price: Current price
                - moving_average: Moving average value
                - signal: Signal type (BULLISH, BEARISH, NEUTRAL)
                - confidence: Confidence level (0.0 to 1.0)
                
        Raises:
            ValueError: If prices and moving_averages have different lengths.
        """
        if len(prices) != len(moving_averages):
            raise ValueError("Prices and moving averages must have the same length")
        
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        self.prices = prices
        self.moving_averages = moving_averages
        self.signals = []
        
        for i in range(len(prices)):
            price = prices[i]
            ma = moving_averages[i]
            
            if ma is None:
                continue
            
            # Determine signal type
            if price > ma:
                signal_type = self.SIGNAL_BULLISH
                confidence = self._calculate_confidence(price, ma, 'bullish')
            elif price < ma:
                signal_type = self.SIGNAL_BEARISH
                confidence = self._calculate_confidence(price, ma, 'bearish')
            else:
                signal_type = self.SIGNAL_NEUTRAL
                confidence = 0.5
            
            signal_record = {
                'index': i,
                'price': price,
                'moving_average': ma,
                'signal': signal_type,
                'confidence': confidence,
            }
            
            if dates and i < len(dates):
                signal_record['date'] = dates[i]
            
            self.signals.append(signal_record)
        
        return self.signals
    
    def detect_crossovers(self, prices: List[float], moving_averages: List[float],
                         dates: Optional[List[datetime]] = None) -> List[Dict]:
        """
        Detect crossover points where price crosses above or below the moving average.
        
        Args:
            prices (List[float]): List of price values.
            moving_averages (List[float]): List of moving average values.
            dates (Optional[List[datetime]]): List of dates corresponding to prices.
            
        Returns:
            List[Dict]: List of crossover dictionaries with keys:
                - index: Position in the price array
                - date: Date of the crossover (if provided)
                - price: Current price
                - moving_average: Moving average value
                - crossover_type: Type of crossover (BULLISH or BEARISH)
                - previous_price: Price at previous index
                - previous_ma: Moving average at previous index
                
        Raises:
            ValueError: If prices and moving_averages have different lengths.
        """
        if len(prices) != len(moving_averages):
            raise ValueError("Prices and moving averages must have the same length")
        
        if not prices or len(prices) < 2:
            raise ValueError("Need at least 2 price points to detect crossovers")
        
        self.crossovers = []
        
        for i in range(1, len(prices)):
            current_price = prices[i]
            current_ma = moving_averages[i]
            previous_price = prices[i - 1]
            previous_ma = moving_averages[i - 1]
            
            # Skip if either moving average is None
            if current_ma is None or previous_ma is None:
                continue
            
            # Detect bullish crossover (price crosses above MA)
            if previous_price <= previous_ma and current_price > current_ma:
                crossover_record = {
                    'index': i,
                    'price': current_price,
                    'moving_average': current_ma,
                    'crossover_type': self.SIGNAL_BULLISH,
                    'previous_price': previous_price,
                    'previous_ma': previous_ma,
                }
                
                if dates and i < len(dates):
                    crossover_record['date'] = dates[i]
                
                self.crossovers.append(crossover_record)
            
            # Detect bearish crossover (price crosses below MA)
            elif previous_price >= previous_ma and current_price < current_ma:
                crossover_record = {
                    'index': i,
                    'price': current_price,
                    'moving_average': current_ma,
                    'crossover_type': self.SIGNAL_BEARISH,
                    'previous_price': previous_price,
                    'previous_ma': previous_ma,
                }
                
                if dates and i < len(dates):
                    crossover_record['date'] = dates[i]
                
                self.crossovers.append(crossover_record)
        
        return self.crossovers
    
    def get_signals(self) -> List[Dict]:
        """
        Get all detected signals.
        
        Returns:
            List[Dict]: List of signal records.
        """
        return self.signals.copy()
    
    def get_crossovers(self) -> List[Dict]:
        """
        Get all detected crossovers.
        
        Returns:
            List[Dict]: List of crossover records.
        """
        return self.crossovers.copy()
    
    def get_signals_by_type(self, signal_type: str) -> List[Dict]:
        """
        Get signals of a specific type.
        
        Args:
            signal_type (str): Type of signal (BULLISH, BEARISH, or NEUTRAL).
            
        Returns:
            List[Dict]: List of signals of the specified type.
        """
        return [s for s in self.signals if s['signal'] == signal_type]
    
    def get_consecutive_signals(self, min_consecutive: int = 2) -> List[Tuple[int, int, str]]:
        """
        Get groups of consecutive signals of the same type.
        
        Args:
            min_consecutive (int): Minimum number of consecutive signals to return.
            
        Returns:
            List[Tuple[int, int, str]]: List of (start_index, end_index, signal_type) tuples.
        """
        if not self.signals:
            return []
        
        consecutive_groups = []
        current_signal = self.signals[0]['signal']
        start_index = 0
        
        for i in range(1, len(self.signals)):
            if self.signals[i]['signal'] != current_signal:
                # End of a group
                if i - start_index >= min_consecutive:
                    consecutive_groups.append((start_index, i - 1, current_signal))
                
                current_signal = self.signals[i]['signal']
                start_index = i
        
        # Handle the last group
        if len(self.signals) - start_index >= min_consecutive:
            consecutive_groups.append((start_index, len(self.signals) - 1, current_signal))
        
        return consecutive_groups
    
    @staticmethod
    def _calculate_confidence(price: float, moving_average: float, signal_type: str) -> float:
        """
        Calculate confidence level for a signal based on distance from moving average.
        
        Args:
            price (float): Current price.
            moving_average (float): Moving average value.
            signal_type (str): Type of signal (bullish or bearish).
            
        Returns:
            float: Confidence level between 0.0 and 1.0.
        """
        if moving_average == 0:
            return 0.5
        
        # Calculate percentage difference
        percentage_diff = abs(price - moving_average) / moving_average
        
        # Cap confidence at 1.0 and scale based on percentage difference
        # Higher difference = higher confidence
        confidence = min(1.0, 0.5 + (percentage_diff / 2))
        
        return confidence
