'''
Created on 21 may. 2017

@author: jose
'''
import argparse
import time
import simplejson as json
from objetos import bbdd
from objetos import objApl


def recuperaConfig(conn):
    
    sql = 'select * from tb_sda_config'
    config = conn.consulta(sql)
    return config

def importaAplicacion(arg,cnf):
    
    
    conf=cnf['BaseDatos']
    conn=bbdd.bbdd(bd=conf['bd'],u=conf['user'],pw=conf['password'],h=conf['host'],p=conf['port'])
    config = recuperaConfig(conn)
    ultimaSync = config[0][1]
    if type(arg.nombre) <> str:
        sql = "select  id_apl,nombre from tb_aplicacion where fsync >= '" + ultimaSync +"'"
    else :
        sql = "select  id_apl,nombre from tb_aplicacion where fsync >= '" + ultimaSync +"' and nombre ='" + arg.nombre    
    datos=conn.consulta(sql)
    print (time.strftime("%c")+"-- Inicio del inventario de aplicaciones ")
    for apl in datos:
        print (time.strftime("%c")+"-- Procesando aplicacion  "+apl['nombre'])
        ap = objApl.objApl(id_apl=apl[0])
        ap.sincroniza()
    return

def parametros():
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