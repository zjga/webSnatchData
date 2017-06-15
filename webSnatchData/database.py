#-*- coding: utf-8 -*-
import re
import pymssql
import string
import urllib
import socket

def UpdateDatabaseEmail(url,Value1,Value2,Value3,Value4):
    con=pymssql.connect(host='192.168.1.252',user='netdata1',password='@@231abc',database='NetData')
    curA=con.cursor()
    InsertSql="Insert into NetData1(url,Value1,Value2,Value3,Value4) values('"+str(url)+"','"+Value1.replace("'","''")+"','"+Value2.replace("'","''")+"','"+Value3.replace("'","''")+"','"+Value4.replace("'","''")+"')"
    curA.execute(InsertSql)
    con.commit()
    con.close()

def main():
    #socket.setdefaulttimeout(8.0)
    UpdateDatabaseEmail('22url111','Test1111','Test1111','Test1111','Test1111')
    print ('Insert OK!!!')
    socket.setdefaulttimeout(8.0)
    
if __name__ == '__main__':
    main()
