# -*- coding: utf-8 -*-
'''
Created on 9 may. 2017

@author: JFS035
'''
from bs4 import BeautifulSoup
import requests 
import re

def descubre(host, puerto, user, password):
    
    dic= {}
    cabeceras = { 'Accept': '*/*','Content-Type': 'application/html' }
    url = 'http://'+host+':'+puerto+'/probe/sysinfo.htm'
    r = requests.post(url,headers = cabeceras ,auth=(user,password))
    html = BeautifulSoup(r.text, "html.parser")
    entradas = html.find_all('div',{'id':'contentBody'})
    dic['jvm'] = html.find('a', {'href':'http://java.sun.com/'}).contents[0].replace('\r\n','').replace('\t','')
    dic['version'] = entradas[0].contents[5].contents[4]
    url = 'http://'+host+':'+puerto+'/probe/datasources.htm'
    r = requests.post(url,headers = cabeceras ,auth=(user,password))
    html = BeautifulSoup(r.text, "html.parser")
    t_datasource= html.find('table',{'id':'global_resources'}).tbody.find_all('tr')
    dic['jdbc']=[]

    for datasource in t_datasource:
        dic_data={}
        columna=datasource.find_all('td')
        dic_data['esquema'] = columna[7].text
        dic_data['usuario'] = columna[6].text
        dic_data['nombre'] = columna[1].text
        dic['jdbc'].append(dic_data)
    
   
    return dic

def aplicacion(host, puerto, user, password):
    dic={}
    return dic

if __name__ == '__main__':
    descubre("megadesa.munimadrid.es","8080","administrator","megadesa")
    
    pass