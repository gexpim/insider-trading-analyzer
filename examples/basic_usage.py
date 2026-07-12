#!/usr/bin/env python3
"""Basic usage examples for Insider Trading Analyzer."""

from claude_analyzer import InsiderAnalyzer
from batch_processor import BatchProcessor


def example_single_transaction():
    """Example: Analyze a single transaction."""
    print("Example 1: Analyzing Single Transaction")
    print("=" * 50)
    
    analyzer = InsiderAnalyzer()
    
    # Create a sample transaction
    transaction = {
        'company': 'Apple',
        'insider': 'Tim Cook',
        'role': 'CEO',
        'type': 'BUY',
        'shares': 100000,
        'price': 195.00,
        'value': 19500000,
        'date': '2024-07-15',
        'holdings_before': 500000,
        'holdings_after': 600000
    }
    
    # Analyze
    analysis = analyzer.analyze_transaction(transaction)
    print(analysis)
    print()


def example_batch_analysis():
    """Example: Analyze multiple transactions in a batch."""
    print("\nExample 2: Batch Analysis of Multiple Transactions")
    print("=" * 50)
    
    processor = BatchProcessor()
    
    transactions = [
        {
            'company': 'Microsoft',
            'insider': 'Satya Nadella',
            'role': 'CEO',
            'type': 'BUY',
            'shares': 75000,
            'price': 450.00,
            'value': 33750000,
            'date': '2024-07-14',
            'holdings_before': 350000,
            'holdings_after': 425000
        },
        {
            'company': 'NVIDIA',
            'insider': 'Jensen Huang',
            'role': 'CEO',
            'type': 'BUY',
            'shares': 250000,
            'price': 125.00,
            'value': 31250000,
            'date': '2024-07-13',
            'holdings_before': 900000,
            'holdings_after': 1150000
        },
        {
            'company': 'Google',
            'insider': 'Ruth Porat',
            'role': 'CFO',
            'type': 'SELL',
            'shares': 50000,
            'price': 185.00,
            'value': 9250000,
            'date': '2024-07-12',
            'holdings_before': 300000,
            'holdings_after': 250000
        }
    ]
    
    # Process batch
    results = processor.process_batch(transactions, batch_size=3)
    
    for batch in results['batches']:
        print(f"\nBatch {batch['batch_number']}:")
        print(batch['analysis'])
    
    # Save results
    processor.save_results("batch_analysis_example.json")
    print()


def example_company_comparison():
    """Example: Compare insider trading across companies."""
    print("\nExample 3: Company Comparison")
    print("=" * 50)
    
    analyzer = InsiderAnalyzer()
    
    transactions_by_company = {
        'Apple': [
            {
                'insider': 'Tim Cook',
                'role': 'CEO',
                'type': 'BUY',
                'shares': 100000,
                'price': 195.00,
                'date': '2024-07-15'
            },
            {
                'insider': 'Luca Maestri',
                'role': 'CFO',
                'type': 'BUY',
                'shares': 50000,
                'price': 195.00,
                'date': '2024-07-14'
            }
        ],
        'Microsoft': [
            {
                'insider': 'Satya Nadella',
                'role': 'CEO',
                'type': 'BUY',
                'shares': 75000,
                'price': 450.00,
                'date': '2024-07-14'
            }
        ],
        'NVIDIA': [
            {
                'insider': 'Jensen Huang',
                'role': 'CEO',
                'type': 'BUY',
                'shares': 250000,
                'price': 125.00,
                'date': '2024-07-13'
            }
        ]
    }
    
    # Compare
    analysis = analyzer.compare_companies(transactions_by_company)
    print(analysis)
    print()


if __name__ == "__main__":
    print("Insider Trading Analyzer - Usage Examples\n")
    
    # Run examples
    example_single_transaction()
    example_batch_analysis()
    example_company_comparison()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
