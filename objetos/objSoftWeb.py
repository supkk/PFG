# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''

from objetos import objSi
from objetos import bbdd
import time


class objSoftWeb(objSi.objSi):
    '''
    classdocs
    '''

    def __init__(self, idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home=''):
        '''
        Constructor
        '''
        super(objSoftWeb,self).__init__(id_serv=idserv,id_sw=sw,id_entorno=ent,ip=ip,user=user,home=home)
        self.soft=soft
        self.puerto=port
        self.dic_Web= {}
        self.id_si=0

    def descubre(self,cnf,param):
        
        modulo = "from plugins import "+self.soft + " as module"
        exec modulo
        cnf=cnf['conecta_ssh']
        self.dic_Web = module.descubre(host=self.ip,user=cnf['user'],password=cnf['password'],port=self.puerto,c_ps=param)
        if self.dic_Web <> None:
            self.version = self.dic_Web['version']
        
        return  self.dic_Web <> None
    
    
    def actualizaInstancia(self, id_si,conn):
        
        modificado = super(objSoftWeb,self).actualizaInstancia(id_si, conn)
        dsw,id_Web = conn.retInstanciaWeb(id_si)
        data =(self.dic_Web['urladmin'],)
        if data <> dsw :
            sql ="update tb_servweb set urladmin=%s, fsync='"+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado = True
            
        return modificado, id_Web
    
    def actualizaVirtualHost(self,vh,conn,id_web):
        
        modificado= False
        dvh,id_vh = conn.retInstanciaVH(id_web,vh['dns'],vh['puerto'])
        if id_vh == None :
            data = (self.id_web,vh['dns'],vh['puerto'],vh['ssl'],vh['rcert'],vh['rutacert'],time.strftime("%c"))
            sql ="insert into tb_vhost (id_web,dns,puerto,ssl,rcert,rutacert,fsync) values (%s,%s,%s,%s,%s,%s,%s)"
            id_vh=conn.actualizaTabla(sql,data)
            modificado =True
        else:
            data =(vh['ssl'],vh['rcert'],vh['rutacert'])
            if data <> dvh :
                sql ="update tb_vhost set ssl=%s, rcert=%s,rutacert=%s, fsync='"+time.strftime("%c")+"' where id_web="+str(id_web)+ " and dns ='" + vh['dns']+ "' and puerto=" + str(vh['puerto'])
                conn.actualizaTabla(sql,data)
                modificado = True
            
        return modificado, id_vh
    
    def actualizaUrl(self,url,conn,id_vh):
        
        modificado= False
        durl,id_url = conn.existeInstanciaUrl(id_vh,url['nombre'])
        if id_url == None :
            data = (id_vh,url['nombre'],url['valor'],time.strftime("%c"))
            sql ="insert into tb_url (id_vh,nombre,valor,fsync) values (%s,%s,%s,%s)"
            conn.actualizaTabla(sql,data)
            modificado =True
        else:
            data =(url['valor'])
            if data <> durl :
                sql ="update tb_url set valor=%s, fsync='"+time.strftime("%c")+"' where id_vh="+str(id_vh)+ " and nombre ='" + url['nombre'] + "'"
                conn.actualizaTabla(sql,data)
                modificado = True
            
        return modificado, id_vh
    
    def marcarVHBorrados(self,conn,id_valor):
        
        sql = "update tb_Vhost set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_vh="+str(id_valor) 
        conn.actualizaTabla(sql)
        sql = "select id_url from tb_url where id_vh="+str(id_valor)
        lurl =conn.consulta(sql)
        for url in lurl :
            self.marcarUrlBorrados(conn,url[0])
        
        return
    
    def gestionaVHBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select id_vh,dns,puerto from TB_vhost where id_web=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for vh in dic :
                if item[1]== vh['dns'] and item[2] == int(vh['puerto']):
                    encontrado =True
                    break
            if not encontrado :
                self.marcarVHBorrados(conn,item[0])
                modificado =True
                
        return modificado
    
    def marcarUrlBorrados(self,conn,id_valor):
        
        sql = "update tb_url set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_url="+str(id_valor) 
        conn.actualizaTabla(sql)
        
        return
    
    def gestionaUrlBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select nombre,id_url from TB_url where id_vh=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for url in dic :
                if item[0]== url['nombre'] :
                    encontrado =True
                    break
            if not encontrado :
                self.marcarUrlBorrados(conn,item[1])
                modificado =True
                
        return modificado
    
    def grabaBBDD(self,conn):
        
        modificado = False
        puertos =[]
        self.id_si = conn.existeInstanciaSW(self.id_serv,self.id_sw,self.puerto,'tb_servweb') 
        if self.id_si == None :
            self.id_si = super(objSoftWeb,self).grabaBBDD(conn)
            data = (self.id_si,self.dic_Web['urladmin'],self.puerto,time.strftime("%c"))
            sql ='insert into tb_servweb (id_si,urladmin,puerto,fsync) values(%s,%s,%s,%s)'
            self.id_web=conn.actualizaTabla(sql,data)
            if self.id_si <> None:
                for vh in self.dic_Web['vh']:
                    data = (self.id_web,vh['dns'],vh['puerto'],vh['ssl'],vh['rcert'],vh['rutacert'],time.strftime("%c"))
                    sql ="insert into tb_vhost (id_web,dns,puerto,ssl,rcert,rutacert,fsync) values (%s,%s,%s,%s,%s,%s,%s)"
                    id_vh=conn.actualizaTabla(sql,data)
                    if id_vh <> None :
                        puertos.append(vh['puerto'])
                        for url in vh['url']:
                            data = (id_vh,url['nombre'],url['valor'],time.strftime("%c"))
                            sql ="insert into tb_url (id_vh,nombre,valor,fsync) values (%s,%s,%s,%s)"
                            conn.actualizaTabla(sql,data)
                    else :
                        print (time.strftime("%c")+"-- Error al insertar el virtualhost "+self.dic_Web['dns']+":"+str(self.dic_Web['puerto']))   
            else:
                print (time.strftime("%c")+"-- Error al insertar la instancia de Servidor web "+self.dic_Web['version'])
        else:
            mod_web,self.id_web = self.actualizaInstancia(self.id_si,conn)
            for vh in self.dic_Web['vh']: 
                mod, id_vh = self.actualizaVirtualHost(vh,conn,self.id_web)
                mod_web = mod or mod_web
                mod_url=False
                for url in vh['url']:
                    mod, id_vh = self.actualizaUrl(url,conn,id_vh)
                    mod_url = mod or mod_url
                mod_url = self.gestionaUrlBorrados(conn,vh['url'],id_vh) or mod_url
                if mod_url :
                    modificado = True
                    conn.apuntaModificado('tb_vhost','id_vh',id_vh)
            mod_web = self.gestionaVHBorrados(conn,self.dic_Web['vh'],self.id_web) or mod_web
            if mod_web == True:
                conn.apuntaModificado( "tb_servweb","id_web",self.id_web)
                modificado = False
                
        return modificado,puertos
      
      