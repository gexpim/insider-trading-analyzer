#!/usr/bin/env python3
"""Main entry point for Insider Trading Analyzer."""

import os
import sys
from datetime import datetime
import yaml
from batch_processor import BatchProcessor
from claude_analyzer import InsiderAnalyzer
from dotenv import load_dotenv

load_dotenv()


def load_config(config_file: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Config file {config_file} not found")
        return {}


def validate_environment() -> bool:
    """Validate required environment variables."""
    required = ['ANTHROPIC_API_KEY']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print("Error: Missing environment variables:")
        for var in missing:
            print(f"  - {var}")
        print("\nPlease set these in .env file or environment.")
        return False
    
    return True


def run_single_analysis():
    """Run analysis on a single sample transaction."""
    print("\n" + "="*60)
    print("Single Transaction Analysis")
    print("="*60)
    
    analyzer = InsiderAnalyzer()
    
    # Sample transaction - Microsoft CEO buying stock
    transaction = {
        'company': 'Microsoft',
        'insider': 'Satya Nadella',
        'role': 'CEO',
        'type': 'BUY',
        'shares': 50000,
        'price': 450.00,
        'value': 22500000,
        'date': '2024-07-12',
        'holdings_before': 400000,
        'holdings_after': 450000
    }
    
    print(f"\nAnalyzing transaction: {transaction['insider']} ({transaction['role']}) at {transaction['company']}")
    print(f"Type: {transaction['type']} | Shares: {transaction['shares']:,} | Price: ${transaction['price']}")
    
    analysis = analyzer.analyze_transaction(transaction)
    print(f"\nAnalysis:\n{analysis}")
    
    return analysis


def run_batch_analysis():
    """Run analysis on multiple transactions."""
    print("\n" + "="*60)
    print("Batch Analysis")
    print("="*60)
    
    processor = BatchProcessor()
    
    # Sample batch of transactions
    transactions = [
        {
            'company': 'Microsoft',
            'insider': 'Satya Nadella',
            'role': 'CEO',
            'type': 'BUY',
            'shares': 50000,
            'price': 450.00,
            'value': 22500000,
            'date': '2024-07-12',
            'holdings_before': 400000,
            'holdings_after': 450000
        },
        {
            'company': 'Google',
            'insider': 'Sundar Pichai',
            'role': 'CEO',
            'type': 'SELL',
            'shares': 25000,
            'price': 180.00,
            'value': 4500000,
            'date': '2024-07-11',
            'holdings_before': 300000,
            'holdings_after': 275000
        },
        {
            'company': 'NVIDIA',
            'insider': 'Jensen Huang',
            'role': 'CEO',
            'type': 'BUY',
            'shares': 100000,
            'price': 120.00,
            'value': 12000000,
            'date': '2024-07-10',
            'holdings_before': 1000000,
            'holdings_after': 1100000
        }
    ]
    
    print(f"\nProcessing {len(transactions)} transactions...")
    results = processor.process_batch(transactions, batch_size=2)
    
    for batch in results['batches']:
        print(f"\nBatch {batch['batch_number']} Analysis:")
        print(batch['analysis'])
    
    # Save results
    output_file = processor.save_results()
    print(f"\nResults saved to: {output_file}")
    
    return results


def run_company_comparison():
    """Compare insider trading across multiple companies."""
    print("\n" + "="*60)
    print("Company Comparison Analysis")
    print("="*60)
    
    analyzer = InsiderAnalyzer()
    
    # Group transactions by company
    transactions_by_company = {
        'Microsoft': [
            {
                'insider': 'Satya Nadella',
                'role': 'CEO',
                'type': 'BUY',
                'shares': 50000,
                'price': 450.00,
                'date': '2024-07-12'
            }
        ],
        'Google': [
            {
                'insider': 'Sundar Pichai',
                'role': 'CEO',
                'type': 'SELL',
                'shares': 25000,
                'price': 180.00,
                'date': '2024-07-11'
            }
        ],
        'NVIDIA': [
            {
                'insider': 'Jensen Huang',
                'role': 'CEO',
                'type': 'BUY',
                'shares': 100000,
                'price': 120.00,
                'date': '2024-07-10'
            }
        ]
    }
    
    print("\nComparing insider trading activity across companies...")
    analysis = analyzer.compare_companies(transactions_by_company)
    print(f"\n{analysis}")
    
    return analysis


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("Insider Trading Analyzer")
    print("Powered by Claude AI & SEC Data")
    print("="*60)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Load config
    config = load_config()
    
    print("\nRunning demonstration analysis...\n")
    
    # Run analyses
    try:
        # Single transaction
        single_analysis = run_single_analysis()
        
        # Batch analysis
        batch_results = run_batch_analysis()
        
        # Company comparison
        comparison = run_company_comparison()
        
        print("\n" + "="*60)
        print("Analysis Complete")
        print("="*60)
        print("\nResults have been saved to the ./results directory")
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
