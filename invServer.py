'''
Created on 15 mar. 2017

@author: jose
'''
from objetos import objServidor
from objetos import objFS
from objetos import objIp
from objetos import bbdd


if __name__ == '__main__':
    server = objServidor.objServidor('server1','LINUX',4000000,'i5',5,4,'SSNN','192.168.1.1', '4.0-66 Ubuntu SMP x86_64 GNU/Linux')
    fs=objFS.objFS('/home',2500,'ext4','INTERNO')
    fs2=objFS.objFS('/bin',2500,'ext4','NFS')
    fs3=objFS.objFS('/bin/ext',2500,'ext4','NFS')
    ip=objIp.objIp('192.168.1.122','7c:b0:c2:76:b9:a7','255.255.255.0','ETH0','Ethernet Cable')
    ip2=objIp.objIp('192.168.1.123','7c:b0:c2:76:b9:a8','255.255.255.0','ETH1','Ethernet Cable')
    ip3=objIp.objIp('192.168.1.124','7c:b0:c2:76:b9:a8','255.255.255.0','ETH3','Ethernet Cable')
    server.anade_FS(fs)
    server.anade_IP(ip)
    server.anade_FS(fs2)
    server.anade_IP(ip2)
    server.anade_FS(fs3)
    server.anade_IP(ip3)
    conn=bbdd.bbdd()
    server.grabaBBDD(conn)
        