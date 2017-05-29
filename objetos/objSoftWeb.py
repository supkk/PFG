# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''

from objetos import objSi
import time


class objSoftWeb(objSi.objSi):
    '''
    classdocs
    
    Representa una instancia de servidor web
    
    '''

    def __init__(self, idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home='',id_si=0,conn=None,fsync=None):
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
        super(objSoftWeb,self).__init__(id_serv=idserv,id_sw=sw,id_entorno=ent,ip=ip,user=user,home=home,id_si=0)
        self.soft=soft
        self.puerto=port
        self.fsync=fsync
        self.id_si=id_si
        if id_si ==0:
            self.dic_Web = {}
        else:
            self.dic_Web= self._cargaSoftware(id_si,conn)
        
        return
    
    def _cargaSoftware(self,id_si,conn):
        
        dic=super(objSoftWeb,self)._cargaSoftware(conn)
        data=(id_si,self.fsync)
        sql= "select sw.urladmin,si.version,sw.puerto, sw.id_web,sw._id from tb_softwareInstancia si inner join tb_servweb sw on si.id_si = sw.id_si where sw.id_si=%s and sw.fsync >=%s" 
        data = conn.consulta(sql,data)
        dic['id_web']=data[0][3]
        dic['urladmin']= data[0][0]
        dic['version']= data[0][1]
        dic['puerto']= data[0][2]
        dic['_id']=data[0][4]
        data = (data[0][3],self.fsync)
        sql = "select id_vh,dns,puerto,ssl,rcert,rutacert, _id,deleted from tb_vhost where id_web=%s and fsync >=%s"
        lvh = conn.consulta(sql,data)
        dic['vh']=[]
        for vh in lvh:
            d_vh={}
            d_vh['id_vh']=vh[0]
            d_vh['dns']=vh[1]
            d_vh['puerto']=vh[2]
            d_vh['ssl']=vh[3]
            d_vh['rcert']=vh[4]
            d_vh['rutacert']=vh[5]
            d_vh['_id']=vh[6]
            d_vh['deleted']= False if vh[7] == None else vh[7]
            data=(vh[0],self.fsync)
            sql="select nombre,valor,id_tipo,_id,deleted,id_url from tb_url where id_vh=%s and fsync >=%s"
            lurl=conn.consulta(sql,data)
            d_vh['url']=[]
            for url in lurl:
                d_url={}
                d_url['id_url']=url[5]
                d_url['nombre']=url[0]
                d_url['valor']=url[1]
                d_url['tipo']=url[2]
                d_url['_id']=url[3]
                d_url['deleted']=False if url[4] == None else url[4]
                d_vh['url'].append(d_url.copy())
            dic['vh'].append(d_vh.copy())
        
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
        cnf=cnf['conecta_ssh']
        self.dic_Web = module.descubre(host=self.ip,user=cnf['user'],password=cnf['password'],port=self.puerto,c_ps=param)
        if self.dic_Web <> None:
            self.version = self.dic_Web['version']
        
        return  self.dic_Web <> None
    
    
    def _actualizaInstancia(self, id_si,conn):
        
        modificado = super(objSoftWeb,self)._actualizaInstancia(id_si, conn)
        dsw,id_Web = conn.retInstanciaWeb(id_si)
        data =(self.dic_Web['urladmin'],)
        if data <> dsw :
            sql ="update tb_servweb set urladmin=%s, fsync='"+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado = True
            
        return modificado, id_Web
    
    def _actualizaVirtualHost(self,vh,conn,id_web):
        
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
    
    def _actualizaUrl(self,url,conn,id_vh):
        
        modificado= False
        durl,id_url = conn.existeInstanciaUrl(id_vh,url['nombre'])
        if id_url == None :
            data = (id_vh,url['nombre'],url['valor'],url['tipo'],time.strftime("%c"))
            sql ="insert into tb_url (id_vh,nombre,valor,id_tipo,fsync) values (%s,%s,%s,%s,%s)"
            conn.actualizaTabla(sql,data)
            modificado =True
        else:
            data =(url['valor'],url['tipo'])
            if data <> durl :
                sql ="update tb_url set valor=%s, id_tipo=%s,fsync='"+time.strftime("%c")+"' where id_vh="+str(id_vh)+ " and nombre ='" + url['nombre'] + "'"
                conn.actualizaTabla(sql,data)
                modificado = True
            
        return modificado, id_vh
    
    def _marcarVHBorrados(self,conn,id_valor):
        
        sql = "update tb_Vhost set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_vh="+str(id_valor) 
        conn.actualizaTabla(sql)
        sql = "select id_url from tb_url where id_vh="+str(id_valor)
        lurl =conn.consulta(sql)
        for url in lurl :
            self._marcarUrlBorrados(conn,url[0])
        
        return
    
    def _gestionaVHBorrados(self, conn,dic, id_valor):
        
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
                self._marcarVHBorrados(conn,item[0])
                modificado =True
                
        return modificado
    
    def _marcarUrlBorrados(self,conn,id_valor):
        
        sql = "update tb_url set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_url="+str(id_valor) 
        conn.actualizaTabla(sql)
        
        return
    
    def _gestionaUrlBorrados(self, conn,dic, id_valor):
        
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
                self._marcarUrlBorrados(conn,item[1])
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
                            data = (id_vh,url['nombre'],url['valor'],url['tipo'],time.strftime("%c"))
                            sql ="insert into tb_url (id_vh,nombre,valor,id_tipo,fsync) values (%s,%s,%s,%s,%s)"
                            conn.actualizaTabla(sql,data)
                    else :
                        print (time.strftime("%c")+"-- Error al insertar el virtualhost "+self.dic_Web['dns']+":"+str(self.dic_Web['puerto']))   
            else:
                print (time.strftime("%c")+"-- Error al insertar la instancia de Servidor web "+self.dic_Web['version'])
        else:
            mod_web,self.id_web = self._actualizaInstancia(self.id_si,conn)
            for vh in self.dic_Web['vh']: 
                mod, id_vh = self._actualizaVirtualHost(vh,conn,self.id_web)
                mod_web = mod or mod_web
                mod_url=False
                for url in vh['url']:
                    mod, id_vh = self._actualizaUrl(url,conn,id_vh)
                    mod_url = mod or mod_url
                mod_url = self._gestionaUrlBorrados(conn,vh['url'],id_vh) or mod_url
                if mod_url :
                    modificado = True
                    conn.apuntaModificado('tb_vhost','id_vh',id_vh)
            mod_web = self._gestionaVHBorrados(conn,self.dic_Web['vh'],self.id_web) or mod_web
            if mod_web == True:
                conn.apuntaModificado( "tb_servweb","id_web",self.id_web)
                modificado = False
                
        return modificado,puertos
    
    def _borraSoftWeb(self, clase, id_valor, api):

        ok = True
        if id_valor <> '' :
            data = {'deleted':'True'}
            id_Class = api.actualizaClase(clase,data,id_valor)

        return id_Class
    
    def _sincronizaUrl(self,api, url,conn):
        
        
        data= {}
        data['Tipo']= api.retIdLookup('url-Tipo',url['tipo'])
        data['Code']= "URL_"+url['tipo']+"_"+str(url['id_url'])
        data['Estado']=api.retIdLookup('CI-Estado','NV')
        data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
        data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_Web['entorno'])
        data['nombre']=url['nombre']
        data['valor']=url['valor'] 
        if not url['deleted']:
            if url['_id'] == None:
                id_class = api.creaClase('url',data)
            else :
                id_class = api.actualizaClase('url',data,url['_id'])
        else:
            id_class = self._borraSoftWeb('url',url['_id'],api)
            
        return id_class
    
    def _sincronizaVH(self,api,vh,conn):
        
       
        data = {'Code': "VH"+str(vh['id_vh'])}
        data['Estado']=api.retIdLookup('CI-Estado','NV')
        data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
        data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_Web['entorno'])
        data['DNS']=vh['dns']
        data['puerto']=str(vh['puerto']) 
        data['SSL']=str(vh['ssl'])
        data['requiereCertificado']=str(vh['rcert'])
        data['contCertificados']=vh['rutacert']
        if not vh['deleted']:
            if vh['_id'] == None:
                id_Class = api.creaClase('VirtualHost',data)
            else :
                id_Class = api.actualizaClase('VirtualHost',data,vh['_id'])
        else:
            id_Class = self._borraSoftWeb('VirtualHost',vh['_id'],api)
    
        return id_Class
    
    
    def sincroniza(self,conn,api,_idsw):
        '''
        Sincroniza un CI con CMDBuild
        
        Parametro
            conn:  Objeto de conexion con la BD SDA_DB
            api:  Objeto de conexion con CMDBuild
            _idws: Identificador en CMDBuild de la instancia de software
        '''  
        
        if not self.dic_Web['deleted']:    
            data = {'Code': "WEB"+str(self.dic_Web['id_web'])}          
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Entorno']= api.retIdLookup('CI-Entorno',self.dic_Web['entorno'])
            data['Version']= self.dic_Web['version']
            data['Home']= self.dic_Web['home']
            data['Usuario']= self.dic_Web['usuario']
            data['urlAdmin']= self.dic_Web['urladmin']
            if self.dic_Web['_id']==None:
                id_Class = api.creaClase('ServWeb',data)
                
            else :
                id_Class = api.actualizaClase('ServWeb',data,self.dic_Web['_id'])
            if id_Class <> None:
                conn.apuntaId('tb_servweb',id_Class,'id_si',self.id_si)
                conn.apuntaId('tb_softwareinstancia',id_Class,'id_si',self.id_si)
                data = {}
                data['_sourceType'] = "SoftwareInstalado"
                data['_sourceId'] = str(_idsw)
                data['_destinationId'] = id_Class
                data['_destinationType'] = "ServWeb"
                api.creaRelacion('SItoSoftInstancia',data)
                for vh in self.dic_Web['vh']:
                    id_class_vh = self._sincronizaVH(api, vh,conn)
                    if id_class_vh <> None:
                        conn.apuntaId('tb_vhost',id_class_vh,'id_vh',vh['id_vh'])
                        data = {}
                        data['_sourceType'] = "ServWeb"
                        data['_sourceId'] = id_Class
                        data['_destinationId'] = id_class_vh
                        data['_destinationType'] = "VirtualHost"
                        api.creaRelacion('ServWebToVH',data)
                        for url in vh['url']:
                            id_class_url = self._sincronizaUrl(api, url,conn)
                            if id_class_url <> None:
                                conn.apuntaId('tb_url',id_class_url,'id_url',url['id_url'])
                                data = {}
                                data['_sourceType'] = "url"
                                data['_sourceId'] = id_class_url
                                data['_destinationId'] = id_class_vh
                                data['_destinationType'] = "VirtualHost"
                                api.creaRelacion('urlToVH',data)   
        else:
            self._borraSoftWeb('ServWeb',self.dic_Web['_id'],api)
        return
    
    
    
      
      