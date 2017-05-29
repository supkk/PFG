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
    Representa una sesion de acceso a un servidor por ssh
    '''


    def __init__(self, ip,u,p):
        '''
        Constructor
        
            ip: IP del servidor 
            u: Usuario
            p: Contraseña
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
    
    def cargaPlantilla(self,tipo):
        '''
        Carga una plantilla de comandos para ejecutar en el servidor
        
        Parametro
            tipo: Indica el tipo de la plantilla
        '''

        fichero = "./conf/"+tipo+"/"+self.so+".json"
        dc = json.loads(open(fichero).read())
        
        return dc 

    def enviaComando(self,cmd,patron='',saltar = 0):
        '''
        Envia un comando al servidor y formatea la salida
        
        Parametros
            cmd: Cadena con comando
            patron: Expresion regular para el formateo de la salida
            saltar: Indica si hay que saltar algún campo de salida
        '''

            
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
 

            