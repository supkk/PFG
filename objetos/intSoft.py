# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''
from objetos import objSoftWeb
from objetos import objSoftBBDD
from objetos import objSoftSapl

class intSoft(object):
    '''
    classdocs
    '''


    def __init__(self, cs='', idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home=''):
        '''
        Constructor
        '''
        
        if cs == 'SWEB' :
            self.o = objSoftWeb.objSoftWeb(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home)
        elif cs == 'SAPL':
            self.o = objSoftSapl.objSoftSapl(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home)
        elif cs == 'BBDD':
            self.o = objSoftBBDD.objSoftBBDD(idserv=idserv,sw=sw,ent=ent,ip=ip,soft=soft,user=user,port=port,home=home)
        else :
            self.o=None
            
    def descubre(self):
        self.o.descubre()
        return
    
    def grabaBBDD(self):
        self.o.grabaBBDD()
        return 


                
        