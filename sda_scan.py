# -*- coding: utf-8 -*-
'''
Created on 1 mar. 2017

@author: jose
'''
import nmap
import argparse
import time
from objetos.objDispositivo import ObjDispositivo
from objetos.bbdd import bbdd
import simplejson as json



def parametros():
    '''
    Procesa la linea de comandos del script y construye un objeto argparse. Tambien carga los ficheros de configuracion
     
    Salida 
     
       cnf : Diccionario con los parametros de configuracion
       args: Objeto con los pararámetros que se pasan al script  
    '''
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--ip" ,help="Descubre solo una IP" )
    group.add_argument("-r", "--red",help="Descubre toda una red"  )
    parser.add_argument("-c","--conf",help="ruta del fichero de configuración",default='./conf/config.json')
    args = parser.parse_args()  
    cnf =  json.loads(open(args.conf).read())
    return cnf,args;

def obtener_dispositivo(d):
    '''
    Carga en el objeto ObjDispositivo una Ip descubierta por nmap
    
    Parametro
        d : Objeto descubierto por nmap
        s : Objeto Dispositivo
        
    
    '''
    
    os="NO DESCUBIERTO"
    if 'tcp' in d.keys():
        if 22 in d['tcp'].keys():
            os="LINUX"
        elif 135 in d['tcp'].keys():
            os="WINDOWS"
              
    s=ObjDispositivo(d['addresses']['ipv4'],time.strftime("%c"),'NMAP',d['hostnames'][0]['name'][:25],os)   
    return s

def scan_NMAP(param,conf):
    '''
    Realiza un escaneo de la red para descubrir las IP que están activas
    
    Parametros
    
    param: Objeto con los pararámetros que se pasan al script
    conf: diccionario con la  configuración de BBDD
    
    '''
    
    print (time.strftime("%c")+"--"+"Inicio de  descubrimiento por nmap")
    try:
        
        nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
    except nmap.PortScannerError:
        print(time.strftime("%c")+"--"+'Nmap not found')
        return ""
    except:
        print(time.strftime("%c")+"--"+"Unexpected error:")
        return ""
    if type(param.ip)== str :
        result = nm.scan(param.ip)
    else:
        result = nm.scan(param.red)
    conn = bbdd(bd=conf['bd'],u=conf['user'],pw=conf['password'],h=conf['host'],p=conf['port'])
    for s in result['scan']  :
        disp = obtener_dispositivo(result['scan'][s])
        if not conn.insertaDisp(disp):
            print (time.strftime("%c")+"--"+"Ya existe la IP "+disp.ip)
        else:
            print (time.strftime("%c")+"--"+"Descubierta la IP "+disp.ip)
    conn.cierraDB()
    print (time.strftime("%c")+"--"+"Descubrimiento NMAP terminado")
    return 

if __name__ == '__main__':
    conf,cmd_param=parametros()
    scan_NMAP(cmd_param,conf['BaseDatos'])
  
    
    
    
    