'''
Created on 14 mar. 2017

@author: jose
'''


class objIp(object):
    '''
    classdocs
    '''


    def __init__(self,ip='',mac='',mascara='',nombre='',tipoRed='OTR',net=0,_id=None):
        '''
        Constructor
        '''
        self._id=_id
        self.nombre = nombre
        self.ip = ip
        self.mac = mac
        self.mascara = mascara 
        self.tipoRed = tipoRed
        self.net = 0

    def estaCargado(self):
        
        return self._id <> None

    def grabaBBDD(self,conn,id_disp):
        conn.grabaIPS(self,id_disp)
        return
    
    def sincroniza (self,api,conn, id_disp,_id_Disp):
        
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
                api.creaRelacion('ServidorToInterface',data)
                data['_sourceType'] = "Red"
                data['_sourceId'] = self.net
                api.creaRelacion('RedToInterface',data)
                sql = "update tb_Interface set _id =" + str(id_class) + " where id_disp = " + str(id_disp)
                conn.actualizaTabla(sql) 
            else :
                return
        else :
            api.actualizaClase('Interface',data,self._id)
        return
    
    
    