# -*- coding: utf-8 -*-
'''
Created on 1 abr. 2017

@author: jose
'''
import time
from objetos import intSoft

class objSoft(object):
    '''
    Representa una instancia de software corriendo en un servidor
    '''


    def __init__(self,idsw='',cadRunning='',_id=None, deleted=False,fsync='01/01/01',idserv=0,conn=None,ultimasync):
        '''
        Constructor
        
        Parametros
            idsw: Identificador del software
            cadRunning : Cadena de busqueda del software
            _id: Identificador de software en CMDBUild
            deleted : Indica si está borrado
            fsync : Fecha de la última sincronización
            idserv: Identificador del Servidor
            conn: Conexion con SDA_DB
            ultimasync: Ultima sincronización que se realizó
            
        '''
        self._id = _id
        self.idsw = idsw
        self.cadRunning = cadRunning
        self.deleted = deleted
        self.fsync=fsync
        if idserv <> 0:
            dt,id_si = conn.retSofInstancia(idsw,idserv)
            if dt <> None:
                self.iswf=intSoft.intSoft(cs=conn.retCatSoftware(idsw)[0],idserv=idserv,sw=idsw,ent=dt[3],user=dt[2],home=dt[1],id_si=id_si,conn=conn,fsync=ultimasync)
            else:
                self.iswf= None
        return
    
    
    
    def grabaBBDD(self,conn,id_serv):
        
        '''
        Graba un objeto instancia de software en la BD SDA_DB
        Parametro
        
            conn :Conexión con BD
            id_serv: Identificador del Servidor
        
        Salida
            modificado: Indica si se ha modificado
        '''
        modificado = conn.grabaSw(self,id_serv)

        return modificado
    
    def borraSwCMDB(self,api,conn,id_serv):
        '''
        Marca como borrado el software en CMDBuild
        
        Parametros:
        
            api: Conexión con CMDBuild
            conn: Conexión con la BD SDA_DB
            id_serv: Identificador del dispositivo
            
        Salida
            Indica si la tarea ha terminado correctamente
        '''
        
        ok = True
        if self._id <> '' :
            data = {'deleted':'True'}
            ok = api.actualizaClase('SoftwareInstalado',data,self._id)
#        sql = "delete from tb_soft_running where id_sw="+str(self.idsw)+ " and id_serv="+str(id_serv)
#        conn.actualizaTabla(sql)
    
        return ok
      
    def _estaCargado(self):
        return self._id <>  None
    
    def sincroniza(self,api,conn,id_serv,_idServ,ultimaSync):  
        '''
        Sincroniza un Interfaz con CMDBuild
        
        Parametros:
        
            api: Conexión con CMDBuild
            conn: Conexión con la BD SDA_DB
            id_serv: Identificador del Servidor
            _idServ: Identificacion del Servidor en CMDBuild
            ultimaSync : Fecha de la última sincronización del CI
        '''

        if not self.deleted :
            data = {'Code': str(self.idsw)}
            data['Description']=conn.retDescSoftware(self.idsw)
            nombre = data['Description']
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")

            if not self._estaCargado() :
                id_class = api.creaClase('SoftwareInstalado',data)
                if  id_class > 0:
                    self._id=id_class
                    sql = "update tb_soft_running set _id =" + str(id_class) + " where id_serv = " + str(id_serv)+" and id_sw=" + str(self.idsw)
                    conn.actualizaTabla(sql) 
                    data = {}
                    data['_sourceType'] = "Servidor"
                    data['_sourceId'] = _idServ
                    data['_destinationId'] = id_class
                    data['_destinationType'] = "SoftwareInstalado"
                    api.creaRelacion('ServidorToSwInstalado',data)
                    data['_sourceType'] = "CatalogoSw"
                    data['_sourceId'] = conn.retIdCatalogoSw(self.idsw)
                    api.creaRelacion('CatalogoToSoftware',data)
                    print (time.strftime("%c")+"-- Añadido el  Software "+ nombre ) 
            else :
                if self.fsync > ultimaSync :
                    api.actualizaClase('SoftwareInstalado',data,self._id)
                    print (time.strftime("%c")+"-- Actualizado el  Software "+ nombre )
        else:
            self.borraSwCMDB(api, conn,id_serv)
            print (time.strftime("%c")+"-- Borrado el  Software "+ nombre )
        if self.iswf <> None:
            self.iswf.sincroniza(conn,api, self._id)
        return