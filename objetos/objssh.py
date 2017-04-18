# -*- coding: utf-8 -*-
'''
Created on 12 abr. 2017

@author: jose
'''
import paramiko
import simplejson as json

import re



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
        if "el6" in banner:
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
            salida =re.compile(patron).findall(salida)
        if saltar > 0 :
            salida.pop(saltar)
                     
        return salida
 

            