'''
Created on 14 mar. 2017

@author: jose
'''
from objetos import bbdd

class objFS(object):
    '''
    classdocs
    '''


    def __init__(self, ids, montaje, size, tipo):
        '''
        Constructor
        '''
        self.montaje = montaje
        self.size = size
        self.tipo = tipo
            
    def grabaBBDD(self,conn,id_serv):
        conn.grabaFS(self,id_serv)
        return