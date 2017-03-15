'''
Created on 15 mar. 2017

@author: jose
'''
from objetos import objServidor
from objetos import objFS
from objetos import objIp
from objetos import bbdd


if __name__ == '__main__':
    server = objServidor.objServidor('server1','LINUX',4000000,'i5',5)
    fs=objFS.objFS('/home',2500,'ext4')
    fs2=objFS.objFS('/bin',2500,'ext4')
    ip=objIp.objIp('192.168.1.122','7c:b0:c2:76:b9:a7','192.168.1.0','255.255.255.0','192.168.1.1','192.168.1.255')
    ip2=objIp.objIp('192.168.1.123','7c:b0:c2:76:b9:a7','192.168.1.0','255.255.255.0','192.168.1.1','192.168.1.255')
    server.anade_FS(fs)
    server.anade_IP(ip)
    server.anade_FS(fs2)
    server.anade_IP(ip2)
    conn=bbdd.bbdd()
    server.grabaBBDD(conn)
        