# -*- coding: utf-8 -*-
'''
Created on 9 may. 2017

@author: JFS035
'''
from bs4 import BeautifulSoup
import requests 
import simplejson as json
import re
import time


def compruebaConexion(ip,puerto):
    '''
    Comprueba que el software especificado escucha en el puerto indicado
    
    Parametros
        ip : IP del servidor en proceso
        puerto: Puerto de escucha
    
    Salida
    
        True si correcto
     
    '''
    try :
        url="http://"+ip.strip()+":"+puerto
        conn = requests.get(url,data="HEAD")
        Correcto= ("COYOTE" in conn.headers['Server'].upper() )
             
        
    except Exception, error:
        Correcto = False
        
    return Correcto


def _retBDyEqm(cad_conex,user):
    if 'oracle' in cad_conex:
        patron='.*SERVICE_NAME=(.*?)\)'
        res=re.findall(patron,cad_conex,re.DOTALL)
        bd=res[0]
        eqm=user
        host=''
    
    return bd, eqm, host


def descubre(host, user, password,puerto):
    '''
    Prueba a descubrir un Servidor tomcat
    
    Parametro
    
        host:Ip del servidor
        user: Usuario con permisos de administracion
        password: password del usuario
        port:puerto de escucha de la consola
        c_ps:Salida del comando ps 
    
    Salida 
    
        Diccionario con los datos del servidor
    '''
    dic= {}
    host=host.strip()
    cabeceras = { 'Accept': '*/*','Content-Type': 'application/html' }
    url = 'http://'+host+':'+puerto+'/probe/sysinfo.htm'
    try :
        r = requests.get(url,headers = cabeceras ,auth=(user,password))
        html = BeautifulSoup(r.text, "html.parser")
        entradas = html.find_all('div',{'id':'contentBody'})
        dic['jvm'] = html.find('a', {'href':'http://java.oracle.com/'}).contents[0].replace('\r\n','').replace('\t','')
        dic['version'] = entradas[0].contents[5].contents[4].strip()
        url = 'http://'+host+':'+puerto+'/probe/datasources.htm'
        r = requests.get(url,headers = cabeceras ,auth=(user,password))
        print (time.strftime("%c")+"--"+"Descubierto servidor Tomcat version "+dic['version'] )
        dic['jdbc']=[]
        if "There are no data sources" not in r.text:
            html = BeautifulSoup(r.text, "html.parser")  
            t_datasource= html.find('table',{'id':'global_resources'}).tbody.find_all('tr')
            for datasource in t_datasource:
                dic_data={}
                columna=datasource.find_all('td')
                dic_data['nombre_bd'],dic_data['esquema'],dic_data['host']= _retBDyEqm(columna[7].attrs['title'],columna[6].text)
                dic_data['usuario'] = columna[6].text
                dic_data['nombre'] = columna[1].text.strip()
                dic['jdbc'].append(dic_data.copy())
                print (time.strftime("%c")+"--"+"Descubierto servidor DataSource "+ dic_data['nombre'])
        else :
    #           Solo para probar
            dic_data={}
            dic_data['nombre_bd']='cmdbuild'
            dic_data['esquema']='public'
            dic_data['usuario']='postgres'
            dic_data['nombre']='cmdbuild'
            dic_data['host']='192.168.1.29'
            dic['jdbc'].append(dic_data.copy())
            dic_data['nombre_bd']='cmdbuild'
            dic_data['esquema']='shark'
            dic_data['usuario']='postgres'
            dic_data['nombre']='shark'
            dic_data['host']='192.168.1.29'
            dic['jdbc'].append(dic_data.copy())
    except :
        dic = None
   
    return dic

def descubreAplicacion(host,user, password,puerto):
    '''
    Prueba a descubrir aplicaciones en un Servidor tomcat
    
    Parametro
    
        host:Ip del servidor
        user: Usuario con permisos de administracion
        password: password del usuario
        port:puerto de escucha de la consola
        c_ps:Salida del comando ps 
    
    Salida 
    
        Diccionario con los datos de las aplicaciones
    '''
    if puerto == 0:
        f= open('/home/jose/workspace/PFG/plugins/apl.json')
        contenido=f.read()
        dic = json.loads(contenido)
    else :
        dic ={'apl':[]}
        dic_t={}
        host = host.strip()
        cabeceras = { 'Accept': '*/*','Content-Type': 'application/html' }
        url = 'http://'+host+':'+puerto+'/probe/datasources.htm'
        try :
            r = requests.get(url,headers = cabeceras ,auth=(user,password))
            html = BeautifulSoup(r.text, "html.parser")
            tabla= html.find('table',{'id':'app_resources'}).tbody.find_all('tr')
            
            for entrada in tabla :
                dic_apl={}
                dic_url={}
                dic_jdbc=[]
                columna=entrada.find_all('td')
                app = str(columna[1].text[1:].strip())
                dic_apl['acronimo']=app
                dic_apl['nombre']= app
                dic_apl['version']=''
                dic_url['valor']= app
                dic_url['tipo']='AC'
                dic_apl['url']=[dic_url.copy()]
                jdbc=columna[2].text.strip()
                dic_jdbc.append(jdbc[5:])
                dic_apl['jdbc']=dic_jdbc
                dic['apl'].append(dic_apl.copy())
            
        except Exception, error : 
            print error
    return dic

if __name__ == '__main__':
    
    descubreAplicacion('megadesa.munimadrid.es','administrator','megadesa','8080')
