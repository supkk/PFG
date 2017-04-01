'''
Created on 4 mar. 2017

@author: jose
'''
import socket

class ObjDispositivo(object):
    '''
    classdocs
    '''
    
    def __init__(self, ip,fd,td,nombre,os):
        '''
        Constructor
        '''
        self.ip=ip
        self.fd=fd
        self.td=td
        self.nombre=nombre
        self.os=os
        self.indice=socket.inet_aton(ip)
        self.apagado = 0
        
        return
        
    def update(self,s):
        if self.fd =='' :
            self.fd=s.fd 
        if self.td =='' :
            self.td=s.td 
        if self.nombre =='' :
            self.nombre =s.nombre 
        if self.os =='' :
            self.os=s.os     
        
        return