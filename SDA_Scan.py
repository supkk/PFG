'''
Created on 1 mar. 2017

@author: jose
'''
import nmap;
import argparse;


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
        result = nm.scan(param.ip, arguments='-O')
    else:
        result = nm.scan(param.red)
    print ("Descubrimiento NMAP terminado")
    return result

if __name__ == '__main__':
    ls=[]
    cmd_param=parametros()
    scan_NMAP(cmd_param)