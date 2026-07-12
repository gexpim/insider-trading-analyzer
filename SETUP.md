# Setup Instructions

## Prerequisites

- Python 3.9 or higher
- Anthropic API key
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/gexpim/insider-trading-analyzer.git
cd insider-trading-analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-v7-...
   ```

3. (Optional) Customize other settings in `.env`

### 5. Verify Installation

```bash
python main.py
```

You should see sample analysis output.

## Running the Analyzer

### Single Transaction Analysis

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
    'value': 22500000,
    'date': '2024-07-12'
}

analysis = analyzer.analyze_transaction(transaction)
print(analysis)
```

### Batch Processing

```python
from batch_processor import BatchProcessor

processor = BatchProcessor()
transactions = [...]  # List of transactions

results = processor.process_batch(transactions)
processor.save_results()
```

### Fetch Real SEC Data

```python
from sec_fetcher import SECFetcher

fetcher = SECFetcher()

# Fetch Microsoft Form 4 filings
filings = fetcher.fetch_company_filings("0000789019", days_back=30)

for filing in filings:
    print(filing)
```

## Example Usage

See the `examples/` directory for complete usage examples.

## Troubleshooting

### ImportError: No module named 'anthropic'

Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### API Key Error

Verify your `.env` file has the correct API key:
```bash
cat .env | grep ANTHROPIC_API_KEY
```

### SEC EDGAR Timeout

The SEC API sometimes takes time to respond. The code has automatic retries.

## Support

For issues or questions, please open a GitHub issue.
