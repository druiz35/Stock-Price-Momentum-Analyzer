"""
Exponential Moving Average (EMA) Calculator

Implements EMA using exponential smoothing formula with deque for efficient
window management. EMA gives more weight to recent prices than older prices.
"""

from collections import deque
from typing import List, Optional


class EMACalculator:
    """
    Calculates Exponential Moving Average using exponential smoothing.
    
    EMA formula: EMA_t = (Price_t * multiplier) + (EMA_t-1 * (1 - multiplier))
    where multiplier = 2 / (window_size + 1)
    
    Time Complexity: O(n) where n is the length of the price array.
    Space Complexity: O(window_size) for the deque.
    """
    
    def __init__(self):
        """
        Initialize the EMA calculator.
        """
        self.prices: List[float] = []
        self.ema_values: List[float] = []
        self.window: deque = deque()
        self.multiplier: float = 0.0
    
    def calculate(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate Exponential Moving Average for the given prices and window size.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the moving average window.
            
        Returns:
            List[float]: List of EMA values. The first value is the SMA of the first
                        window (seed value), and subsequent values are calculated using
                        the exponential smoothing formula.
                        
        Raises:
            ValueError: If prices list is empty or window_size is invalid.
            TypeError: If prices contain non-numeric values.
        """
        # Validate inputs
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(prices)})")
        
        # Validate that all prices are numeric
        try:
            prices = [float(p) for p in prices]
        except (ValueError, TypeError):
            raise TypeError("All prices must be numeric values")
        
        self.prices = prices
        self.ema_values = []
        self.window = deque(maxlen=window_size)
        
        # Calculate the multiplier for exponential smoothing
        self.multiplier = 2.0 / (window_size + 1)
        
        # Initialize with the first window
        for i in range(window_size):
            self.window.append(prices[i])
        
        # Calculate the seed EMA (SMA of the first window)
        seed_ema = sum(self.window) / window_size
        self.ema_values.append(seed_ema)
        
        # Calculate EMA for the remaining prices
        current_ema = seed_ema
        for i in range(window_size, len(prices)):
            # Add the new price to the window (automatically removes the oldest)
            self.window.append(prices[i])
            # Apply exponential smoothing formula
            current_ema = (prices[i] * self.multiplier) + (current_ema * (1 - self.multiplier))
            self.ema_values.append(current_ema)
        
        return self.ema_values
    
    def get_ema_at_index(self, index: int) -> float:
        """
        Get the EMA value at a specific index.
        
        Args:
            index (int): The index of the EMA value to retrieve.
            
        Returns:
            float: The EMA value at the given index.
            
        Raises:
            IndexError: If the index is out of range.
        """
        if not self.ema_values:
            raise IndexError("No EMA values calculated yet")
        
        if index < 0 or index >= len(self.ema_values):
            raise IndexError(f"Index {index} out of range for EMA values")
        
        return self.ema_values[index]
    
    def get_all_ema_values(self) -> List[float]:
        """
        Get all calculated EMA values.
        
        Returns:
            List[float]: List of all EMA values.
        """
        return self.ema_values.copy()
    
    def calculate_with_padding(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate EMA with padding for the initial window.
        
        Returns a list of the same length as prices, with None values for positions
        where a full window is not available.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the moving average window.
            
        Returns:
            List[float]: List of EMA values with None padding at the start.
        """
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(prices)})")
        
        # Calculate EMA without padding
        ema_values = self.calculate(prices, window_size)
        
        # Add None padding at the beginning
        padded_ema = [None] * (window_size - 1) + ema_values
        
        return padded_ema
    
    def get_multiplier(self) -> float:
        """
        Get the multiplier used in the exponential smoothing formula.
        
        Returns:
            float: The multiplier value (2 / (window_size + 1)).
        """
        return self.multiplier
    
    @staticmethod
    def calculate_multiplier(window_size: int) -> float:
        """
        Calculate the multiplier for a given window size.
        
        Args:
            window_size (int): Size of the moving average window.
            
        Returns:
            float: The multiplier value.
            
        Raises:
            ValueError: If window_size is not positive.
        """
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        return 2.0 / (window_size + 1)
