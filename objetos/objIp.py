# -*- coding: utf-8 -*-
'''
Created on 14 mar. 2017

@author: jose
'''
import ipaddress
import time



class objIp(object):
    '''
    Representa un interface de red
    '''


    def __init__(self,ip='',mac='',mascara='',nombre='',tipoRed='OTR',net=0,_id=None,deleted=False,fsync=''):
        '''
        Constructor
        
        Parametros:
            ip: Ip del Interface
            mac: Dirección MAC del Interface
            mascara: Mascara condifurada
            nombre: Nombre del interface
            tipoRed: Tipo de red 
            net: idenficador de la red
            _id: Identificador de la Red en CMDBuild
            deleted: Indica si la red ha sido borrada
            fsync: Fecha de la última sincronización del CI
        '''
        self._id=_id
        self.nombre = nombre
        self.ip = ip
        self.mac = mac
        self.mascara = self._convertirIP(mascara) 
        self.tipoRed = tipoRed
        self.net = net
        self.deleted = deleted
        self.fsync=fsync


  
    def _convertirIP(self,m):
        
        if "." in m :
            mask= m 
        else :
            mask=ipaddress.IPv4Address(int(m,16)).__str__()
            
        return mask
    
    def _estaCargado(self):
        
        return self._id <> None

    def borraIntCMDB(self,api,conn,id_disp):
        '''
        Marca como borrado un Interfaz en CMDBuild
        
        Parametros:
        
            api: Conexión con CMDBuild
            conn: Conexión con la BD SDA_DB
            id_disp: Identificador del dispositivo
            
        Salida
            Indica si la tarea ha terminado correctamente
        '''
        
        ok = True
        if self._id <> None :
            data = {'deleted':'True'}
            ok = api.actualizaClase('Interface',data,self._id)
        sql = "delete from tb_Interface where id_disp=" + str(id_disp) + " and nombre ='"+self.nombre+"'" 
        conn.actualizaTabla(sql)
        
        return ok
     
    def grabaBBDD(self,conn,id_disp):
        '''
        Graba el objeto en la BD SDA_DB
        
        Parametros
        
            conn: Conexión con la BD SDA_DB
            id_disp: Identificador del servidor
        
        Salida 
        
            Indica si se ha modificado
        '''
        modificado = conn.grabaIPS(self,id_disp)

        return modificado
    
    def sincroniza (self,api,conn, id_disp,_id_Disp,ultimaSync):
        '''
        Sincroniza un Interfaz con CMDBuild
        
        Parametros:
        
            api: Conexión con CMDBuild
            conn: Conexión con la BD SDA_DB
            id_disp: Identificador del Dispositivo
            _id_Disp: Identificacion del Dispositivo en CMDBuild
            ultimaSync : Fecha de la última sincronización del CI
        '''
        
        if not self.deleted :
            data = {}
            data['Code'] = self.ip
            data['Description'] = self.ip
            data['Nombre'] = self.nombre
            data['Estado'] = api.retIdLookup('CI-Estado','NV')
            data['Tipo'] = api.retIdLookup('Interface-Tipo',self.tipoRed)
            data['MAC'] = self.mac
            data['IP'] = self.ip
            data['Mascara'] = self.mascara
            data['Carga'] = api.retIdLookup('CI-TipoCarga',"AU")
            if self._estaCargado()==False:
                id_class = api.creaClase('Interface',data)
                if  id_class > 0:
                    data = {}
                    data['_sourceType'] = "Dispositivo"
                    data['_sourceId'] = _id_Disp
                    data['_destinationId'] = id_class
                    data['_destinationType'] = "Interface"
                    api.creaRelacion('DispToInterfaces',data)
                    data['_sourceType'] = "Red"
                    data['_sourceId'] = conn.retCodeRed(self.net)
                    api.creaRelacion('RedToInterface',data)
                    sql = "update tb_Interface set _id =" + str(id_class) + " where id_disp = " + str(id_disp) +" and nombre ='"+self.nombre+"'"               
                    conn.actualizaTabla(sql) 
                    print (time.strftime("%c")+"-- Añadido el  Interfaz "+ self.nombre + " con la IP " + self.ip)
            else :
                if self.fsync > ultimaSync :
                    api.actualizaClase('Interface',data,self._id)
                    print (time.strftime("%c")+"-- Actualizado el  Interfaz "+ self.nombre + " con la IP " + self.ip)
        else:
            self.borraIntCMDB(api, conn,id_disp)
            print (time.strftime("%c")+"-- Borrado el  Interfaz "+ self.nombre + " con la IP " + self.ip)
        return
    
    
    