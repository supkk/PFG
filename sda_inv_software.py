# -*- coding: utf-8 -*-

'''
Created on 7 may. 2017

@author: jose
'''
from objetos import objssh
from objetos import bbdd
from objetos import intSoft
import argparse
import simplejson as json
import time
from easysnmp import Session

def compruebaConexionPuerto(n_proceso,ip,puerto):
    
    Correcto = False
    modulo = "from plugins import "+n_proceso + " as module"
    try :
        exec modulo
        Correcto = module.compruebaConexion(ip,puerto)
    except :
        print (time.strftime("%c")+"-- Error: No encuentro  plugin "+n_proceso)  
        Correcto = False
    
    return Correcto


def descubreInstanciaSSH(n_proceso,ip,config):
    try:
        datos_instancia = []
        conexSSH = objssh.objssh(ip,config['user'],config['password'])
        comando = "ps -ef | grep " + n_proceso + " | awk '!/grep/{print $1\";\"$2\";\"$8\";\"$0}'"
        sal_ps = conexSSH.enviaComando(comando, "([^;]+);([^;]+);([^;]+);([^\n]+)?", 0)
        for user,pid,home,param in sal_ps:
            comando= 'sudo -S netstat -puntl | grep ' + str(pid) +"| awk '{print $4}' "
            puertos = conexSSH.enviaComando(comando,".*:([^\n]+)",0)
            for port in puertos:
                if compruebaConexionPuerto(n_proceso,ip,port):
                    datos_instancia.append([user,port,home,param])
                        
    except Exception, error:
        print (time.strftime("%c")+"--"+"Error al conectar por SSH con --> "+ip )
        print (time.strftime("%c")+"--", error)
        datos_instancia=None
    
    return datos_instancia

def descubreInstanciaSNMP(n_proceso,ip,config):
    datos_Instancia=None
    return datos_Instancia


def descubreInstancia(n_proceso,ip,config):
    
    datos_base = descubreInstanciaSSH(n_proceso,ip,config)
    if datos_base == None:
        datos_base = descubreInstanciaSNMP(n_proceso,ip,config)
        
    return datos_base

def marcarSIBorrados (conn,cs, id_si):
    Correcto = False
    sql = "update tb_softwareInstancia set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_si="+str(id_si)
    conn.actualizaTabla(sql,confirma=False)
    sql = "select id_serv,id_sw from tb_softwareinstancia where id_si="+str(id_si)
    ids=conn.consulta(sql)[0]
    sql = "update tb_soft_running set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_serv=%s and id_sw=%s"
    conn.actualizaTabla(sql,confirma=False,data=ids)
    if cs =='SAPL':
        Correcto=conn.borraConectoresDB(id_si)
    elif cs =='BBDD':
        Correcto=conn.borraBD(id_si)
    elif cs == 'SWEB':
        Correcto=conn.borraSWeb(id_si)
    if Correcto : 
        conn.confirma()
    else :
        conn.deshace()
    return

def gestionaSIBorrados(conn,lsi,idserv):
    modificado =False
    sql= "select s.id_si,i.id_cat from tb_softwareinstancia s inner join tb_inv_software i on i.id_sw=s.id_sw where s.id_serv=" + str(idserv)
    litem = conn.consulta(sql)
    for item in litem:
        encontrado = False
        for si in lsi :
            if item[0]== si :
                encontrado =True
                break
        if not encontrado :
            marcarSIBorrados(conn,item[1],item[0])
            modificado = True         
            
    return modificado

def descubreSoftware(arg,cnf):
    
    conf=cnf['BaseDatos']
    conn=bbdd.bbdd(bd=conf['bd'],u=conf['user'],pw=conf['password'],h=conf['host'],p=conf['port'])
    if type(arg.ip) <> str:
        sql = 'select id_disp from TB_Dispositivos'
    else :
        sql = "select id_disp,ip from TB_Dispositivos where ip='"+arg.ip+"'"
    datos=conn.consulta(sql)
    
    print (time.strftime("%c")+"-- Inicio del inventario de software ")
    for id_disp,ip in datos :
        lp=[]
        lsi=[]
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
            ent = conn.retEntorno(idserv)
            instSoft = descubreInstancia(n_proceso,ip,cnf['conecta_ssh'])
            if instSoft == None:
                print (time.strftime("%c")+"-- No he podido conectar con el servidor  "+nombreServ)
                continue
            for user,port, home, param in instSoft: 
                if port not in lp:
                    ent = conn.retEntorno(idserv)
                    os = intSoft.intSoft(cs=cs,idserv=idserv,sw=sw[0],ent=ent,ip=ip,soft=n_proceso,user=user,port=port,home=home)
                    if os.o <> None:
                        correcto=os.descubre(cnf,param)
                        if correcto :
                            lp.append(os.grabaBBDD(conn))
                            lsi.append (os.o.id_si)
                    else:
                        print (time.strftime("%c")+"-- El software de tipo "+cs +" no está soportado")  
        gestionaSIBorrados(conn,lsi,idserv)
        print (time.strftime("%c")+"-- Finalizo de procesar el servidor "+nombreServ)    
    conn.cierraDB()
    return

def parametros():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Descubre elementos de red", action="store_true")
    parser.add_argument("-i", "--ip" ,help="Inventaria el software de un servidor" )
    parser.add_argument("-c","--conf",help="ruta del fichero de configuración",default='./conf/config.json')
    args = parser.parse_args()  
    cnf =  json.loads(open(args.conf).read())
    return cnf,args;

if __name__ == '__main__':
    conf,cmd_param=parametros()
    descubreSoftware(cmd_param,conf)
    