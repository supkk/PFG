# -*- coding: utf-8 -*-
'''
Created on 12 abr. 2017

@author: jose
'''
import paramiko
import simplejson as json
from objetos.objServidor import objServidor
import re
from objetos.objFS import objFS
from objetos.objIp import objIp


class objssh(object):
    '''
    classdocs
    '''


    def __init__(self, ip,u,p):
        '''
        Constructor
        '''
        self.ssh = paramiko.SSHClient()  # Iniciamos un cliente SSH
        self.ssh.load_system_host_keys()  # Agregamos el listado de host conocidos
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Si no encuentra el host, lo agrega automáticamente
        self.ssh.connect(ip, username=u, password=p,banner_timeout=10)  # Iniciamos la conexión.
        self.p = p
        banner = self.enviaComando("uname -a")
        if "SunOS" in banner:
            self.so = "sunos"
        if "Ubuntu"in banner:
            self.so ="Ubuntu"
        if "RHEL" in banner:
            self.so = "RHEL"
            
        return
    
    def cargaConf(self):

        fichero = "/home/jose/workspace/PFG/conf/"+self.so+".json"
        dc = json.loads(open(fichero).read())
        
        return dc 

    def enviaComando(self,cmd,patron='',saltar = 0):

            
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        if "sudo" in cmd:
            stdin.write(self.p+'\n')
            stdin.flush()
        
        salida = stdout.read()
        errores = stderr.read()
        if patron<>'':
            salida =re.findall(patron, salida)
        if saltar > 0 :
            salida.pop(saltar)
                     
        return salida
 
def procesaFS_SSH(c,dctC):
    
    if dctC['fileSystem'].haskey('saltar'):
        saltar = dctC['fileSystem']['saltar']
    else :
        saltar=0
    fss = c.enviaComando(dctC['fileSystem']['comando'], dctC['fileSystem']['regex'],saltar)
    listafs=[]
    for fs in fss:
        listafs.append(objFS(montaje=fs[1],size=int(fs[0]),tipoFs=fs[2],tipoAl='INT'))
        
    return listafs

def procesaIP_SSH(c,dctC):
    
    if dctC['net'].haskey('saltar'):
        saltar = dctC['net']['saltar']
    else :
        saltar=0
    ints = c.enviaComando(dctC['net']['comando'], dctC['net']['regex'],saltar)
    listaint=[]
    for i in ints:
        listaint.append(objIP(nombre=i[1],size=int(fs[0]),tipoFs=fs[2],tipoAl='INT'))
    return
def procesaSW_SSH(c):
    return   
def DescubreSSH(ip):
    
    try:
        conexSSH = objssh(ip,"jose","Jafs11")
        dctC =conexSSH.cargaConf()
    except :
        return None
    serv=objServidor()
    serv.nombre = conexSSH.enviaComando(dctC['nombre']['comando'], dctC['nombre']['regex'])[0]
    serv.ram = conexSSH.enviaComando(dctC['ram']['comando'], dctC['ram']['regex'])[0]
    serv.gw = conexSSH.enviaComando(dctC['gw']['comando'], dctC['gw']['regex'])[0]
    serv.cpu = conexSSH.enviaComando(dctC['cpu']['comando'], dctC['cpu']['regex'])[0]
    serv.n_cpu = conexSSH.enviaComando(dctC['n_cpu']['comando'], dctC['n_cpu']['regex'])[0]
    serv.v_os = conexSSH.enviaComando(dctC['version_os']['comando'], dctC['version_os']['regex'])[0]
    serv.core = 1
    serv.sn = conexSSH.enviaComando(dctC['sn']['comando'], dctC['sn']['regex'])[0]
    serv.sfs = procesaFS_SSH(conexSSH,dctC)[:]
    serv.ips = procesaIP_SSH()[:]   
    serv = procesaSW_SSH()[:]
    
    return serv

if __name__ == '__main__':
    
    DescubreSSH("192.168.1.39")
            