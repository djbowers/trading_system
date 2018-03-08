import pandas as pd
# import pymysql
import mysql.connector
from mysql.connector import errorcode
import gdax_history
import sys




cnx = mysql.connector.connect(
                                user='justinj1515', password='P!o2i3u4y5t6r7e8w9q0',
                                # user='data_uploader', password='P1o2i3u4y5',
                                host="mydatabases.ck6y04wr4wru.us-east-2.rds.amazonaws.com",
                                database='test_1_db',
                                port='3306'
                                )

cursor = cnx.cursor()



table1_name = 'test_table1'
table2_name = 'test_table2'

time = '1803011246'
high = '15000'
low = '7000'
open_price = '13000'
close_price = '10000'




# ## ---------------------------------
# ##
# ##      query data from table
# ##
# ## _________________________________
#
#
#
# query = ("SELECT date, open_price, close_price, high, low FROM BTC_USD "
#          "WHERE date BETWEEN %s AND %s")
#
# start = '1803011246'
# end = '1803011250'
#
# ## Run Query
# cursor.execute(query, (start, end))
#
#
# ## Go through Query Results
# for (period, open_p, close_p, high, low) in cursor:
#   print("on {} |OPEN: {} |CLOSE: {} -- |HIGH: {} |LOW: {}".format(
#     period, open_p, close_p, high, low))
# #












## ---------------------------------
##
##      add data to table
##
## _________________________________



def add_row(time, close_price, open_price, high, low):
    add_to_table1 = ("INSERT INTO BTC_USD "
                   "(date, close_price, open_price, high, low) "
                  "VALUES (%(date)s, %(close_price)s, %(open_price)s, %(high)s, %(low)s)")
    # Row 1 Entry
    row1 = {
        'date': time,
        'close_price':close_price,
        'high': high,
        'low': low,
        'open_price': open_price,
        }


    ## add to table 1
    cursor.execute(add_to_table1, row1)

    # Make sure data is committed to the database
    cnx.commit()



def get_24_hour_high():
    ## execute Query to get 24 hour high

def get_24_hour_low():
    ## execute Query to get 24 hour high



def algorithm(current_time):

    ## see if now is test_period high

    test_period = 24

    ## Query db to return MAX(test_period) & MIN(test_period)

    high = get_24get_24_hour_high()
    low = get_24_hour_low()

    if high[0] == current_time:
        results = [True, 'Long']

    if low[0] == current_time:
        results = [True, 'Short']

    return results


    ## if result == now, buy!




    ## Query db to return the last 14 days of information.
    ## format days from db as 24 hours periods
    ## use MIN() & MAX() query's to get daily high and lows


    ## get atr

    # piece_start_datetime = datetime.datetime.strptime(str(), '%y%m%d%H%M')



def main():
    # btc_history = gdax_history.main()
    btc_history = ## get from SQL
    for m in btc_history:

        time = m['time']
        close_price = m['close']
        open_price = m['open']
        high = m['high']
        low = m['low']


        ## returns [(True, False), (long, short)]
        in_or_out = algorithm(time)

        # print(m)
        # sys.exit()







if __name__ == '__main__':
    main()



# # ---------------------------------
# #
# #      add table to database
# #
# # _________________________________
#
#
# DB_NAME = 'btc_usd'
#
# TABLES = {}
# TABLES['btc_usd'] = (
#     "CREATE TABLE `btc_usd` ("
#     "  `date` int(11) NOT NULL,"
#     "  `high` varchar(14) NOT NULL,"
#     "  `low` varchar(14) NOT NULL,"
#     "  `open` varchar(14) NOT NULL,"
#     "  `close` varchar(14) NOT NULL,"
#     "  PRIMARY KEY (`date`)"
#     ") ENGINE=InnoDB")
#
# TABLES['test_table2'] = (
#     "CREATE TABLE `test_table2` ("
#     "  `date` int(11) NOT NULL,"
#     "  `high` varchar(14) NOT NULL,"
#     "  `low` varchar(14) NOT NULL,"
#     "  `open` varchar(14) NOT NULL,"
#     "  `close` varchar(14) NOT NULL,"
#     "  PRIMARY KEY (`date`)"
#     ") ENGINE=InnoDB")
#
# for name, ddl in TABLES.items():
#     try:
#         print("Creating table {}: ".format(name), end='')
#         cursor.execute(ddl)
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("already exists.")
#         else:
#             print(err.msg)
#     else:
#         print("OK")
#
# cursor.close()
#
# cnx.close()
