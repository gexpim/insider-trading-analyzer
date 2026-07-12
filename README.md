# Insider Trading Analyzer

A comprehensive system for analyzing insider trading activity from SEC sources using Claude AI.

## Features

- Real-time monitoring of Form 4 insider trades
- AI-powered analysis using Claude
- Support for AI stocks, SpaceTech stocks, and technology stocks
- Pattern detection and risk assessment
- Batch processing and multi-turn analysis
- Automated alerts and reporting

## Supported Companies

### AI Stocks
- NVIDIA (NVDA)
- Microsoft (MSFT)
- Google/Alphabet (GOOGL)
- Meta (META)
- Amazon (AMZN)
- Tesla (TSLA)
- Broadcom (AVGO)
- AMD (AMD)

### SpaceTech Stocks
- Virgin Galactic (SPCE)
- Axiom Space (AXIM)
- Relativity Space (RLTY)
- Planet Labs (PL)
- Rocket Lab (RKLB)

### Technology Leaders
- Apple (AAPL)
- Oracle (ORCL)
- Salesforce (CRM)
- Adobe (ADBE)
- Intel (INTC)

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`
2. Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

### Run Analysis

```bash
python main.py
```

## Architecture

```
SEC EDGAR API
    ↓
[SEC Fetcher] → Fetch Form 4 filings
    ↓
[Form 4 Parser] → Parse XML → Extract transactions
    ↓
[Claude Analyzer] → Multi-turn analysis
    ↓
[Results] → JSON/CSV export
```

## Modules

### `sec_fetcher.py`
Fetches insider trading data from SEC EDGAR API.

### `form4_parser.py`
Parses Form 4 XML filings to extract transaction details.

### `claude_analyzer.py`
Uses Claude AI for intelligent analysis of insider trades.

### `batch_processor.py`
Handles batch processing of multiple transactions.

### `main.py`
Main orchestrator that coordinates all components.

## Usage Examples

### Analyze Single Transaction

```python
from claude_analyzer import InsiderAnalyzer

analyzer = InsiderAnalyzer()
transaction = {
    'company': 'Microsoft',
    'insider': 'Satya Nadella',
    'role': 'CEO',
    'type': 'BUY',
    'shares': 50000,
    'price': 450.00,
    'date': '2024-07-12'
}

analysis = analyzer.analyze_transaction(transaction)
print(analysis)
```

### Batch Analysis

```python
from batch_processor import BatchProcessor

processor = BatchProcessor()
transactions = [...]
results = processor.process_batch(transactions)
```

## Output Format

Analysis results include:
- Transaction significance assessment
- Pattern analysis
- Insider sentiment (confidence/concern)
- Company prospect indicators
- Risk level assessment
- Recommendations

## Compliance

- This tool is for informational and analytical purposes only
- Not financial advice
- Complies with SEC Form 4 disclosure requirements
- Respects all applicable securities regulations

## Requirements

- Python 3.9+
- Anthropic API key
- Internet connection for SEC EDGAR API

## Contributing

Contributions welcome! Please submit pull requests or issues.

## License

MIT License
