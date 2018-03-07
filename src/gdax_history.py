import os
import time
import subprocess
from subprocess import Popen
from subprocess import check_output
import shutil

#from __future__ import print_function
import glob
import base64
import mimetypes
import json
import email
import smtplib
import sys

sys.path.append('/Users/JustinJacob/Desktop/Splash/ProgrammingDev/Projects/AJmStatus/Jobs')
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages')
import datetime
import urllib.request
import simplejson
import locale
import gdax, time
# from pymongo import MongoClient




public_client = gdax.PublicClient()


public_client.get_products()
# Get the order book at the default level.
public_client.get_product_order_book('BTC-USD')
# Get the order book at a specific level.
public_client.get_product_order_book('BTC-USD', level=1)
# Get the product ticker for a specific product.
ticker = public_client.get_product_ticker(product_id='BTC-USD')
# Get the product trades for a specific product.
public_client.get_product_trades(product_id='ETH-USD')
# Get historic rates
history_db = public_client.get_product_historic_rates('BTC-USD')
# To include other parameters, see function docstring:
public_client.get_product_historic_rates('ETH-USD', granularity=3000)
# Get 24 hours stats
public_client.get_product_24hr_stats('ETH-USD')
# Get currencies
public_client.get_currencies()
# Get time
public_client.get_time()

# def datetime_to_iso8601(date):
#     return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
#       year=date.year,
#       month=date.month,
#       day=date.day,
#       hour=date.hour,
#       minute=date.minute,
#       second=date.second)

#
# # hey()
# # db = datetime_to_iso8601(datetime(2015, 1, 1),datetime(2016, 1, 1), 60 )
# db = datetime_to_iso8601(datetime(2015, 1, 1))
print('done')
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
