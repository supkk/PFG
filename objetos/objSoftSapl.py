# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''
from objetos import objSi
import time
import re

class objSoftSapl(objSi.objSi):
    '''
    classdocs
    Representa una Instancia de servidor de aplicaciones
    
    '''


    def __init__( self,idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home='',id_si=0,conn=None,fsync=None):
        '''
        Constructor
        
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
        super(objSoftSapl,self).__init__(id_serv=idserv,id_sw=sw,id_entorno=ent,ip=ip,user=user,home=home,id_si=id_si)
        self.soft=soft
        self.puerto=port
        self.id_sa=0
        self.id_si=id_si
        self.fsync=fsync
        
        if id_si ==0:
            self.dic_SA = {}
        else:
            self.dic_SA = self._cargaSoftware(id_si,conn)
        
        return
    
    def _cargaSoftware(self,id_si,conn):
        
        dic=super(objSoftSapl,self)._cargaSoftware(conn)
        data=(id_si,self.fsync)
        sql= "select id_sa,jvm,puerto,_id from tb_servaplicaciones where id_si=%s and fsync >=%s" 
        data = conn.consulta(sql,data)
        dic['id_SA']=data[0][0]
        dic['jvm']= data[0][1]
        dic['puerto']= data[0][2]
        dic['_id']=data[0][3]
        data = (data[0][0],self.fsync)
        sql = "select id_edb,usuario,nombre,_id,deleted,id_cbd from tb_conectorbd where id_sa=%s and fsync >=%s"
        lcdb = conn.consulta(sql,data)
        dic['jdbc']=[]
        for cdb in lcdb:
            d_cdb={}
            d_cdb['usuario']=cdb[1]
            d_cdb['nombre']=cdb[2]
            ddb=conn.retidsEsquemaBD(cdb[0])
            d_cdb['nombre_db']=ddb[0][1]
            d_cdb['esquema']=ddb[0][0]
            d_cdb['_id']=cdb[3]
            d_cdb['id_cbd']=cdb[5]
            d_cdb['deleted']= False if cdb[4] == None else cdb[4]
            dic['jdbc'].append(d_cdb.copy())
        
        return dic
    
    def descubre(self,cnf,param):
        
        '''
        Prueba a descubrir un tipo de software
        
        Parametro
        
        cnf: Diccionario de configuración
        param: Parametros del script
        
        Salida 
        
        Indica si el descubrimiento ha ido bien
        '''
        
        cnf=cnf['conecta_probe']
        modulo = "from plugins import "+self.soft + " as module"
        exec modulo
        self.dic_SA = module.descubre(host=self.ip,user=cnf['user'],password=cnf['password'],puerto=self.puerto)
        if self.dic_SA <> None:
            self.version = self.dic_SA['version']
        
        return self.dic_SA <> None
    
    def _actualizaInstancia(self, id_si,conn):
        
        modificado = super(objSoftSapl,self)._actualizaInstancia(id_si, conn)
        dsa,id_sa = conn.retInstanciaSA(id_si)
        dsa=unicode(dsa,'utf-8')
        data =(self.dic_SA['jvm'])
        if data <> dsa :
            sql ="update tb_servaplicaciones set jvm=%s, fsync='"+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado = True
            
        return modificado, id_sa
    
    def _actualizaConector(self,ds,conn,id_sa):
        
        modificado= False
        dcbd,id_cdb = conn.retInstanciaCDB(id_sa,ds['nombre'])
        if id_cdb == None :
            p,id_edb=conn.retEsquemaDB(ds['esquema'],ds['nombre_bd'])
            if id_edb == None :
                print (time.strftime("%c")+"-- Error el esquema al que apunta el conector no existe "+ds['esquema']+"  "+ds['nombre_bd'])
            else :
                data = (id_edb,ds['usuario'],ds['nombre'],time.strftime("%c"),self.id_sa)
                sql ="insert into tb_conectorbd (id_edb,usuario,nombre,fsync,id_sa) values (%s,%s,%s,%s,%s)"
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data =(ds['usuario'],ds['nombre'])
            if data <> dcbd :
                sql ="update tb_conectorBD set usuario=%s, nombre=%s, fsync='"+time.strftime("%c")+"' where id_cbd="+str(id_cdb)
                conn.actualizaTabla(sql,data)
                modificado = True
            
        return modificado, id_cdb
    
    def _marcarCDBBorrados(self,conn,id_valor):
        
        sql = "update tb_ConectorBD set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_cdb="+str(id_valor) 
        conn.actualizaTabla(sql)
        
        return
    
    def _gestionaCDBBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select nombre,id_cbd from  TB_Conectorbd where id_sa=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for ds in dic :
                if item[0]== ds['nombre'] :
                    encontrado =True
                    break
            if not encontrado :
                self._marcarCDBBorrados(conn,item[1])
                modificado =True
                
        return modificado
    
    def grabaBBDD(self,conn):
      
        '''
        Graba un objeto instancia de software en la BD SDA_DB
        Parametro
        
        conn :Conexión con BD
        
        Salida
        port: Puertos de la instancia procesados
        '''
        
        mod_cdb = False
        self.id_si = conn.existeInstanciaSW(self.id_serv,self.id_sw,self.puerto,'tb_servAplicaciones') 
        if self.id_si == None :
            self.id_si = super(objSoftSapl,self).grabaBBDD(conn)
            data = (self.id_si,self.puerto,self.dic_SA['jvm'],time.strftime("%c"))
            sql ='insert into tb_servaplicaciones (id_si,puerto,jvm,fsync) values(%s,%s,%s,%s)'
            self.id_sa=conn.actualizaTabla(sql,data)
            if self.id_sa <> None:
                for ds in self.dic_SA['jdbc']:
                    p,id_edb=conn.retEsquemaDB(ds['esquema'],ds['nombre_bd'])
                    if id_edb == None :
                        print (time.strftime("%c")+"-- Error el esquema al que apunta el conector no existe "+ds['esquema']+"  "+ds['nombre_bd'])
                    else:    
                        data = (id_edb,ds['usuario'],ds['nombre'],time.strftime("%c"),self.id_sa)
                        sql ="insert into tb_conectorbd (id_edb,usuario,nombre,fsync,id_sa) values (%s,%s,%s,%s,%s)"
                        conn.actualizaTabla(sql,data)
            else:
                print (time.strftime("%c")+"-- Error al insertar la instancia de Servidor aplicaciones "+self.dic['version'])
        else:
            mod_cdb, self.id_sa = self._actualizaInstancia(self.id_si,conn)
            for ds in self.dic_SA['jdbc']: 
                mod, id_cdb = self._actualizaConector(ds,conn,self.id_sa)
                mod_cdb = mod or mod_cdb
            mod_cdb = self._gestionaCDBBorrados(conn,self.dic_SA['jdbc'],self.id_sa) or mod_cdb
            if mod_cdb == True:
                conn.apuntaModificado( "tb_servaplicaciones","id_sa",self.id_sa)
                
        return mod_cdb,self.puerto
    
    
    def _borraSoftSA(self, clase,data, id_valor, api):

        ok = True
        if data['Code'] <> '' :
            data = {'deleted':'True'}
            id_Class = api.actualizaClase(clase,data,id_valor)

        return id_Class
    
    def _sincronizaJDBC(self,jdbc,api):
        
        if not jdbc['deleted']:
            data = {'Code': jdbc['nombre']} 
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_SA['entorno'])
            data['nombre']= jdbc['nombre']
            data['usuario']= jdbc['usuario']
            if jdbc['_id']==None:
                id_Class = api.creaClase('ConectorJDBC',data)
            else :
                id_Class = api.actualizaClase('ConectorJDBC',data,jdbc['_id'])
        else:
            id_Class = self._borraSoftSA('ConectorJDBC',data,jdbc['_id'],api)
            
        return id_Class
    
    def sincroniza(self,conn,api,_idsw):
        
        if not self.dic_SA['deleted']:    
            data = {'Code': "SA_"+str(self.dic_SA['id_SA'])}          
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_SA['entorno'])
            data['Version']= self.dic_SA['version']
            data['Home']= self.dic_SA['home']
            data['JVM'] = str(self.dic_SA['jvm'].decode('ASCII','ignore')).split('-')[0]
            data['usuario']= self.dic_SA['usuario']
            data['puerto']= self.dic_SA['puerto']
            if self.dic_SA['_id']==None:
                id_Class = api.creaClase('ServAplicaciones',data)
            else :
                id_Class = api.actualizaClase('ServAplicaciones',data,self.dic_SA['_id'])
            if id_Class <> None:
                conn.apuntaId('tb_servaplicaciones',id_Class,'id_si',self.id_si)
                conn.apuntaId('tb_softwareinstancia',id_Class,'id_si',self.id_si)
                data = {}
                data['_sourceType'] = "SoftwareInstalado"
                data['_sourceId'] = str(_idsw)
                data['_destinationId'] = id_Class
                data['_destinationType'] = "ServAplicaciones"
                api.creaRelacion('SItoSoftInstancia',data)
                for jdbc in self.dic_SA['jdbc']:
                    id_class_jdbc = self._sincronizaJDBC( jdbc,api)
                    if id_class_jdbc <> None:
                        conn.apuntaId('tb_ConectorBD',id_class_jdbc,'id_cbd',jdbc['id_cbd'])
                        data = {}
                        data['_sourceType'] = "ConectorJDBC"
                        data['_sourceId'] = id_class_jdbc
                        data['_destinationId'] = id_Class
                        data['_destinationType'] = "ServAplicaciones"
                        api.creaRelacion('ConJDBCToSA',data)
                        id_Class_eqm=conn.ret_IdEsquemaBD(jdbc['esquema'],jdbc['nombre_db'])
                        if id_Class_eqm <> None:
                            data = {}
                            data['_sourceType'] = "EsquemaDB"
                            data['_sourceId'] = id_Class_eqm
                            data['_destinationId'] = id_class_jdbc
                            data['_destinationType'] = "ConectorJDBC"
                            api.creaRelacion('ConJDBCToSA',data)
        else:
            id_Class=self._borraSoftSA('BD',data,self.dic_SA['_id'],api)
            
        return
    
    
    
