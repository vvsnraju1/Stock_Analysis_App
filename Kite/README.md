# Zerodha Kite Agent

A simple OpenAI Agent that connects to your Zerodha trading account using the Kite MCP (Model Context Protocol) server.

## Prerequisites

- Python 3.9+
- A Zerodha trading account
- An OpenAI API key

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The agent uses the Kite MCP Server configuration from `Kite/Server.py`. This file contains the configuration for connecting to the Zerodha Kite MCP server.

## Available Scripts

This repository includes several agent scripts for different use cases:

1. **kite_agent.py** - Basic agent for general Zerodha account interaction
2. **advanced_kite_agent.py** - Enhanced agent with additional financial analysis tools
3. **portfolio_analysis.py** - Specialized agent for in-depth portfolio analysis

## Usage

### General Assistant

```bash
export OPENAI_API_KEY=your_openai_api_key
python kite_agent.py
```

### Advanced Financial Advisor

```bash
export OPENAI_API_KEY=your_openai_api_key
python advanced_kite_agent.py
```

### Automated Portfolio Analysis

```bash
export OPENAI_API_KEY=your_openai_api_key
python portfolio_analysis.py
```

If you haven't set the API key as an environment variable, the programs will prompt you to enter it.

### Example Queries

- "Show me my current portfolio holdings"
- "What's the current price of Infosys?"
- "Get real-time market data for RELIANCE"
- "Analyze my portfolio performance"
- "Calculate my portfolio's diversification metrics"
- "What's my exposure to the banking sector?"

## Features

- Portfolio analysis and optimization
- Real-time market data and quotes
- Investment position analysis
- Stock research and fundamental analysis
- Risk assessment and metrics calculation
- Sector allocation and diversification analysis

## Security Note

These agents require authorization to access your Zerodha account. When you run them for the first time, you'll be asked to authorize the connection through a secure Zerodha login flow.

## Troubleshooting

- If you encounter session errors, you may need to reauthorize your Zerodha account.
- Ensure your Zerodha account is active and not locked.
- Check your internet connection as the agent requires online access to both OpenAI and Zerodha servers. 