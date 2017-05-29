# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''
from objetos import objSoftWeb
from objetos import objSoftBBDD
from objetos import objSoftSapl


class intSoft(object):
    '''
    classdocs
    Interfaz a las clases objSoftWeb, objSoftBBDD, objSoftSapl
    
    '''


    def __init__(self, cs='', idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home='',id_si=0,conn=None,fsync=None):
        '''
        Constructor
        cs: identificador de la categoria de software
        idserv: identificador del servidor
        sw: identificador del software
        ent: Entorno donde se ha instalado
        ip: Ip donde ha sido descubierto
        soft: Cadena de software
        user:Usuario propietario del proceso
        port: Puerto de escucha
        home: Directorio de instalacion del software
        id_si: Identificador de Instancia software
        conn: Conexión a la BD SDA_DB
        fsync: Fecha de la última sincronizacion
        '''
        self.id_sw=sw
        self.id_serv=idserv
        self.cs=cs
        
        if cs == 'SWEB' :
            self.o = objSoftWeb.objSoftWeb(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home,id_si=id_si,conn=conn,fsync=fsync)                             
        elif cs == 'SAPL':
            self.o = objSoftSapl.objSoftSapl(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home,id_si=id_si,conn=conn,fsync=fsync)
        elif cs == 'BBDD':
            self.o = objSoftBBDD.objSoftBBDD(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home,id_si=id_si,conn=conn,fsync=fsync)
        else :
            self.o=None
            
    def descubre(self,cnf,param):
        '''
        Prueba a descubrir un tipo de software
        
        Parametro
        
        cnf: Diccionario de configuración
        param: Parametros del script
        
        Salida 
        
        Indica si el descubrimiento ha ido bien
        '''
        correcto=self.o.descubre(cnf,param)

        return correcto
    
    def sincroniza(self,conn,api,_idsw):
        
        '''
        Sincroniza un CI con CMDBuild
        
        Parametro
        conn:  Objeto de conexion con la BD SDA_DB
        api:  Objeto de conexion con CMDBuild
        _idws: Identificador en CMDBuild de la instancia de software
        '''
    
        self.o.sincroniza(conn, api,_idsw)
        return
    
    def grabaBBDD(self,conn):
        
        '''
        Graba un objeto instancia de software en la BD SDA_DB
        Parametro
        
        conn :Conexión con BD
        
        Salida
        port: Puertos de la instancia procesados
        '''
        modificado,ports= self.o.grabaBBDD(conn)

        if modificado:
            conn.apuntaModificado( "tb_soft_running","id_sw",self.id_sw)
            conn.apuntaModificado( "tb_Servidor","id_serv",self.id_serv)
            conn.apuntaModificado( "tb_Disp","id_disp",conn.retIdDisp(self.id_serv))
        return ports


                
        