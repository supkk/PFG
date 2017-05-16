# -*- coding: utf-8 -*-
'''
Created on 27 mar. 2017

@author: jose
'''
import requests 
import simplejson as json

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
        r = requests.post(uri,headers = self.cabeceras, data=data)
        if r.ok :
            result = json.loads(r.text)['data']
        else :   
            result = -1
            
        return result
    
    def actualizaClase(self,clase,attr,idclass):
        
        uri = self.url+"classes/"+clase+"/cards/"+str(idclass)
        data = str(attr)
        data = data.replace('\'', '"')
        r = requests.put(uri,headers = self.cabeceras, data=data)
        result = None
        if r.ok :
            result = idclass
            
        return result
    
    def creaRelacion(self,dominio,attr):
        
        uri = self.url+"domains/" + dominio + "/relations/"
        data = str(attr)
        data = data.replace('\'', '"')
        r = requests.post(uri,headers = self.cabeceras, data=data)
        if r.ok :
            result = json.loads(r.text)['data']
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
    
     