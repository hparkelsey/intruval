from time import sleep

import pygsheets
from pandas_datareader import data

gc = pygsheets.authorize(service_file='creds.json')
sh = gc.open('Intruval')

rangeBegin = 2
rangeEnd = 101

while True:

    print("In progress")

    Tickers = sh[0].get_values('A' + str(rangeBegin), 'A' + str(rangeEnd))

    prices = []
    eps = []

    x = 1

    for tickname in Tickers:
        tickers = [tickname]
        prices.append([float(data.get_quote_yahoo(tickname)['price'])])
        try:
            eps.append([float(data.get_quote_yahoo(tickname)['forwardEps'])])
        except KeyError:
            try:
                eps.append([float(data.get_quote_yahoo(tickname)['currentEps'])])
            except KeyError:
                try:
                    eps.append([float(data.get_quote_yahoo(tickname)['epsTrailingTwelveMonths'])])
                except KeyError:
                    print(str(tickname))
                    eps.append([float(sh[0].get_col(3)[x])])
        x += 1

    sh[0].update_values('B' + str(rangeBegin) + ':B' + str(rangeEnd), prices)
    sh[0].update_values('C' + str(rangeBegin) + ':C' + str(rangeEnd), eps)

    print("Done!")

    sleep(10)