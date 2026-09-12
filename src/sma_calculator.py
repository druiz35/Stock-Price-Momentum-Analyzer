"""
Simple Moving Average (SMA) Calculator

Implements efficient sliding window algorithm to calculate SMA for rolling windows
of price data. SMA is the arithmetic mean of prices over a specified window size.
"""

from typing import List, Tuple


class SMACalculator:
    """
    Calculates Simple Moving Average using an efficient sliding window approach.
    
    Time Complexity: O(n) where n is the length of the price array.
    Space Complexity: O(n) for storing the results.
    """
    
    def __init__(self):
        """
        Initialize the SMA calculator.
        """
        self.prices: List[float] = []
        self.sma_values: List[float] = []
    
    def calculate(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate Simple Moving Average for the given prices and window size.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the moving average window.
            
        Returns:
            List[float]: List of SMA values. The first (window_size - 1) values
                        are None, and subsequent values are the SMA for each window.
                        
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
        self.sma_values = []
        
        # Initialize the window sum with the first window
        window_sum = sum(prices[:window_size])
        
        # Add SMA for the first complete window
        self.sma_values.append(window_sum / window_size)
        
        # Slide the window across the remaining prices
        for i in range(window_size, len(prices)):
            # Remove the leftmost price from the window
            window_sum -= prices[i - window_size]
            # Add the new rightmost price to the window
            window_sum += prices[i]
            # Calculate and store the SMA
            self.sma_values.append(window_sum / window_size)
        
        return self.sma_values
    
    def get_sma_at_index(self, index: int) -> float:
        """
        Get the SMA value at a specific index.
        
        Args:
            index (int): The index of the SMA value to retrieve.
            
        Returns:
            float: The SMA value at the given index.
            
        Raises:
            IndexError: If the index is out of range.
        """
        if not self.sma_values:
            raise IndexError("No SMA values calculated yet")
        
        if index < 0 or index >= len(self.sma_values):
            raise IndexError(f"Index {index} out of range for SMA values")
        
        return self.sma_values[index]
    
    def get_all_sma_values(self) -> List[float]:
        """
        Get all calculated SMA values.
        
        Returns:
            List[float]: List of all SMA values.
        """
        return self.sma_values.copy()
    
    def calculate_with_padding(self, prices: List[float], window_size: int) -> List[float]:
        """
        Calculate SMA with padding for the initial window.
        
        Returns a list of the same length as prices, with None values for positions
        where a full window is not available.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the moving average window.
            
        Returns:
            List[float]: List of SMA values with None padding at the start.
        """
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        if window_size > len(prices):
            raise ValueError(f"Window size ({window_size}) cannot exceed prices length ({len(prices)})")
        
        # Calculate SMA without padding
        sma_values = self.calculate(prices, window_size)
        
        # Add None padding at the beginning
        padded_sma = [None] * (window_size - 1) + sma_values
        
        return padded_sma
    
    @staticmethod
    def calculate_single_window(prices: List[float], window_size: int) -> float:
        """
        Calculate SMA for a single window of prices.
        
        Args:
            prices (List[float]): List of price values.
            window_size (int): Size of the moving average window.
            
        Returns:
            float: The SMA value for the window.
            
        Raises:
            ValueError: If window_size doesn't match prices length.
        """
        if len(prices) != window_size:
            raise ValueError(f"Prices length ({len(prices)}) must equal window size ({window_size})")
        
        if not prices:
            raise ValueError("Prices list cannot be empty")
        
        return sum(prices) / len(prices)
