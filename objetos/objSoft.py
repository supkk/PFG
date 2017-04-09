'''
Created on 1 abr. 2017

@author: jose
'''

class objSoft(object):
    '''
    classdocs
    '''


    def __init__(self,idsw='',cadRunning='',_id=0, deleted=False):
        '''
        Constructor
        '''
        self._id = _id
        self.idsw = idsw
        self.cadRunning = cadRunning
        self.deleted = deleted
        return
    
    def grabaBBDD(self,conn,id_serv):
        modificado = conn.grabaSw(self,id_serv)
        return modificado
    
    def estaCargado(self):
        return self._id <>  None
    
    def sincroniza(self,api,conn,id_serv,_idServ):  
        
        data = {'Code': str(self.idsw)}
        data['Description']=conn.retDescSoftware(self.idsw)
        data['Estado']=api.retIdLookup('CI-Estado','NV')
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
        else :
            api.actualizaClase('SoftwareInstalado',data,self._id)
        return