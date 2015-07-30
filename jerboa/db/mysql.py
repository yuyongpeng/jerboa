#encoding=utf8
'''
Created on 2015年7月30日

@author: admin
'''
import datetime

import mysql.connector



cnx = mysql.connector.connect(user='root', password='modernmedia',
                         host='127.0.0.1', database='slate_editor')
cursor = cnx.cursor()
query = ("SELECT first_name, last_name, hire_date FROM employees "
         "WHERE hire_date BETWEEN %s AND %s")
hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)
cursor.execute(query, (hire_start, hire_end))
cursor.fetchall()
for (first_name, last_name, hire_date) in cursor:
    print("{}, {} was hired on {:%d %b %Y}".format(last_name, first_name, hire_date))
cursor.close()
cnx.close()




class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        