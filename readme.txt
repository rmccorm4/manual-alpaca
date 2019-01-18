Manual_Alpaca.py
by Matt Haines
http://www.throwinggoodmoney.com

In a folder called "manual_alpaca" you should have:

manual_alpaca.py
keys.csv
live_keys.csv
man_alp_help.txt
readme.txt

You need to install these packages:

import alpaca_trade_api as tradeapi
import os
import sys
from pandas import read_csv



This only works with the alpaca.markets brokerage and python 3.x

You need both a live key set and a paper key set for full functionality.

Replace the text in the csv files with your public and private keys.

Help file should explain the rest!

Wait...why have a manual trading script when the whole point of 
Alpaca is to trade your bots and algos?

What if your algo fails and you're away from the server?

What if you're still testing your algo but want to trade manually?

There ya go.
