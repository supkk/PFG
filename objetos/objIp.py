'''
Created on 14 mar. 2017

@author: jose
'''


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
        
    def grabaBBDD(self,conn,id_serv):
        conn.grabaIPS(self,id_serv)
        return