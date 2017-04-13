# -*- coding: utf-8 -*-
'''
Created on 1 mar. 2017

@author: jose
'''
import nmap
import argparse
import time
from objetos.listServer import listServer
from objetos.objDispositivo import ObjDispositivo


def parametros():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Descubre elementos de red", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--ip"  )
    group.add_argument("-r", "--red"  )
    parser.add_argument("-p","--Pantalla",action="store_true")
    parser.add_argument("-b","--bbdd",help="Cadena de conexion a BBDD")
    args = parser.parse_args()  
    return args;

def obtener_dispositivo(d):
    
    os="NO DESCUBIERTO"
    if 'tcp' in d.keys():
        if 22 in d['tcp'].keys():
            os="LINUX"
        elif 135 in d['tcp'].keys():
            os="WINDOWS"
              
    s=ObjDispositivo(d['addresses']['ipv4'],time.strftime("%c"),'NMAP',d['hostnames'][0]['name'][:25],os)   
    return s

def scan_NMAP(param):
    print ("Intentando el descubrimiento por nmap")
    try:
        
        nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
    except nmap.PortScannerError:
        print('Nmap not found')
        return ""
    except:
        print("Unexpected error:")
        return ""
    if type(param.ip)== str :
        result = nm.scan(param.ip)
    else:
        result = nm.scan(param.red)
    print ("Descubrimiento NMAP terminado")
    
    for s in result['scan']  :
        disp = obtener_dispositivo(result['scan'][s])
        ls.insert_or_update(disp)
    return ls

if __name__ == '__main__':
    ls=listServer([])
    cmd_param=parametros()
    ls=scan_NMAP(cmd_param)
    ls.grabarBBDD()
    
    
    
    