[![PyPi version](https://img.shields.io/pypi/v/geckoterminal-api)](https://pypi.python.org/pypi/geckoterminal-api/)
[![Python 3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![codecov](https://codecov.io/gh/dineshpinto/geckoterminal-api/graph/badge.svg?token=JQLPDDAFX0)](https://codecov.io/gh/dineshpinto/geckoterminal-api)
[![API unittest](https://github.com/dineshpinto/geckoterminal-api/actions/workflows/unittests.yml/badge.svg)](https://github.com/dineshpinto/geckoterminal-api/actions/workflows/unittests.yml)

# GeckoTerminal API

## RESTful Python client for GeckoTerminal DeFi and DeX aggregator

Wrapper around the [GeckoTerminal](https://www.geckoterminal.com) DeFi and DeX
aggregator operating across 90+ blockchains. This is an
unofficial wrapper and is currently in beta.
Please report any issues you find.

## Installation

```bash
pip install geckoterminal-api
```

## Usage

```python
from geckoterminal_api import GeckoTerminalAPI

gt = GeckoTerminalAPI()
```

```ipython
>>> gt.network_trending_pools(network="solana")
```

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

```ipython
>>> gt.network_new_pools(network="arbitrum")
```

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
