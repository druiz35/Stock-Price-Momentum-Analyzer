"""
Data Loader Module

Handles loading, parsing, and validating historical stock price data from CSV files.
Supports multiple date formats and ensures data integrity through validation and sorting.
"""

import csv
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import os


class DataLoader:
    """
    Loads and validates historical stock price data from CSV files.
    
    Attributes:
        data (List[Dict]): List of price records with date, open, high, low, close, volume.
        date_formats (List[str]): Supported date format strings.
    """
    
    SUPPORTED_DATE_FORMATS = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
    ]
    
    REQUIRED_FIELDS = ['date', 'close']
    OPTIONAL_FIELDS = ['open', 'high', 'low', 'volume']
    
    def __init__(self):
        """
        Initialize the DataLoader with empty data.
        """
        self.data: List[Dict] = []
    
    def load_csv(self, filepath: str) -> List[Dict]:
        """
        Load stock price data from a CSV file.
        
        Args:
            filepath (str): Path to the CSV file.
            
        Returns:
            List[Dict]: List of validated and sorted price records.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is invalid or required fields are missing.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if not filepath.endswith('.csv'):
            raise ValueError(f"File must be a CSV file: {filepath}")
        
        self.data = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                if reader.fieldnames is None:
                    raise ValueError("CSV file is empty or has no headers")
                
                # Normalize field names to lowercase
                fieldnames = [field.lower().strip() for field in reader.fieldnames]
                
                # Validate required fields
                for required_field in self.REQUIRED_FIELDS:
                    if required_field not in fieldnames:
                        raise ValueError(f"Missing required field: {required_field}")
                
                for row_idx, row in enumerate(reader, start=2):
                    # Normalize row keys
                    normalized_row = {k.lower().strip(): v for k, v in row.items()}
                    
                    # Validate and parse the record
                    try:
                        validated_record = self._validate_record(normalized_row, row_idx)
                        if validated_record is not None:
                            self.data.append(validated_record)
                    except ValueError as e:
                        # Log invalid records but continue processing
                        print(f"Warning: Skipping row {row_idx}: {e}")
                        continue
        
        except csv.Error as e:
            raise ValueError(f"CSV parsing error: {e}")
        
        if not self.data:
            raise ValueError("No valid records found in the CSV file")
        
        # Sort by date chronologically
        self.data.sort(key=lambda x: x['date'])
        
        return self.data
    
    def _validate_record(self, row: Dict, row_idx: int) -> Optional[Dict]:
        """
        Validate and parse a single record from the CSV.
        
        Args:
            row (Dict): The row data with normalized keys.
            row_idx (int): The row index for error reporting.
            
        Returns:
            Optional[Dict]: Validated record or None if invalid.
            
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        # Check for missing required fields
        if not row.get('date') or not row.get('date').strip():
            raise ValueError("Missing or empty 'date' field")
        
        if not row.get('close') or not row.get('close').strip():
            raise ValueError("Missing or empty 'close' field")
        
        # Parse date
        date_str = row['date'].strip()
        parsed_date = self._parse_date(date_str)
        
        if parsed_date is None:
            raise ValueError(f"Invalid date format: {date_str}")
        
        # Parse close price
        try:
            close_price = float(row['close'].strip())
            if close_price < 0:
                raise ValueError("Close price cannot be negative")
        except ValueError:
            raise ValueError(f"Invalid close price: {row['close']}")
        
        # Parse optional fields
        record = {
            'date': parsed_date,
            'close': close_price,
        }
        
        # Optional fields
        for field in self.OPTIONAL_FIELDS:
            if field in row and row[field] and row[field].strip():
                try:
                    value = float(row[field].strip())
                    if value < 0:
                        raise ValueError(f"{field} cannot be negative")
                    record[field] = value
                except ValueError:
                    raise ValueError(f"Invalid {field} value: {row[field]}")
            else:
                record[field] = None
        
        return record
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse a date string using supported formats.
        
        Args:
            date_str (str): The date string to parse.
            
        Returns:
            Optional[datetime]: Parsed datetime object or None if parsing fails.
        """
        for date_format in self.SUPPORTED_DATE_FORMATS:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
        
        return None
    
    def get_prices(self) -> List[float]:
        """
        Get a list of closing prices in chronological order.
        
        Returns:
            List[float]: List of closing prices.
        """
        return [record['close'] for record in self.data]
    
    def get_data(self) -> List[Dict]:
        """
        Get the complete loaded and validated data.
        
        Returns:
            List[Dict]: List of price records.
        """
        return self.data
    
    def validate_data_integrity(self) -> Tuple[bool, List[str]]:
        """
        Validate the integrity of loaded data.
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_issues)
        """
        issues = []
        
        if not self.data:
            issues.append("No data loaded")
            return False, issues
        
        # Check for chronological order
        for i in range(1, len(self.data)):
            if self.data[i]['date'] < self.data[i-1]['date']:
                issues.append(f"Data not in chronological order at index {i}")
                break
        
        # Check for duplicate dates
        dates = [record['date'] for record in self.data]
        if len(dates) != len(set(dates)):
            issues.append("Duplicate dates found in data")
        
        # Check for reasonable price values
        for i, record in enumerate(self.data):
            if record['close'] <= 0:
                issues.append(f"Invalid price at index {i}: {record['close']}")
            
            if record['high'] is not None and record['low'] is not None:
                if record['high'] < record['low']:
                    issues.append(f"High price less than low price at index {i}")
                if record['close'] > record['high'] or record['close'] < record['low']:
                    issues.append(f"Close price outside high-low range at index {i}")
        
        return len(issues) == 0, issues
