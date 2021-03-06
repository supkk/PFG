# -*- coding: utf-8 -*-

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
from objetos import objssh
import time
import argparse 
import simplejson as json


def procesaFS_SSH(c,dctC):
    
    if 'saltar' in dctC['fileSystem'].keys():
        saltar = dctC['fileSystem']['saltar']
    else :
        saltar=0
    fss = c.enviaComando(dctC['fileSystem']['comando'], dctC['fileSystem']['regex'],saltar)
    listafs=[]
    for fs in fss:
        listafs.append(objFS.objFS(montaje=fs[1],size=int(fs[0]),tipoFs=fs[2],tipoAl='INTERNO'))
        
    return listafs

def procesaIP_SSH(c,dctC):
    
    if 'saltar' in dctC['fileSystem'].keys():
        saltar = dctC['net']['saltar']
    else :
        saltar=0
    ints = c.enviaComando(dctC['net']['comando'], dctC['net']['regex'],saltar)
    listaint=[]
    for i in ints:
        listaint.append(objIp.objIp(ip=i[1],mac=i[3],mascara=i[2],nombre=i[0],tipoRed='OTRO'))
                        
    return listaint

def procesaSW_SSH(c,dctC,lsoft):
    
    if 'saltar' in dctC['fileSystem'].keys():
        saltar = dctC['net']['saltar']
    else :
        saltar=0
    sws = c.enviaComando(dctC['procesos']['comando'], dctC['procesos']['regex'],saltar)
    listaSw=[]
    dic={}
    for ls in lsoft:
        dic[ls[0]] = ls[1]
        
    for sw in sws:
        for k,v in dic.items() :
            if  v in sw :
                soft = objSoft.objSoft(k,dic[k])
                listaSw.append(soft)
                dic[k]='___NINGUNO__________'
                
                    
    return listaSw  

def descubreSSH(ip,lsoft,con,config):
    
    try:
        conexSSH = objssh.objssh(ip,config['user'],config['password'])
        dctC =conexSSH.cargaPlantilla("so")
    except Exception, error:
        print (time.strftime("%c")+"--"+"Error al conectar por SSH con --> "+ip )
        print (time.strftime("%c")+"--", error)
        return None
    
    serv=objServidor.objServidor()
    serv.nombre = conexSSH.enviaComando(dctC['nombre']['comando'], dctC['nombre']['regex'])[0].strip()
    serv.ram = conexSSH.enviaComando(dctC['ram']['comando'], dctC['ram']['regex'])[0]
    serv.gw = conexSSH.enviaComando(dctC['gw']['comando'], dctC['gw']['regex'])[0]
    serv.cpu = conexSSH.enviaComando(dctC['cpu']['comando'], dctC['cpu']['regex'])[0].strip()
    serv.ncpu = conexSSH.enviaComando(dctC['n_cpu']['comando'], dctC['n_cpu']['regex'])[0]
    serv.v_os = conexSSH.enviaComando(dctC['version_os']['comando'], dctC['version_os']['regex'])[0].strip()
    serv.cores = conexSSH.enviaComando(dctC['cores']['comando'], dctC['cores']['regex'])[0]
    serv.sn = conexSSH.enviaComando(dctC['sn']['comando'], dctC['sn']['regex'])[0]
    serv.so = conexSSH.enviaComando(dctC['id_so']['comando'], dctC['id_so']['regex'])[0]
    serv.sfs = procesaFS_SSH(conexSSH,dctC)[:]
    serv.ips = procesaIP_SSH(conexSSH,dctC)[:]   
    serv.sws = procesaSW_SSH(conexSSH,dctC,lsoft)[:]
    serv.virtual = (conexSSH.enviaComando(dctC['virtual']['comando'], dctC['virtual']['regex'])[0]<> '')
    marca = conexSSH.enviaComando(dctC['marca']['comando'], dctC['marca']['regex'])[0].strip()
    serv.id_marca= con.retIdFab(marca)
    if serv.id_marca == 'NA':
        print (time.strftime("%c")+"-- Posible marca nueva  "+ marca)
    
    
    return serv

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



def procesaFS(c,serv):
    
    primero =True
    fileSystem = c.walk('hrStorageIndex')
    for fs in fileSystem :
        tipofs = c.get ('HOST-RESOURCES-MIB::hrStorageType.'+str(fs.value)).value
        if tipofs in ('.1.3.6.1.2.1.25.2.1.4','.1.3.6.1.2.1.25.2.1.7') :
            if primero == True:
                diferencial = int(fs.value) - 1
                primero = False
            m = c.get ('HOST-RESOURCES-MIB::hrStorageDescr.'+str(fs.value)).value.split(' ')[0]
            if m <> 'NOSUCHINSTANCE' :
                s = c.get ('HOST-RESOURCES-MIB::hrStorageSize.'+str(fs.value)).value
                bloque = c.get ('HOST-RESOURCES-MIB::hrStorageAllocationUnits.'+str(fs.value)).value
                s = int(s.encode('ascii'))* int(bloque.encode('ascii'))/1000000
                indice = int(fs.value) - diferencial
                t = c.get ('HOST-RESOURCES-MIB::hrFSType.'+str(indice)).value
                if t=='.1.3.6.1.2.1.25.3.9.23' :    
                    tf='EXT4'
                    ta='INT'
                elif t=='.1.3.6.1.2.1.25.3.9.9':
                    tf='NTFS'
                    ta='INT'
                elif t=='.1.3.6.1.2.1.25.3.9.5':
                    tf='FAT'
                    ta='INT'
                else :
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
            cad_soft = sw.value +" "+c.get('hrSWRunName.'+sw.oid_index).value +" "+c.get('hrSWRunParameters.'+sw.oid_index).value
            if 'VBoxService' in cad_soft:
                serv.virtual=True
            for k,v in dic.items() :
                if  v in cad_soft :
                    soft = objSoft.objSoft(k,dic[k])
                    serv.anade_SW(soft)
                    dic[k]='___NINGUNO__________'
    return serv

def descubreIPLinux(ip,lsoft,con,config):

    
    try:
        serv=objServidor.objServidor()
        c = Session(hostname=ip, community='public', version=2)
        serv.v_os = c.get('SNMPv2-MIB::sysDescr.0').value
        serv.so,serv.nombre = procesaUname(serv.v_os)
        serv.entorno = serv.recEntorno()
        ram = c.get ('HOST-RESOURCES-MIB::hrMemorySize.0').value
        serv.ram = int(ram.encode('ascii'))/1000
        serv.gw = c.get ('IP-MIB::ip.21.1.7.0.0.0.0').value
        serv.cpu, serv.ncpu,serv.cores = procesaCPU(c)
        serv = procesaInterfaz(c,serv)  
        serv = procesaFS(c,serv)   
        serv = procesaSW(c,serv,lsoft)  
        serv.id_marca ='NA'
    except Exception,  error:
        print (time.strftime("%c")+"--"+"No conecto por SNMP. Intento por SSH --> "+ip)
        serv=descubreSSH(ip,lsoft,con,config)
    
    return serv

def descubreWMI(ip):
    serv=None
    return serv

def descubreWindows(ip,listaSoftware):
    try:
        serv=objServidor.objServidor()
        c = Session(hostname=ip, community='public', version=2)
        serv.v_os = c.get('SNMPv2-MIB::sysDescr.0').value.split('- Software:')[1].strip()
        serv.so = serv.v_os.split(' ')[0]
        serv.nombre = c.get ('SNMPv2-MIB::sysName.0').value
        serv.entorno = serv.recEntorno()
        ram = c.get ('HOST-RESOURCES-MIB::hrMemorySize.0').value
        serv.ram = int(ram.encode('ascii'))/1000
        serv.gw = c.get ('IP-MIB::ip.21.1.7.0.0.0.0').value
        serv.cpu, serv.ncpu,serv.cores = procesaCPU(c)
        serv = procesaInterfaz(c,serv)  
        serv = procesaFS(c,serv)   
        serv = procesaSW(c,serv,listaSoftware)  
        serv.id_marca ='NA'
    except Exception,  error:
        print (time.strftime("%c")+"--"+"Error al conectar por SNMP. Lo intento por WMI --> "+ip)
        print (time.strftime("%c")+"--", Exception, error)
        serv=descubreWMI(ip)
    return serv

def descubreOtros(ip):
    return None

def parametros():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--ip" ,help="Descubre solo una IP" )
    parser.add_argument("-c","--conf",help="ruta del fichero de configuración",default='./conf/config.json')
    args = parser.parse_args()  
    cnf =  json.loads(open(args.conf).read())
    return cnf,args;


def main():
    cnf,arg = parametros()
    
    serv=None
    conf=cnf['BaseDatos']
    conn=bbdd.bbdd(bd=conf['bd'],u=conf['user'],pw=conf['password'],h=conf['host'],p=conf['port'])
    if type(arg.ip) <> str:
        sql = 'select ip,id_so from TB_Dispositivos'
    else :
        sql = "select ip,id_so from TB_Dispositivos where ip='"+arg.ip+"'"
    datos=conn.consulta(sql)
    sql = 'select id_sw,n_proceso from tb_inv_software'
    lsoft =conn.consulta(sql)
    for reg in datos:  
        print (time.strftime("%c")+"-- Comienzo a procesar el servidor "+ reg[0])
        if reg[1]=='LX' :
            serv=descubreIPLinux(reg[0],lsoft,conn,cnf['conecta_ssh'])
        elif reg[1]=='WS' :
            serv=descubreWindows(reg[0],lsoft)
        else:
            serv=descubreOtros(reg[0])
        if serv <> None :
            serv.grabaBBDD(conn,reg[0])
            conn.apuntaProcesado(reg[0],serv.id_disp)
        else :
            conn.apuntaApagado(reg[0])
        conn.confirma()
        print (time.strftime("%c")+"-- Procesado el servidor "+ reg[0])
    return

if __name__ == '__main__':
    main()
        