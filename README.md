[![PyPi version](https://img.shields.io/pypi/v/geckoterminal-api)](https://pypi.python.org/pypi/geckoterminal-api/)
[![Downloads](https://static.pepy.tech/badge/geckoterminal-api)](https://pepy.tech/project/geckoterminal-api)
[![Python 3.12](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![codecov](https://codecov.io/gh/dineshpinto/geckoterminal-api/graph/badge.svg?token=JQLPDDAFX0)](https://codecov.io/gh/dineshpinto/geckoterminal-api)
[![API unittest](https://github.com/dineshpinto/geckoterminal-api/actions/workflows/unittests.yml/badge.svg)](https://github.com/dineshpinto/geckoterminal-api/actions/workflows/unittests.yml)

# GeckoTerminal API

A lightweight Python wrapper for the [GeckoTerminal](https://www.geckoterminal.com) DeFi & DeX aggregator, supporting 90+ chains and 500+ DEXs.

## Key Features

- **Market Data**: Fetch price, volume, and historical charts for any token.
- **Pool Discovery**: Identify pools trading a specific token.
- **Candlestick Charts**: Generate OHLCV-based candlestick charts.
- **Sync/Async support:** Supports both synchronous and asynchronous API.

> **Note:** The API is currently in beta and subject to change. Please report issues.

## Installation

```bash
pip install geckoterminal-api
```

## Documentation

Refer to the official [GeckoTerminal API docs](https://www.geckoterminal.com/dex-api) for detailed information.

## Quickstart

### Synchronous API Example

```python
from geckoterminal_api import GeckoTerminalAPI

gt = GeckoTerminalAPI()
# Fetch supported networks and their IDs
gt.networks()
```

### Asynchronous API Example

```python
import asyncio
from geckoterminal_api import AsyncGeckoTerminalAPI

agt = AsyncGeckoTerminalAPI()
# Fetch supported networks and their IDs
asyncio.run(agt.networks())
```

## Usage Examples

### Fetch Trades for a Specific Pool

```python
# Query $ANALOS pool on Solana
trades = gt.network_pool_trades(network="solana", pool="69grLw4PcSypZnn3xpsozCJFT8vs8WA5817VUVnzNGTh")

for trade_data in trades["data"]:
    trade = trade_data["attributes"]
    print(f'{trade["block_timestamp"]} -- {trade["kind"]}: {float(trade["volume_in_usd"]):.2f} USD')
```

_(truncated output)_

```text
2023-12-27T08:27:24Z -- buy: 0.06 USD
2023-12-27T08:27:22Z -- buy: 54.73 USD
2023-12-27T08:27:22Z -- sell: 43.11 USD
2023-12-27T08:27:22Z -- sell: 105.08 USD
2023-12-27T08:27:20Z -- sell: 552.80 USD
2023-12-27T08:27:17Z -- buy: 1116.88 USD
2023-12-27T08:27:14Z -- sell: 1110.02 USD
2023-12-27T08:27:12Z -- buy: 52.44 USD
2023-12-27T08:27:02Z -- buy: 41.72 USD
2023-12-27T08:26:59Z -- sell: 15.31 USD
```

### Discover Trending Pools

```python
# Trending pools on Solana
trending_pools = gt.network_trending_pools(network="solana")
print(trending_pools)
```

_(truncated output)_

```json
{
  "id": "solana_EP2ib6dYdEeqD8MfE2ezHCxX3kP3K2eLKkirfPm5eyMx",
  "type": "pool",
  "attributes": {
    "base_token_price_usd": "0.216341",
    "address": "EP2ib6dYdEeqD8MfE2ezHCxX3kP3K2eLKkirfPm5eyMx",
    "name": "$WIF / SOL",
    "fdv_usd": "214518552",
    "market_cap_usd": "201410163.369506",
    "price_change_percentage": {
      "h1": "2.75",
      "h24": "-11.76"
    },
    "transactions": {
      "h1": {
        "buys": 1143,
        "sells": 494,
        "buyers": 282,
        "sellers": 249
      },
      "h24": {
        "buys": 33874,
        "sells": 21413,
        "buyers": 6790,
        "sellers": 5363
      }
    },
    "volume_usd": {
      "h1": "782023.141511",
      "h24": "41413570.131944"
    }
  }
}
```

### Discover New Pools

```python
# New pools on Arbitrum
new_pools = gt.network_new_pools(network="arbitrum")
print(new_pools)
```

_(truncated output)_

```json
{
  "id": "arbitrum_0x9405117878d3a7ff7968b3d6f322bf428c168ca7",
  "type": "pool",
  "attributes": {
    "base_token_price_usd": "0.000463649357219151",
    "address": "0x9405117878d3a7ff7968b3d6f322bf428c168ca7",
    "name": "JUPITER / WETH",
    "pool_created_at": "2023-12-23T22:19:36Z",
    "fdv_usd": "9736.64",
    "price_change_percentage": {
      "h1": "55.09",
      "h24": "55.09"
    },
    "transactions": {
      "h1": {
        "buys": 24,
        "sells": 4,
        "buyers": 24,
        "sellers": 4
      },
      "h24": {
        "buys": 24,
        "sells": 4,
        "buyers": 24,
        "sellers": 4
      }
    },
    "volume_usd": {
      "h1": "3191.9671827550049",
      "h24": "3191.9671827550049"
    },
    "reserve_in_usd": "14348.4777"
  }
}
```

_and many more..._

## Proxy Support

### Synchronous API Proxy Setup

```python
from geckoterminal_api import GeckoTerminalAPI

proxies = {
    'http': 'http://10.10.10.10:8000',
    'https': 'http://10.10.10.10:8000',
}
gt = GeckoTerminalAPI(proxies=proxies)
```

### Asynchronous API Proxy Setup

```python
from geckoterminal_api import AsyncGeckoTerminalAPI

proxy = "http://proxy.com"
agt = AsyncGeckoTerminalAPI(proxy=proxy)
```

## Disclaimer

This project is for educational purposes only. You should not construe any such
information or other material as legal, tax, investment, financial, or other advice.
Nothing contained here constitutes a solicitation, recommendation, endorsement, or
offer by me or any third party service provider to buy or sell any securities or other
financial instruments in this or in any other jurisdiction in which such solicitation or
offer would be unlawful under the securities laws of such jurisdiction.

Under no circumstances will I be held responsible or liable in any way for any claims,
damages, losses, expenses, costs, or liabilities whatsoever, including, without
limitation, any direct or indirect damages for loss of profits.
