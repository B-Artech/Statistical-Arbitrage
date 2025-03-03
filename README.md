# PAIRS TRADING STATISTICAL ARBITRAGE

Base on the paper study

(http://yats.free.fr/doc/cointegration-en.pdf)
(https://estudogeral.uc.pt/retrieve/275337/Dissertation_Ines_Fernandes.pdf)

## Table of Contents

- [PAIRS'S TRADING STATISTICAL ARBITRAGE](#pairss-trading-statistical-arbitrage)
  - [Table of Contents](#table-of-contents)
  - [Disclaimer](#disclaimer)
  - [Stage one - pair analysis framework](#stage-one---pair-analysis-framework)
  - [Stage two -  Backtest](#stage-two----backtest)
  - [Stage three - Live trading](#stage-three---live-trading)
  - [Stage four - Risk Monitor](#stage-four---risk-monitor)
  - [Stage five - Watch-list](#stage-five---watch-list)
  - [Improvement of the system](#improvement-of-the-system)
  - [Contributing](#Contributing)

## Disclaimer

This is for educational purposes only, do not run this in production !!!

## Stage one - pair analysis framework

The Idea behind this strategy came from many sources and research.
Thus I came up with full trading framework strategy broken down to several stages.

This methodology provides foundation for statistical arbitrage trading strategies identifying assets with significant mean-reverting properties.

Pair selection process:

Cointegration test using Engle-Granger test to determine whether two assets move together over time
Calculate correleation and dependency metrics between assets

  Person correlation
  
  Sperman Correlation
  
  Kendall's Tau ordinal association
  
Hedge Ratio using Ordinary Least Square regression

Half Life of mean reversion using Orstein-Uhlenbeck process

## Stage two -  Backtest

By performing a simple backtest, we can significantly refine the selection pairs, reducing the initial pool from +20000 pairs to only the mots statistically viable ones.
This process evaluates the historical performance of selected pairs using mean reverting strategy, testing entry and exits signal base on the z_score threshold.
The results helps identify pairs with the highest profitability potential, improving confidence before moving into live trading.

## Stage three - Live trading

Timeframe is 1 Day or 1 hour base on the volatility levels, usual when volatility drys out we can change timeframes to 1h.

Position size & leverage:
Positions size are determined using dollar terms base on the ATR measures of each asset in a trading pair.
Leverage are used in this strategy between 2-3x to reduce margin requirements.

Execution of live Trades:

Obtaining information about traded pairs from csv file.
Compute the spread and z_score to determine trade signal.
Opening long when spread is undervalued and showing reversal signals.
Opening short when spread is overvalued and showing reversal signals.
Ensuring that trades are only opened if there is no existing open position for the pair.
Save trade details for tracking and risk management.

## Stage four - Risk Monitor

Risk Monitor works as a separate bot to monitor account risk for drawdowns.

Risk parameter management:
Maximum daily risk threshold of -5% from the high water mark.
Account balance is measured every 60 seconds and tha daily threshold is restarting at the beginning of the day.
If the loss exceeds the threshold all positions are closed and trading is suspended for 24H.

## Stage five - Watch-list

Since we trade pairs it could be difficult to visual mach assets on trading platforms.
Therefore Watchlist is a system that can easily and quickly check each traded pair.

Watchlist is Running in the Browser:

Start server locally and run watchlist.py.
The app will automatically rearrange positions to always display nominator(Symbol we buy) in the first position.
This allow us to easily monitor the performance of the spread and keep an eye on the percentage variation (% Var).

## Improvement of the system

VOLATILITY

Trading  specific timeframe base volatility:
High volatility --> Higher Timeframe resolution ex 1d
Low volatility --> Lower Timeframe resolution ex 1h

ROLLING Z_SCORE vs STATIONARY SPREAD

Currently, out primary execution signal is base on a rolling z_score, with default lookback period of 21(this parameter can be adjusted).
Since finding truly stationary pairs is somewhat rare, the rolling z_score approach helps identify potential trading opportunities more frequently.

Although this system is designed for automation, some manual intervention is still required.
I highly recommend maintaining a separate file for tracing the most promising pairs for further analysis.

TRADING FROM WATCH-LIST

Before execution trades base on predefine signal parameters, trades should first be added to a watchlist for gatekeeping.
This allows for monitoring performance before making a final decision on execution.


## Contributing
Contributions are welcome! If you'd like to contribute to this project
