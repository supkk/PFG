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


    def __init__(self, dic_apl={},id_sa=0,id_apl=0,conn=None):
        '''
        Constructor
        '''
        self.dic_apl=dic_apl
        self.id_sa=id_sa
        self.id_apl=id_apl
        if id_apl<> 0:
            self.__cargaAplicacion__(conn)
        
        return
    
    def __cargaAplicacion__(self,conn):
        sql ="select acronimo,nombre,version,deleted,_id,fsync from tb_aplicacion where id_apl=" + str(self.id_apl)
        r = conn.consulta(sql)
        self.dic_apl['acronimo']=r[0][0]
        self.dic_apl['nombre']=r[0][1]
        self.dic_apl['version']=r[0][2]
        self.dic_apl['deleted']=False if r[0][3] == None else r[0][3]
        self.dic_apl['_id']=r[0][4]
        self.dic_apl['fsync']=r[0][5]
        sql ="select id_url,tipo_url,deleted from tb_map_url_apl where id_apl="+str(self.id_apl)
        lurl= conn.consulta(sql)
        self.dic_apl['url']=[]
        for url in lurl:
            d_url={}
            d_url['_id']=conn.retidClassUrl(url[0])[0]
            d_url['tipo_url']=url[1]
            d_url['deleted']=False if url[2] == None else url[2]
            self.dic_apl['url'].append(d_url.copy())
        sql ="select id_cbd,deleted from tb_map_cbd_apl where id_apl="+str(self.id_apl)
        lcbd= conn.consulta(sql)
        self.dic_apl['jdbc']=[]
        for cbd in lcbd:
            d_cbd={}
            d_cbd['_id']=conn.retidClassConectorJDBC(cbd[0])[0]
            d_cbd['deleted']=False if cbd[1] == None else cbd[1]
            self.dic_apl['jdbc'].append(d_cbd.copy())
        sql ="select id_sa,deleted from tb_map_sa_ap  where id_apl="+str(self.id_apl)
        lsa= conn.consulta(sql)
        self.dic_apl['SA']=[]
        for sa in lsa:
            d_sa={}
            d_sa['_id']=conn.retidClassSA(sa[0])[0]
            d_sa['deleted']=False if sa[1] == None else sa[1]
            self.dic_apl['SA'].append(d_sa.copy())

        return 
    
    def __estaCargado__(self):
        return (self.dic_apl['_id']>0)
    
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
    
    def __BorraSoftApl__(self, clase, id_valor, api):

        data = {'deleted':'True'}
        id_Class = api.actualizaClase(clase,data,id_valor)

        return id_Class
    
    def sincroniza(self,api,conn, ultimaSync):
        if not self.dic_apl['deleted']:
            data={}
            data['Code']=self.dic_apl['nombre']
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU") 
            sql = "select si.id_entorno  from tb_softwareinstancia si inner join tb_servaplicaciones sa on sa.id_si=si.id_si inner join tb_map_sa_ap map on map.id_sa=sa.id_sa where map.id_apl="+str(self.id_apl)
            ent=conn.consulta(sql)
            if len(ent)==0:
                ent="PRO"
            else:
                ent=ent[0][0]
            data['Entorno']= api.retIdLookup('CI-Entorno',ent)
            data['nombre']=self.dic_apl['nombre']
            data['version']=self.dic_apl['version']
            data['acronimo']=self.dic_apl['acronimo']
            if not self.__estaCargado__():
                id_class = api.creaClase('Aplicacion',data)
                print (time.strftime("%c")+"-- Creada la aplicacion " + self.dic_apl['nombre'] ) 
            else :
                if self.dic_apl['fsync'] > ultimaSync :
                    id_class=api.actualizaClase('Aplicacion',data,self.dic_apl['_id'])
                    print (time.strftime("%c")+"-- Actualizada la aplicacion " + self.dic_apl['nombre'] ) 
            if id_class > 0 :
                conn.apuntaId('tb_aplicacion',id_class,'id_apl',self.id_apl)
                for url in self.dic_apl['url']:
                    data = {}
                    data['_sourceType'] = "Aplicacion"
                    data['_sourceId'] = id_class
                    data['_destinationId'] = url['_id']
                    data['_destinationType'] = "url"
                    if url['tipo_url'] == 'UT':
                        rel = "AplToUsaUrl"
                    else:
                        rel= "AplAccUrl"
                    api.creaRelacion(rel,data)
                for jdbc in self.dic_apl['jdbc']:
                    data = {}
                    data['_sourceType'] = "Aplicacion"
                    data['_sourceId'] = id_class
                    data['_destinationId'] = jdbc['_id']
                    data['_destinationType'] = "ConectorJDBC"
                    api.creaRelacion('AplToJDBC',data)
                for sa in self.dic_apl['SA']:
                    data = {}
                    data['_sourceType'] = "ServAplicaciones"
                    data['_sourceId'] =sa['_id']
                    data['_destinationId'] =  id_class
                    data['_destinationType'] = "Aplicacion"
                    api.creaRelacion('ServAplToApl',data)
        else:
            id_class = self.__BorraSoftApl__('Aplicacion',self.dic_apl['_id'],api)        
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
    
        