'''
Created on 14 mar. 2017

@author: jose
'''


class objIp(object):
    '''
    classdocs
    '''


    def __init__(self, ip,mac,mascara,nombre):
        '''
        Constructor
        '''
        self._id=0
        self.class_code = ''
        self.nombre = nombre
        self.ip = ip
        self.mac = mac
        self.mascara = mascara 
        self.TipoRed = ''
        self.net = 0

    def grabaBBDD(self,conn,id_serv):
        conn.grabaIPS(self,id_serv)
        return