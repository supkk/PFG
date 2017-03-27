'''
Created on 13 mar. 2017

@author: jose
'''

class objServidor(object):
    '''
    classdocs
    '''

    
    def __init__(self, nombre,so,ram,cpu,ncpu,cores,sn,gw,v_os):
        '''
        Constructor
        '''
        self.id_serv = 0
        self.id_disp = 0 
        self.nombre = nombre
        self.so = so
        self.ram = ram
        self.cpu = cpu
        self.ncpu = ncpu
        self.cores = cores
        self.sn = sn
        self.gw = gw
        self.v_os = v_os
        self.sfs = []
        self.ips = []
        self.sws = []
        
    def anade_FS(self,fs):
        self.sfs.append(fs)
        return
        
    def anade_IP(self,ip):
        self.ips.append(ip)
        return
    
    def anade_SW(self,soft):
        self.sws.append(soft)
        return
    
    def grabaBBDD(self,conn):

        try :
            self.id_disp, self.id_serv = conn.grabaServidor(self)
            if conn.existeFS(self.id_serv):
                conn.borraFS(self.id_serv)
            for sf in self.sfs :
                sf.grabaBBDD(conn,self.id_serv)
            if conn.existeInterface(self.id_disp)<> None:
                conn.borraInterfaces(self.id_disp)
            for ip in self.ips:
                ip.grabaBBDD(conn,self.id_disp)
            for sw in self.sws :
                sw.grabaBBDD(conn,self.id_serv)
            conn.confirma()
        except Exception, error :
            print (error)
            conn.deshace()
        
        return
    

        
        
        