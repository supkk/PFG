# -*- coding: utf-8 -*-
'''
Created on 9 may. 2017

@author: JFS035
'''
from bs4 import BeautifulSoup
import requests 
import re


def compruebaConexion(ip,puerto):
    try :
        url="http://"+ip.strip()+":"+puerto
        conn = requests.get(url,data="HEAD")
        Correcto= ("COYOTE" in conn.headers['Server'].upper() )
             
        
    except Exception, error:
        Correcto = False
        
    return Correcto


def retBDyEqm(cad_conex):
    bd=''
    eqm=''
    
    return bd, eqm
def descubre(host, user, password,puerto):
    
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
        dic['jdbc']=[]
        if "There are no data sources" not in r.text:
            html = BeautifulSoup(r.text, "html.parser")  
            t_datasource= html.find('table',{'id':'global_resources'}).tbody.find_all('tr')
            for datasource in t_datasource:
                dic_data={}
                columna=datasource.find_all('td')
                dic_data['nombre_bd'],dic_data['esquema'] = retBDyEqm(columna[7].text)
                dic_data['usuario'] = columna[6].text
                dic_data['nombre'] = columna[1].text
                dic['jdbc'].append(dic_data.copy())
        else :
    #           Solo para probar
            dic_data={}
            dic_data['nombre_bd']='cmdbuild'
            dic_data['esquema']='public'
            dic_data['usuario']='postgres'
            dic_data['nombre']='cmdbuild'
            dic['jdbc'].append(dic_data.copy())
            dic_data['nombre_bd']='cmdbuild'
            dic_data['esquema']='shark'
            dic_data['usuario']='postgres'
            dic_data['nombre']='shark'
            dic['jdbc'].append(dic_data.copy())
    except :
        dic = None
   
    return dic

def aplicacion(host, puerto, user, password):
    dic={}
    return dic

