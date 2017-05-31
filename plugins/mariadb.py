# -*- coding: utf-8 -*-
'''
Created on 9 may. 2017

@author: jose
'''
import MySQLdb
import time


def _consulta (conn,sql):
    
    cur=conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    
    return rows

def _ObtieneTipoTabla (tipo):
    
    if tipo=='VIEW':
        cod='VST'
    else:
        cod='TBL'
        
    return cod

def _obtenerPrincipal(ip,user,password,port):
    
    dic={}
    try :
        datos = [ip, user, password, 'MYSQL'] 
        conn = MySQLdb.connect(*datos)
        buf=_consulta(conn,"select version()")
        dic['version']=buf[0][0].split(',')[0]
        buf=_consulta(conn,"select user from mysql.user where super_priv='Y'")
        dic['admin']=buf[0][0]
        dic['Esquema']=[]
        lbd = _consulta (conn, "select SCHEMA_NAME from SCHEMATA")
        conn.close()
    except :
        print (time.strftime("%c")+"-- Error al conectar a la instancia de BBDD en la IP "+ ip)      

    return dic,lbd

def compruebaConexion(ip,puerto):
    '''
    Comprueba que el software especificado escucha en el puerto indicado
    
    Parametros
        ip : IP del servidor en proceso
        puerto: Puerto de escucha
    
    Salida
        True si correcto
     
    '''
    try :
        datos = [ip, 'u', 'p', 'mysql'] 
        conn = MySQLdb.connect(*datos)
        
    except MySQLdb.connections.OperationalError:
        Correcto = True
    except :
        Correcto = False
        
    return Correcto

def descubre(ip,user,password,port):
    '''
    Prueba a descubrir un Servidor de BD postgres
    
    Parametro
    
        host:Ip del servidor
        user: Usuario con permisos de administracion
        password: password del usuario
        port:puerto de escucha de la consola
        c_ps:Salida del comando ps 
    
    Salida 
    
        Indica si el descubrimiento ha ido bien
    '''
    
    dic,lbd=_obtenerPrincipal(ip,user,password,port)
    dic['Esquema']=[]
    try :
        datos = [ip, user, password,'information_schema'] 
        conn = MySQLdb.connect(*datos)
    except :
        print (time.strftime("%c")+"-- Error de acceso a  la instancia de BBDD information_schema"  ) 
    
    if conn.open == 1:
        for bd in lbd:
            d={}
            sql = "select table_name,table_type from information_schema.tables where table_schema='"+bd[0]+"'"
            l_tb= _consulta(conn, sql)
            d['nombre_db']=bd[0]
            d['nombre']=bd[0]
            d['propietario']=''
            d['Tablas']=[]
            for tb in l_tb:
                t={}
                t['nombre']=tb[0]
                t['tipo']= _ObtieneTipoTabla(tb[1])
                sql="select column_name, column_key from columns where table_schema='"+bd[0]+"' and table_name='"+tb[0]+"'"
                l_at=_consulta(conn,sql)
                t['attTabla']=[]
                for at in l_at:
                    a={}
                    a['nombre']= at[0]
                    a['indice']=(at[1] == '')
                    t['attTabla'].append(a.copy())
                d['Tablas'].append(t.copy())
            dic['Esquema'].append(d.copy())  
        conn.close() 
    return dic

if __name__ == '__main__':
#    compruebaConexion('192.168.1.26', 0)
    descubre("192.168.1.26","root","password", 5432)
    pass