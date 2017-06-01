# -*- coding: utf-8 -*-
'''
Created on 11 may. 2017

@author: JFS035
'''
from objetos import objssh
import time
import re
import socket
import simplejson as json
import requests


def compruebaConexion(ip,puerto):
    '''
    Comprueba que el software especificado escucha en el puerto indicado
    
    Parametros
        n_proceso : Cadena que se utiliza para detectar un software 
        ip : IP del servidor en proceso
    
    Salida
    
        True si correcto
     
    '''
    try :
        url="http://"+ip.strip()+":"+puerto
        conn = requests.get(url,data="HEAD")
        Correcto= ( "APACHE/" in conn.headers['Server'].upper() )
             
        
    except Exception, error:
        Correcto = False
        
    return Correcto

def _cargaDefecto ():
    f= open('/home/jose/workspace/PFG/plugins/apache.json')
    contenido=f.read()
    dic = json.loads(contenido)
    return dic

def _recDNS(dns,ip):
    
    if dns == '*' :
        dns=ip
    cad_dns=socket.gethostbyaddr(dns)[0]
        
    return cad_dns

def _obtenerRutaConfiguracion(c_ps):
    
    if c_ps=='':
        conf = '/etc/httpd/conf/httpd.conf'
    elif '-f' in c_ps :
        conf = c_ps.split('-f')[1]
        if c_ps[0]<>'/':
            if '-d' in c_ps:
                ruta = re.findall("([^ ]+)", c_ps.split('-d')[1])
                conf = ruta[0].strip() +"/"+ conf.strip()
    elif '-d' in c_ps:
        conf = c_ps.split('-d')[1].strip() + '/conf/httpd.conf'
        
    return conf

def descubre(host,user,password,port, c_ps):
    
    '''
    Prueba a descubrir un Servidor web apache
    
    Parametro
    
        host:Ip del servidor
        user: Usuario con permisos de administracion
        password: password del usuario
        port:puerto de escucha de la consola
        c_ps:Salida del comando ps 
    
    Salida 
    
        Diccionario con los datos del servidor
    '''

    if port  == 0:
        dic = _cargaDefecto()
        return dic
    dic={}
    conexSSH = objssh.objssh(host,user,password)
    
    try :
        conf_file = _obtenerRutaConfiguracion(c_ps)   
#        cad_vh = " awk '!/#/  {print $0}' <<<file>>>> |  awk '/VirtualHost /  {printf $0\";\"} /SSL/ {printf($0)} /KeyFile/ {printf $0} /<\/VirtualHost>/ {print \"||\"}'"
        cad_vh = "awk '!/#/  {print $0}' <<<file>>>> |  tr -d \"\n\" | grep -o \"VirtualHost.*<\""
        cad_vh=cad_vh.replace("<<<file>>>>",conf_file) 
        sal_vh = conexSSH.enviaComando(cad_vh, "(.*)")
        error =False
    except :
        print (time.strftime("%c")+"-- Error al conectar con el servidor " + host )
        error=True
    
    if not error:
        dic['admin']=''
        dic['vh']=[]
        for vh in sal_vh:
            if vh=='' : 
                continue
            dic_vh={}
            buff=re.findall('VirtualHost([^:]+):([^>]+)',vh)
            dic_vh['dns']=_recDNS(buff[0][0].strip(),host)
            dic_vh['puerto'] = buff[0][1]
            if  "SSLENABLE" in vh.upper():
                dic_vh['ssl'] = True
                buff=re.findall('KeyFile.*"([^"]+)',vh)
                dic_vh['rutacert']=buff[0]
                dic_vh['rcert']=re.search('SSLClientAuth[ ]+On',vh)
            l_url = re.findall('ProxyPass.*?(/[^\s]+)',vh)
            dic_vh['url']=[]
            for url in l_url:
                dic_url={}
                if '*' not in url :
                    dic_url['nombre']=url[1:]
                    dic_url['valor']=url
                    dic_url['tipo']='AC'
                    dic_vh['url'].append(dic_url.copy())
            dic['vh'].append(dic_vh.copy())    
    else :
        dic= None
            
    return dic

if __name__ == '__main__':
    descubre('webserverintradesa10.munimadrid.es','JFS035_ADM','password35',80,'')
    

