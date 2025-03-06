# Memecoin Trading Bot

A sophisticated Python-based algorithmic trading bot designed to automatically buy and sell memecoins on the Solana blockchain. The bot leverages the Jupiter Swap API for executing trades with optimal routes and pricing, while using Supabase for persistent storage and position management.

## 🚀 Features

- **Automated Buying**: Identify and purchase promising memecoins using customizable strategy parameters
- **Smart Selling**: Automatically sell based on profit targets, stop-loss conditions, or time-based exit strategies
- **Position Tracking**: Comprehensive tracking of all open and closed positions with performance metrics
- **Supabase Integration**: Cloud-based storage for reliable position data management and analytics
- **Jupiter API Integration**: Access to Solana's leading aggregator for best execution prices
- **Configurable Environment**: Easily customize the bot's behavior through environment variables

## 📁 Project Structure

```
memecoin-trading-bot/
├── .env                  # Environment variables configuration
├── .gitignore            # Git ignore file
├── .vscode/              # VSCode configuration
│   └── settings.json     # Editor settings
├── buy/                  # Buy module
│   ├── __pycache__/      # Python cache directory
│   ├── buy.py            # Main buying logic implementation
│   ├── gmgn_trending.py  # GMGN trending token detection
│   ├── main.py           # Entry point for buy operations
│   └── swap.py           # Jupiter swap implementation
├── requirements.txt      # Python dependencies
└── sell/                 # Sell module
    ├── __pycache__/      # Python cache directory
    ├── gmgn_price.py     # GMGN price fetching implementation
    └── main.py           # Entry point for sell operations
```

## 📋 Requirements

- Python 3.8 or newer
- Solana wallet with SOL for transactions
- Supabase account for database storage
- RPC node access for Solana blockchain interaction
- Required Python packages (detailed in requirements.txt):
  - `solana`
  - `requests`
  - `python-dotenv`
  - `supabase-py`
  - `loguru` (for advanced logging)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/memecoin-trading-bot.git
   cd memecoin-trading-bot
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   
   # On Unix/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   RPC_NODE=<your_solana_rpc_node_url>
   PRIVATE_KEY=<your_base58_encoded_private_key>
   SUPABASE_URL=<your_supabase_project_url>
   SUPABASE_KEY=<your_supabase_api_key>
   
   # Optional configuration
   SOL_AMOUNT=0.05           # Default SOL amount per trade
   MAX_POSITIONS=5           # Maximum concurrent positions
   TARGET_PROFIT=2.5         # Target profit percentage
   STOP_LOSS=50              # Stop loss percentage
   POSITION_TIMEOUT=300      # Position timeout in seconds (5 minutes)
   ```

## 🔄 Usage

### Buy Module

The buy module is responsible for identifying and purchasing potential memecoin opportunities:

```bash
python buy/main.py
```

**Key Features**:
- **Token Discovery**: Monitors various sources for trending tokens including GMGN
- **Liquidity Analysis**: Ensures sufficient liquidity before executing trades
- **Slippage Control**: Implements protective measures against excessive slippage
- **Transaction Verification**: Validates transactions on-chain before confirming positions

### Sell Module

The sell module continuously monitors open positions and executes sell orders based on predefined conditions:

```bash
python sell/main.py
```

**Selling Conditions**:
- **Profit Target**: Sells when price increases by the configured target percentage (default: 2.5%)
- **Stop Loss**: Liquidates position if price drops below configured threshold (default: 50%)
- **Time-Based Exit**: Closes positions that have been open beyond the configured timeout (default: 5 minutes)
- **Market Volatility Adjustment**: Dynamically adjusts exit conditions based on market conditions

## 📊 Position Management

The bot maintains detailed records of all trading positions in Supabase with the following information:
- Token address and symbol
- Entry price and current price
- Position size and value
- Profit/loss metrics
- Timestamp data
- Transaction hashes

## 🔍 Logging

The application implements comprehensive logging using Python's `logging` module:
- Timestamps for all log entries
- Differentiated log levels (INFO, WARNING, ERROR, DEBUG)
- Trade execution details
- Error tracing and exception handling

Example log output:
```
2023-08-15 14:32:45 INFO     [buy.py] Scanning for new memecoin opportunities...
2023-08-15 14:32:48 INFO     [gmgn_trending.py] Found 3 trending tokens on GMGN
2023-08-15 14:32:52 INFO     [buy.py] Attempting to buy BONK (BoNKzKV75RjJP1NNdpXEXPrGs1rQhBYMQWiJT8RTw9To)
2023-08-15 14:32:58 INFO     [swap.py] Received quote for 1000000 BONK at 0.00000025 SOL each
2023-08-15 14:33:01 INFO     [swap.py] Transaction confirmed: 5tSgRMYvxN6FdtdkVFJbNJk2JAChYmdSwKHJBYzxKBdgvPAYJmPdypCnJ6wSKGh8UbwvKvJU
```

## 🔐 Security Considerations

- Store your private key securely and never commit it to version control
- Use a dedicated wallet with limited funds for bot operations
- Implement rate limiting to prevent API abuse
- Consider using a hardware wallet for signing transactions in production

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

Trading cryptocurrencies, especially memecoins, involves significant risk. This bot is provided for educational and experimental purposes only. Use at your own risk. The authors are not responsible for any financial losses incurred through the use of this software.
