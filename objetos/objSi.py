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
        self.dic_si={}

        
        return
    
    def cargaSoftware(self,conn):
        dic={}
        sql = 'select id_entorno,version,home,usuario,deleted,_id from tb_softwareinstancia where id_si='+str(self.id_si)
        lsi=conn.consulta(sql)
        dic['entorno']=lsi[0][0]
        dic['version']=lsi[0][1]
        dic['home']=lsi[0][2]
        dic['usuario']=lsi[0][3]
        dic['deleted']=False if lsi[0][4] == None else lsi[0][4]
        self.dic_si=dic

        
        return dic
    
    
    def actualizaInstancia(self, id_si,conn):
        
        modificado=False
        di = conn.retInstanciaSW(id_si)
        data = (self.version.encode('ascii','ignore'),self.home,self.user,self.id_entorno)
        if data <> di :
            sql ="update tb_softwareinstancia set version=%s, home=%s,usuario=%s,id_entorno=%s, fsync='"+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado =True
            
        return modificado
    
    def grabaBBDD(self,conn):
        
        data=(self.id_sw,self.id_serv,self.id_entorno,self.version,self.home,self.user,time.strftime("%c"))
        sql = 'insert into tb_softwareinstancia (id_sw,id_serv,id_entorno,version,home,usuario,fsync) values (%s,%s,%s,%s,%s,%s,%s)'
        self.id_si=conn.actualizaTabla(sql,data)
       
        return self.id_si
        