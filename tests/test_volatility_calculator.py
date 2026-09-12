"""
Unit Tests for Volatility Calculator Module

Tests standard deviation, price range, and relative strength calculations.
"""

import unittest
import math
from src.volatility_calculator import VolatilityCalculator


class TestVolatilityCalculator(unittest.TestCase):
    """
    Test cases for the VolatilityCalculator class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.calculator = VolatilityCalculator()
    
    def test_calculate_volatility_basic(self):
        """
        Test basic volatility (standard deviation) calculation.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        volatility = self.calculator.calculate_volatility(prices, window_size)
        
        # Should have 3 values
        self.assertEqual(len(volatility), 3)
        # All values should be non-negative
        for vol in volatility:
            self.assertGreaterEqual(vol, 0)
    
    def test_calculate_volatility_constant_prices(self):
        """
        Test volatility for constant prices (should be 0).
        """
        prices = [100, 100, 100, 100]
        window_size = 2
        
        volatility = self.calculator.calculate_volatility(prices, window_size)
        
        # All volatility values should be 0 for constant prices
        for vol in volatility:
            self.assertAlmostEqual(vol, 0.0, places=4)
    
    def test_calculate_volatility_single_element_window(self):
        """
        Test volatility with window size of 1.
        """
        prices = [100, 102, 101, 103]
        window_size = 1
        
        volatility = self.calculator.calculate_volatility(prices, window_size)
        
        # All volatility values should be 0 (single element has no variance)
        for vol in volatility:
            self.assertAlmostEqual(vol, 0.0, places=4)
    
    def test_calculate_volatility_window_size_equals_length(self):
        """
        Test volatility when window size equals array length.
        """
        prices = [100, 102, 101, 103]
        window_size = 4
        
        volatility = self.calculator.calculate_volatility(prices, window_size)
        
        # Should return single value
        self.assertEqual(len(volatility), 1)
        self.assertGreaterEqual(volatility[0], 0)
    
    def test_calculate_volatility_window_size_larger_than_array(self):
        """
        Test error handling when window size exceeds array length.
        """
        prices = [100, 102, 101]
        window_size = 5
        
        with self.assertRaises(ValueError):
            self.calculator.calculate_volatility(prices, window_size)
    
    def test_calculate_volatility_empty_array(self):
        """
        Test error handling for empty price array.
        """
        prices = []
        window_size = 3
        
        with self.assertRaises(ValueError):
            self.calculator.calculate_volatility(prices, window_size)
    
    def test_calculate_volatility_invalid_window_size(self):
        """
        Test error handling for invalid window sizes.
        """
        prices = [100, 102, 101, 103]
        
        # Zero window size
        with self.assertRaises(ValueError):
            self.calculator.calculate_volatility(prices, 0)
        
        # Negative window size
        with self.assertRaises(ValueError):
            self.calculator.calculate_volatility(prices, -1)
    
    def test_calculate_volatility_with_padding(self):
        """
        Test volatility calculation with padding.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        volatility = self.calculator.calculate_volatility_with_padding(prices, window_size)
        
        # Should have same length as prices
        self.assertEqual(len(volatility), len(prices))
        # First window_size-1 values should be None
        for i in range(window_size - 1):
            self.assertIsNone(volatility[i])
        # Remaining values should be volatility
        for i in range(window_size - 1, len(volatility)):
            self.assertIsNotNone(volatility[i])
    
    def test_calculate_price_range_basic(self):
        """
        Test basic price range calculation.
        """
        high_prices = [105, 107, 106, 108, 110]
        low_prices = [95, 97, 96, 98, 100]
        window_size = 3
        
        price_ranges = self.calculator.calculate_price_range(high_prices, low_prices, window_size)
        
        # Should have 3 values
        self.assertEqual(len(price_ranges), 3)
        # All values should be positive
        for pr in price_ranges:
            self.assertGreater(pr, 0)
    
    def test_calculate_price_range_manual_calculation(self):
        """
        Test price range calculation against manual calculation.
        """
        high_prices = [105, 107, 106]
        low_prices = [95, 97, 96]
        window_size = 3
        
        price_ranges = self.calculator.calculate_price_range(high_prices, low_prices, window_size)
        
        # Expected: max(105,107,106) - min(95,97,96) = 107 - 95 = 12
        self.assertEqual(len(price_ranges), 1)
        self.assertAlmostEqual(price_ranges[0], 12.0, places=2)
    
    def test_calculate_price_range_length_mismatch(self):
        """
        Test error handling for mismatched array lengths.
        """
        high_prices = [105, 107, 106]
        low_prices = [95, 97]
        window_size = 2
        
        with self.assertRaises(ValueError):
            self.calculator.calculate_price_range(high_prices, low_prices, window_size)
    
    def test_calculate_price_range_empty_arrays(self):
        """
        Test error handling for empty arrays.
        """
        high_prices = []
        low_prices = []
        window_size = 3
        
        with self.assertRaises(ValueError):
            self.calculator.calculate_price_range(high_prices, low_prices, window_size)
    
    def test_calculate_price_range_with_padding(self):
        """
        Test price range calculation with padding.
        """
        high_prices = [105, 107, 106, 108, 110]
        low_prices = [95, 97, 96, 98, 100]
        window_size = 3
        
        price_ranges = self.calculator.calculate_price_range_with_padding(high_prices, low_prices, window_size)
        
        # Should have same length as input
        self.assertEqual(len(price_ranges), len(high_prices))
        # First window_size-1 values should be None
        for i in range(window_size - 1):
            self.assertIsNone(price_ranges[i])
    
    def test_calculate_relative_strength_basic(self):
        """
        Test basic relative strength calculation.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        rs = self.calculator.calculate_relative_strength(prices, window_size)
        
        # Should have 3 values
        self.assertEqual(len(rs), 3)
        # All values should be between 0 and 1
        for r in rs:
            self.assertGreaterEqual(r, 0.0)
            self.assertLessEqual(r, 1.0)
    
    def test_calculate_relative_strength_all_up_moves(self):
        """
        Test relative strength with all up moves.
        """
        prices = [100, 101, 102, 103, 104]
        window_size = 3
        
        rs = self.calculator.calculate_relative_strength(prices, window_size)
        
        # All windows have only up moves, so RS should be 1.0
        for r in rs:
            self.assertAlmostEqual(r, 1.0, places=4)
    
    def test_calculate_relative_strength_all_down_moves(self):
        """
        Test relative strength with all down moves.
        """
        prices = [100, 99, 98, 97, 96]
        window_size = 3
        
        rs = self.calculator.calculate_relative_strength(prices, window_size)
        
        # All windows have only down moves, so RS should be 0.0
        for r in rs:
            self.assertAlmostEqual(r, 0.0, places=4)
    
    def test_calculate_relative_strength_mixed_moves(self):
        """
        Test relative strength with mixed up and down moves.
        """
        prices = [100, 102, 101, 103]
        window_size = 3
        
        rs = self.calculator.calculate_relative_strength(prices, window_size)
        
        # Window 1: 100->102 (up), 102->101 (down) = 1 up, 1 down = 0.5
        # Window 2: 102->101 (down), 101->103 (up) = 1 up, 1 down = 0.5
        self.assertEqual(len(rs), 2)
        for r in rs:
            self.assertAlmostEqual(r, 0.5, places=4)
    
    def test_calculate_relative_strength_with_padding(self):
        """
        Test relative strength calculation with padding.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        rs = self.calculator.calculate_relative_strength_with_padding(prices, window_size)
        
        # Should have same length as prices
        self.assertEqual(len(rs), len(prices))
        # First window_size-1 values should be None
        for i in range(window_size - 1):
            self.assertIsNone(rs[i])
    
    def test_calculate_returns(self):
        """
        Test percentage returns calculation.
        """
        prices = [100, 110, 121]
        
        returns = VolatilityCalculator.calculate_returns(prices)
        
        # Expected: [0.1, 0.1]
        self.assertEqual(len(returns), 2)
        self.assertAlmostEqual(returns[0], 0.1, places=4)
        self.assertAlmostEqual(returns[1], 0.1, places=4)
    
    def test_calculate_returns_insufficient_data(self):
        """
        Test error handling for insufficient data in returns calculation.
        """
        prices = [100]
        
        with self.assertRaises(ValueError):
            VolatilityCalculator.calculate_returns(prices)
    
    def test_calculate_returns_zero_price(self):
        """
        Test returns calculation with zero price.
        """
        prices = [100, 0, 110]
        
        returns = VolatilityCalculator.calculate_returns(prices)
        
        # Should handle zero price gracefully
        self.assertEqual(len(returns), 2)
        self.assertEqual(returns[0], 0.0)  # Division by zero handled
    
    def test_get_volatility_values(self):
        """
        Test retrieving volatility values.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate_volatility(prices, window_size)
        
        volatility = self.calculator.get_volatility_values()
        
        self.assertEqual(len(volatility), 3)
    
    def test_get_price_ranges(self):
        """
        Test retrieving price range values.
        """
        high_prices = [105, 107, 106, 108, 110]
        low_prices = [95, 97, 96, 98, 100]
        window_size = 3
        self.calculator.calculate_price_range(high_prices, low_prices, window_size)
        
        ranges = self.calculator.get_price_ranges()
        
        self.assertEqual(len(ranges), 3)
    
    def test_get_relative_strength_values(self):
        """
        Test retrieving relative strength values.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate_relative_strength(prices, window_size)
        
        rs = self.calculator.get_relative_strength_values()
        
        self.assertEqual(len(rs), 3)
    
    def test_volatility_large_dataset(self):
        """
        Test volatility calculation on large dataset.
        """
        prices = list(range(1, 10001))  # 10,000 prices
        window_size = 50
        
        volatility = self.calculator.calculate_volatility(prices, window_size)
        
        # Should have correct length
        self.assertEqual(len(volatility), len(prices) - window_size + 1)
        # All values should be numeric
        for vol in volatility:
            self.assertIsInstance(vol, (int, float))


if __name__ == '__main__':
    unittest.main()
