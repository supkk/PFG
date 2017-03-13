'''
Created on 13 mar. 2017

@author: jose
'''

class objServidor(object):
    '''
    classdocs
    '''

    
    def __init__(self, nombre,so,ram,sf,ips,sw):
        '''
        Constructor
        '''
        self.nombre=nombre
        self.so = so
        self.ram = ram
        self.sf = []
        self.ips = []
        self.sw = []
        
    def anade_FS(self,fs):
        self.sf.append(fs)
        return
        
    def anade_IP(self,ip):
        self.ips.append(ip)
        return
    
    def anade_SW(self,soft):
        self.sw.append(soft)
        return
    
    def grabarBBDD(self):
        return