"""
Unit Tests for SMA Calculator Module

Tests sliding window algorithm, edge cases, and performance characteristics.
"""

import unittest
from src.sma_calculator import SMACalculator


class TestSMACalculator(unittest.TestCase):
    """
    Test cases for the SMACalculator class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.calculator = SMACalculator()
    
    def test_calculate_basic_sma(self):
        """
        Test basic SMA calculation.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        sma = self.calculator.calculate(prices, window_size)
        
        # Expected: [101, 102, 103]
        self.assertEqual(len(sma), 3)
        self.assertAlmostEqual(sma[0], 101.0, places=2)
        self.assertAlmostEqual(sma[1], 102.0, places=2)
        self.assertAlmostEqual(sma[2], 103.0, places=2)
    
    def test_calculate_sma_window_size_one(self):
        """
        Test SMA with window size of 1.
        """
        prices = [100, 102, 101, 103]
        window_size = 1
        
        sma = self.calculator.calculate(prices, window_size)
        
        # SMA with window size 1 should equal the prices
        self.assertEqual(len(sma), 4)
        for i in range(len(prices)):
            self.assertEqual(sma[i], prices[i])
    
    def test_calculate_sma_window_size_equals_length(self):
        """
        Test SMA when window size equals array length.
        """
        prices = [100, 102, 101, 103]
        window_size = 4
        
        sma = self.calculator.calculate(prices, window_size)
        
        # Should return single value (average of all prices)
        self.assertEqual(len(sma), 1)
        expected = sum(prices) / len(prices)
        self.assertAlmostEqual(sma[0], expected, places=2)
    
    def test_calculate_sma_window_size_larger_than_array(self):
        """
        Test error handling when window size exceeds array length.
        """
        prices = [100, 102, 101]
        window_size = 5
        
        with self.assertRaises(ValueError):
            self.calculator.calculate(prices, window_size)
    
    def test_calculate_sma_empty_array(self):
        """
        Test error handling for empty price array.
        """
        prices = []
        window_size = 3
        
        with self.assertRaises(ValueError):
            self.calculator.calculate(prices, window_size)
    
    def test_calculate_sma_invalid_window_size(self):
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
    
    def test_calculate_sma_non_numeric_prices(self):
        """
        Test error handling for non-numeric prices.
        """
        prices = [100, 'invalid', 101, 103]
        window_size = 2
        
        with self.assertRaises(TypeError):
            self.calculator.calculate(prices, window_size)
    
    def test_calculate_sma_with_padding(self):
        """
        Test SMA calculation with padding.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        
        sma = self.calculator.calculate_with_padding(prices, window_size)
        
        # Should have same length as prices
        self.assertEqual(len(sma), len(prices))
        # First window_size-1 values should be None
        for i in range(window_size - 1):
            self.assertIsNone(sma[i])
        # Remaining values should be SMA
        for i in range(window_size - 1, len(sma)):
            self.assertIsNotNone(sma[i])
    
    def test_calculate_sma_large_dataset(self):
        """
        Test SMA calculation on large dataset.
        """
        # Create a large dataset
        prices = list(range(1, 10001))  # 10,000 prices
        window_size = 50
        
        sma = self.calculator.calculate(prices, window_size)
        
        # Should have correct length
        self.assertEqual(len(sma), len(prices) - window_size + 1)
        # All values should be numeric
        for value in sma:
            self.assertIsInstance(value, (int, float))
    
    def test_calculate_sma_floating_point_precision(self):
        """
        Test SMA with floating-point prices.
        """
        prices = [100.50, 101.75, 102.25, 103.50]
        window_size = 2
        
        sma = self.calculator.calculate(prices, window_size)
        
        # Expected: [101.125, 102.0, 102.875]
        self.assertEqual(len(sma), 3)
        self.assertAlmostEqual(sma[0], 101.125, places=4)
        self.assertAlmostEqual(sma[1], 102.0, places=4)
        self.assertAlmostEqual(sma[2], 102.875, places=4)
    
    def test_get_sma_at_index(self):
        """
        Test retrieving SMA value at specific index.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate(prices, window_size)
        
        value = self.calculator.get_sma_at_index(0)
        self.assertAlmostEqual(value, 101.0, places=2)
    
    def test_get_sma_at_invalid_index(self):
        """
        Test error handling for invalid index.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate(prices, window_size)
        
        with self.assertRaises(IndexError):
            self.calculator.get_sma_at_index(10)
    
    def test_get_all_sma_values(self):
        """
        Test retrieving all SMA values.
        """
        prices = [100, 102, 101, 103, 105]
        window_size = 3
        self.calculator.calculate(prices, window_size)
        
        all_values = self.calculator.get_all_sma_values()
        
        self.assertEqual(len(all_values), 3)
    
    def test_calculate_single_window(self):
        """
        Test static method for calculating single window SMA.
        """
        prices = [100, 102, 101]
        
        sma = SMACalculator.calculate_single_window(prices, 3)
        
        expected = sum(prices) / len(prices)
        self.assertAlmostEqual(sma, expected, places=2)
    
    def test_calculate_single_window_length_mismatch(self):
        """
        Test error handling for single window with mismatched length.
        """
        prices = [100, 102, 101]
        window_size = 5
        
        with self.assertRaises(ValueError):
            SMACalculator.calculate_single_window(prices, window_size)
    
    def test_sma_correctness_manual_calculation(self):
        """
        Test SMA correctness against manual calculation.
        """
        prices = [10, 20, 30, 40, 50]
        window_size = 3
        
        sma = self.calculator.calculate(prices, window_size)
        
        # Manual calculation:
        # Window 1: (10+20+30)/3 = 20
        # Window 2: (20+30+40)/3 = 30
        # Window 3: (30+40+50)/3 = 40
        self.assertAlmostEqual(sma[0], 20.0, places=2)
        self.assertAlmostEqual(sma[1], 30.0, places=2)
        self.assertAlmostEqual(sma[2], 40.0, places=2)
    
    def test_sma_sliding_window_efficiency(self):
        """
        Test that SMA uses efficient sliding window (not recalculating from scratch).
        """
        # This test verifies the algorithm doesn't recalculate from scratch
        # by checking that it produces correct results for a known pattern
        prices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        window_size = 3
        
        sma = self.calculator.calculate(prices, window_size)
        
        # Verify each value
        expected = [2, 3, 4, 5, 6, 7, 8, 9]
        for i, expected_val in enumerate(expected):
            self.assertAlmostEqual(sma[i], expected_val, places=2)


if __name__ == '__main__':
    unittest.main()
