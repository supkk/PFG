# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''
import time

class objSi(object):
    '''
    classdocs
    '''


    def __init__(self, _id='',id_si=0,id_sw=0,id_serv=0,id_entorno='PRO',version='',ip='',user='',home=''):
        '''
        Constructor
        '''
        self._id=_id
        self.id_si=id_si
        self.id_sw=id_sw
        self.id_serv=id_serv
        self.id_entorno=id_entorno
        self.version=version
        self.home=home
        self.ip = ip
        self.user=user

        
        return
    
    def actualizaInstancia(self, id_si,conn):
        modificado=False
        
        di = conn.retInstanciaSW(id_si)
        data = (self.version,self.home,self.user,self.id_entorno)
        if data <> di :
            sql ="update tb_softwareinstancia set version=%s, home=%s,user=%s,id_entorno=%s, fsync="+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado =True
            
        return modificado
    
    def grabaBBDD(self,conn):
        
        data=(self.id_sw,self.id_serv,self.id_entorno,self.version,self.home,self.user,time.strftime("%c"))
        sql = 'insert into tb_softwareinstancia (id_sw,id_serv,id_entorno,version,home,usuario,fsync) values (%s,%s,%s,%s,%s,%s,%s)'
        self.id_si=conn.actualizaTabla(sql,data)
       
        return self.id_si
        