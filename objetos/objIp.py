'''
Created on 14 mar. 2017

@author: jose
'''



class objIp(object):
    '''
    classdocs
    '''


    def __init__(self,ip='',mac='',mascara='',nombre='',tipoRed='OTR',net=0,_id=None,deleted=False,fsync=''):
        '''
        Constructor
        '''
        self._id=_id
        self.nombre = nombre
        self.ip = ip
        self.mac = mac
        self.mascara = mascara 
        self.tipoRed = tipoRed
        self.net = net
        self.deleted = deleted
        self.fsync=fsync

    def estaCargado(self):
        
        return self._id <> None

    def borraIntCMDB(self,api,conn):
        
        ok = True
        if self._id <> '' :
            data = {'deleted':'True'}
            ok = api.actualizaClase('Interface',data,self._id)
        sql = "delete from tb_Interface where _id="+str(self._id)
        conn.actualizaTabla(sql)
        
        return ok
     
    def grabaBBDD(self,conn,id_disp):
        modificado = conn.grabaIPS(self,id_disp)
        return modificado
    
    def sincroniza (self,api,conn, id_disp,_id_Disp,ultimaSync):
        

        
        if not self.deleted :
            data = {}
            data['Code'] = self.ip
            data['Description'] = self.ip
            data['Nombre'] = self.nombre
            data['Estado'] = api.retIdLookup('CI-Estado','NV')
            data['Tipo'] = api.retIdLookup('InterfaceTipo',self.tipoRed)
            data['MAC'] = self.mac
            data['IP'] = self.ip
            data['Mascara'] = self.mascara
            if self.estaCargado()==False:
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
            else :
                if self.fsync > ultimaSync :
                    api.actualizaClase('Interface',data,self._id)
        else:
            self.borraIntCMDB(api, conn)
        
        return
    
    
    