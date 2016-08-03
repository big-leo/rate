#!/usr/bin/env python3.4
'''tools for get PrivatBank rate'''
import sys
import getopt
#import threading
from urllib.request import urlopen
import json


def using():
    '''help for using'''
    print('./rate.py --start "01.12.2014" --to "01.12.2015" --currency "USD" --rate "saleRate"')
    sys.exit(0)


def get_rate(date_rate, curr, in_rate):
    '''get data from url PrivatBank'''
    response = urlopen('https://api.privatbank.ua/p24api/exchange_rates?json&date=' + date_rate)
    data = response.read().decode()
    json_data = json.loads(data)
    for line in json_data['exchangeRate']:
        if line['currency'] == curr:
            rate = line[in_rate]
            break
    return rate


def opt_parse():
    '''parsing input options'''
    result = dict()
    param1 = 's:t:c:r:h'
    param2 = ['start=', 'to=', 'currency=', 'rate=', 'help']
    try:
        opts, args = getopt.getopt(sys.argv[1:], param1, param2)
    except getopt.GetoptError:
        using()
    print('opts: ', opts)
    print('args: ', args)
    opts = dict(opts)
    if '-h' in opts or '--help' in opts:
        using()
    return opts


if __name__ == '__main__':
    '''main loop'''
    opts = opt_parse()
    for
    print(get_rate(opts['--start'], opts['--currency'], opts['--rate']))
