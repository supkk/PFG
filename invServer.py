'''
Created on 15 mar. 2017

@author: jose
'''
from objetos import objServidor
from objetos import objFS
from objetos import objIp
from objetos import bbdd
from objetos import objSoft
from easysnmp import Session



def procesaUname(un):
    s = un.split(' ')
    return s[0], s[1]

def procesaCPU (c):
    
    cpu = c.walk('hrDeviceType')
    cores = 0
    ncpu=0
    for el in cpu:
        if '.1.3.6.1.2.1.25.3.1.3' in el.value :
            indice = el.oid_index
            cores+=1
    if cores < 2:
        ncpu=1
    else:
        ncpu = cores /2
        cores = 2
        
    procesor = c.get('HOST-RESOURCES-MIB::hrDeviceDescr.'+ str(indice)).value  
     
    return procesor,ncpu, cores

def descubreSSH(ip):
    ok=None
    return ok

def procesaFS(c,serv):
    
    fileSystem = c.walk('hrStorageIndex')
    for fs in fileSystem :
        m = c.get ('HOST-RESOURCES-MIB::hrFSMountPoint.'+str(fs.value)).value
        if m <> 'NOSUCHINSTANCE' :
            s = c.get ('HOST-RESOURCES-MIB::hrStorageSize.'+str(fs.value)).value
            t = c.get ('HOST-RESOURCES-MIB::hrFSType.'+str(fs.value)).value
            if t=='.1.3.6.1.2.1.25.3.9.23' :    
                tf='EXT'
                ta='INT'
            else:
                tf='OTR'
                ta='OTR'
            oFS = objFS.objFS(m,s,tf,ta)
            serv.anade_FS(oFS)
    
    
    return serv

def procesaInterfaz(c,serv):
        
    inter=c.walk('ifIndex')
    dic={}
    for i in inter :
        na = c.get('ifName.'+i.value).value
        mac = c.get('ifPhysAddress.'+i.value).value
        mac = ':'.join(['%x' % ord(x) for x in mac])
        dic[i.value]=[na,mac,'0.0.0.0','0.0.0.0']
    ips= c.walk('IP-MIB::ipAdEntIfIndex')
    for i in ips:
        ip = i.oid_index
        dic[i.value][2]=ip
        m = c.get('ipAdEntNetMask.'+ip).value
        dic[i.value][3]=m
     
    for ind in dic.keys():
        interfaz = objIp.objIp(dic[ind][2],dic[ind][1],dic[ind][3],dic[ind][0],'OTRO')
        serv.anade_IP(interfaz)
       
    return serv

def procesaSW(c,serv,lsoft):
    
    sws=c.walk('hrSWRunPath')
    dic={}
    for ls in lsoft:
        dic[ls[0]] = ls[1]
    for sw in sws :
        if sw.value <> '':
            cad_soft = sw.value +" "+ c.get('hrSWRunParameters.'+sw.oid_index).value
            for k,v in dic.items() :
                if  v in cad_soft :
                    soft = objSoft.objSoft(dic[k])
                    serv.anade_SW(soft)
                    dic[k]='___NINGUNO__________'
    return serv

def descubreIPLinux(ip,lsoft):

    
    try:
        serv=objServidor.objServidor('','',0,'',1,1,'','','')
        c = Session(hostname=ip, community='public', version=2)
        serv.v_os = c.get('SNMPv2-MIB::sysDescr.0').value
        serv.so,serv.nombre = procesaUname(serv.v_os)
        ram = c.get ('HOST-RESOURCES-MIB::hrMemorySize.0').value
        serv.ram = int(ram.encode('ascii'))/1000000
        serv.gw = c.get ('IP-MIB::ip.21.1.7.0.0.0.0').value
        serv.cpu, serv.ncpu,serv.cores = procesaCPU(c)
        serv = procesaInterfaz(c,serv)  
        serv = procesaFS(c,serv)   
        serv = procesaSW(c,serv,lsoft)  
    except Exception,  error:
        print error
        serv=descubreSSH(ip)
    
    return serv

def descubreWindows(ip):
    return

def descubreOtros(ip):
    return

def main():
    serv=None
    conn=bbdd.bbdd()
    sql = 'select * from TB_Dispositivos'
    datos=conn.consulta(sql)
    sql = 'select id_sw,n_proceso from tb_inv_software'
    lsoft =conn.consulta(sql)
    for reg in datos:  
        if reg[4]=='LX' :
            serv=descubreIPLinux(reg[0],lsoft)
        elif reg[4]=='WN' :
            descubreWindows(reg[0])
        else:
            descubreOtros(reg[0])
        if serv <> None :
            serv.grabaBBDD(conn,reg[0])
        else :
            conn.apuntaApagado(reg[0])
    return

if __name__ == '__main__':
    main()
        