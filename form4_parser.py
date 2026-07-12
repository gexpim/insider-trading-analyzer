"""Parser for SEC Form 4 XML documents."""

from xml.etree import ElementTree as ET
from typing import List, Dict, Optional
from datetime import datetime


class Form4Parser:
    """Parses Form 4 XML to extract insider trading transactions."""
    
    NAMESPACES = {
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'default': 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001018724'
    }
    
    @staticmethod
    def parse_form4(xml_content: str) -> Dict:
        """Parse Form 4 XML document.
        
        Args:
            xml_content: XML content as string
            
        Returns:
            Dictionary with parsed Form 4 data
        """
        try:
            root = ET.fromstring(xml_content)
            
            form4_data = {
                'issuer': Form4Parser._extract_issuer(root),
                'reporting_owner': Form4Parser._extract_reporting_owner(root),
                'transactions': Form4Parser._extract_transactions(root),
                'holdings': Form4Parser._extract_holdings(root)
            }
            
            return form4_data
            
        except ET.ParseError as e:
            print(f"Error parsing Form 4 XML: {e}")
            return {}
    
    @staticmethod
    def _extract_issuer(root: ET.Element) -> Dict:
        """Extract issuer (company) information."""
        issuer = root.find('.//issuer')
        if issuer is None:
            return {}
        
        return {
            'company_name': Form4Parser._get_text(issuer, 'companyName'),
            'cik': Form4Parser._get_text(issuer, 'cik'),
            'ticker': Form4Parser._get_text(issuer, 'tickerSymbol')
        }
    
    @staticmethod
    def _extract_reporting_owner(root: ET.Element) -> Dict:
        """Extract reporting owner (insider) information."""
        owner = root.find('.//reportingOwner')
        if owner is None:
            return {}
        
        owner_info = owner.find('.//reportingOwnersInfo')
        if owner_info is None:
            return {}
        
        return {
            'name': Form4Parser._get_text(owner_info, 'rptOwnerName'),
            'relationship': Form4Parser._get_text(owner_info, 'relationshipOfReportingOwnerToIssuer'),
            'is_officer': Form4Parser._get_text(owner_info, 'officerTitle') != '',
            'officer_title': Form4Parser._get_text(owner_info, 'officerTitle'),
            'is_director': Form4Parser._get_text(owner_info, 'isDirector') == '1',
            'is_ten_percent': Form4Parser._get_text(owner_info, 'isTenPercentOwner') == '1'
        }
    
    @staticmethod
    def _extract_transactions(root: ET.Element) -> List[Dict]:
        """Extract transaction details."""
        transactions = []
        
        # Find all non-derivative transactions
        trans_list = root.findall('.//nonDerivativeTable/nonDerivativeTransaction')
        for trans in trans_list:
            transaction = {
                'type': Form4Parser._get_text(trans, 'transactionType'),
                'date': Form4Parser._get_text(trans, 'transactionDate/value'),
                'security': Form4Parser._get_text(trans, 'securityTitle/value'),
                'shares': Form4Parser._parse_float(trans, 'transactionShares/value'),
                'price': Form4Parser._parse_float(trans, 'transactionPrice/value'),
                'amount': Form4Parser._parse_float(trans, 'transactionAcquiredDisposedCode'),
            }
            if transaction['shares'] or transaction['price']:
                transactions.append(transaction)
        
        return transactions
    
    @staticmethod
    def _extract_holdings(root: ET.Element) -> List[Dict]:
        """Extract current holdings information."""
        holdings = []
        
        hold_list = root.findall('.//nonDerivativeTable/nonDerivativeHolding')
        for holding in hold_list:
            h = {
                'security': Form4Parser._get_text(holding, 'securityTitle/value'),
                'shares': Form4Parser._parse_float(holding, 'sharesOwnedFollowingTransaction/value'),
                'ownership_form': Form4Parser._get_text(holding, 'ownershipForm/value')
            }
            if h['shares']:
                holdings.append(h)
        
        return holdings
    
    @staticmethod
    def _get_text(element: ET.Element, path: str) -> str:
        """Safely extract text from XML element."""
        elem = element.find(path)
        return elem.text if elem is not None and elem.text else ''
    
    @staticmethod
    def _parse_float(element: ET.Element, path: str) -> Optional[float]:
        """Safely parse float from XML element."""
        text = Form4Parser._get_text(element, path)
        try:
            return float(text) if text else None
        except ValueError:
            return None


if __name__ == "__main__":
    # Example: Parse a Form 4 document
    # This would require actual Form 4 XML content
    sample_xml = """<?xml version="1.0"?>
    <form4>
        <issuer>
            <companyName>Microsoft Corporation</companyName>
            <cik>0000789019</cik>
            <tickerSymbol>MSFT</tickerSymbol>
        </issuer>
    </form4>"""
    
    parser = Form4Parser()
    result = parser.parse_form4(sample_xml)
    print("Parsed Form 4:", result)
