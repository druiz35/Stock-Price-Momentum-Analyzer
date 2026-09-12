"""
Unit Tests for Data Loader Module

Tests CSV parsing, data validation, date format handling, and error cases.
"""

import unittest
import tempfile
import os
from datetime import datetime
from src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    """
    Test cases for the DataLoader class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.loader = DataLoader()
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
    
    def test_load_valid_csv(self):
        """
        Test loading a valid CSV file.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,99.75
"""
        filepath = self._create_temp_csv(content)
        
        data = self.loader.load_csv(filepath)
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['close'], 100.00)
        self.assertEqual(data[1]['close'], 101.50)
        self.assertEqual(data[2]['close'], 99.75)
    
    def test_load_csv_with_all_fields(self):
        """
        Test loading CSV with all optional fields.
        """
        content = """date,open,high,low,close,volume
2023-01-01,99.50,102.00,98.00,100.00,1000000
2023-01-02,100.50,103.00,99.00,101.50,1100000
"""
        filepath = self._create_temp_csv(content)
        
        data = self.loader.load_csv(filepath)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['open'], 99.50)
        self.assertEqual(data[0]['high'], 102.00)
        self.assertEqual(data[0]['low'], 98.00)
        self.assertEqual(data[0]['volume'], 1000000.0)
    
    def test_load_csv_different_date_formats(self):
        """
        Test loading CSV with different date formats.
        """
        # Test YYYY-MM-DD format
        content1 = """date,close
2023-01-01,100.00
2023-01-02,101.50
"""
        filepath1 = self._create_temp_csv(content1)
        data1 = self.loader.load_csv(filepath1)
        self.assertEqual(len(data1), 2)
        
        # Test MM/DD/YYYY format
        content2 = """date,close
01/01/2023,100.00
01/02/2023,101.50
"""
        filepath2 = self._create_temp_csv(content2)
        data2 = self.loader.load_csv(filepath2)
        self.assertEqual(len(data2), 2)
    
    def test_load_csv_chronological_sorting(self):
        """
        Test that data is sorted chronologically.
        """
        content = """date,close
2023-01-03,99.75
2023-01-01,100.00
2023-01-02,101.50
"""
        filepath = self._create_temp_csv(content)
        
        data = self.loader.load_csv(filepath)
        
        # Check that dates are in order
        for i in range(1, len(data)):
            self.assertLessEqual(data[i-1]['date'], data[i]['date'])
    
    def test_load_csv_missing_required_field(self):
        """
        Test error handling for missing required fields.
        """
        content = """date,open,high
2023-01-01,99.50,102.00
"""
        filepath = self._create_temp_csv(content)
        
        with self.assertRaises(ValueError):
            self.loader.load_csv(filepath)
    
    def test_load_csv_missing_date_value(self):
        """
        Test error handling for missing date values.
        """
        content = """date,close
,100.00
2023-01-02,101.50
"""
        filepath = self._create_temp_csv(content)
        
        # Should skip invalid row and load valid ones
        data = self.loader.load_csv(filepath)
        self.assertEqual(len(data), 1)
    
    def test_load_csv_invalid_price(self):
        """
        Test error handling for invalid price values.
        """
        content = """date,close
2023-01-01,invalid
2023-01-02,101.50
"""
        filepath = self._create_temp_csv(content)
        
        # Should skip invalid row
        data = self.loader.load_csv(filepath)
        self.assertEqual(len(data), 1)
    
    def test_load_csv_negative_price(self):
        """
        Test error handling for negative prices.
        """
        content = """date,close
2023-01-01,-100.00
2023-01-02,101.50
"""
        filepath = self._create_temp_csv(content)
        
        # Should skip invalid row
        data = self.loader.load_csv(filepath)
        self.assertEqual(len(data), 1)
    
    def test_load_csv_empty_file(self):
        """
        Test error handling for empty CSV file.
        """
        filepath = self._create_temp_csv("")
        
        with self.assertRaises(ValueError):
            self.loader.load_csv(filepath)
    
    def test_load_csv_file_not_found(self):
        """
        Test error handling for non-existent file.
        """
        with self.assertRaises(FileNotFoundError):
            self.loader.load_csv('/nonexistent/file.csv')
    
    def test_load_csv_non_csv_file(self):
        """
        Test error handling for non-CSV files.
        """
        filepath = os.path.join(self.temp_dir, 'test.txt')
        with open(filepath, 'w') as f:
            f.write('test')
        
        with self.assertRaises(ValueError):
            self.loader.load_csv(filepath)
    
    def test_get_prices(self):
        """
        Test getting prices from loaded data.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,99.75
"""
        filepath = self._create_temp_csv(content)
        self.loader.load_csv(filepath)
        
        prices = self.loader.get_prices()
        
        self.assertEqual(len(prices), 3)
        self.assertEqual(prices[0], 100.00)
        self.assertEqual(prices[1], 101.50)
        self.assertEqual(prices[2], 99.75)
    
    def test_validate_data_integrity_valid(self):
        """
        Test data integrity validation for valid data.
        """
        content = """date,close
2023-01-01,100.00
2023-01-02,101.50
2023-01-03,99.75
"""
        filepath = self._create_temp_csv(content)
        self.loader.load_csv(filepath)
        
        is_valid, issues = self.loader.validate_data_integrity()
        
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_data_integrity_no_data(self):
        """
        Test data integrity validation with no data loaded.
        """
        is_valid, issues = self.loader.validate_data_integrity()
        
        self.assertFalse(is_valid)
        self.assertIn('No data loaded', issues[0])
    
    def test_validate_data_integrity_duplicate_dates(self):
        """
        Test data integrity validation for duplicate dates.
        """
        content = """date,close
2023-01-01,100.00
2023-01-01,101.50
"""
        filepath = self._create_temp_csv(content)
        self.loader.load_csv(filepath)
        
        is_valid, issues = self.loader.validate_data_integrity()
        
        self.assertFalse(is_valid)
        self.assertTrue(any('Duplicate dates' in issue for issue in issues))
    
    def test_validate_data_integrity_high_low_range(self):
        """
        Test data integrity validation for high-low range.
        """
        content = """date,high,low,close
2023-01-01,100.00,110.00,105.00
"""
        filepath = self._create_temp_csv(content)
        self.loader.load_csv(filepath)
        
        is_valid, issues = self.loader.validate_data_integrity()
        
        self.assertFalse(is_valid)
        self.assertTrue(any('High price less than low price' in issue for issue in issues))
    
    def test_case_insensitive_headers(self):
        """
        Test that CSV headers are case-insensitive.
        """
        content = """Date,Close
2023-01-01,100.00
2023-01-02,101.50
"""
        filepath = self._create_temp_csv(content)
        
        data = self.loader.load_csv(filepath)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['close'], 100.00)
    
    def test_whitespace_handling(self):
        """
        Test handling of whitespace in CSV.
        """
        content = """date, close
2023-01-01, 100.00
2023-01-02, 101.50
"""
        filepath = self._create_temp_csv(content)
        
        data = self.loader.load_csv(filepath)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['close'], 100.00)


if __name__ == '__main__':
    unittest.main()
