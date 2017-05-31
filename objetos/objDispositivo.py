# -*- coding: utf-8 -*-
'''
Created on 4 mar. 2017

@author: jose
'''
import socket

class ObjDispositivo(object):
    '''
    Representa un dispositivo, servidor, router o electronica de red
    '''
    
    def __init__(self, ip,fd,td,nombre,os):
        '''
        Constructor
        
        Parametros
        
        ip: Ip del dispositivo
        fd: Fecha de descubrimiento
        td: Tipo de descubrimiento empleado
        nombre: Nombre del dispositivo
        os: Código de Sistema Operativo
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
        
        '''
        Actualiza los atributos  del objeto 
        
        Parametro:
        s: datos a actualizar
        
        '''
        if self.fd =='' :
            self.fd=s.fd 
        if self.td =='' :
            self.td=s.td 
        if self.nombre =='' :
            self.nombre =s.nombre 
        if self.os =='' :
            self.os=s.os     
        
        return