import pandas as pd
# import pymysql
import mysql.connector
from mysql.connector import errorcode




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



def
## ---------------------------------
##
##      query data from table
##
## _________________________________



query = ("SELECT date, open_price, close_price, high, low FROM BTC_USD "
         "WHERE date BETWEEN %s AND %s")

start = '1803011246'
end = '1803011250'

## Run Query
cursor.execute(query, (start, end))


## Go through Query Results
for (period, open_p, close_p, high, low) in cursor:
  print("on {} |OPEN: {} |CLOSE: {} -- |HIGH: {} |LOW: {}".format(
    period, open_p, close_p, high, low))







# ## ---------------------------------
# ##
# ##      add data to table
# ##
# ## _________________________________
#
#
#
# def add_row()
#
# add_to_table1 = ("INSERT INTO "+table1_name+" "
#                "(date, high, low, open, close) "
#               "VALUES (%(date)s, %(high)s, %(low)s, %(open)s, %(close)s)")
#
# add_to_table2 = ("INSERT INTO "+table2_name+" "
#               "(date, high, low, open, close) "
#               "VALUES (%(date)s, %(high)s, %(low)s, %(open)s, %(close)s)")
#
#
#
# # Row 1 Entry
# row1 = {
#   'date': time,
#   'high': high,
#   'low': low,
#   'open': open_price,
#   'close':close_price
# }
#
# # Row 2 Entry
# row2 = {
#   'date': time,
#   'high': high,
#   'low': low,
#   'open': open_price,
#   'close':close_price
# }
#
#
#
# ## add to table 1
# cursor.execute(add_to_table1, row1)
#
#
# ## add to table 2
# cursor.execute(add_to_table2, row2)
#
#
# # Make sure data is committed to the database
# cnx.commit()





## ---------------------------------
##
##      add table to database
##
## _________________________________


# DB_NAME = 'test_1_db'
#
# TABLES = {}
# TABLES['test_table1'] = (
#     "CREATE TABLE `test_table1` ("
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

cursor.close()

cnx.close()
