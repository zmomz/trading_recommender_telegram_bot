# Crypto Bollinger Bands Telegram Bot

This project implements a cryptocurrency trading signals bot utilizing **Bollinger Bands** and **Relative Strength Index (RSI)** indicators, providing automated buy and sell recommendations via Telegram.

---

## Overview

- **Symbols:** Customizable cryptocurrencies (default: ETH/USDT).
- **Exchange:** Binance (Public API, no authentication required).
- **Indicators:** Bollinger Bands (window=21), RSI (window=21).
- **Notifications:** Delivered through Telegram messaging.

---

## Project Goals

- Automate market analysis using technical indicators.
- Provide real-time trading alerts for cryptocurrency pairs.
- Simplify decision-making processes in cryptocurrency trading.

---

## Features

- Fetches live OHLCV (Open-High-Low-Close-Volume) data.
- Computes Bollinger Bands and RSI values.
- Determines overbought and oversold market conditions.
- Sends real-time Telegram notifications for buy/sell signals.
- Schedule-based continuous market monitoring.

---

## Technologies and Libraries

- Python 3
- ccxt (Binance API integration)
- pandas (data manipulation)
- ta (technical analysis indicators)
- python-telegram-bot (Telegram API integration)
- schedule (task scheduling)
- datetime & time (time-related operations)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/zmomz/trading_recommender_telegram_bot.git
cd trading_recommender_telegram_bot
```

### 2. Install Dependencies
```bash
pip install ccxt pandas ta python-telegram-bot schedule
```

### 3. Telegram Bot Setup
- Create a Telegram Bot using [@BotFather](https://telegram.me/BotFather).
- Obtain the Bot Token and replace it in the script:
```python
telegram_keys = {
    'test':'your_test_bot_token',
    'live':'your_live_bot_token'
}
```

### 4. Configuration
- Modify cryptocurrency pairs in the script:
```python
symbols = ["ETH/USDT", "BTC/USDT", ...] # add or remove pairs as needed
```

- Adjust the time frame and limits if required:
```python
timeframe = '5m'
full_day_limit_5_m = 289
```

### 5. Running the Bot
Run the bot continuously using:
```bash
python your_script_name.py
```

---

## Usage

- Users initiate communication with the Telegram Bot to subscribe for signals.
- The bot automatically detects and records active chat IDs.
- Sends actionable buy (🟩) and sell (🟥) notifications based on predefined technical indicator thresholds.

---

## Trading Logic

- **Buy Signal (Oversold):**
  - Price below Lower Bollinger Band (LBB) and RSI ≤ 35.

- **Sell Signal (Overbought):**
  - Price above Higher Bollinger Band (HBB) and RSI ≥ 70.

---

## Future Enhancements

- Integrate more trading indicators.
- Enhance with backtesting capabilities.
- Provide customizable alert thresholds.

---

## Contributions

Open issues or pull requests to contribute.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Disclaimer:**  
This bot provides market signals based on algorithmic indicators and does **not guarantee profits**. Always perform your due diligence before trading.
