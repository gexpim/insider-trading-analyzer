"""Claude AI Analyzer for Insider Trading Transactions."""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class InsiderAnalyzer:
    """Analyzes insider trading transactions using Claude AI."""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        self.conversation_history = []
    
    def analyze_transaction(self, transaction: Dict) -> str:
        """Analyze a single insider trading transaction.
        
        Args:
            transaction: Transaction details dictionary
            
        Returns:
            Claude's analysis as string
        """
        # Reset conversation for new analysis
        self.conversation_history = []
        
        # Format transaction data
        transaction_text = self._format_transaction(transaction)
        
        # First turn: Initial analysis request
        user_message = f"""Analyze this insider trading transaction for potential insights:

{transaction_text}

Please evaluate:
1. Significance: Is this a large transaction relative to holdings?
2. Pattern: Does this align with typical executive behavior?
3. Sentiment: Does this suggest confidence (buy) or concern (sell)?
4. Context: What might this indicate about company prospects?
5. Risk Level: Any red flags or concerns?

Provide a concise analysis."""
        
        response = self._send_message(user_message)
        
        # Second turn: Deep dive
        follow_up = "Based on your analysis, what are the top 3 risks or opportunities this transaction might indicate for the company?"
        
        detailed_response = self._send_message(follow_up)
        
        return f"{response}\n\n**Deeper Analysis:**\n{detailed_response}"
    
    def analyze_batch(self, transactions: List[Dict]) -> str:
        """Analyze multiple transactions for patterns.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Claude's batch analysis as string
        """
        self.conversation_history = []
        
        # Format batch data
        batch_text = self._format_batch(transactions)
        
        # First turn: Pattern detection
        user_message = f"""Analyze these insider trading transactions for patterns and signals:

{batch_text}

Identify:
1. Key patterns across transactions
2. Insider confidence levels (buying vs selling)
3. Potential risks or opportunities
4. Unusual activity
5. Sector trends if applicable

Format as structured insights."""
        
        response = self._send_message(user_message)
        
        # Second turn: Risk assessment
        follow_up = "What would you score as the overall risk level (Low/Medium/High/Critical) and why? What actions should be taken?"
        
        risk_response = self._send_message(follow_up)
        
        # Third turn: Investment implications
        investment_question = "What investment implications do these trades suggest? Are there any sector winners or losers?"
        
        investment_response = self._send_message(investment_question)
        
        return f"{response}\n\n**Risk Assessment:**\n{risk_response}\n\n**Investment Implications:**\n{investment_response}"
    
    def compare_companies(self, transactions_by_company: Dict[str, List[Dict]]) -> str:
        """Compare insider trading activity across companies.
        
        Args:
            transactions_by_company: Dict with company names as keys and transaction lists as values
            
        Returns:
            Claude's comparison analysis
        """
        self.conversation_history = []
        
        # Format comparison data
        comparison_text = self._format_company_comparison(transactions_by_company)
        
        # First turn: Sector comparison
        user_message = f"""Compare the insider trading activity across these companies:

{comparison_text}

Analyze:
1. Which companies show the most executive confidence?
2. Which show the most concern?
3. Are there sector-wide trends?
4. Which companies have the most unusual activity?
5. What does this tell us about competitive positioning?"""
        
        response = self._send_message(user_message)
        
        # Second turn: Recommendations
        follow_up = "Based on this insider activity, which company appears to have the strongest fundamentals and which appears weakest? Why?"
        
        recommendation = self._send_message(follow_up)
        
        return f"{response}\n\n**Company Recommendations:**\n{recommendation}"
    
    def _send_message(self, user_message: str) -> str:
        """Send message to Claude and maintain conversation history.
        
        Args:
            user_message: The user's message
            
        Returns:
            Claude's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Send to Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system="You are an expert financial analyst specializing in insider trading patterns and SEC filings. Provide insightful, data-driven analysis of trading activity. Be concise but thorough.",
            messages=self.conversation_history
        )
        
        # Extract response text
        assistant_message = response.content[0].text
        
        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    @staticmethod
    def _format_transaction(transaction: Dict) -> str:
        """Format transaction data for Claude."""
        return f"""Transaction Details:
- Company: {transaction.get('company', 'N/A')}
- Insider: {transaction.get('insider', 'N/A')}
- Role: {transaction.get('role', 'N/A')}
- Type: {transaction.get('type', 'N/A')} (BUY/SELL)
- Shares: {transaction.get('shares', 'N/A'):,}
- Price: ${transaction.get('price', 'N/A')}
- Transaction Value: ${transaction.get('value', 'N/A'):,}
- Filing Date: {transaction.get('date', 'N/A')}
- Holdings Before: {transaction.get('holdings_before', 'N/A'):,}
- Holdings After: {transaction.get('holdings_after', 'N/A'):,}"""
    
    @staticmethod
    def _format_batch(transactions: List[Dict]) -> str:
        """Format batch of transactions for Claude."""
        summary = "Recent Insider Trading Activity:\n\n"
        for i, t in enumerate(transactions, 1):
            summary += f"{i}. {t.get('insider', 'Unknown')} ({t.get('role', 'Unknown')}) at {t.get('company', 'Unknown')}: "
            summary += f"{t.get('type', 'N/A')} {t.get('shares', 0):,} shares @ ${t.get('price', 0)} "
            summary += f"({t.get('date', 'N/A')})\n"
        return summary
    
    @staticmethod
    def _format_company_comparison(transactions_by_company: Dict[str, List[Dict]]) -> str:
        """Format company comparison data for Claude."""
        summary = "Insider Trading by Company:\n\n"
        for company, transactions in transactions_by_company.items():
            summary += f"**{company}** ({len(transactions)} transactions):\n"
            for t in transactions:
                summary += f"  - {t.get('insider')}: {t.get('type')} {t.get('shares', 0):,} shares\n"
            summary += "\n"
        return summary


if __name__ == "__main__":
    # Example usage
    analyzer = InsiderAnalyzer()
    
    # Sample transaction
    sample_transaction = {
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
    
    analysis = analyzer.analyze_transaction(sample_transaction)
    print("Analysis:\n", analysis)
