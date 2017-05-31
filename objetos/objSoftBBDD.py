# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''

from objetos import objSi
import time



class objSoftBBDD(objSi.objSi):
    '''
    classdocs
    Representa una instancia de BD
    '''

    def __init__(self, idserv=0, sw=0, ent='PRO',ip='',soft='',user='',port=0,home='',id_si='0',conn=None,fsync=None):
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
        super(objSoftBBDD,self).__init__(id_serv=idserv,id_sw=sw,id_entorno=ent,ip=ip,user=user,home=home,id_si=id_si)
        self.soft=soft
        self.puerto=port
        self.id_db = 0
        self.id_si = id_si
        self.fsync=fsync
        if id_si ==0:
            self.dic_BD = {}
        else:
            self.dic_BD = self._cargaSoftware(id_si,conn)
        
        return
    
    def _cargaSoftware(self,id_si,conn):
        
        dic=super(objSoftBBDD,self).cargaSoftware(conn)
        data=(id_si,self.fsync)
        sql= "select  puerto,admin,id_db,_id from tb_db where id_si=%s and fsync >=%s" 
        data = conn.consulta(sql,data)
        dic['admin']= data[0][1]
        dic['puerto']= data[0][0]
        dic['_id']= data[0][3]                
        dic['id_db']= data[0][2]
        data = (data[0][2],self.fsync)

        sql = "select nombre,propietario,nombre_db,id_edb,_id,deleted from tb_esquemabd  where id_db=%s and fsync >=%s"
        ledb = conn.consulta(sql,data)
        dic['esquema']=[]
        for edb in ledb:
            d_edb={}
            d_edb['nombre']=edb[0]
            d_edb['propietario']=edb[1]
            d_edb['nombre_db']=edb[2]
            d_edb['_id']=edb[4]
            d_edb['id_edb']=edb[3]
            d_edb['deleted']=False if edb[5] == None else edb[5]
            data=(edb[3],self.fsync)
            sql="select nombre,id_tipo_tabla,id_tb,_id,deleted from tb_tabla where id_edb=%s and fsync >=%s"
            ltb=conn.consulta(sql,data)
            d_edb['Tabla']=[]
            for tb in ltb:
                d_tb={}
                d_tb['nombre']=tb[0]
                d_tb['tipo_tabla']=tb[1]
                d_tb['_id']=tb[3]
                d_tb['id_tb']=tb[2]
                d_tb['deleted']=False if tb[4] == None else tb[4]
                data=(tb[2],self.fsync)
                sql = "select nombre, indice,_id,deleted,id_att from tb_atributotabla where id_tb=%s  and fsync >=%s "
                latb=conn.consulta(sql,data)
                d_tb['campos']=[]
                for at in latb:
                    d_at={}
                    d_at['nombre']=at[0]
                    d_at['indice']=at[1]
                    d_at['_id']=at[2]
                    d_at['deleted']=False if at[3] == None else at[3]
                    d_at['id_at']=at[4]
                    d_tb['campos'].append(d_at.copy())
                d_edb['Tabla'].append(d_tb.copy())
            dic['esquema'].append(d_edb.copy())
        
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
        
        modulo = "from plugins import "+self.soft + " as module"
        exec modulo
        cnf=cnf['conecta_bd']
        self.dic_BD = module.descubre(ip=self.ip,user=cnf['user'],password=cnf['password'],port=self.puerto)
        if self.dic_BD <> None:
            self.version = self.dic_BD['version']

        return self.dic_BD <> None
    
    def _actualizaInstancia(self,id_si,conn):
        
        modificado = super(objSoftBBDD,self).actualizaInstancia(id_si, conn)
        dbd,id_db= conn.retInstanciaBD(id_si)
        data =(self.dic_BD['admin'])
        if data <> dbd :
            sql ="update tb_bd set admin=%s, fsync="+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado = True
        
        return modificado,id_db
    
    def _actualizaEsquema(self,eqm,conn,id_db):
        
        modificado =False
        de,id_edb = conn.retEsquemaDB(eqm['nombre'],eqm['nombre_db'])
        data = (eqm['propietario'])
        if not id_edb is None :
            if de <> data :
                sql ="update tb_bd set propietario=%s, fsync="+time.strftime("%c")+"' where id_si="+str(id_edb)
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data = (self.id_db,eqm['nombre'],eqm['propietario'],time.strftime("%c"),eqm['nombre_db'])
            sql ="insert into tb_esquemabd (id_db,nombre,propietario,fsync,nombre_db) values (%s,%s,%s,%s,%s)"
            id_edb=conn.actualizaTabla(sql,data)
            print (time.strftime("%c")+"-- Actualizada esquema BBDD "+eqm['nombre']+ " en BD "+eqm['nombre_db'])
            modificado =True
    
 
        return modificado,id_edb
    
    def _actualizaTabla(self,tb,conn,id_edb):
        
        modificado =False
        dt,id_tb = conn.retTablaDB(tb['nombre'],id_edb)
        data = (tb['tipo'])
        if id_tb <> None :
            if dt <> data :
                sql ="update tb_tabla set id_tipo_tabla=%s, fsync="+time.strftime("%c")+"' where id_si="+str(id_tb)
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data = (id_edb,tb['nombre'],tb['tipo'],time.strftime("%c"))
            sql ="insert into tb_tabla (id_edb,nombre,id_tipo_tabla,fsync) values (%s,%s,%s,%s)"
            id_tb=conn.actualizaTabla(sql,data)
            modificado =True
 
        return modificado,id_tb
    
    def _actualizaAtrTabla(self,attb,conn,id_tb):
        
        modificado =False
        datt,id_atr = conn.retAttrTablaDB(attb['nombre'],id_tb)
        data = (attb['indice']=="True")
        if id_atr <> None :
            if datt <> data :
                sql ="update tb_atributotabla set indice=%s, fsync='"+time.strftime("%c")+"' where id_si="+str(id_atr)
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data = (id_tb,attb['nombre'],attb['indice'],time.strftime("%c"))
            sql ="insert into tb_atributotabla (id_tb,nombre,indice,fsync) values (%s,%s,%s,%s)"
            id_tb=conn.actualizaTabla(sql,data)
            modificado =True
 
        return modificado,id_tb
    
    
    def _marcarAttrTablaBorrados(self,conn,id_valor):
        
        sql = "update tb_AtributoTabla set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_att="+str(id_valor) 
        conn.actualizaTabla(sql)
        return
    
    def _gestionaAttrTablaBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select id_att,nombre from  TB_atributoTabla where id_tb=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for Attr in dic :
                if item[1]== Attr['nombre'] :
                    encontrado =True
                    break
            if not encontrado :
                self._marcarAttrTablaBorrados(conn,item[0])
                modificado = True         
                
        return modificado
    
    def _marcarTablaBorrados(self,conn,id_valor):
        
        sql = "update tb_Tabla set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_tb="+str(id_valor) 
        conn.actualizaTabla(sql)
        sql = "select id_att from tb_atributoTabla where id_tb="+str(id_valor)
        lattrtablas =conn.consulta(sql)
        for attb in lattrtablas :
            self._marcarAttrTablaBorrados(conn,attb[0])
        
        return
    
    def _gestionaTablaBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select id_tb,nombre from  TB_Tabla where id_edb=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for tabla in dic :
                if item[1]== tabla['nombre'] :
                    encontrado =True
                    break
            if not encontrado :
                self._marcarTablaBorrados(conn,item[0])
                modificado = True         
                
        return modificado
    
    def _marcarEqmBorrados(self,conn,id_valor):
        
        sql = "update tb_EsquemaBD set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_edb="+str(id_valor) 
        conn.actualizaTabla(sql)
        sql = "select id_tb from tb_Tabla where id_edb="+str(id_valor)
        ltablas =conn.consulta(sql)
        for tb in ltablas :
            self._marcarTablaBorrados(conn,tb[0])
        
        return
    
    def _gestionaEqmBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select id_edb,nombre,nombre_db from  TB_EsquemaBD where id_db=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for eqm in dic :
                if item[1]== eqm['nombre'] and item[2] == eqm['nombre_db']:
                    encontrado =True
                    break
            if not encontrado :
                self._marcarEqmBorrados(conn,item[0])
                modificado =True
                
        return modificado
    
    def grabaBBDD(self,conn):
        '''
        Graba un objeto instancia de software en la BD SDA_DB
        
        Parametro
        
            conn :Conexión con BD
        
        Salida
            port: Puertos de la instancia procesados
            modificado: Indica si se ha modificado
        '''
        
        modificado = False
        self.id_si = conn.existeInstanciaSW(self.id_serv,self.id_sw,self.puerto,'tb_db') 
        if self.id_si == None :
            self.id_si = super(objSoftBBDD,self).grabaBBDD(conn)
            data = (self.id_si,self.puerto,self.dic_BD['admin'],time.strftime("%c"))
            sql ='insert into tb_db (id_si,puerto,admin,fsync) values(%s,%s,%s,%s)'
            id_db=conn.actualizaTabla(sql,data)
            if id_db <> None:
                modificado = True
                for eqm in self.dic_BD['Esquema']:
                    data = (id_db, eqm['nombre'],eqm['nombre_db'],eqm['propietario'],time.strftime("%c"))
                    sql = 'insert into tb_esquemabd (id_db,nombre, nombre_db,propietario,fsync) values (%s,%s,%s,%s,%s)'
                    id_edb=conn.actualizaTabla(sql,data)
                    print (time.strftime("%c")+"-- Insertada instancia BBDD "+eqm['nombre_db']+ " con esquema "+eqm['nombre'])
                    if id_edb <>None:
                        for tb in eqm['Tablas']:
                            data = (id_edb,tb['nombre'],tb['tipo'],time.strftime("%c"))
                            print (time.strftime("%c")+"-- Insertada Tabla BBDD "+tb['nombre']+ " en esquema "+eqm['nombre'])
                            sql = 'insert into tb_tabla (id_edb,nombre,id_tipo_tabla,fsync) values (%s,%s,%s,%s)'
                            id_tb=conn.actualizaTabla(sql,data)
                            for atb in tb['attTabla']:
                                data=(id_tb,atb['nombre'],atb['indice'],time.strftime("%c"))
                                sql ='insert into tb_atributotabla (id_tb,nombre,indice,fsync) values (%s,%s,%s,%s)'
                                conn.actualizaTabla(sql,data)
        else :
            modificado, self.id_db = self._actualizaInstancia(self.id_si,conn)    
            for eqm in self.dic_BD['Esquema']:
                mod,id_edb = self._actualizaEsquema(eqm,conn,self.id_db)    
                modificado = mod or modificado
                mod_tb=False
                for tb in eqm['Tablas']:
                    mod, id_tb = self._actualizaTabla(tb,conn,id_edb)    
                    mod_tb = mod or mod_tb
                    mod_atr=False
                    for atb in tb['attTabla']:
                        mod = self._actualizaAtrTabla(atb,conn,id_tb)   
                        mod_atr = mod or mod_atr
                    mod_atr = self._gestionaAttrTablaBorrados(conn,tb['attTabla'],id_tb) or mod_atr
                    if mod_atr == True:
                        modificado=True    
                        conn.apuntaModificado("tb_tabla","id_tb",id_tb)
                mod_tb = self._gestionaTablaBorrados(conn,eqm['Tablas'],id_edb) or mod_tb
                if mod_tb == True :
                    modificado = True
                    conn.apuntaModificado("tb_EsquemaBD","id_edb",id_edb)
            modificado = self._gestionaEqmBorrados(conn,self.dic_BD['Esquema'], self.id_db) or modificado
            if modificado== True:
                conn.apuntaModificado( "tb_db","id_si",self.id_si)
        return modificado,self.puerto
    
    def _BorraSoftBBDD(self, clase, id_valor, api):

        data = {'deleted':'True'}
        id_Class = api.actualizaClase(clase,data,id_valor)

        return id_Class
    
    def _sincronizaTabla(self,tb,api):
        
        if not tb['deleted']:
            data = {'Code': tb['nombre']} 
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_BD['entorno'])
            data['Nombre']= tb['nombre']
            data['Tipo']= api.retIdLookup('Tabla-Tipo',tb['tipo_tabla'])
            if tb['_id']==None:
                id_Class_tb = api.creaClase('Tabla',data)
            else :
                id_Class_tb = api.actualizaClase('Tabla',data,tb['_id'])
        else:
            id_Class_tb = self._BorraSoftBBDD('Tabla',tb['_id'],api)
            
        return id_Class_tb
    
    def _sincronizaEsquema(self,eqm,api):
        
        if not eqm['deleted']:
            data = {'Code': eqm['nombre']} 
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_BD['entorno'])
            data['nombre']= eqm['nombre']
            data['nombre_db']= eqm['nombre_db']
            data['propietario']= eqm['propietario']
            if eqm['_id']==None:
                id_Class_eqm = api.creaClase('EsquemaBD',data)
            else :
                id_Class_eqm = api.actualizaClase('EsquemaBD',data,eqm['_id'])
        else:
            id_Class_eqm=self._BorraSoftBBDD('EsquemaBD', eqm['_id'],api)
                
        return id_Class_eqm
    
    def _sincronizaAtributo(self,at,api):
        
        if not at['deleted']:
            data = {'Code': at['nombre']} 
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_BD['entorno'])
            data['nombre']= at['nombre']
            data['Indice']= at['indice']
            if at['_id']==None:
                id_Class_at = api.creaClase('CamposTabla',data)
            else :
                id_Class_at = api.actualizaClase('CamposTabla',data,at['_id'])
        else :
            id_Class_at=self._BorraSoftBBDD('CamposTabla',at['_id'],api)
            
        return id_Class_at
    
    def sincroniza(self,conn,api,_idsw):
        
        '''
        Sincroniza un CI con CMDBuild
        
        Parametro
            conn:  Objeto de conexion con la BD SDA_DB
            api:  Objeto de conexion con CMDBuild
            _idws: Identificador en CMDBuild de la instancia de software
        '''
        
        if not self.dic_BD['deleted']:    
            data = {'Code': "BBDD_"+str(self.dic_BD['id_db'])}          
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_BD['entorno'])
            data['Version']= self.dic_BD['version']
            data['Home']= self.dic_BD['home']
            data['Usuario']= self.dic_BD['usuario']
            data['admin']= self.dic_BD['admin']
            data['puerto']= self.dic_BD['puerto']
            if self.dic_BD['_id']==None:
                id_Class = api.creaClase('BD',data)
            else :
                id_Class = api.actualizaClase('BD',data,self.dic_BD['_id'])
            if id_Class <> None:
                conn.apuntaId('tb_DB',id_Class,'id_si',self.id_si)
                conn.apuntaId('tb_softwareinstancia',id_Class,'id_si',self.id_si)
                data = {}
                data['_sourceType'] = "SoftwareInstalado"
                data['_sourceId'] = str(_idsw)
                data['_destinationId'] = id_Class
                data['_destinationType'] = "BD"
                api.creaRelacion('SItoSoftInstancia',data)
                for eqm in self.dic_BD['esquema']:
                    id_Class_eqm=self._sincronizaEsquema(eqm,api)
                    if id_Class_eqm > 0 :
                        conn.apuntaId('tb_EsquemaBD',id_Class_eqm,'id_edb',eqm['id_edb'])
                        data = {}
                        data['_sourceType'] = "BD"
                        data['_sourceId'] = str(self.dic_BD['_id'])
                        data['_destinationId'] = id_Class_eqm
                        data['_destinationType'] = "EsquemaBD"
                        api.creaRelacion('BDtoEsquemaDB',data)
                        for tb in eqm['Tabla']:
                            id_Class_tb=self._sincronizaTabla(tb,api)
                            if id_Class_tb > 0 :
                                conn.apuntaId('tb_Tabla',id_Class_tb,'id_tb',tb['id_tb'])
                                data = {}
                                data['_sourceType'] = "EsquemaBD"
                                data['_sourceId'] = id_Class_eqm
                                data['_destinationId'] = id_Class_tb
                                data['_destinationType'] = "Tabla"
                                api.creaRelacion('EsquemaDBToTabla',data)
                                for at in tb['campos']:
                                    id_Class_at=self._sincronizaAtributo(at,api)
                                    if id_Class > 0 :
                                        conn.apuntaId('tb_AtributoTabla',id_Class_at,'id_att',at['id_at'])
                                        data = {}
                                        data['_sourceType'] = "Tabla"
                                        data['_sourceId'] = id_Class_tb
                                        data['_destinationId'] = id_Class_at
                                        data['_destinationType'] = "CamposTabla"
                                        api.creaRelacion('TablaToCamposTabla',data)
        else :
            id_Class_at=self._BorraSoftBBDD('BD',self.dic_BD['_id'],api)
                        
                        
        return
    
    
    