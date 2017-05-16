# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''
from objetos import objSoftWeb
from objetos import objSoftBBDD
from objetos import objSoftSapl
import time

class intSoft(object):
    '''
    classdocs
    '''


    def __init__(self, cs='', idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home='',id_si=0,conn=None,fsync=None):
        '''
        Constructor
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
        correcto=self.o.descubre(cnf,param)

        return correcto
    
    def sincroniza(self,conn,api,_idsw):
        self.o.sincroniza(conn, api,_idsw)
        return
    
    def grabaBBDD(self,conn):
        modificado,ports= self.o.grabaBBDD(conn)

        if modificado:
            conn.apuntaModificado( "tb_soft_running","id_sw",self.id_sw)
            conn.apuntaModificado( "tb_Servidor","id_serv",self.id_serv)
            conn.apuntaModificado( "tb_Disp","id_disp",conn.retIdDisp(self.id_serv))
        return ports


                
        