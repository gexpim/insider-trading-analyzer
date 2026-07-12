"""Batch processor for analyzing multiple insider trading transactions."""

import json
from typing import List, Dict
from datetime import datetime
from claude_analyzer import InsiderAnalyzer
from sec_fetcher import SECFetcher
from form4_parser import Form4Parser


class BatchProcessor:
    """Process batches of insider trading transactions through Claude."""
    
    def __init__(self, output_dir: str = "./results"):
        self.analyzer = InsiderAnalyzer()
        self.fetcher = SECFetcher()
        self.parser = Form4Parser()
        self.output_dir = output_dir
        self.results = []
    
    def process_batch(self, transactions: List[Dict], batch_size: int = 5) -> Dict:
        """Process batch of transactions through Claude.
        
        Args:
            transactions: List of transaction dictionaries
            batch_size: Number of transactions per batch
            
        Returns:
            Dictionary with batch results
        """
        batches = [transactions[i:i+batch_size] for i in range(0, len(transactions), batch_size)]
        
        all_results = {
            'timestamp': datetime.now().isoformat(),
            'total_transactions': len(transactions),
            'batches': []
        }
        
        for batch_num, batch in enumerate(batches, 1):
            print(f"Processing batch {batch_num}/{len(batches)}...")
            
            batch_result = {
                'batch_number': batch_num,
                'transaction_count': len(batch),
                'analysis': self.analyzer.analyze_batch(batch),
                'transactions': batch
            }
            
            all_results['batches'].append(batch_result)
        
        self.results = all_results
        return all_results
    
    def process_companies(self, companies: Dict[str, List[str]], days_back: int = 30) -> Dict:
        """Process insider trades for multiple companies.
        
        Args:
            companies: Dict with company names as keys and CIK lists as values
            days_back: Days to look back for filings
            
        Returns:
            Processing results
        """
        all_transactions = {}
        
        for sector, ciks in companies.items():
            print(f"\nFetching {sector}...")
            all_transactions[sector] = []
            
            for cik in ciks:
                print(f"  Processing {cik}...")
                filings = self.fetcher.fetch_company_filings(cik, days_back)
                
                for filing in filings:
                    # Fetch and parse Form 4
                    xml_content = self.fetcher.fetch_filing_document(filing['url'])
                    if xml_content:
                        parsed = self.parser.parse_form4(xml_content)
                        if parsed and parsed.get('transactions'):
                            all_transactions[sector].append(parsed)
        
        # Analyze by sector
        sector_analyses = {}
        for sector, transactions in all_transactions.items():
            if transactions:
                print(f"\nAnalyzing {sector}...")
                sector_analyses[sector] = self.analyzer.analyze_batch(
                    [t for t in transactions if t][:10]  # Limit to 10 per sector
                )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'sectors': sector_analyses,
            'transactions_by_sector': {k: len(v) for k, v in all_transactions.items()}
        }
    
    def save_results(self, filename: str = None) -> str:
        """Save batch results to JSON file.
        
        Args:
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/analysis_{timestamp}.json"
        
        # Create output directory if needed
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Prepare data for JSON serialization
        serializable_results = self._make_serializable(self.results)
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"Results saved to {filename}")
        return filename
    
    @staticmethod
    def _make_serializable(obj):
        """Convert non-serializable objects to JSON-safe types."""
        if isinstance(obj, dict):
            return {k: BatchProcessor._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [BatchProcessor._make_serializable(item) for item in obj]
        elif isinstance(obj, (datetime,)):
            return obj.isoformat()
        else:
            return obj


if __name__ == "__main__":
    # Example usage
    processor = BatchProcessor()
    
    # Sample transactions
    sample_transactions = [
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
        }
    ]
    
    results = processor.process_batch(sample_transactions)
    processor.save_results()
