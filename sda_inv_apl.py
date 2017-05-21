# -*- coding: utf-8 -*-
'''
Created on 14 may. 2017

@author: jose
'''
import argparse
import time
import simplejson as json
from objetos import bbdd
from objetos import objApl


def descubreAplicacion(n_proceso,ip,cnf,puerto):
 
    modulo = "from plugins import "+n_proceso + " as module"
    try :
        exec modulo
        dic = module.descubreAplicacion(ip,cnf['user'],cnf['password'],puerto)
        lapl = dic['apl'] 
    except Exception, error:
        print error
        print (time.strftime("%c")+"-- Error: No encuentro  plugin "+n_proceso)  
        lapl=None
        
    return lapl

def marcarAplBorrados(conn,id_valor):
        
        sql = "update tb_aplicacion set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_apl="+str(id_valor) 
        conn.actualizaTabla(sql)
        return
    
    
def gestionaAplBorrados(conn, apls,id_sa):
    
    modificado =False
    sql= "select id_apl from tb_map_sa_ap where id_sa ="+ str(id_sa)
    litem = conn.consulta(sql)
    for item in litem:
        encontrado = False
        for ap in apls :
            if item[0]== ap :
                encontrado =True
                break
        if not encontrado :
            marcarAplBorrados(conn,item[0])
            modificado = True         
            
    return modificado

def descubreApl(arg,cnf):
    
    conf=cnf['BaseDatos']
    conn=bbdd.bbdd(bd=conf['bd'],u=conf['user'],pw=conf['password'],h=conf['host'],p=conf['port'])
    if type(arg.ip) <> str:
        sql = 'select id_disp from TB_Dispositivos'
    else :
        sql = "select id_disp,ip from TB_Dispositivos where ip='"+arg.ip+"'"
    datos=conn.consulta(sql)
    for id_disp,ip in datos :
        if id_disp == None:
            print (time.strftime("%c")+"-- Debe inventariar primero el hardware ")
            exit
        idserv=conn.retIdserv(id_disp)
        sql = 'select id_sw from tb_soft_running where id_serv='+str(idserv)
        lsr = conn.consulta(sql)
        nombreServ= conn.retNombreServ(id_disp)
        print (time.strftime("%c")+"-- Comienzo a procesar el servidor "+nombreServ)
        for sw in lsr :
            cs,n_proceso = conn.retCatSoftware(sw[0])
            if cs=='SAPL':
                data = (sw[0],idserv)
                sql ="select si.id_si, sa.puerto, sa.id_sa from tb_softwareinstancia si inner join tb_servaplicaciones sa on si.id_si=sa.id_si where si.id_sw=%s  and si.id_serv=%s"
                linst=conn.consulta(sql,data)
                if linst == None:
                    print (time.strftime("%c")+"-- Debe inventariar primero la infraestructura software ")
                    exit
                modificado = False
                lista_apl=[]
                for inst in linst:
                    apls = descubreAplicacion(n_proceso,ip,cnf["conecta_probe"],inst[1])
                    if apls <> None:
                        for apl in apls:
                            ap=objApl.objApl(apl,inst[2])
                            id_apl,mod_apl=ap.grabaBBDD(conn)
                            lista_apl.append(id_apl)
                        modificado = mod_apl or modificado
                        modificado = gestionaAplBorrados(conn,lista_apl,inst[2])
                        if modificado:
                            conn.apuntaModificado("tb_servaplicaciones", "id_sa",inst[2] )
                            conn.apuntaModificado("tb_softwareinstancia","id_si",inst[0] )
                            sql = "update tb_soft_running set fsync'="+time.strftime("%c") + "' where idserv=%s and id_sw=%s"
                            data=(idserv,sw)
                            conn.actualizatabla(sql,data)
                            conn.apuntaModificado("tb_servidor","id_serv",idserv)
    print (time.strftime("%c")+"-- Fin del inventario de Aplicaciones ")
    return

def parametros():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip" ,help="Inventaría aplicaciones de un servidor" )
    parser.add_argument("-c","--conf",help="ruta del fichero de configuración",default='./conf/config.json')
    args = parser.parse_args()  
    cnf =  json.loads(open(args.conf).read())
    return cnf,args;

if __name__ == '__main__':
    conf,cmd_param=parametros()
    descubreApl(cmd_param,conf)
    