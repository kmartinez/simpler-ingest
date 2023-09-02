from peewee import *
from credentials import *

#CONFIGURE DATABASE HERE
#db = SqliteDatabase('data.db')
db = MySQLDatabase('icetracker', user=USERNAME, password=PASSWORD, host='localhost', port=3306)