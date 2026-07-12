"""SEC EDGAR Data Fetcher for Insider Trading Information."""

import requests
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
from dotenv import load_dotenv

load_dotenv()

class SECFetcher:
    """Fetches insider trading data from SEC EDGAR API."""
    
    BASE_URL = "https://data.sec.gov"
    HEADERS = {
        "User-Agent": os.getenv("SEC_USER_AGENT", "InsiderTradingAnalyzer/1.0")
    }
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def fetch_company_filings(self, cik: str, days_back: int = 30) -> List[Dict]:
        """Fetch Form 4 filings for a company.
        
        Args:
            cik: Company CIK number
            days_back: Number of days to look back
            
        Returns:
            List of Form 4 filings
        """
        try:
            # Fetch company submissions
            url = f"{self.BASE_URL}/submissions/CIK{cik:0>10}.json"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            filings = []
            
            # Extract Form 4 filings
            recent_filings = data.get('filings', {}).get('recent', {})
            
            for i, form in enumerate(recent_filings.get('form', [])):
                if form == '4':
                    filing = {
                        'form': form,
                        'filing_date': recent_filings['filingDate'][i],
                        'accession': recent_filings['accessionNumber'][i],
                        'url': f"{self.BASE_URL}/Archives/{recent_filings['accessionNumber'][i].replace('-', '')}"
                    }
                    filings.append(filing)
            
            # Filter by date
            cutoff_date = (datetime.now() - timedelta(days=days_back)).date()
            filtered = [
                f for f in filings 
                if datetime.strptime(f['filing_date'], '%Y-%m-%d').date() >= cutoff_date
            ]
            
            return filtered
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching filings for CIK {cik}: {e}")
            return []
    
    def fetch_filing_document(self, filing_url: str) -> Optional[str]:
        """Fetch the actual Form 4 XML document.
        
        Args:
            filing_url: URL to the filing
            
        Returns:
            XML content as string
        """
        try:
            # Form 4 documents are typically in XML format
            xml_url = filing_url.replace('0000', '', 1)
            xml_url = xml_url + "/form4.xml"
            
            response = self.session.get(xml_url, timeout=self.timeout)
            response.raise_for_status()
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching filing document: {e}")
            return None
    
    def batch_fetch_companies(self, cik_list: List[str], days_back: int = 30) -> Dict:
        """Fetch filings for multiple companies.
        
        Args:
            cik_list: List of CIK numbers
            days_back: Number of days to look back
            
        Returns:
            Dictionary with company CIK as key and filings as value
        """
        results = {}
        
        for cik in cik_list:
            filings = self.fetch_company_filings(cik, days_back)
            results[cik] = filings
            time.sleep(0.5)  # Rate limiting
        
        return results


if __name__ == "__main__":
    # Example usage
    fetcher = SECFetcher()
    
    # Fetch Microsoft filings
    msft_cik = "0000789019"
    filings = fetcher.fetch_company_filings(msft_cik, days_back=30)
    
    print(f"Found {len(filings)} Form 4 filings for Microsoft")
    for filing in filings[:5]:
        print(f"  - {filing['filing_date']}: {filing['accession']}")
