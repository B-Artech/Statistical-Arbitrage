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

This is for educational purposes only.

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

By performing a simple backtest, we can significantly refine the selection pairs, reducing the initial pool from +20000 pairs to only the most statistically viable ones.

This process evaluates the historical performance of selected pairs using mean reverting strategy, testing entry and exits signal base on the z_score threshold.

The results helps identify pairs with the highest profitability potential, improving confidence before moving into live trading.

## Stage three - Live trading

Timeframe is 1 Day or 1 hour base on the volatility levels, usual when volatility dries out we can change timeframes to 1h.

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

 System Objective
 
The system will continuously scan for trading pairs that reach a predefined Z-score threshold. Instead of opening a live trade immediately,
these pairs will be added to a watchlist for further observation.

The goal is to monitor their spread movement and performance over time before committing to a live trade.

Step 1: Scanning for Potential Trade Pairs
The system scans the market in real-time for pairs that meet specific criteria.

The primary condition for adding a pair to the watchlist is that its Z-score surpasses a predefined threshold (e.g., ±2.0).

Once a pair meets this threshold, it is added to the watchlist instead of executing a trade immediately.

Step 2: Adding to the Watchlist & Storing Key Information
Once a pair enters the watchlist, the system records essential trade data at that moment, including:

Entry Prices: The prices of both assets in the pair when it was added to the watchlist.

Spread Entry Value: The spread between the two assets at the time of watchlist entry.

Z-Score (at Entry): The statistical measure indicating deviation from the mean when added.

Other Relevant Data: Correlation strength, volatility, and any additional market conditions.

Step 3: Monitoring Performance Over Time
The system will track the spread movement and key indicators at regular intervals (e.g., every 1 hour).

Each update will show how the pair has performed since being added to the watchlist.

Performance will be measured based on:
Change in spread value (percentage movement).

Consistency of spread mean reversion (is the spread tightening or widening?).

Trend of the Z-score (is it moving toward 0 or becoming more extreme?).


Step 4: Identifying Consistent Positive Performance
The system analyzes the observed performance over multiple time intervals.

Pairs that show stable or favorable movement toward mean reversion will be flagged as potential trade candidates.

Pairs that show erratic or worsening spread movement may be removed from the watchlist.

Step 5: Trade Execution Decision
If the pair consistently shows favorable movement, it qualifies for a potential live trade.

The trader (or automated system) can then decide to open a live trade based on predefined entry conditions.

If performance remains inconsistent, the pair is either removed from the watchlist or monitored further.


3 Key Benefits of This Approach

✔ Avoids Premature Entries: Ensures that only strong candidates are traded, reducing false signals.

✔ Data-Driven Trade Selection: Observes pairs before committing capital, leading to better trade quality.

✔ Performance-Based Filtering: Helps eliminate weak opportunities early.

✔ Flexible Decision-Making: Allows both manual and automated execution based on proven performance.


Contributions are welcome! If you'd like to contribute to this project


