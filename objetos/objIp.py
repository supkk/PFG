'''
Created on 14 mar. 2017

@author: jose
'''


class objIp(object):
    '''
    classdocs
    '''


    def __init__(self, ip,mac,mascara,nombre,tipoRed):
        '''
        Constructor
        '''
        self._id=0
        self.nombre = nombre
        self.ip = ip
        self.mac = mac
        self.mascara = mascara 
        self.tipoRed = tipoRed
        self.net = 0

    def grabaBBDD(self,conn,id_disp):
        conn.grabaIPS(self,id_disp)
        return