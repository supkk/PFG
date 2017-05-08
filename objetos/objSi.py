# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''


class objSi(object):
    '''
    classdocs
    '''


    def __init__(self, _id='',id_si=0,id_sw=0,id_serv=0,id_entorno='PRO',version='',usuario='',ip='',user='',home=''):
        '''
        Constructor
        '''
        self._id=_id
        self.id_si=id_si
        self.id_sw=id_sw
        self.id_serv=id_serv
        self.id_entorno=id_entorno
        self.version=version
        self.home=home
        self.usuario=usuario
        self.ip = ip
        self.user=user

        
        return
    
    def grabaBBDD(self,conn):
        
        Modificado = True
        
       
        return Modificado
        