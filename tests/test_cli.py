"""
Integration Tests for CLI Module

Tests command-line argument parsing, output formatting, and end-to-end workflows.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime
from src.cli import StockAnalyzerCLI


class TestStockAnalyzerCLI(unittest.TestCase):
    """
    Test cases for the StockAnalyzerCLI class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.cli = StockAnalyzerCLI()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """
        Clean up test fixtures.
        """
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def _create_temp_csv(self, content: str) -> str:
        """
        Create a temporary CSV file with the given content.
        
        Args:
            content (str): CSV content.
            
        Returns:
            str: Path to the temporary file.
        """
        filepath = os.path.join(self.temp_dir, 'test.csv')
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
    
    def test_cli_help(self):
        """
        Test CLI help command.
        """
        # Should not raise an error
        result = self.cli.run(['--help'])
        # Help returns 0
        self.assertEqual(result, 0)
    
    def test_sma_command(self):
        """
        Test SMA command.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['sma', '--input', filepath, '--window', '3', '--output', output_file])
        
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(output_file))
    
    def test_ema_command(self):
        """
        Test EMA command.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['ema', '--input', filepath, '--window', '3', '--output', output_file])
        
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(output_file))
    
    def test_signals_command(self):
        """
        Test signals command.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['signals', '--input', filepath, '--window', '3', '--output', output_file])
        
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(output_file))
    
    def test_volatility_command(self):
        """
        Test volatility command.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['volatility', '--input', filepath, '--window', '3', '--output', output_file])
        
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(output_file))
    
    def test_analyze_command(self):
        """
        Test analyze command.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
2023-01-06,105.00
2023-01-07,106.50
2023-01-08,107.00
2023-01-09,108.50
2023-01-10,109.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['analyze', '--input', filepath, '--output', output_file])
        
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(output_file))
    
    def test_output_format_csv(self):
        """
        Test CSV output format.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.csv')
        
        result = self.cli.run(['sma', '--input', filepath, '--window', '3', '--format', 'csv', '--output', output_file])
        
        self.assertEqual(result, 0)
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn('Index', content)
            self.assertIn('Price', content)
    
    def test_output_format_json(self):
        """
        Test JSON output format.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.json')
        
        result = self.cli.run(['sma', '--input', filepath, '--window', '3', '--format', 'json', '--output', output_file])
        
        self.assertEqual(result, 0)
        with open(output_file, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
    
    def test_output_format_text(self):
        """
        Test text output format.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['sma', '--input', filepath, '--window', '3', '--format', 'text', '--output', output_file])
        
        self.assertEqual(result, 0)
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn('SMA Analysis', content)
    
    def test_custom_window_sizes(self):
        """
        Test analyze command with custom window sizes.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
2023-01-06,105.00
2023-01-07,106.50
2023-01-08,107.00
2023-01-09,108.50
2023-01-10,109.00
2023-01-11,110.00
2023-01-12,111.50
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['analyze', '--input', filepath, '--short-window', '5',
                              '--medium-window', '8', '--long-window', '10', '--output', output_file])
        
        self.assertEqual(result, 0)
    
    def test_use_ema_flag(self):
        """
        Test analyze command with EMA flag.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,102.00
2023-01-04,103.50
2023-01-05,104.00
2023-01-06,105.00
2023-01-07,106.50
2023-01-08,107.00
2023-01-09,108.50
2023-01-10,109.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['analyze', '--input', filepath, '--use-ema', '--output', output_file])
        
        self.assertEqual(result, 0)
    
    def test_detect_crossovers_flag(self):
        """
        Test signals command with crossover detection.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,99.00
2023-01-03,101.00
2023-01-04,103.50
2023-01-05,104.00
"""
        filepath = self._create_temp_csv(content)
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = self.cli.run(['signals', '--input', filepath, '--window', '2',
                              '--detect-crossovers', '--output', output_file])
        
        self.assertEqual(result, 0)
    
    def test_missing_required_argument(self):
        """
        Test error handling for missing required arguments.
        """
        # Missing --input argument
        result = self.cli.run(['sma', '--window', '3'])
        
        # Should return error code
        self.assertNotEqual(result, 0)
    
    def test_invalid_file(self):
        """
        Test error handling for invalid file.
        """
        result = self.cli.run(['sma', '--input', '/nonexistent/file.csv', '--window', '3'])
        
        # Should return error code
        self.assertNotEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
