# -*- coding: utf-8 -*-
'''
Created on 27 mar. 2017

@author: jose
'''
import requests 
import simplejson as json
import time

class cmdbuild(object):
    '''
    classdocs
    '''


    def __init__(self, host,puerto, user, password):
        '''
        Constructor
        '''
        self.cabeceras = { 'Accept': '*/*','Content-Type': 'application/json' }
        data = '{"username":"'+user+'","password":"'+password+'"}'
        self.url = 'http://'+host+':'+puerto+'/cmdbuild/services/rest/v1/'
        r = requests.post(self.url+"sessions",headers = self.cabeceras ,data=data)
        resultado=json.loads(r.text)
        self.cabeceras['CMDBuild-Authorization'] = resultado['data']['_id']

        return
    
    def creaClase(self,clase,attr):
        
        uri = self.url+"classes/"+clase+"/cards/"
        data = str(attr)
        data = data.replace('\'', '"')
        data = data.replace('False','false')
        data = data.replace('True','true')
        r = requests.post(uri,headers = self.cabeceras, data=data)
        if r.ok :
            result = json.loads(r.text)['data']
            print (time.strftime("%c")+"-- Nueva clase "+ clase + " CODIGO " + data )
        else :   
            print (time.strftime("%c")+"-- Error al sincronizar la Nueva clase "+ clase + " CODIGO " + data )
            result = -1
            
        return result
    
    def actualizaClase(self,clase,attr,idclass):
        
        uri = self.url+"classes/"+clase+"/cards/"+str(idclass)
        data = str(attr)
        data = data.replace('\'', '"')
        data = data.replace('False','false')
        data = data.replace('True','true')
        r = requests.put(uri,headers = self.cabeceras, data=data)
        
        if r.ok :
            print (time.strftime("%c")+"-- Actualizada clase "+ clase + " CODIGO "+str(idclass) )
            result = idclass
        else:
            print (time.strftime("%c")+"-- Error al Actualizar la  clase "+ clase + " CODIGO "+str(idclass) )
            result = None
            
        return result
    
    def creaRelacion(self,dominio,attr):
        
        uri = self.url+"domains/" + dominio + "/relations/"
        data = str(attr)
        data = data.replace('\'', '"')
        r = requests.post(uri,headers = self.cabeceras, data=data)
        if r.ok :
            result = json.loads(r.text)['data']
            print (time.strftime("%c")+"-- Creada relacion con "+attr['_destinationType']  )
        else :  
            result = -1
        return result
    
    def actualizaRelacion(self,dominio,attr,idomain): 
        
        uri = self.url+"domains/"+dominio+"/relations/"+str(idomain)
        data = str(attr)
        data = data.replace('\'', '"')
        r = requests.put(uri,headers = self.cabeceras, data=data)
        
        return r.ok
    
    def  retIdLookup(self,name, ele):
        
        idLookup=''
        uri = self.url+"lookup_types/"+name+"/values"
        r = requests.get(uri,headers = self.cabeceras)
        resultado=json.loads(r.text)
        for l in resultado["data"] :
            if l['code'] == ele.strip() :
                idLookup = l['_id'] 
                break
                            
        return idLookup
    
if __name__ == '__main__':
    conn = cmdbuild("192.168.1.41","admin","admin")
    data = {"Code":"PR8","nombreDisp":"Prueba5"}
    r=conn.creaClase("Servidor", data)
    data = {"Code":"PR5","nombreDisp":"Prueba6","Estado":281}
    r=conn.actualizaClase("Servidor", data,r)
    
    print r
    
     