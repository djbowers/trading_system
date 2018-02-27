import pandas as pd
import pymysql
import mysql

host="mydatabases.ck6y04wr4wru.us-east-2.rds.amazonaws.com"
port=3306
dbname="test_1_db"
user="justinj1515"
password="P1o2i3u4y5"

conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)



cursor = conn.cursor()

# cursor.execute ("select * from test_1_db")


# db.query("""SELECT spam, eggs, sausage FROM breakfast
         # WHERE price < 5""")


# PROMPT> mysql -h mydatabases.ck6y04wr4wru.us-east-2.rds.amazonaws.com -P 3306 -u <mymasteruser>> -p


#
# rds-launch-wizard-1
#
# aws rds authorize-db-security-group-ingress \
#     --db-security-group-name default \
#     --cidrip 192.168.0.0/24

#
# import boto3
# rds = boto3.client('rds')
# try:
#     dbs = rds.describe_db_instances()
#     for db in dbs['mydatabases']:
#         print("%s@%s:%s %s") % (db['MasterUsername'], db['Endpoint']['Address'], db['Endpoint']['Port'], db['DBInstanceStatus'])
# except Exception as e:
#     print(e)
