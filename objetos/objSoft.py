'''
Created on 1 abr. 2017

@author: jose
'''

class objSoft(object):
    '''
    classdocs
    '''


    def __init__(self,cadRunning):
        '''
        Constructor
        '''
        self.cadRunning = cadRunning
        return
    
    def grabaBBDD(self,conn,id_serv):
        conn.grabaSw(self,id_serv)
        return
        