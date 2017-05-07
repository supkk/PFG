# -*- coding: utf-8 -*-
'''
Created on 28 mar. 2017

@author: jose
'''
from objetos import bbdd
from objetos import objServidor
from objetos import cmdbuild
import time
import argparse
import simplejson as json


def sincronizaRed(con,api):
    
    print (time.strftime("%c")+"-- Comienza la sincronización del las redes")
    sql = 'select * from tb_net where _id is null'
    redes = con.consulta(sql)
    for red in redes:
        data='{"Code":"'+str(red[1])+'","nombre":"'+red[2]+'","Estado":'+str(api.retIdLookup('CI-Estado','NV'))+',"IPBase":"'+red[3]+'","Mascara":"'+red[4]+'"}'
        id_class = api.creaClase('Red',data)
        if  id_class > 0:
            sql = "update tb_net set _id =" + str(id_class) + " where id_net = " + str(red[1])
            con.actualizaTabla(sql)
            print (time.strftime("%c")+"-- Sincronizada la red "+red[2])
        else:
            print (time.strftime("%c")+"-- Error al sincronizar la red "+red[2])

    print (time.strftime("%c")+"-- Fin de la sincronización del las redes")
    return

def sincronizaCatalogoSw(con,api):
    
    print (time.strftime("%c")+"-- Comienza la sincronización del catálogo de software")
    sql = 'select id_sw,Descripcion,id_cat,n_proceso,_id from tb_inv_software where _id is null'
    soft = con.consulta(sql)
    for sw in soft:
        data='{"Code":"'+str(sw[0])+'","Description":"'+sw[1]+'","Estado":'+str(api.retIdLookup('CI-Estado','NV'))+',"Categoria":"'+str(api.retIdLookup('Software-Tipo',sw[2]))+'","Patron":"'+sw[3]+'"}'
        id_class = api.creaClase('CatalogoSw',data)
        if  id_class > 0:
            sql = "update tb_inv_software set _id =" + str(id_class) + " where id_sw = " + str(sw[0])
            con.actualizaTabla(sql)
            print (time.strftime("%c")+"-- Sincronizado software "+sw[1])
        else :
            print (time.strftime("%c")+"-- Error al sincronizar el software "+ sw[1])
    print (time.strftime("%c")+"-- Fin de la sincronización del catálogo de software")
            
    return

def recuperaConfig(conn):
    
    sql = 'select * from tb_sda_config'
    config = conn.consulta(sql)
    return config

def actualizaFSync(conn):
    
    sql = "update tb_sda_config set fsync = '"+time.strftime("%c")+"'"
    conn.actualizaTabla(sql)
    
def parametros():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Sincroniza sda con cmdbuild", action="store_true")
    parser.add_argument("-n", "--nombre" ,help="Sincroniza solo un servidor" )
    parser.add_argument("-c","--conf",help="ruta del fichero de configuración",default='./conf/config.json')
    args = parser.parse_args()  
    cnf =  json.loads(open(args.conf).read())
    return cnf,args
    
def main ():
    
    cnf,arg = parametros()
    conf=cnf['BaseDatos']
    conn=bbdd.bbdd(bd=conf['bd'],u=conf['user'],pw=conf['password'],h=conf['host'],p=conf['port'])
    config = recuperaConfig(conn)
    ultimaSync = config[0][1]
    conf=cnf['CMDBuild']
    api = cmdbuild.cmdbuild(conf["host"],conf["port"],conf["user"],conf["password"])
    sincronizaRed(conn,api)
    sincronizaCatalogoSw(conn,api)
    if arg.nombre == None :
        sql = "select d.id_disp, s.id_serv from tb_disp d inner join tb_servidor s on d.id_disp = s.id_disp where  s.fsync >= '" +str(config[0][1])+ "'" 
    else:
        sql = "select d.id_disp, s.id_serv from tb_disp d inner join tb_servidor s on d.id_disp = s.id_disp where  s.fsync >= '" +str(config[0][1])+ "' and d.nombre ='"+arg.nombre +"'" 
  
    lServidores = conn.consulta(sql)
    print (time.strftime("%c")+"-- Iniciando proceso de syncronización. La última fue   "+ str(config[0][1]))
    for s in lServidores:
        serv = objServidor.objServidor(id_disp=s[0],id_serv=s[1])
        print (time.strftime("%c")+"-- Iniciando la sincronizacion del servidor  "+ serv.nombre)
        serv.sincroniza(api,conn,ultimaSync)
        print (time.strftime("%c")+"-- Terminada la sincronizacion del servidor  "+ serv.nombre)
    actualizaFSync(conn)
    print (time.strftime("%c")+"-- Fin del proceso de sincronización")
    return
    
if __name__ == '__main__':
    main()
    