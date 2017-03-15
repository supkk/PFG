'''
Created on 13 mar. 2017

@author: jose
'''

class objServidor(object):
    '''
    classdocs
    '''

    
    def __init__(self, nombre,so,ram,cpu,ncpu):
        '''
        Constructor
        '''
        self.nombre=nombre
        self.so = so
        self.ram = ram
        self.cpu = cpu
        self.ncpu = ncpu
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
            id_serv=conn.grabaServidor(self)
            if conn.existeFS(id_serv):
                conn.borraFS(id_serv)
            for sf in self.sfs :
                sf.grabaBBDD(conn,id_serv)
            if conn.existeIP(id_serv):
                conn.borraIP(id_serv)
            for ip in self.ips:
                ip.grabaBBDD(conn,id_serv)
            for sw in self.sws :
                sw.grabaBBDD(conn,id_serv)
            conn.confirma()
        except Exception, error :
            print (error)
            conn.deshace()
        
        return
    

        
        
        