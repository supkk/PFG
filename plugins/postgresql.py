# -*- coding: utf-8 -*-
'''
Created on 9 may. 2017

@author: jose
'''
import psycopg2

def consulta (conn,sql):
    
    cur=conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    
    return rows

def descubre(ip,user,password,port):
    
    dic={}
    try :
        conn = psycopg2.connect( user=user, password=password, host=ip, port=port)
        
    except :
        print ("Error de acceso a BBDD")
          
    buffer=consulta(conn,"select version()")
    dic['version']=buffer[0]
    buffer=consulta(conn,"SELECT user from pg_shadow where usesuper='t';")
    dic['admin']=buffer[0]
    
    return dic

if __name__ == '__main__':
    descubre("192.168.1.20","postgres","postgres", 5432)
    pass