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
    '''


    def __init__(self, cs='', idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home=''):
        '''
        Constructor
        '''
        self.id_sw=sw
        self.id_serv=idserv
        
        if cs == 'SWEB' :
            self.o = objSoftWeb.objSoftWeb(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home)
        elif cs == 'SAPL':
            self.o = objSoftSapl.objSoftSapl(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home)
        elif cs == 'BBDD':
            self.o = objSoftBBDD.objSoftBBDD(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home)
        else :
            self.o=None
            
    def descubre(self,cnf,param):
        correcto=self.o.descubre(cnf,param)
        return correcto
    
    def grabaBBDD(self,conn):
        modificado,ports= self.o.grabaBBDD(conn)
        id_si = self.o.id_si
        if modificado:
            conn.apuntaModificado( "tb_soft_running","id_sw",self.id_sw)
            conn.apuntaModificado( "tb_Servidor","id_serv",self.id_serv)
            conn.apuntaModificado( "tb_Disp","id_disp",conn.retIdDisp(self.id_serv))
        return id_si,ports


                
        