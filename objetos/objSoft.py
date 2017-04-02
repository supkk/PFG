'''
Created on 1 abr. 2017

@author: jose
'''

class objSoft(object):
    '''
    classdocs
    '''


    def __init__(self,_id,cadRunning):
        '''
        Constructor
        '''
        self._id = _id
        self.cadRunning = cadRunning
        return
    
    def grabaBBDD(self,conn,id_serv):
        conn.grabaSw(self,id_serv)
        return
        