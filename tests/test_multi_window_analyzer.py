"""
Unit Tests for Multi-Window Analyzer Module

Tests multi-window analysis, trend confirmation, and alignment scoring.
"""

import unittest
from datetime import datetime
from src.multi_window_analyzer import MultiWindowAnalyzer


class TestMultiWindowAnalyzer(unittest.TestCase):
    """
    Test cases for the MultiWindowAnalyzer class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.analyzer = MultiWindowAnalyzer()
    
    def test_analyze_basic(self):
        """
        Test basic multi-window analysis.
        """
        prices = list(range(100, 160))  # 60 prices
        
        results = self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        # Check that results contain expected keys
        self.assertIn('prices', results)
        self.assertIn('short_ma', results)
        self.assertIn('medium_ma', results)
        self.assertIn('long_ma', results)
        self.assertIn('signals', results)
        self.assertIn('confirmed_signals', results)
        self.assertIn('alignment_scores', results)
    
    def test_analyze_with_dates(self):
        """
        Test analysis with date information.
        """
        prices = list(range(100, 160))
        dates = [datetime(2023, 1, i+1) for i in range(len(prices))]
        
        results = self.analyzer.analyze(prices, short_window=10, medium_window=20,
                                       long_window=30, dates=dates)
        
        # Check that signals have date information
        self.assertGreater(len(results['signals']), 0)
        if results['signals']:
            self.assertIn('date', results['signals'][0])
    
    def test_analyze_invalid_window_sizes(self):
        """
        Test error handling for invalid window sizes.
        """
        prices = list(range(100, 160))
        
        # Window sizes not in ascending order
        with self.assertRaises(ValueError):
            self.analyzer.analyze(prices, short_window=20, medium_window=10, long_window=30)
    
    def test_analyze_window_size_exceeds_length(self):
        """
        Test error handling when long window exceeds price length.
        """
        prices = list(range(100, 110))  # Only 10 prices
        
        with self.assertRaises(ValueError):
            self.analyzer.analyze(prices, short_window=5, medium_window=8, long_window=20)
    
    def test_analyze_empty_prices(self):
        """
        Test error handling for empty prices.
        """
        prices = []
        
        with self.assertRaises(ValueError):
            self.analyzer.analyze(prices)
    
    def test_analyze_with_sma(self):
        """
        Test analysis using SMA instead of EMA.
        """
        prices = list(range(100, 160))
        
        results = self.analyzer.analyze(prices, short_window=10, medium_window=20,
                                       long_window=30, use_ema=False)
        
        # Should still produce valid results
        self.assertIn('short_ma', results)
        self.assertIn('medium_ma', results)
        self.assertIn('long_ma', results)
    
    def test_alignment_scores_calculation(self):
        """
        Test that alignment scores are calculated correctly.
        """
        prices = list(range(100, 160))
        
        results = self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        alignment_scores = results['alignment_scores']
        
        # Should have same length as prices
        self.assertEqual(len(alignment_scores), len(prices))
        
        # First 29 values should be None (not enough data)
        for i in range(29):
            self.assertIsNone(alignment_scores[i])
        
        # Remaining values should be between 0 and 1
        for i in range(29, len(alignment_scores)):
            if alignment_scores[i] is not None:
                self.assertGreaterEqual(alignment_scores[i], 0.0)
                self.assertLessEqual(alignment_scores[i], 1.0)
    
    def test_confirmed_signals(self):
        """
        Test that confirmed signals are properly identified.
        """
        # Create a strongly bullish trend
        prices = list(range(100, 160))
        
        results = self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        confirmed_signals = results['confirmed_signals']
        
        # Should have some confirmed signals
        self.assertGreater(len(confirmed_signals), 0)
        
        # All confirmed signals should have confirmation_strength
        for signal in confirmed_signals:
            self.assertIn('confirmation_strength', signal)
            self.assertGreaterEqual(signal['confirmation_strength'], 0.0)
            self.assertLessEqual(signal['confirmation_strength'], 1.0)
    
    def test_get_confirmed_signals(self):
        """
        Test retrieving confirmed signals.
        """
        prices = list(range(100, 160))
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        confirmed = self.analyzer.get_confirmed_signals()
        
        self.assertIsInstance(confirmed, list)
    
    def test_get_alignment_scores(self):
        """
        Test retrieving alignment scores.
        """
        prices = list(range(100, 160))
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        scores = self.analyzer.get_alignment_scores()
        
        self.assertEqual(len(scores), len(prices))
    
    def test_get_moving_averages(self):
        """
        Test retrieving all moving averages.
        """
        prices = list(range(100, 160))
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        mas = self.analyzer.get_moving_averages()
        
        self.assertIn('short', mas)
        self.assertIn('medium', mas)
        self.assertIn('long', mas)
        self.assertEqual(len(mas['short']), len(prices))
        self.assertEqual(len(mas['medium']), len(prices))
        self.assertEqual(len(mas['long']), len(prices))
    
    def test_get_trend_at_index(self):
        """
        Test retrieving trend information at specific index.
        """
        prices = list(range(100, 160))
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        trend = self.analyzer.get_trend_at_index(50)
        
        self.assertIn('price', trend)
        self.assertIn('short_ma', trend)
        self.assertIn('medium_ma', trend)
        self.assertIn('long_ma', trend)
        self.assertIn('trend', trend)
        self.assertIn('alignment_score', trend)
    
    def test_get_trend_at_invalid_index(self):
        """
        Test error handling for invalid index in trend retrieval.
        """
        prices = list(range(100, 160))
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        with self.assertRaises(IndexError):
            self.analyzer.get_trend_at_index(1000)
    
    def test_bullish_trend_detection(self):
        """
        Test detection of bullish trends.
        """
        # Create a strongly bullish trend
        prices = list(range(100, 160))
        
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        # Check trend at the end (should be bullish)
        trend = self.analyzer.get_trend_at_index(len(prices) - 1)
        
        self.assertIn('BULLISH', trend['trend'])
    
    def test_bearish_trend_detection(self):
        """
        Test detection of bearish trends.
        """
        # Create a strongly bearish trend
        prices = list(range(160, 100, -1))
        
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        # Check trend at the end (should be bearish)
        trend = self.analyzer.get_trend_at_index(len(prices) - 1)
        
        self.assertIn('BEARISH', trend['trend'])
    
    def test_neutral_trend_detection(self):
        """
        Test detection of neutral trends.
        """
        # Create a flat trend
        prices = [100] * 60
        
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        # Check trend (should be neutral)
        trend = self.analyzer.get_trend_at_index(50)
        
        self.assertEqual(trend['trend'], 'NEUTRAL')
    
    def test_confirmation_strength_levels(self):
        """
        Test that confirmation strength has different levels.
        """
        prices = list(range(100, 160))
        
        results = self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        confirmed_signals = results['confirmed_signals']
        
        # Should have signals with different confirmation strengths
        strengths = set(s['confirmation_strength'] for s in confirmed_signals)
        
        # Should have at least one strength level
        self.assertGreater(len(strengths), 0)
    
    def test_large_dataset_performance(self):
        """
        Test analysis performance on large dataset.
        """
        # Create a large dataset
        prices = list(range(1, 10001))  # 10,000 prices
        
        results = self.analyzer.analyze(prices, short_window=50, medium_window=100, long_window=200)
        
        # Should complete without errors
        self.assertIn('short_ma', results)
        self.assertEqual(len(results['prices']), 10000)
    
    def test_moving_average_ordering(self):
        """
        Test that moving averages maintain proper ordering in bullish trend.
        """
        prices = list(range(100, 160))
        
        self.analyzer.analyze(prices, short_window=10, medium_window=20, long_window=30)
        
        # In a bullish trend, short > medium > long
        trend = self.analyzer.get_trend_at_index(len(prices) - 1)
        
        if trend['short_ma'] is not None and trend['medium_ma'] is not None and trend['long_ma'] is not None:
            self.assertGreater(trend['short_ma'], trend['medium_ma'])
            self.assertGreater(trend['medium_ma'], trend['long_ma'])


if __name__ == '__main__':
    unittest.main()
