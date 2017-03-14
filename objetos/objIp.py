'''
Created on 14 mar. 2017

@author: jose
'''
from objetos import bbdd


class objIp(object):
    '''
    classdocs
    '''


    def __init__(self, ip,mac,red,mascara,enlace,broadcast):
        '''
        Constructor
        '''
        self.ip = ip
        self.mac = mac
        self.red = red
        self.mascara = mascara 
        self.enlace = enlace
        self.broadcast = broadcast
        
    def grabarBBDD(self,conn,id_serv):
        conn.grabaIPS()
        return