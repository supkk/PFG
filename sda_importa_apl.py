# -*- coding: utf-8 -*-
'''
Created on 21 may. 2017

@author: jose
'''
import argparse
import time
from datetime import datetime
import simplejson as json
from objetos import bbdd
from objetos import objApl
from objetos import cmdbuild


def _recuperaConfig(conn):
    
    sql = 'select fsync_apl from tb_sda_config'
    config = conn.consulta(sql)
    return config

def importaAplicacion(arg,cnf):
    '''
    Importa aplicaciones en CMDBuild
    
    Parametros
       cnf : Diccionario con los parametros de configuracion
       args: Objeto con los pararámetros que se pasan al script   
    
    '''
    
    conf=cnf['BaseDatos']
    conn=bbdd.bbdd(bd=conf['bd'],u=conf['user'],pw=conf['password'],h=conf['host'],p=conf['port'])
    config = _recuperaConfig(conn)
    ultimaSync = config[0][0]
    conf=cnf['CMDBuild']
    api = cmdbuild.cmdbuild(conf["host"],conf["port"],conf["user"],conf["password"])
    if type(arg.nombre) <> str:
        sql = "select  id_apl,nombre from tb_aplicacion where fsync >= '" + str(ultimaSync) +"'"
    else :
        sql = "select  id_apl,nombre from tb_aplicacion where  nombre ='" + arg.nombre +"'"
        ultimaSync=datetime.strptime('01/01/01','%d/%m/%y').date()   
    datos=conn.consulta(sql)
    print (time.strftime("%c")+"-- Inicio del inventario de aplicaciones ")
    for apl in datos:
        print (time.strftime("%c")+"-- Procesando aplicacion  "+apl[1])
        ap = objApl.objApl(id_apl=apl[0],conn=conn)
        ap.sincroniza(api,conn,ultimaSync)
    return

def parametros():
    '''
    Procesa la linea de comandos del script y construye un objeto argparse. Tambien carga los ficheros de configuracion
     
    Salida 
     
       cnf : Diccionario con los parametros de configuracion
       args: Objeto con los pararámetros que se pasan al script  
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nombre" ,help="Sincroniza solo una aplicacion" )
    parser.add_argument("-c","--conf",help="ruta del fichero de configuración",default='./conf/config.json')
    args = parser.parse_args()  
    cnf =  json.loads(open(args.conf).read())
    return cnf,args

if __name__ == '__main__':
    conf,cmd_param=parametros()
    importaAplicacion(cmd_param,conf)
    pass