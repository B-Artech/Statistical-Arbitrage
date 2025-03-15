# PAIRS TRADING STATISTICAL ARBITRAGE FOR CRYPTOCURRENCY MARKETS

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

## Disclaimer

**This is for educational purposes only. Although the code works right out of the box, use it only in a testing environment.**

## Stage one - pair analysis framework


This methodology provides foundation for statistical arbitrage trading strategies identifying assets with significant mean-reverting properties.

Pair selection process:

Cointegration test using Engle-Granger test to determine whether two assets move together over time
Calculate correleation and dependency metrics between assets
  
  Person correlation
  
  Sperman Correlation
  
  Kendall's Tau ordinal association
  
Hedge Ratio using Ordinary Least Square regression (While OLS provides a static hedge ratio, the Kalman Filter offers a dynamic approach that allows the hedge ratio to evolve over time.
Logarithmic returns are often preferred with Kalman approach)

Half Life of mean reversion using Orstein-Uhlenbeck process

## Stage two -  Backtest

By performing a simple backtest, we can significantly refine the selection pairs, reducing the initial pool from +20000 pairs to only the most statistically viable ones.

This process evaluates the historical performance of selected pairs using mean reverting strategy, testing entry and exits signal base on the z_score threshold.

The results helps identify pairs with the highest profitability potential, improving confidence before moving into live trading.

## Stage three - Live trading

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
