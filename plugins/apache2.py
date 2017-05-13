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
    try :
        url="http://"+ip.strip()+":"+puerto
        conn = requests.get(url,data="HEAD")
        Correcto= ( "APACHE/" in conn.headers['Server'].upper() )
             
        
    except Exception, error:
        Correcto = False
        
    return Correcto

def cargaDefecto ():
    f= open('/home/jose/workspace/PFG/plugins/apache.json')
    contenido=f.read()
    dic = json.loads(contenido)
    return dic

def recDNS(dns,ip):
    
    if dns == '*' :
        dns=ip
    cad_dns=socket.gethostbyaddr(dns)
        
    return cad_dns

def obtenerRutaConfiguracion(c_ps):
    
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
    
    if port  <> 0:
        dic = cargaDefecto()
        return dic
    dic={}
    conexSSH = objssh.objssh(host,user,password)
    
    try :
        conf_file = obtenerRutaConfiguracion(c_ps)   
        cad_vh = " awk '!/#/  {print $0}' <<<file>>>> |  awk '/VirtualHost /  {printf $0\";\"} /SSL/ {printf($0)} /KeyFile/ {printf $0} /<\/VirtualHost>/ {print \"||\"}'"
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
            dic_vh={}
            buff=re.findall('VirtualHost([^:]+):([^>]+)',sal_vh)
            dic_vh['dns']=recDNS(buff[0],host)
            dic_vh['puerto'] = buff[1]
            if  "SSLENABLE" in vh.upper():
                dic_vh['ssl'] = True
                buff=re.findall('KeyFile.*"([^"]+)',vh)
                dic_vh['rutacert']=buff[0]
                dic_vh['rcert']=re.search('SSLClientAuth[ ]+On',vh)
    else :
        dic= None
            
    return dic

if __name__ == '__main__':
    cmd_ps = "svcwas    6616  6567  0 May09 ?        00:00:00 /opt/IBM/HTTPServer85/HTTPServer/bin/httpd -d /opt/IBM/HTTPServer85/HTTPServer -k start -f conf2/httpd.conf"
    Descubre('10.90.55.116','JFS035_ADM','password35',0,cmd_ps)
    pass