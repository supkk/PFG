'''
Created on 14 mar. 2017

@author: jose
'''

class objFS(object):
    '''
    classdocs
    '''


    def __init__(self,  montaje='', size=0, tipoFs='',tipoAl='',_id=None):
        '''
        Constructor
        '''
        self._id=_id
        self.montaje = montaje
        self.size = size
        self.tipoFs = tipoFs
        self.tipoAl = tipoAl
        
    def estaCargado(self):
        
        return self._id <> None
    
    def sincroniza(self,api, conn,id_serv, _ids):

        data = {}
        data['Code'] = self.montaje
        data['PM'] = self.montaje
        data['Description'] = self.montaje
        data['Capacidad'] = int(self.size/1000)
        data['Estado'] = api.retIdLookup('CI-Estado','NV')
        data['TipoM'] = api.retIdLookup('FileSystemTipoAlmacenamiento',self.tipoAl)
        data['TipoFS'] = api.retIdLookup('FileSystemTipo',self.tipoFs)
        
        if self.estaCargado()==False:
            id_class = api.creaClase('FS',data)

            if  id_class > 0:
                data = {}
                data['_sourceType'] = "Servidor"
                data['_sourceId'] = _ids
                data['_destinationId'] = id_class
                data['_destinationType'] = "FS"
                sql = "update tb_fs set _id =" + str(id_class) + " where id_serv = " + str(id_serv)+ " and montaje = '" +self.montaje + "'"
                api.creaRelacion('ServidorToFileSystem',data)
                conn.actualizaTabla(sql) 
            else :
                return
        else :
            api.actualizaClase('FS',data,self._id)
        return
            
    def grabaBBDD(self,conn,id_serv):
        conn.grabaFS(self,id_serv)
        return