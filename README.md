# backtest
A framework to implement backtest research for trading strategies, especially for CTA strategies.

### Introduction
The project has shown four main steps in backtest research which containes getting data, calculating signal, 
simulating and evaluating performance.

- getting data mainly done in _getdata.py_ modual
- calculating signals mainly done in _ema.py_ modual as an example
- simulating mainly done in _signaltrade.py_ modual, which is also called your strategy
- evaluating performance mainly done in _tradestats.py_ modual, which calculate some indicators to 
evaluate your strategy backtest performance

### Environment
- python 3.0 or above
- pandas/numpy/plotly

### Execution
- python main.py

### How to use in real world
To make the whole project can be executed correctly, I have provided a data file in my project and rewritten 
the _getdata.py_ modual. In real world, if you want to use this framework to implement backtest research, you 
need to finish following operatons.
- rewrite _getdata.py_ to get data from your own data source
- rewrite and rename _ema.py_ to calculate your own signals
- rewrite _signaltrade.py_ to build your own strategy
