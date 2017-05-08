# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''
from objetos import objSi

class objSoftSapl(objSi.objSi):
    '''
    classdocs
    '''


    def __init__( self,idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home=''):
        '''
        Constructor
        '''
        super(objSoftSapl,self).__init__(id_serv=idserv,id_sw=sw,id_entorno=ent,ip=ip,user=user,home=home)
        self.soft=soft
        self.puerto=port
        self.dic_SA = {}
    
    def descubre(self,cnf):
        modulo = "from plugins import "+self.soft + " as module"
        exec modulo
        self.dic_SA = modulo.descubre(host=super(objSoftSapl,self).ip,u=cnf['user'],p=cnf['password'],port=self.puerto)
        return
    def grabaBBDD(self,conn):
        return
