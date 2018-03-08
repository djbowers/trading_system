"""
This module contains all the code for interacting with mySQL database.

"""

def get_table(table_name):
    table_data = {}


def get_period_high(period):
    """
    get the highest price for the given period
    """


def read_db()
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
