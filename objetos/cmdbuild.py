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
    Clase que se encarga de la comunicacion con CMDBuild
    '''


    def __init__(self, host,puerto, user, password):
        '''
        Constructor
        host: Ip de la Instancia de CMDBUild
        puerto: Puerto de escucha
        user: usuario de acceso a CMDBuild
        password: password del usuario
        '''
        self.cabeceras = { 'Accept': '*/*','Content-Type': 'application/json' }
        data = '{"username":"'+user+'","password":"'+password+'"}'
        self.url = 'http://'+host+':'+puerto+'/cmdbuild/services/rest/v1/'
        r = requests.post(self.url+"sessions",headers = self.cabeceras ,data=data)
        resultado=json.loads(r.text)
        self.cabeceras['CMDBuild-Authorization'] = resultado['data']['_id']

        return
    
    def creaClase(self,clase,attr):
        '''
        Crea una instancia de una clase en CMDBuild
        
        Parametro
        
        clase: Nombre de la clase
        attr: Atributos de la clase
        
        salida 
        
        Identificador de la clase en CMDBuild, si falla -1
        '''
        
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
        
        '''
        Actualiza una instancia de una clase en CMDBuild
        
        Parametro
        
        clase: Nombre de la clase
        attr: Atributos de la clase
        idclass :: Identificador de la clase a actualizar
        
        salida 
        
        Identificador de la clase en CMDBuild, si falla None
        '''
        
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
        '''
        Crea una relacion entre dos clases en CMDBuild
        
        Parametro
        
        dominio: Nombre de la relacion
        attr: Atributos de la relacion
        
        salida 
        
        Identificador de la clase en CMDBuild, si falla -1
        '''
        
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
        
        '''
        Actualiza una relacion entre dos clases en CMDBuild
        
        Parametro
        
        dominio: Nombre de la relacion
        attr: Atributos de la relacion
        idomain: Identificador de dominio
        
        salida 
        
        Correcto (true )o No (False
        '''
        
        uri = self.url+"domains/"+dominio+"/relations/"+str(idomain)
        data = str(attr)
        data = data.replace('\'', '"')
        r = requests.put(uri,headers = self.cabeceras, data=data)
        
        return r.ok
    
    def  retIdLookup(self,name, ele):
        
        '''
        Retorna el identificador, en CMDBuild, atributo de tipo lookup
        
        Parametro
        
        name: Nombre del tipo Lookup
        ele : Elemento a buscar
        
        Salida
        
        Identificador del elemento en CMDBuild
        '''
        
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
    
     