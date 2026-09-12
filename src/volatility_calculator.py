"""
Volatility Calculator

Calculates volatility metrics including standard deviation of returns, price range
(high-low), and relative strength using sliding window algorithms.
"""

import math
from typing import List, Dict, Optional, Tuple


class VolatilityCalculator:
    """
    Calculates volatility and price range metrics using sliding windows.
    
    Metrics:
    - Standard Deviation: Measures price variability
    - Price Range: High - Low for each period
    - Relative Strength: Ratio of up moves to down moves
    
    Time Complexity: O(n) for each calculation
    Space Complexity: O(n) for storing results
    """
    
    def __init__(self):
        """
        Initialize the volatility calculator.
        """
        self.prices: List[float] = []
        self.high_prices: Optional[List[float]] = None
        self.low_prices: Optional[List[float]] = None
        self.volatility_values: List[float] = []
        self.price_ranges: List[float] = []
        self.relative_strength: List[float] = []
    
    def calculate_volatility(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate standard deviation (volatility) for rolling windows.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the rolling window.
            
        Returns:
            List[float]: List of standard deviation values for each window.
            
        Raises:
            ValueError: If prices list is empty or window_size is invalid.
        """
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(prices)})")
        
        self.prices = prices
        self.volatility_values = []
        
        # Calculate volatility for each window
        for i in range(len(prices) - window_size + 1):
            window = prices[i:i + window_size]
            std_dev = self._calculate_std_dev(window)
            self.volatility_values.append(std_dev)
        
        return self.volatility_values
    
    def calculate_volatility_with_padding(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate volatility with padding for the initial window.
        
        Returns a list of the same length as prices, with None values for positions
        where a full window is not available.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the rolling window.
            
        Returns:
            List[float]: List of volatility values with None padding at the start.
        """
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(prices)})")
        
        # Calculate volatility without padding
        volatility_values = self.calculate_volatility(prices, window_size)
        
        # Add None padding at the beginning
        padded_volatility = [None] * (window_size - 1) + volatility_values
        
        return padded_volatility
    
    def calculate_price_range(self, high_prices: List[float], low_prices: List[float],
                             window_size: int) -> List[float]:
        """
        Calculate price range (high - low) for rolling windows.
        
        Args:
            high_prices (List[float]): List of high prices.
            low_prices (List[float]): List of low prices.
            window_size (int): Size of the rolling window.
            
        Returns:
            List[float]: List of price range values for each window.
            
        Raises:
            ValueError: If inputs are invalid or lists have different lengths.
        """
        if not high_prices or not low_prices:
            raise ValueError("High and low prices lists cannot be empty")
        
        if len(high_prices) != len(low_prices):
            raise ValueError("High and low prices lists must have the same length")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(high_prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(high_prices)})")
        
        self.high_prices = high_prices
        self.low_prices = low_prices
        self.price_ranges = []
        
        # Calculate price range for each window
        for i in range(len(high_prices) - window_size + 1):
            window_high = max(high_prices[i:i + window_size])
            window_low = min(low_prices[i:i + window_size])
            price_range = window_high - window_low
            self.price_ranges.append(price_range)
        
        return self.price_ranges
    
    def calculate_price_range_with_padding(self, high_prices: List[float], low_prices: List[float],
                                          window_size: int) -> List[float]:
        """
        Calculate price range with padding for the initial window.
        
        Args:
            high_prices (List[float]): List of high prices.
            low_prices (List[float]): List of low prices.
            window_size (int): Size of the rolling window.
            
        Returns:
            List[float]: List of price range values with None padding at the start.
        """
        if not high_prices or not low_prices:
            raise ValueError("High and low prices lists cannot be empty")
        
        if len(high_prices) != len(low_prices):
            raise ValueError("High and low prices lists must have the same length")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(high_prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(high_prices)})")
        
        # Calculate price range without padding
        price_ranges = self.calculate_price_range(high_prices, low_prices, window_size)
        
        # Add None padding at the beginning
        padded_ranges = [None] * (window_size - 1) + price_ranges
        
        return padded_ranges
    
    def calculate_relative_strength(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate relative strength (ratio of up moves to total moves).
        
        RS = (number of up moves) / (total number of moves)
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the rolling window.
            
        Returns:
            List[float]: List of relative strength values (0.0 to 1.0).
            
        Raises:
            ValueError: If prices list is empty or window_size is invalid.
        """
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(prices)})")
        
        self.prices = prices
        self.relative_strength = []
        
        # Calculate relative strength for each window
        for i in range(len(prices) - window_size + 1):
            window = prices[i:i + window_size]
            up_moves = 0
            total_moves = len(window) - 1
            
            if total_moves == 0:
                rs = 0.5  # Neutral if only one price point
            else:
                for j in range(1, len(window)):
                    if window[j] > window[j - 1]:
                        up_moves += 1
                
                rs = up_moves / total_moves
            
            self.relative_strength.append(rs)
        
        return self.relative_strength
    
    def calculate_relative_strength_with_padding(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate relative strength with padding for the initial window.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the rolling window.
            
        Returns:
            List[float]: List of relative strength values with None padding at the start.
        """
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(prices)})")
        
        # Calculate relative strength without padding
        rs_values = self.calculate_relative_strength(prices, window_size)
        
        # Add None padding at the beginning
        padded_rs = [None] * (window_size - 1) + rs_values
        
        return padded_rs
    
    def get_volatility_values(self) -> List[float]:
        """
        Get all calculated volatility values.
        
        Returns:
            List[float]: List of volatility values.
        """
        return self.volatility_values.copy()
    
    def get_price_ranges(self) -> List[float]:
        """
        Get all calculated price range values.
        
        Returns:
            List[float]: List of price range values.
        """
        return self.price_ranges.copy()
    
    def get_relative_strength_values(self) -> List[float]:
        """
        Get all calculated relative strength values.
        
        Returns:
            List[float]: List of relative strength values.
        """
        return self.relative_strength.copy()
    
    @staticmethod
    def _calculate_std_dev(values: List[float]) -> float:
        """
        Calculate standard deviation for a list of values.
        
        Args:
            values (List[float]): List of numeric values.
            
        Returns:
            float: Standard deviation of the values.
        """
        if not values:
            return 0.0
        
        if len(values) == 1:
            return 0.0
        
        # Calculate mean
        mean = sum(values) / len(values)
        
        # Calculate variance
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        
        # Calculate standard deviation
        std_dev = math.sqrt(variance)
        
        return std_dev
    
    @staticmethod
    def calculate_returns(prices: List[float]) -> List[float]:
        """
        Calculate percentage returns from prices.
        
        Returns = (Price_t - Price_t-1) / Price_t-1
        
        Args:
            prices (List[float]): List of price values.
            
        Returns:
            List[float]: List of returns (one less than prices).
            
        Raises:
            ValueError: If prices list has fewer than 2 elements.
        """
        if len(prices) < 2:
            raise ValueError("Need at least 2 prices to calculate returns")
        
        returns = []
        for i in range(1, len(prices)):
            if prices[i - 1] == 0:
                returns.append(0.0)
            else:
                ret = (prices[i] - prices[i - 1]) / prices[i - 1]
                returns.append(ret)
        
        return returns
