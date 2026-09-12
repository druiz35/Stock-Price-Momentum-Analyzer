"""
Unit Tests for Momentum Detector Module

Tests signal detection, crossover identification, and confidence scoring.
"""

import unittest
from datetime import datetime, timedelta
from src.momentum_detector import MomentumDetector


class TestMomentumDetector(unittest.TestCase):
    """
    Test cases for the MomentumDetector class.
        """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.detector = MomentumDetector()
    
    def test_detect_bullish_signals(self):
        """
        Test detection of bullish signals (price > MA).
        """
        prices = [100, 102, 104, 106, 108]
        moving_averages = [100, 101, 102, 103, 104]
        
        signals = self.detector.detect_signals(prices, moving_averages)
        
        # All signals should be bullish
        self.assertEqual(len(signals), 5)
        for signal in signals:
            self.assertEqual(signal['signal'], MomentumDetector.SIGNAL_BULLISH)
    
    def test_detect_bearish_signals(self):
        """
        Test detection of bearish signals (price < MA).
        """
        prices = [100, 98, 96, 94, 92]
        moving_averages = [100, 101, 102, 103, 104]
        
        signals = self.detector.detect_signals(prices, moving_averages)
        
        # All signals should be bearish
        self.assertEqual(len(signals), 5)
        for signal in signals:
            self.assertEqual(signal['signal'], MomentumDetector.SIGNAL_BEARISH)
    
    def test_detect_neutral_signals(self):
        """
        Test detection of neutral signals (price = MA).
        """
        prices = [100, 100, 100]
        moving_averages = [100, 100, 100]
        
        signals = self.detector.detect_signals(prices, moving_averages)
        
        # All signals should be neutral
        self.assertEqual(len(signals), 3)
        for signal in signals:
            self.assertEqual(signal['signal'], MomentumDetector.SIGNAL_NEUTRAL)
    
    def test_detect_signals_with_dates(self):
        """
        Test signal detection with date information.
        """
        prices = [100, 102, 104]
        moving_averages = [100, 101, 102]
        dates = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)]
        
        signals = self.detector.detect_signals(prices, moving_averages, dates)
        
        # All signals should have date information
        self.assertEqual(len(signals), 3)
        for i, signal in enumerate(signals):
            self.assertEqual(signal['date'], dates[i])
    
    def test_detect_signals_length_mismatch(self):
        """
        Test error handling for mismatched array lengths.
        """
        prices = [100, 102, 104]
        moving_averages = [100, 101]
        
        with self.assertRaises(ValueError):
            self.detector.detect_signals(prices, moving_averages)
    
    def test_detect_signals_empty_arrays(self):
        """
        Test error handling for empty arrays.
        """
        prices = []
        moving_averages = []
        
        with self.assertRaises(ValueError):
            self.detector.detect_signals(prices, moving_averages)
    
    def test_detect_signals_with_none_ma(self):
        """
        Test signal detection when MA contains None values.
        """
        prices = [100, 102, 104, 106]
        moving_averages = [None, 101, 102, 103]
        
        signals = self.detector.detect_signals(prices, moving_averages)
        
        # Should skip the first signal (MA is None)
        self.assertEqual(len(signals), 3)
    
    def test_detect_bullish_crossover(self):
        """
        Test detection of bullish crossover (price crosses above MA).
        """
        prices = [100, 99, 101, 103]
        moving_averages = [100, 100, 100, 100]
        
        crossovers = self.detector.detect_crossovers(prices, moving_averages)
        
        # Should detect one bullish crossover at index 2
        self.assertEqual(len(crossovers), 1)
        self.assertEqual(crossovers[0]['index'], 2)
        self.assertEqual(crossovers[0]['crossover_type'], MomentumDetector.SIGNAL_BULLISH)
    
    def test_detect_bearish_crossover(self):
        """
        Test detection of bearish crossover (price crosses below MA).
        """
        prices = [100, 101, 99, 97]
        moving_averages = [100, 100, 100, 100]
        
        crossovers = self.detector.detect_crossovers(prices, moving_averages)
        
        # Should detect one bearish crossover at index 2
        self.assertEqual(len(crossovers), 1)
        self.assertEqual(crossovers[0]['index'], 2)
        self.assertEqual(crossovers[0]['crossover_type'], MomentumDetector.SIGNAL_BEARISH)
    
    def test_detect_multiple_crossovers(self):
        """
        Test detection of multiple crossovers.
        """
        prices = [100, 99, 101, 99, 101]
        moving_averages = [100, 100, 100, 100, 100]
        
        crossovers = self.detector.detect_crossovers(prices, moving_averages)
        
        # Should detect three crossovers
        self.assertEqual(len(crossovers), 3)
    
    def test_detect_crossovers_with_dates(self):
        """
        Test crossover detection with date information.
        """
        prices = [100, 99, 101]
        moving_averages = [100, 100, 100]
        dates = [datetime(2023, 1, 1), datetime(2023, 1, 2), datetime(2023, 1, 3)]
        
        crossovers = self.detector.detect_crossovers(prices, moving_averages, dates)
        
        # Should have date information
        self.assertEqual(len(crossovers), 1)
        self.assertEqual(crossovers[0]['date'], dates[2])
    
    def test_detect_crossovers_insufficient_data(self):
        """
        Test error handling for insufficient data points.
        """
        prices = [100]
        moving_averages = [100]
        
        with self.assertRaises(ValueError):
            self.detector.detect_crossovers(prices, moving_averages)
    
    def test_detect_crossovers_with_none_ma(self):
        """
        Test crossover detection when MA contains None values.
        """
        prices = [100, 99, 101, 103]
        moving_averages = [None, 100, 100, 100]
        
        crossovers = self.detector.detect_crossovers(prices, moving_averages)
        
        # Should skip crossovers involving None MA values
        self.assertEqual(len(crossovers), 1)
    
    def test_get_signals(self):
        """
        Test retrieving detected signals.
        """
        prices = [100, 102, 104]
        moving_averages = [100, 101, 102]
        
        self.detector.detect_signals(prices, moving_averages)
        signals = self.detector.get_signals()
        
        self.assertEqual(len(signals), 3)
    
    def test_get_crossovers(self):
        """
        Test retrieving detected crossovers.
        """
        prices = [100, 99, 101]
        moving_averages = [100, 100, 100]
        
        self.detector.detect_crossovers(prices, moving_averages)
        crossovers = self.detector.get_crossovers()
        
        self.assertEqual(len(crossovers), 1)
    
    def test_get_signals_by_type(self):
        """
        Test retrieving signals of a specific type.
        """
        prices = [100, 102, 98, 104]
        moving_averages = [100, 101, 101, 102]
        
        self.detector.detect_signals(prices, moving_averages)
        bullish_signals = self.detector.get_signals_by_type(MomentumDetector.SIGNAL_BULLISH)
        bearish_signals = self.detector.get_signals_by_type(MomentumDetector.SIGNAL_BEARISH)
        
        self.assertEqual(len(bullish_signals), 3)
        self.assertEqual(len(bearish_signals), 1)
    
    def test_get_consecutive_signals(self):
        """
        Test retrieving consecutive signals of the same type.
        """
        prices = [100, 102, 104, 106, 98, 96]
        moving_averages = [100, 101, 102, 103, 104, 105]
        
        self.detector.detect_signals(prices, moving_averages)
        consecutive = self.detector.get_consecutive_signals(min_consecutive=2)
        
        # Should have groups of consecutive signals
        self.assertGreater(len(consecutive), 0)
    
    def test_confidence_calculation(self):
        """
        Test confidence score calculation.
        """
        prices = [100, 110, 120]
        moving_averages = [100, 100, 100]
        
        signals = self.detector.detect_signals(prices, moving_averages)
        
        # Confidence should increase with distance from MA
        self.assertGreater(signals[1]['confidence'], signals[0]['confidence'])
        self.assertGreater(signals[2]['confidence'], signals[1]['confidence'])
    
    def test_confidence_range(self):
        """
        Test that confidence scores are within valid range.
        """
        prices = [100, 102, 104, 106, 108]
        moving_averages = [100, 101, 102, 103, 104]
        
        signals = self.detector.detect_signals(prices, moving_averages)
        
        # All confidence scores should be between 0 and 1
        for signal in signals:
            self.assertGreaterEqual(signal['confidence'], 0.0)
            self.assertLessEqual(signal['confidence'], 1.0)
    
    def test_signal_attributes(self):
        """
        Test that signals have all required attributes.
        """
        prices = [100, 102, 104]
        moving_averages = [100, 101, 102]
        
        signals = self.detector.detect_signals(prices, moving_averages)
        
        required_keys = ['index', 'price', 'moving_average', 'signal', 'confidence']
        for signal in signals:
            for key in required_keys:
                self.assertIn(key, signal)
    
    def test_crossover_attributes(self):
        """
        Test that crossovers have all required attributes.
        """
        prices = [100, 99, 101]
        moving_averages = [100, 100, 100]
        
        crossovers = self.detector.detect_crossovers(prices, moving_averages)
        
        required_keys = ['index', 'price', 'moving_average', 'crossover_type',
                        'previous_price', 'previous_ma']
        for crossover in crossovers:
            for key in required_keys:
                self.assertIn(key, crossover)


if __name__ == '__main__':
    unittest.main()
