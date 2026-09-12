"""
Command-Line Interface (CLI)

Provides a Bash-based CLI for analyzing stock data with configurable parameters
including window sizes, date ranges, and output formats.
"""

import argparse
import json
import csv
import sys
from datetime import datetime
from typing import Optional, List, Dict
from pathlib import Path

from src.data_loader import DataLoader
from src.sma_calculator import SMACalculator
from src.ema_calculator import EMACalculator
from src.momentum_detector import MomentumDetector
from src.volatility_calculator import VolatilityCalculator
from src.multi_window_analyzer import MultiWindowAnalyzer


class StockAnalyzerCLI:
    """
    Command-line interface for stock price momentum analysis.
    """
    
    def __init__(self):
        """
        Initialize the CLI.
        """
        self.data_loader = DataLoader()
        self.sma_calculator = SMACalculator()
        self.ema_calculator = EMACalculator()
        self.momentum_detector = MomentumDetector()
        self.volatility_calculator = VolatilityCalculator()
        self.multi_window_analyzer = MultiWindowAnalyzer()
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI with the given arguments.
        
        Args:
            args (Optional[List[str]]): Command-line arguments.
            
        Returns:
            int: Exit code (0 for success, 1 for error).
        """
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        
        try:
            if parsed_args.command == 'analyze':
                return self._analyze_command(parsed_args)
            elif parsed_args.command == 'sma':
                return self._sma_command(parsed_args)
            elif parsed_args.command == 'ema':
                return self._ema_command(parsed_args)
            elif parsed_args.command == 'signals':
                return self._signals_command(parsed_args)
            elif parsed_args.command == 'volatility':
                return self._volatility_command(parsed_args)
            else:
                parser.print_help()
                return 0
        
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser.
        
        Returns:
            argparse.ArgumentParser: The configured parser.
        """
        parser = argparse.ArgumentParser(
            description='Stock Price Momentum Analyzer - Identify momentum patterns in stock prices',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Analyze stock data with default settings
  stock-analyzer analyze --input data.csv
  
  # Calculate SMA with custom window size
  stock-analyzer sma --input data.csv --window 20
  
  # Detect momentum signals
  stock-analyzer signals --input data.csv --window 10 --output signals.json
  
  # Calculate volatility metrics
  stock-analyzer volatility --input data.csv --window 20 --output volatility.csv
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Analyze command
        analyze_parser = subparsers.add_parser('analyze', help='Perform comprehensive analysis')
        analyze_parser.add_argument('--input', '-i', required=True, help='Input CSV file')
        analyze_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
        analyze_parser.add_argument('--format', '-f', choices=['csv', 'json', 'text'], default='text',
                                   help='Output format (default: text)')
        analyze_parser.add_argument('--short-window', type=int, default=10, help='Short MA window (default: 10)')
        analyze_parser.add_argument('--medium-window', type=int, default=20, help='Medium MA window (default: 20)')
        analyze_parser.add_argument('--long-window', type=int, default=50, help='Long MA window (default: 50)')
        analyze_parser.add_argument('--use-ema', action='store_true', help='Use EMA instead of SMA')
        
        # SMA command
        sma_parser = subparsers.add_parser('sma', help='Calculate Simple Moving Average')
        sma_parser.add_argument('--input', '-i', required=True, help='Input CSV file')
        sma_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
        sma_parser.add_argument('--format', '-f', choices=['csv', 'json', 'text'], default='text',
                               help='Output format (default: text)')
        sma_parser.add_argument('--window', '-w', type=int, required=True, help='Window size')
        
        # EMA command
        ema_parser = subparsers.add_parser('ema', help='Calculate Exponential Moving Average')
        ema_parser.add_argument('--input', '-i', required=True, help='Input CSV file')
        ema_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
        ema_parser.add_argument('--format', '-f', choices=['csv', 'json', 'text'], default='text',
                               help='Output format (default: text)')
        ema_parser.add_argument('--window', '-w', type=int, required=True, help='Window size')
        
        # Signals command
        signals_parser = subparsers.add_parser('signals', help='Detect momentum signals')
        signals_parser.add_argument('--input', '-i', required=True, help='Input CSV file')
        signals_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
        signals_parser.add_argument('--format', '-f', choices=['csv', 'json', 'text'], default='text',
                                   help='Output format (default: text)')
        signals_parser.add_argument('--window', '-w', type=int, required=True, help='MA window size')
        signals_parser.add_argument('--detect-crossovers', action='store_true', help='Detect crossover points')
        
        # Volatility command
        volatility_parser = subparsers.add_parser('volatility', help='Calculate volatility metrics')
        volatility_parser.add_argument('--input', '-i', required=True, help='Input CSV file')
        volatility_parser.add_argument('--output', '-o', help='Output file (default: stdout)')
        volatility_parser.add_argument('--format', '-f', choices=['csv', 'json', 'text'], default='text',
                                      help='Output format (default: text)')
        volatility_parser.add_argument('--window', '-w', type=int, required=True, help='Window size')
        
        return parser
    
    def _analyze_command(self, args: argparse.Namespace) -> int:
        """
        Execute the analyze command.
        
        Args:
            args (argparse.Namespace): Parsed arguments.
            
        Returns:
            int: Exit code.
        """
        # Load data
        prices = self.data_loader.load_csv(args.input)
        price_list = self.data_loader.get_prices()
        dates = [record['date'] for record in prices]
        
        # Perform analysis
        results = self.multi_window_analyzer.analyze(
            price_list,
            short_window=args.short_window,
            medium_window=args.medium_window,
            long_window=args.long_window,
            dates=dates,
            use_ema=args.use_ema
        )
        
        # Format and output results
        output = self._format_analysis_results(results, args.format)
        self._write_output(output, args.output)
        
        return 0
    
    def _sma_command(self, args: argparse.Namespace) -> int:
        """
        Execute the SMA command.
        
        Args:
            args (argparse.Namespace): Parsed arguments.
            
        Returns:
            int: Exit code.
        """
        # Load data
        prices = self.data_loader.load_csv(args.input)
        price_list = self.data_loader.get_prices()
        dates = [record['date'] for record in prices]
        
        # Calculate SMA
        sma_values = self.sma_calculator.calculate_with_padding(price_list, args.window)
        
        # Format and output results
        output = self._format_ma_results(dates, price_list, sma_values, 'SMA', args.format)
        self._write_output(output, args.output)
        
        return 0
    
    def _ema_command(self, args: argparse.Namespace) -> int:
        """
        Execute the EMA command.
        
        Args:
            args (argparse.Namespace): Parsed arguments.
            
        Returns:
            int: Exit code.
        """
        # Load data
        prices = self.data_loader.load_csv(args.input)
        price_list = self.data_loader.get_prices()
        dates = [record['date'] for record in prices]
        
        # Calculate EMA
        ema_values = self.ema_calculator.calculate_with_padding(price_list, args.window)
        
        # Format and output results
        output = self._format_ma_results(dates, price_list, ema_values, 'EMA', args.format)
        self._write_output(output, args.output)
        
        return 0
    
    def _signals_command(self, args: argparse.Namespace) -> int:
        """
        Execute the signals command.
        
        Args:
            args (argparse.Namespace): Parsed arguments.
            
        Returns:
            int: Exit code.
        """
        # Load data
        prices = self.data_loader.load_csv(args.input)
        price_list = self.data_loader.get_prices()
        dates = [record['date'] for record in prices]
        
        # Calculate moving average
        ma_values = self.ema_calculator.calculate_with_padding(price_list, args.window)
        
        # Detect signals
        signals = self.momentum_detector.detect_signals(price_list, ma_values, dates)
        
        # Optionally detect crossovers
        if args.detect_crossovers:
            crossovers = self.momentum_detector.detect_crossovers(price_list, ma_values, dates)
            output = self._format_signals_results(signals, crossovers, args.format)
        else:
            output = self._format_signals_results(signals, None, args.format)
        
        self._write_output(output, args.output)
        
        return 0
    
    def _volatility_command(self, args: argparse.Namespace) -> int:
        """
        Execute the volatility command.
        
        Args:
            args (argparse.Namespace): Parsed arguments.
            
        Returns:
            int: Exit code.
        """
        # Load data
        prices = self.data_loader.load_csv(args.input)
        price_list = self.data_loader.get_prices()
        dates = [record['date'] for record in prices]
        
        # Calculate volatility
        volatility = self.volatility_calculator.calculate_volatility_with_padding(price_list, args.window)
        
        # Format and output results
        output = self._format_volatility_results(dates, price_list, volatility, args.format)
        self._write_output(output, args.output)
        
        return 0
    
    @staticmethod
    def _format_analysis_results(results: Dict, format_type: str) -> str:
        """
        Format analysis results.
        
        Args:
            results (Dict): Analysis results.
            format_type (str): Output format (csv, json, or text).
            
        Returns:
            str: Formatted output.
        """
        if format_type == 'json':
            # Convert datetime objects to strings for JSON serialization
            results_copy = results.copy()
            return json.dumps(results_copy, indent=2, default=str)
        
        elif format_type == 'csv':
            lines = []
            lines.append('Index,Price,Short_MA,Medium_MA,Long_MA,Signal,Confidence,Alignment_Score')
            
            for i in range(len(results['prices'])):
                short = results['short_ma'][i] or ''
                medium = results['medium_ma'][i] or ''
                long = results['long_ma'][i] or ''
                
                line = f"{i},{results['prices'][i]:.2f},{short},{medium},{long},,{results['alignment_scores'][i] or ''}"
                lines.append(line)
            
            return '\n'.join(lines)
        
        else:  # text
            lines = []
            lines.append("Stock Price Momentum Analysis")
            lines.append("=" * 50)
            lines.append(f"Total data points: {len(results['prices'])}")
            lines.append(f"Short window: {results['short_window']}")
            lines.append(f"Medium window: {results['medium_window']}")
            lines.append(f"Long window: {results['long_window']}")
            lines.append(f"Confirmed signals: {len(results['confirmed_signals'])}")
            lines.append("")
            
            if results['confirmed_signals']:
                lines.append("Recent Confirmed Signals:")
                for signal in results['confirmed_signals'][-5:]:
                    lines.append(f"  Index {signal['index']}: {signal['signal']} "
                               f"(confidence: {signal['confidence']:.2f})")
            
            return '\n'.join(lines)
    
    @staticmethod
    def _format_ma_results(dates: List, prices: List[float], ma_values: List[float],
                          ma_type: str, format_type: str) -> str:
        """
        Format moving average results.
        
        Args:
            dates (List): List of dates.
            prices (List[float]): List of prices.
            ma_values (List[float]): List of MA values.
            ma_type (str): Type of MA (SMA or EMA).
            format_type (str): Output format.
            
        Returns:
            str: Formatted output.
        """
        if format_type == 'json':
            data = []
            for i in range(len(prices)):
                data.append({
                    'index': i,
                    'date': str(dates[i]) if i < len(dates) else None,
                    'price': prices[i],
                    ma_type: ma_values[i],
                })
            return json.dumps(data, indent=2)
        
        elif format_type == 'csv':
            lines = [f'Index,Date,Price,{ma_type}']
            for i in range(len(prices)):
                date_str = str(dates[i]) if i < len(dates) else ''
                ma_val = f"{ma_values[i]:.4f}" if ma_values[i] is not None else ''
                lines.append(f"{i},{date_str},{prices[i]:.2f},{ma_val}")
            return '\n'.join(lines)
        
        else:  # text
            lines = [f"{ma_type} Analysis"]
            lines.append("=" * 50)
            for i in range(min(10, len(prices))):
                ma_val = f"{ma_values[i]:.4f}" if ma_values[i] is not None else 'N/A'
                lines.append(f"Index {i}: Price={prices[i]:.2f}, {ma_type}={ma_val}")
            return '\n'.join(lines)
    
    @staticmethod
    def _format_signals_results(signals: List[Dict], crossovers: Optional[List[Dict]],
                               format_type: str) -> str:
        """
        Format signal detection results.
        
        Args:
            signals (List[Dict]): List of signals.
            crossovers (Optional[List[Dict]]): List of crossovers.
            format_type (str): Output format.
            
        Returns:
            str: Formatted output.
        """
        if format_type == 'json':
            data = {
                'signals': signals,
                'crossovers': crossovers or [],
            }
            return json.dumps(data, indent=2, default=str)
        
        elif format_type == 'csv':
            lines = ['Index,Date,Price,Signal,Confidence']
            for signal in signals:
                date_str = str(signal.get('date', ''))
                lines.append(f"{signal['index']},{date_str},{signal['price']:.2f},"
                           f"{signal['signal']},{signal['confidence']:.4f}")
            return '\n'.join(lines)
        
        else:  # text
            lines = ["Signal Detection Results"]
            lines.append("=" * 50)
            lines.append(f"Total signals: {len(signals)}")
            
            bullish = [s for s in signals if s['signal'] == 'BULLISH']
            bearish = [s for s in signals if s['signal'] == 'BEARISH']
            lines.append(f"Bullish signals: {len(bullish)}")
            lines.append(f"Bearish signals: {len(bearish)}")
            
            if crossovers:
                lines.append(f"Crossovers detected: {len(crossovers)}")
            
            return '\n'.join(lines)
    
    @staticmethod
    def _format_volatility_results(dates: List, prices: List[float], volatility: List[float],
                                  format_type: str) -> str:
        """
        Format volatility results.
        
        Args:
            dates (List): List of dates.
            prices (List[float]): List of prices.
            volatility (List[float]): List of volatility values.
            format_type (str): Output format.
            
        Returns:
            str: Formatted output.
        """
        if format_type == 'json':
            data = []
            for i in range(len(prices)):
                data.append({
                    'index': i,
                    'date': str(dates[i]) if i < len(dates) else None,
                    'price': prices[i],
                    'volatility': volatility[i],
                })
            return json.dumps(data, indent=2)
        
        elif format_type == 'csv':
            lines = ['Index,Date,Price,Volatility']
            for i in range(len(prices)):
                date_str = str(dates[i]) if i < len(dates) else ''
                vol_val = f"{volatility[i]:.4f}" if volatility[i] is not None else ''
                lines.append(f"{i},{date_str},{prices[i]:.2f},{vol_val}")
            return '\n'.join(lines)
        
        else:  # text
            lines = ["Volatility Analysis"]
            lines.append("=" * 50)
            for i in range(min(10, len(prices))):
                vol_val = f"{volatility[i]:.4f}" if volatility[i] is not None else 'N/A'
                lines.append(f"Index {i}: Price={prices[i]:.2f}, Volatility={vol_val}")
            return '\n'.join(lines)
    
    @staticmethod
    def _write_output(content: str, output_file: Optional[str] = None) -> None:
        """
        Write output to file or stdout.
        
        Args:
            content (str): Content to write.
            output_file (Optional[str]): Output file path (None for stdout).
        """
        if output_file:
            with open(output_file, 'w') as f:
                f.write(content)
            print(f"Output written to {output_file}")
        else:
            print(content)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args (Optional[List[str]]): Command-line arguments.
        
    Returns:
        int: Exit code.
    """
    cli = StockAnalyzerCLI()
    return cli.run(args)


if __name__ == '__main__':
    sys.exit(main())
