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


    def __init__(self, dic_apl,id_sa):
        '''
        Constructor
        '''
        self.dic_apl=dic_apl
        self.id_sa=id_sa
        self.id_apl=0
        
        return
    
    
    def actualizaAplicacion(self,conn):
        
        modificado = False
        dapl=conn.retInstanciaApl(self.id_apl)

        for url in self.dic_apl['url']:
            lsurl=conn.retIdUrl(url['valor'])
            if lsurl <> None:
                for id_url in lsurl:    
                    data=(self.id_apl,id_url[0],url['tipo'],time.strftime("%c"))
                    if  conn.existeRelacionUrl(data)== False:
                        sql = "insert into tb_map_url_apl (id_apl,id_url,tipo_url,fsync) values (%s,%s,%s,%s)"
                        conn.actualizaTabla(sql,data,lastval=False)
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
        data=(self.id_apl,self.id_sa)
        if not conn.existeRelacionSA(data):
            data=(self.id_apl,self.id_sa,time.strftime("%c"))
            sql = "insert into tb_map_sa_ap (id_apl,id_sa,fsync) values (%s,%s,%s)"
            conn.actualizaTabla(sql,data)
            modificado=True
            
        data=(self.dic_apl['acronimo'],self.dic_apl['nombre'],self.dic_apl['version'])
        if data <> dapl or modificado:
            sql ="update tb_aplicacion set version='"+self.dic_apl['version']+"', fsync='"+time.strftime("%c")+"' where id_apl="+str(self.id_apl)
            conn.actualizaTabla(sql)
            modificado = True
                    
        return modificado
    
    
    def grabaBBDD(self,conn):
        
        mod_apl=False
        self.id_apl=conn.existeAplicacion(self.dic_apl['nombre'],self.id_sa)
        if self.id_apl == None:
            data=(self.dic_apl['acronimo'],self.dic_apl['nombre'],self.dic_apl['version'],time.strftime("%c"))
            sql = "insert into tb_aplicacion (acronimo,nombre,version,fsync) values (%s,%s,%s,%s)"
            self.id_apl=conn.actualizaTabla(sql,data)
            data=(self.id_apl,self.id_sa,time.strftime("%c"))
            sql = "insert into tb_map_sa_ap (id_apl,id_sa,fsync) values (%s,%s,%s)"
            conn.actualizaTabla(sql,data,lastval=False)
            for url in self.dic_apl['url']:
                lsurl=conn.retIdUrl(url['valor'])
                if lsurl <> None:
                    for id_url in lsurl:    
                        data=(self.id_apl,id_url,url['tipo'],time.strftime("%c"))
                        sql = "insert into tb_map_url_apl (id_apl,id_url,tipo_url,fsync) values (%s,%s,%s,%s)"
                        conn.actualizaTabla(sql,data,lastval=False)
                else:
                    print (time.strftime("%c")+"-- No se ha podido encontrar la url "+url)
                    
            for jdbc in self.dic_apl['jdbc']:
                p,id_cdb=conn.retInstanciaCDB(self.id_sa,jdbc)
                if id_cdb <> None:
                    data=(self.id_apl,id_cdb,time.strftime("%c"))
                    sql = "insert into tb_map_cbd_apl (id_apl,id_cbd,fsync) values (%s,%s,%s)"
                    conn.actualizaTabla(sql,data,lastval=False)
                else:
                    print (time.strftime("%c")+"-- No se ha podido encontrar el controlador "+jdbc)
            
        else:
            mod_apl=self.actualizaAplicacion(conn)
            if mod_apl:
                conn.apuntaModificado( "tb_aplicacion","id_apl",self.id_apl)
            
        return self.id_apl,mod_apl
    
        