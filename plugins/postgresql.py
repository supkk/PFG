# -*- coding: utf-8 -*-
'''
Created on 9 may. 2017

@author: jose
'''
import psycopg2
import time

def consulta (conn,sql):
    
    cur=conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    
    return rows

def ObtieneTipoTabla (tipo):
    
    if tipo=='r':
        cod='TBL'
    else:
        cod='VST'
        
    return cod

def obtenerPrincipal(ip,user,password,port):
    
    dic={}
    try :
        conn = psycopg2.connect( user=user, password=password, host=ip, port=port)
        buf=consulta(conn,"select version()")
        dic['version']=buf[0][0].split(',')[0]
        buf=consulta(conn,"SELECT user from pg_shadow where usesuper='t';")
        dic['admin']=buf[0][0]
        dic['Esquema']=[]
        lbd = consulta (conn, "select d.datname,u.usename from pg_database d,pg_user u where u.usesysid=d.datdba")
        conn.close()
    except :
        print (time.strftime("%c")+"-- Error al conectar a la instancia de BBDD en la IP "+ ip)      

    return dic,lbd

def compruebaConexion(ip,puerto):
    try :
        conn = psycopg2.connect( user="u", password="p", host=ip, port=puerto)
        
    except psycopg2.OperationalError:
        Correcto = True
    except :
        Correcto = False
        
    return Correcto

def descubre(ip,user,password,port):
    
    dic,lbd=obtenerPrincipal(ip,user,password,port)
    dic['Esquema']=[]
    
    for bd in lbd:
        d={}
        try :
            conn = psycopg2.connect( database=bd[0],user=user, password=password, host=ip, port=port)
        except :
            print (time.strftime("%c")+"-- Error de acceso a  la instancia de BBDD " + bd[0]) 
            continue
        
        sql = "select distinct  table_schema from information_schema.columns WHERE table_schema not in ( 'pg_catalog', 'information_schema')"
        leqm= consulta(conn, sql)

        for eqm in leqm :
            d['nombre_db']=bd[0]
            d['nombre']=eqm[0]
            d['propietario']=bd[1]
            d['Tablas']=[]
            sql= "SELECT  c.relname, (c.relkind ) FROM pg_class c LEFT JOIN pg_namespace n ON n.oid = c.relnamespace where c.relkind not in ('i','t','S') and n.nspname='" +eqm[0]+"'"
            l_tb=consulta(conn,sql)
            for tb in l_tb:
                t={}
                t['nombre']=tb[0]
                t['tipo']= ObtieneTipoTabla(tb[1])
                sql="SELECT DISTINCT column_name, data_type from information_schema.columns where table_schema ='"+eqm[0]+"' and table_name='"+tb[0]+"'"
                l_at=consulta(conn,sql)
                t['attTabla']=[]
                for at in l_at:
                    a={}
                    a['nombre']= at[0]
                    a['indice']='False'
                    t['attTabla'].append(a.copy())
                d['Tablas'].append(t.copy())
            dic['Esquema'].append(d.copy())  
        conn.close() 
    return dic

if __name__ == '__main__':
    descubre("192.168.1.20","postgres","postgres", 5432)
    pass