# -*- coding: utf-8 -*-
'''
Created on 1 abr. 2017

@author: jose
'''
import time
from objetos import intSoft
from objetos import bbdd
 

class objSoft(object):
    '''
    classdocs
    '''


    def __init__(self,idsw='',cadRunning='',_id=None, deleted=False,fsync='01/01/01',idserv=0,conn=None,ultimasync='01/01/01'):
        '''
        Constructor
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
        modificado = conn.grabaSw(self,id_serv)

        return modificado
    
    def borraSwCMDB(self,api,conn,id_serv):
        
        ok = True
        if self._id <> '' :
            data = {'deleted':'True'}
            ok = api.actualizaClase('SoftwareInstalado',data,self._id)
#        sql = "delete from tb_soft_running where id_sw="+str(self.idsw)+ " and id_serv="+str(id_serv)
#        conn.actualizaTabla(sql)
    
        return ok
      
    def estaCargado(self):
        return self._id <>  None
    
    def sincroniza(self,api,conn,id_serv,_idServ,ultimaSync):  
        

        if not self.deleted :
            data = {'Code': str(self.idsw)}
            data['Description']=conn.retDescSoftware(self.idsw)
            nombre = data['Description']
            data['Estado']=api.retIdLookup('CI-Estado','NV')
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")

            if not self.estaCargado() :
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