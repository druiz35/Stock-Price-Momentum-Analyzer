"""
Unit Tests for EMA Calculator Module

Tests exponential smoothing formula, deque optimization, and convergence behavior.
"""

import unittest
from src.ema_calculator import EMACalculator


class TestEMACalculator(unittest.TestCase):
    """
    Test cases for the EMACalculator class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.calculator = EMACalculator()
    
    def test_calculate_basic_ema(self):
        """
        Test basic EMA calculation.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        ema = self.calculator.calculate(prices, window_size)
        
        # Should have 3 values (window_size to end)
        self.assertEqual(len(ema), 3)
        # First value should be SMA of first window
        expected_seed = sum(prices[:3]) / 3
        self.assertAlmostEqual(ema[0], expected_seed, places=2)
    
    def test_calculate_ema_window_size_one(self):
        """
        Test EMA with window size of 1.
        """
        prices = [100, 102, 101, 103]
        window_size = 1
        
        ema = self.calculator.calculate(prices, window_size)
        
        # With window size 1, multiplier = 2/(1+1) = 1.0
        # So EMA should equal the prices
        self.assertEqual(len(ema), 4)
        for i in range(len(prices)):
            self.assertAlmostEqual(ema[i], prices[i], places=2)
    
    def test_calculate_ema_window_size_equals_length(self):
        """
        Test EMA when window size equals array length.
        """
        prices = [100, 102, 101, 103]
        window_size = 4
        
        ema = self.calculator.calculate(prices, window_size)
        
        # Should return single value (seed EMA)
        self.assertEqual(len(ema), 1)
        expected = sum(prices) / len(prices)
        self.assertAlmostEqual(ema[0], expected, places=2)
    
    def test_calculate_ema_window_size_larger_than_array(self):
        """
        Test error handling when window size exceeds array length.
        """
        prices = [100, 102, 101]
        window_size = 5
        
        with self.assertRaises(ValueError):
            self.calculator.calculate(prices, window_size)
    
    def test_calculate_ema_empty_array(self):
        """
        Test error handling for empty price array.
        """
        prices = []
        window_size = 3
        
        with self.assertRaises(ValueError):
            self.calculator.calculate(prices, window_size)
    
    def test_calculate_ema_invalid_window_size(self):
        """
        Test error handling for invalid window sizes.
        """
        prices = [100, 102, 101, 103]
        
        # Zero window size
        with self.assertRaises(ValueError):
            self.calculator.calculate(prices, 0)
        
        # Negative window size
        with self.assertRaises(ValueError):
            self.calculator.calculate(prices, -1)
    
    def test_calculate_ema_non_numeric_prices(self):
        """
        Test error handling for non-numeric prices.
        """
        prices = [100, 'invalid', 101, 103]
        window_size = 2
        
        with self.assertRaises(TypeError):
            self.calculator.calculate(prices, window_size)
    
    def test_calculate_ema_with_padding(self):
        """
        Test EMA calculation with padding.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        ema = self.calculator.calculate_with_padding(prices, window_size)
        
        # Should have same length as prices
        self.assertEqual(len(ema), len(prices))
        # First window_size-1 values should be None
        for i in range(window_size - 1):
            self.assertIsNone(ema[i])
        # Remaining values should be EMA
        for i in range(window_size - 1, len(ema)):
            self.assertIsNotNone(ema[i])
    
    def test_calculate_ema_multiplier(self):
        """
        Test that multiplier is calculated correctly.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        self.calculator.calculate(prices, window_size)
        
        # Multiplier should be 2 / (window_size + 1)
        expected_multiplier = 2.0 / (window_size + 1)
        self.assertAlmostEqual(self.calculator.get_multiplier(), expected_multiplier, places=4)
    
    def test_calculate_ema_convergence(self):
        """
        Test that EMA converges over time.
        """
        # Create a constant price series
        prices = [100] * 100
        window_size = 10
        
        ema = self.calculator.calculate(prices, window_size)
        
        # EMA should converge to the constant price
        # Later values should be closer to 100
        self.assertAlmostEqual(ema[-1], 100.0, places=1)
    
    def test_calculate_ema_responsiveness(self):
        """
        Test that EMA is responsive to price changes.
        """
        # Create a series with a sudden price jump
        prices = [100] * 10 + [150] * 10
        window_size = 5
        
        ema = self.calculator.calculate(prices, window_size)
        
        # EMA should increase after the price jump
        # Later values should be higher than earlier values
        self.assertGreater(ema[-1], ema[0])
    
    def test_calculate_ema_large_dataset(self):
        """
        Test EMA calculation on large dataset.
        """
        # Create a large dataset
        prices = list(range(1, 10001))  # 10,000 prices
        window_size = 50
        
        ema = self.calculator.calculate(prices, window_size)
        
        # Should have correct length
        self.assertEqual(len(ema), len(prices) - window_size + 1)
        # All values should be numeric
        for value in ema:
            self.assertIsInstance(value, (int, float))
    
    def test_calculate_ema_floating_point_precision(self):
        """
        Test EMA with floating-point prices.
        """
        prices = [100.50, 101.75, 102.25, 103.50]
        window_size = 2
        
        ema = self.calculator.calculate(prices, window_size)
        
        # Should have 3 values
        self.assertEqual(len(ema), 3)
        # All values should be numeric
        for value in ema:
            self.assertIsInstance(value, (int, float))
    
    def test_get_ema_at_index(self):
        """
        Test retrieving EMA value at specific index.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate(prices, window_size)
        
        value = self.calculator.get_ema_at_index(0)
        expected_seed = sum(prices[:3]) / 3
        self.assertAlmostEqual(value, expected_seed, places=2)
    
    def test_get_ema_at_invalid_index(self):
        """
        Test error handling for invalid index.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate(prices, window_size)
        
        with self.assertRaises(IndexError):
            self.calculator.get_ema_at_index(10)
    
    def test_get_all_ema_values(self):
        """
        Test retrieving all EMA values.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate(prices, window_size)
        
        all_values = self.calculator.get_all_ema_values()
        
        self.assertEqual(len(all_values), 3)
    
    def test_calculate_multiplier_static(self):
        """
        Test static method for calculating multiplier.
        """
        window_size = 10
        multiplier = EMACalculator.calculate_multiplier(window_size)
        
        expected = 2.0 / (window_size + 1)
        self.assertAlmostEqual(multiplier, expected, places=4)
    
    def test_calculate_multiplier_invalid_window(self):
        """
        Test error handling for invalid window size in multiplier calculation.
        """
        with self.assertRaises(ValueError):
            EMACalculator.calculate_multiplier(0)
    
    def test_ema_vs_sma_responsiveness(self):
        """
        Test that EMA is more responsive than SMA to recent changes.
        """
        from src.sma_calculator import SMACalculator
        
        # Create a series with a price jump at the end
        prices = [100] * 20 + [150]
        window_size = 10
        
        ema_calc = EMACalculator()
        sma_calc = SMACalculator()
        
        ema = ema_calc.calculate(prices, window_size)
        sma = sma_calc.calculate(prices, window_size)
        
        # EMA should be higher than SMA at the end (more responsive)
        self.assertGreater(ema[-1], sma[-1])
    
    def test_ema_seed_value(self):
        """
        Test that EMA seed value is correctly calculated as SMA.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        ema = self.calculator.calculate(prices, window_size)
        
        # First EMA value should be SMA of first window
        expected_seed = (100 + 102 + 101) / 3
        self.assertAlmostEqual(ema[0], expected_seed, places=4)
    
    def test_ema_exponential_smoothing_formula(self):
        """
        Test that EMA follows the exponential smoothing formula.
        """
        prices = [100, 105, 110]
        window_size = 2
        
        ema = self.calculator.calculate(prices, window_size)
        
        # Multiplier = 2 / (2 + 1) = 2/3
        multiplier = 2.0 / 3.0
        
        # Seed EMA = (100 + 105) / 2 = 102.5
        seed_ema = 102.5
        self.assertAlmostEqual(ema[0], seed_ema, places=4)
        
        # Next EMA = 110 * (2/3) + 102.5 * (1/3)
        expected_ema_1 = 110 * multiplier + seed_ema * (1 - multiplier)
        self.assertAlmostEqual(ema[1], expected_ema_1, places=4)


if __name__ == '__main__':
    unittest.main()
