#!/usr/bin/env python
#coding=utf-8
 
import time
import sys
import os
import MySQLdb

def now() :
        #return str('2011-01-31 00:00:00')
        return str( time.strftime( '%Y-%m-%d %H:%M:%S' , time.localtime() ) )

def log( qps,tps , logs ) :
        f = file( logs , 'a' , 0 )
        f.write( now() + '  ' + str(qps) +'  '+ str(tps) + '\n' )
        f.close()

def main() :
    logs = "/root/yangql/mysqlqps_tps.xls"
 
    try:
      conn = MySQLdb.connect(host='172.xx.xxx.xxx',port=3306,user='idbuser',passwd='passwd', charset='utf8')
    except  MySQLdb.ERROR,e:
      print "Error %d:%s"%(e.args[0],e.args[1])
      exit(1)

    conn.autocommit(True)
    cursor=conn.cursor()
    diff = 1
    mystat1={}
    mystat2={}

    sql = "show global status where Variable_name in ('com_delete','com_insert','com_select','com_update')"
    #sql = "show global status where Variable_name in ('Com_commit','com_delete','com_insert','Com_rollback','com_select','com_update','Questions');"
    while True:
       try :
          cursor.execute(sql)
          results1 = cursor.fetchall()
          first = []
          print results1          
          for rec in results1:
              first.append(rec[1])
          
          print first        
          time.sleep(diff)
          cursor.execute(sql)
          results2 = cursor.fetchall()
          second = []
          for rec in results2:
              second.append(rec[1])
       
          qps = 0
          tps = 0
          for i in range(0, 4):
              if i!= 2:
                 b = int(second[i]) - int(first[i])
                 tps += b
              else  : 
                 a = int(second[i]) - int(first[i])
                 qps += a
 
          print 'qps = %s , tps = %s '  %(qps/diff , tps/diff)
          log(qps,tps,logs)
       except KeyboardInterrupt :
          print "exit .."
          sys.exit()
  
    conn.close()
if __name__ == '__main__':
   main()
