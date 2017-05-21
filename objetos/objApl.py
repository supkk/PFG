# -*- coding: utf-8 -*-
'''
Created on 14 may. 2017

@author: jose
'''
from objetos import bbdd
import time

class objApl(object):
    '''
    classdocs
    '''


    def __init__(self, dic_apl=None,id_sa=0,id_apl=0):
        '''
        Constructor
        '''
        self.dic_apl=dic_apl
        self.id_sa=id_sa
        self.id_apl=id_apl
        if id_apl<> 0:
            self.__cargaAplicacion__()
        
        return
    
    def __cargaAplicacion__(self):
        
        return 
    
    
    def __actualizaAplicacion__(self,conn):
        
        modificado = False
        dapl=conn.retInstanciaApl(self.id_apl)
        
        data=(self.dic_apl['acronimo'],self.dic_apl['nombre'],self.dic_apl['version'])
        if data <> dapl or modificado:
            sql ="update tb_aplicacion set version='"+self.dic_apl['version']+"', fsync='"+time.strftime("%c")+"' where id_apl="+str(self.id_apl)
            conn.actualizaTabla(sql)
            print (time.strftime("%c")+"--Actualizada aplicación "+self.dic_apl['nombre'])
            modificado = True

        for url in self.dic_apl['url']:
            lsurl=conn.retIdUrl(url['valor'])
            if lsurl <> None:
                for id_url in lsurl:    
                    data=(self.id_apl,id_url[0],url['tipo'],time.strftime("%c"))
                    if  conn.existeRelacionUrl(data)== False:
                        sql = "insert into tb_map_url_apl (id_apl,id_url,tipo_url,fsync) values (%s,%s,%s,%s)"
                        conn.actualizaTabla(sql,data,lastval=False)
                        print (time.strftime("%c")+"--Actualizada relacion con url "+url['valor'])
                        modificado=True
                        
        for jdbc in self.dic_apl['jdbc']:
            p,id_cdb=conn.retInstanciaCDB(self.id_sa,jdbc)
            if id_cdb <> None:
                data =(self.id_apl,id_cdb)
                if not conn.existeRelacionCBD(data):
                    data=(self.id_apl,id_cdb,time.strftime("%c"))
                    sql = "insert into tb_map_cbd_apl (id_apl,id_cbd,fsync) values (%s,%s,%s)"
                    modificado=True
                    conn.actualizaTabla(sql,data,lastval=False)
                    print (time.strftime("%c")+"--Actualizada relacion con conector "+jdbc['jdbc'])
        data=(self.id_apl,self.id_sa)
        if not conn.existeRelacionSA(data):
            data=(self.id_apl,self.id_sa,time.strftime("%c"))
            sql = "insert into tb_map_sa_ap (id_apl,id_sa,fsync) values (%s,%s,%s)"
            conn.actualizaTabla(sql,data)
            print (time.strftime("%c")+"--Actualizada relacion con Servidor de aplicaciones "+ str(self.id_sa))
            modificado=True
            

                    
        return modificado
    
    
    def sincroniza(self):
        return
    
    def grabaBBDD(self,conn):
        
        mod_apl=False
        self.id_apl=conn.existeAplicacion(self.dic_apl['nombre'],self.id_sa)
        if self.id_apl == None:
            data=(self.dic_apl['acronimo'],self.dic_apl['nombre'],self.dic_apl['version'],time.strftime("%c"))
            sql = "insert into tb_aplicacion (acronimo,nombre,version,fsync) values (%s,%s,%s,%s)"
            self.id_apl=conn.actualizaTabla(sql,data)
            data=(self.id_apl,self.id_sa,time.strftime("%c"))
            sql = "insert into tb_map_sa_ap (id_apl,id_sa,fsync) values (%s,%s,%s)"
            print (time.strftime("%c")+"-- Encontrada nueva aplicación "+self.dic_apl['nombre'])
            conn.actualizaTabla(sql,data,lastval=False)
            for url in self.dic_apl['url']:
                lsurl=conn.retIdUrl(url['valor'])
                if lsurl <> None:
                    for id_url in lsurl:    
                        data=(self.id_apl,id_url,url['tipo'],time.strftime("%c"))
                        sql = "insert into tb_map_url_apl (id_apl,id_url,tipo_url,fsync) values (%s,%s,%s,%s)"
                        conn.actualizaTabla(sql,data,lastval=False)
                        print (time.strftime("%c")+"-- Se establece relacion con url "+url['valor'])
                else:
                    print (time.strftime("%c")+"-- No se ha podido encontrar la url "+url['valor'])
                    
            for jdbc in self.dic_apl['jdbc']:
                p,id_cdb=conn.retInstanciaCDB(self.id_sa,jdbc)
                if id_cdb <> None:
                    data=(self.id_apl,id_cdb,time.strftime("%c"))
                    sql = "insert into tb_map_cbd_apl (id_apl,id_cbd,fsync) values (%s,%s,%s)"
                    conn.actualizaTabla(sql,data,lastval=False)
                    print (time.strftime("%c")+"-- se establece relacion con controlador "+jdbc)
                else:
                    print (time.strftime("%c")+"-- No se ha podido encontrar el controlador "+jdbc)
            
        else:
            mod_apl=self.__actualizaAplicacion__(conn)
            if mod_apl:
                conn.apuntaModificado( "tb_aplicacion","id_apl",self.id_apl)
            
        return self.id_apl,mod_apl
    
        