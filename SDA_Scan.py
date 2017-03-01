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
    args = parser.parse_args()  
    return args;

def inicio(param):
    nm = nmap.PortScanner()
    if (param.ip.len()>0) :
       result = nm.scan(param.ip)
    else:
       result = nm.scan(param.red)
    print result
    return result

if __name__ == '__main__':
    cmd_param=parametros()
    inicio(cmd_param)