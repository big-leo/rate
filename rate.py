#!/usr/bin/env python3.4
'''tools for get PrivatBank rate'''
import sys
import getopt
#import threading
from urllib.request import urlopen
import json
from datetime import datetime, timedelta


PB_CURRENCY = 'UAH,AUD,CAD,CZK,DKK,HUF,ILS,JPY,LVL,LTL,NOK,SKK,SEK,CHF,RUB,GBP,USD,BYR,EUR,GEL,PLZ'
PB_RATE = 'saleRate,purchaseRate'


def using():
    '''help for using'''
    print('--currency:\n%s\n--rate:\n%s' % (PB_CURRENCY, PB_RATE))
    print('./rate.py --start "01.12.2014" --to "01.12.2015" --currency "USD" --rate "saleRate"')
    sys.exit(0)


def validate_opt(start_date, end_date, curr, rate):
    '''validate input options'''
    try:
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        end_date = datetime.strptime(end_date, '%d.%m.%Y')
    except ValueError:
        using()
    if not curr in PB_CURRENCY.split(','):
        using()
    if not rate in PB_RATE.split(','):
        using()


def gen_days(start_date, end_date):
    '''generator for days'''
    next_date = start_date
    while not next_date > end_date:
        #print(next_date)
        yield next_date.strftime('%d.%m.%Y')
        next_date += timedelta(days=1)


def get_rate(date_rate, curr, in_rate):
    '''get data from url PrivatBank'''
    pburl = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    response = urlopen(pburl + date_rate)
    data = response.read().decode()
    json_data = json.loads(data)
    #print(json.dumps(json_data, indent=4))
    for line in json_data['exchangeRate']:
        if line['currency'] == curr:
            rate = line[in_rate]
            break
    #print(rate)
    return rate


def opt_parse():
    '''parsing input options'''
    result = dict()
    #param1 = 's:t:c:r:h'
    param1 = ''
    param2 = ['start=', 'to=', 'currency=', 'rate=', 'help']
    try:
        opts, args = getopt.getopt(sys.argv[1:], param1, param2)
    except getopt.GetoptError:
        using()
    #print('opts: ', opts)
    #print('args: ', args)
    opts = dict(opts)
    if '--help' in opts:
        using()
    return opts


if __name__ == '__main__':
    '''main loop'''
    opts = opt_parse()
    start_date = opts['--start']
    end_date = opts['--to']
    curr = opts['--currency']
    rate = opts['--rate']

    validate_opt(start_date, end_date, curr, rate)
    start_date = datetime.strptime(start_date, '%d.%m.%Y')
    end_date = datetime.strptime(end_date, '%d.%m.%Y')

    days = gen_days(start_date, end_date)
    rates = dict([((get_rate(d, curr, rate)), d) for d in days])
    max_rate = max(rates)
    max_date = rates[max_rate]
    max_date = datetime.strptime(max_date, '%d.%m.%Y')
    max_date = max_date.strftime('%d.%m.%y')
    print('Most expensive "%s" for %s was %s = %f' % (rate, curr, max_date, max_rate))
