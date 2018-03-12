import pandas as pd
# import pymysql
import mysql.connector
from mysql.connector import errorcode
import gdax_history
import sys
import datetime
import operator








# table1_name = 'test_table1'
# table2_name = 'test_table2'
#
# time = '1803011246'
# high = '15000'
# low = '7000'
# open_price = '13000'
# close_price = '10000'




## ---------------------------------
##
##      query data from table
##
## _________________________________

def get_btc_history_from_db(end):

    cnx = mysql.connector.connect(
                                    user='justinj1515', password='P!o2i3u4y5t6r7e8w9q0',
                                    # user='data_uploader', password='P1o2i3u4y5',
                                    host="mydatabases.ck6y04wr4wru.us-east-2.rds.amazonaws.com",
                                    database='test_1_db',
                                    port='3306'
                                    )

    cursor = cnx.cursor()

    end_datetime = datetime.datetime.strptime(str(end), '%y%m%d%H%M')
    start_datetime = end_datetime - datetime.timedelta(minutes = 43200)
    start = start_datetime.strftime('%y%m%d%H%M')

    query = ("SELECT time, close_price, open_price, MAX(high), low FROM BTC_USD "
             "WHERE time BETWEEN %s AND %s")

    ## Run Query
    cursor.execute(query, (start, end))

    history_dict = {}

    # print(end)

    ## Go through Query Results
    for (period, close_price, open_price, high, low) in cursor:
        # print("on {} |OPEN: {} |CLOSE: {} -- |HIGH: {} |LOW: {}".format(
        #         period, close_price, open_price, high, low))
        history_dict[period] = {
                'close_price':close_price,
                'open_price': open_price,
                'high': high,
                'low': low}

    return history_dict









# ## ---------------------------------
# ##
# ##      add data to table
# ##
# ## _________________________________
#
#
#
# def add_row(time, close_price, open_price, high, low):
#     add_to_table1 = ("INSERT INTO BTC_USD "
#                    "(time, close_price, open_price, high, low) "
#                   "VALUES (%(time)s, %(close_price)s, %(open_price)s, %(high)s, %(low)s)")
#     # Row 1 Entry
#     row1 = {
#         'time': time,
#         'close_price':close_price,
#         'open_price': open_price,
#         'high': high,
#         'low': low,
#         }
#
#
#     ## add to table 1
#     cursor.execute(add_to_table1, row1)
#
#     # Make sure data is committed to the database
#     cnx.commit()





def get_period_high(end, period):
    ## execute Query to get 24 hour high

    cnx = mysql.connector.connect(
                                    user='justinj1515', password='P!o2i3u4y5t6r7e8w9q0',
                                    # user='data_uploader', password='P1o2i3u4y5',
                                    host="mydatabases.ck6y04wr4wru.us-east-2.rds.amazonaws.com",
                                    database='test_1_db',
                                    port='3306'
                                    )

    cursor = cnx.cursor()

    requested_period = period*60

    end_datetime = datetime.datetime.strptime(str(end), '%y%m%d%H%M')
    start_datetime = end_datetime - datetime.timedelta(minutes = requested_period)
    start = start_datetime.strftime('%y%m%d%H%M')

    query = ("SELECT time, close_price, open_price, MAX(high), low FROM BTC_USD "
             "WHERE time BETWEEN %s AND %s")

    ## Run Query
    cursor.execute(query, (start, end))

    history_dict = {}

    # print(end)

    ## Go through Query Results
    for (period, close_price, open_price, high, low) in cursor:
        # print("on {} |OPEN: {} |CLOSE: {} -- |HIGH: {} |LOW: {}".format(
        #         period, close_price, open_price, high, low))
        history_dict['result'] = { 'time':period,
                'close_price':close_price,
                'open_price': open_price,
                'high': high,
                'low': low}

    return history_dict





def get_period_low(end, period):
    ## execute Query to get 24 hour low

    cnx = mysql.connector.connect(
                                    user='justinj1515', password='P!o2i3u4y5t6r7e8w9q0',
                                    # user='data_uploader', password='P1o2i3u4y5',
                                    host="mydatabases.ck6y04wr4wru.us-east-2.rds.amazonaws.com",
                                    database='test_1_db',
                                    port='3306'
                                    )

    cursor = cnx.cursor()

    requested_period = period*60

    end_datetime = datetime.datetime.strptime(str(end), '%y%m%d%H%M')
    start_datetime = end_datetime - datetime.timedelta(minutes = requested_period)
    start = start_datetime.strftime('%y%m%d%H%M')

    query = ("SELECT time, close_price, open_price, high, MIN(low) FROM test_table_1 "
             "WHERE time BETWEEN %s AND %s")


    print('------START--------')
    print(start)
    print(end)
    ## Run Query
    cursor.execute(query, (start, end))

    history_dict = {}

    # print(end)

    ## Go through Query Results
    for (period, close_price, open_price, high, low) in cursor:
        # print("on {} |OPEN: {} |CLOSE: {} -- |HIGH: {} |LOW: {}".format(
        #         period, close_price, open_price, high, low))
        history_dict['result'] = { 'time':period,
                'close_price':close_price,
                'open_price': open_price,
                'high': high,
                'low': low}

    return history_dict


    # max(stats.items(), key=operator.itemgetter(1))[0]



# def pyramid_buy(data):
#     ## Look for N movements beyond entry triggers




def algorithm(current_time):

    ## if no triggers change this, it will return FALSE
    results = [False, '']

    ## Query DB for last 30 days of info ending at current_time.
    db_history = get_btc_history_from_db(current_time)

    ## window to test for breakouts
    test_period = 720

    ## Query db to return MAX(test_period)
    high = get_period_high(current_time, test_period)

    ## Query db to return MIN(test_period)
    low = get_period_low(current_time, test_period)

    ## Look for Pyramid Buy triggers
    # pyramind_buy = pyramid_buy(db_history)

    ## format results
    print('low')
    print(low['result'])
    print(current_time)
    if high['result']['time'] == current_time:
        ## breakout has occured, now == test_period high
        results = [True, 'Long']

    if low['result']['time'] == current_time:
        ## breakout has occured, now == test_period low
        results = [True, 'Short']

    return results


# def get_stops(entry_price):
    ##calculate stop prices for entry position

    ## get 2N stop value
    ## get 12 hour low value
    # return stop_list

# def place_order(position, stops):
    ## place order on exchange

def lookin_to_buy(current_time):
    position = algorithm(current_time)
    if position[0] == True:
        stops = get_stops(entry_price)
        place_order(position, stops)
        record(position, stops)

def position_manager():
    active_positions_api = get_active_positions_api()
    active_positions_db = get_active_positions_db()


    ## Compare two results to see which positions have exited by stops
    exited_positions = diff_of_both()

    record(exited_positions)

    ## look to see if current price is high enough to move all open stops


def main():

    ##             date format:
    ##             YYMMDDHHMM
    current_time = 1803020100


    # btc_history = gdax_history.main()

    ## query db for data in relevant time frame
    btc_history = get_btc_history_from_db(current_time)

    ## returns [(True, False), (long, short)]
    in_or_out = algorithm(current_time)

    print(in_or_out)


if __name__ == '__main__':
    main()
