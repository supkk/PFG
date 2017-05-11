'''
Created on 11 may. 2017

@author: JFS035
'''
from objetos import objssh
import time
import re

def obtenerRutaConfiguracion(c_ps):
    if c_ps=='':
        conf = '/etc/httpd/conf/httpd.conf'
    elif '-f' in c_ps :
        conf = c_ps.split('-f')[1]
        if c_ps[0]<>'/':
            if '-d' in c_ps:
                ruta = re.findall("([^ ]+)", c_ps.split('-d')[1])
                conf = ruta +"/"+ conf
    elif '-d' in c_ps:
        conf = c_ps.split('-d')[1] + '/conf/httpd.conf'
        
    return conf

def Descubre(ip,user,password,port, c_ps):
    
    dic={}
    conexSSH = objssh.objssh(ip,user,password)
    
    try :
        conf_file = obtenerRutaConfiguracion(c_ps)   
        cad_vh = " awk '!/#/  {print $0}' <<<file>>>>|  awk '/VirtualHost /  {printf $0\";\"} /SSL/ {printf($0)} /KeyFile/ {printf $0} /<\/VirtualHost>/ {print \"||\"}'".sub("<<<file>>>>",conf_file) 
    except :
        print (time.strftime("%c")+"-- Error al conectar con el servidor " + ip )
    return dic

if __name__ == '__main__':
    cmd_ps = "svcwas    6616  6567  0 May09 ?        00:00:00 /opt/IBM/HTTPServer85/HTTPServer/bin/httpd -d /opt/IBM/HTTPServer85/HTTPServer -k start -f conf2/httpd.conf"
    Descubre('10.90.55.116','JFS035_ADM','password35',80,cmd_ps)
    pass