'''
Created on 14 mar. 2017

@author: jose
'''

class objFS(object):
    '''
    classdocs
    '''


    def __init__(self, _id=None, montaje='', size=0, tipoFs='',tipoAl=''):
        '''
        Constructor
        '''
        self._id=_id
        self.montaje = montaje
        self.size = size
        self.tipoFs = tipoFs
        self.tipoAl = tipoAl
        
            
    def grabaBBDD(self,conn,id_serv):
        conn.grabaFS(self,id_serv)
        return