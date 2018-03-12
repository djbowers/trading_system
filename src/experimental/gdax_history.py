import os
import time
import subprocess
from subprocess import Popen
from subprocess import check_output
import shutil
import glob
import base64
import mimetypes
import json
import email
import smtplib
import sys
import datetime
import urllib.request
import simplejson
import locale
import time
import gdax, time
import pandas as pd



def get_history(start, end):
    """
    inputs are dates as strings
    formatted like "YYMMDDHHMM"
    note: HH = 24-hour periods

    Returns a dictionary of data from gdax. Max frames of 50
    """
    print('history start')
    print(start)
    print(end)


    product = "{}-{}".format("BTC", "USD")
    publicClient = gdax.PublicClient()

    ## unit is granulatrity (by the second)
    unit = 3600


    end = datetime.datetime.strptime(end, '%y%m%d%H%M')
    start = datetime.datetime.strptime(start, '%y%m%d%H%M')

    hist = publicClient.get_product_historic_rates(
                product,
                start=start.isoformat(),
                end=end.isoformat(),
                granularity=unit)


    if len(hist) == 1:
        for r in range(1, 10, 1):
            time.sleep(2)
            hist = publicClient.get_product_historic_rates(
                        product,
                        start=start.isoformat(),
                        end=end.isoformat(),
                        granularity=unit)
            if len(hist) > 1:
                break

    return hist
def add_to_dict(history_dict, history_slice):
    ## add the data in each slice of history to a dict


    if len(history_slice) == 1:
        print(history_slice)
        # time.sleep(1)

    ## look through desired
    for period in history_slice:
        # print('Period-----')
        # print(period)
        readable_date = time.ctime(period[0])


        period_datetime = datetime.datetime.strptime(readable_date, "%a %b %d %H:%M:%S %Y")
        period_string = period_datetime.strftime('%y%m%d%H%M')


        ## add info to dict
        history_dict.append({'time': str(period_string),
                                    'low': int(period[1]),
                                    'high': str(period[2]),
                                    'open': str(period[3]),
                                    'close': str(period[4]),
                                    'volume': str(period[5])})

        # ## add info to dict
        # history_dict[period_string] = {'time': period_string,
        #                             'low': period[1],
        #                             'high': period[2],
        #                             'open': period[3],
        #                             'close': period[4],
        #                             'volume': period[5]}
    return history_dict



def get_btc_price_history(start, end):
    history_dict = []
    # for i in range(1, 5, 1):

    if (end - start) > 121200:
        print('more than 500!!')

        diff = end-start
        full_chunks = int(diff/121200)
        print(full_chunks)
        piece_start_datetime = datetime.datetime.strptime(str(start), '%y%m%d%H%M')
        piece_end_datetime = piece_start_datetime + datetime.timedelta(minutes = 18000)


        # 350 minute  chunks
        for l in range(1,full_chunks,1):
            print(str(piece_end_datetime.strftime('%y%m%d%H%M')))

            history_slice = get_history(str(piece_start_datetime.strftime('%y%m%d%H%M')), str(piece_end_datetime.strftime('%y%m%d%H%M')))

            history_dict = add_to_dict(history_dict, history_slice)
            piece_start_datetime = piece_start_datetime + datetime.timedelta(minutes = 18000)
            piece_end_datetime = piece_end_datetime + datetime.timedelta(minutes = 18000)

        # piece_end = int(piece_end_datetime.strftime('%y%m%d%H%M'))

        # left_over = end - piece_end
        # piece_start += left_over
        # piece_end += left_over

        history_slice = get_history(str(piece_start_datetime.strftime('%y%m%d%H%M')), str(piece_end_datetime.strftime('%y%m%d%H%M')))
        history_dict = add_to_dict(history_dict, history_slice)

    else:
        history_slice = get_history(str(start), str(end))
        history_dict = add_to_dict(history_dict, history_slice)


        # time.sleep(1)

    return history_dict



    # x = 0
    # ## history_dict is formatted dict ready to upload to SQL db
    # for p in sorted(history_dict):
    #
    #     print(str(p)+' low: '+str(history_dict[p]['low'])+'  high: '+str(history_dict[p]['high'])+'   open: '+str(history_dict[p]['open'])+'   close: '+str(history_dict[p]['close'])+'  vol: '+str(history_dict[p]['volume']))
    #
    #
    #     x+=1
    #     if x == 20:
    #         sys.exit()




# def lookin_to_buy(data):
# 	'''
# 	- for backtesting, use SQL_db with different range
# 	than normal (today = Jan 1 2015 12:00 am).
# 	- no orders will actually be placed
# 	- log_activity will reset on demand
#
#
#     ## First get last 14 day
#
#     ## get
#
# 	'''
    # atr_period_days_tune = 14






def main():
    ## get historic price of btc

    ## date format
    ##           YYMMDDHHMM
    gdax_start = 1801130101
    gdax_end =   1802130101

    # start = 1802150101
    # end =   1802271301
    #
    # print(end-start)
    # sys.exit()
    #
    #
    # product = "{}-{}".format("BTC", "USD")
    # publicClient = gdax.PublicClient()
    #
    # ## unit is granulatrity (by the second)
    # unit = 3600
    #
    #
    # end = datetime.datetime.strptime(str(end), '%y%m%d%H%M')
    # start = datetime.datetime.strptime(str(start), '%y%m%d%H%M')
    #
    # hist = publicClient.get_product_historic_rates(
    #             product,
    #             start=start.isoformat(),
    #             end=end.isoformat(),
    #             granularity=unit)
    #
    # print(len(hist))
    # sys.exit()

    ## 1st query
    # gdax_start = 1802270501
    # gdax_end =   1802281001

    btc_history = get_btc_price_history(gdax_start, gdax_end)

    return btc_history
    #
    # for i in btc_history:
    #     print(i)
    #     break
    # # today =
    #
    #
    # df = pd.DataFrame(btc_history, columns=['time', 'low', 'high', 'open','close','volume' ])
    # df.set_index('time', inplace=True)
    #
    # print(df)

    # for i in btc_history:
    #     print(i)
    #     print(btc_history[0])
    #     break

if __name__ == '__main__':
    main()







## -----------------------------------
##
##      various gdax functions
##
## ------------------------------------
# h1 = bitcoinaverage.restful_client.Restful_client()

# restful_client.history_global
#
# sys.exit()
#
# public_client = gdax.PublicClient()
#
#
# public_client.get_products()
# # Get the order book at the default level.
# public_client.get_product_order_book('BTC-USD')
# # Get the order book at a specific level.
# public_client.get_product_order_book('BTC-USD', level=1)
# # Get the product ticker for a specific product.
# ticker = public_client.get_product_ticker(product_id='BTC-USD')
# # Get the product trades for a specific product.
# public_client.get_product_trades(product_id='ETH-USD')
# # Get historic rates
# history_db = public_client.get_product_historic_rates('BTC-USD')
# # To include other parameters, see function docstring:
# public_client.get_product_historic_rates('ETH-USD', granularity=3000)
# # Get 24 hours stats
# public_client.get_product_24hr_stats('ETH-USD')
# # Get currencies
# public_client.get_currencies()
# # Get time
# public_client.get_time()
#
# # def datetime_to_iso8601(date):
# #     return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
# #       year=date.year,
# #       month=date.month,
# #       day=date.day,
# #       hour=date.hour,
# #       minute=date.minute,
# #       second=date.second)
#
# #
# # db = datetime_to_iso8601(datetime(2015, 1, 1),datetime(2016, 1, 1), 60 )
# # db = datetime_to_iso8601(datetime(2015, 1, 1))
# print('done')
#
# history_db = public_client.get_product_historic_rates('BTC-USD')
#
# # print(history_db)
#
# for i in history_db:
#     print(i)

#
#
#
#
#
#
# class GDAX(object):
#     def __init__(self, pair):
#         self.pair = pair
#         self.uri = 'https://api.gdax.com/products/{pair}/candles'.format(pair=self.pair)
#
#     def fetch(self, start, end, granularity):
#         data = []
#           # We will fetch the candle data in windows of maximum 100 items.
#         delta = timedelta(minutes=granularity * 100)
#
#         slice_start = start
#         while slice_start != end:
#             slice_end = min(slice_start + delta, end)
#             data += self.request_slice(slice_start, slice_end, granularity)
#             slice_start = slice_end
#
#           # I prefer working with some sort of a structured data, instead of
#           # plain arrays.
#         data_frame = pandas.DataFrame(data=data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
#         data_frame.set_index('time', inplace=True)
#         return data_frame
#
#     def request_slice(self, start, end, granularity):
#           # Allow 3 retries (we might get rate limited).
#         retries = 3
#         for retry_count in xrange(0, retries):
#             # From https://docs.gdax.com/#get-historic-rates the response is in the format:
#             # [[time, low, high, open, close, volume], ...]
#             response = requests.get(self.uri, {
#                   'start': GDAX.__date_to_iso8601(start),
#                   'end': GDAX.__date_to_iso8601(end),
#                   'granularity': granularity * 60  # GDAX API granularity is in seconds.
#                 })
#
#         if response.status_code != 200 or not len(response.json()):
#             if retry_count + 1 == retries:
#                 raise Exception('Failed to get exchange data for ({}, {})!'.format(start, end))
#             else:
#                     # Exponential back-off.
#                 sleep(1.5 ** retry_count)
#         else:
#                   # Sort the historic rates (in ascending order) based on the timestamp.
#             result = sorted(response.json(), key=lambda x: x[0])
#             return result
#

#
#
# data_frame = GDAX('BTC-USD').fetch(datetime(2017, 6, 1), datetime(2017, 8, 1), 60)
#
# print(data_frame)







#
# last_price = ''
#
# for i in range(1,100):
#
#
#     ticker = public_client.get_product_ticker(product_id='BTC-USD')
#     price=ticker['price']
#
#     if last_price == price:
#         continue
#
#     print(ticker['price'])
#     last_price=price
#
#     time.sleep(.1)



#
# ## CONNECT TO WEB SOCKET
# # Paramaters are optional
#
#
#
#
#
# class myWebsocketClient(gdax.WebsocketClient):
#     def on_open(self):
#         self.url = "wss://ws-feed.gdax.com/"
#         # self.products = ["LTC-USD", "BTC-USD"]
#         self.products = ["BTC-USD"]
#         self.message_count = 0
#         print("Lets count the messages!")
#     def on_message(self, msg):
#         self.message_count += 1
#         print(msg)
#         if 'price' in msg and 'type' in msg:
#             print ("Message type:", msg["type"],
#                    "\t@ {:.3f}".format(float(msg["price"])))
#     def on_close(self):
#         print("-- Goodbye! --")
#
# wsClient = myWebsocketClient()
# wsClient.start()
# print(wsClient.url, wsClient.products)
# while (wsClient.message_count < 20):
#
#     print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
#     time.sleep(1)
# wsClient.close()
#

# # All Auto Bill vendors and amounts
# url = "https://api-public.sandbox.gdax.com"
# req = urllib.request.urlopen(url)
# gdax_api = simplejson.load(req)

# print(public_client.get_product_historic_rates('ETH-USD'))



## ----------------------------------------
## maybe bitcoinaverage or other for of data

# from bitcoinaverage import history




#
#
#
# import hashlib
# import hmac
# import requests
# import time
#
# secret_key = 'Yjg1OWZjMzFmM2Q5NGUxZjgyM2FiMWJmMGIwMTM5MDY1ZDgzOWQwYWQ1YTY0NzhjOWNlOGNjYWYxMzgwMGIyNw'
# public_key = 'ZjQyZmQxM2NkOGQ4NGMxZDg2NmZlOTlmNWM2ZmE1OTY'
# timestamp = int(time.time())
# payload = '{}.{}'.format(timestamp, public_key)
# hex_hash = hmac.new(secret_key.encode(), msg=payload.encode(), digestmod=hashlib.sha256).hexdigest()
# signature = '{}.{}'.format(payload, hex_hash)
#
# # symbol_set = 'global'

#
# # url = 'https://apiv2.bitcoinaverage.com/indices/{symbol_set}/history/{symbol}?period={period}&format={format}'
# url = 'https://apiv2.bitcoinaverage.com/indices/global/history/BTCUSD?period=daily&format=json'
# # url = 'https://apiv2.bitcoinaverage.com/indices/global/ticker/BTCUSD'
# headers = {'X-Signature': signature}
# result = requests.get(url=url, headers=headers)
#
# history_api_results = result.json()
#
# for i in history_api_results:
#     print(i)
# # print(result.json())
