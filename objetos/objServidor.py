'''
Created on 13 mar. 2017

@author: jose
'''

class objServidor(object):
    '''
    classdocs
    '''

    
    def __init__(self, nombre,so,ram,sf,ips,sw,cpu,ncpu):
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
            for sf in self.sfs :
                sf.grabaBBDD(conn,id_serv)
            for ip in self.ips:
                ip.grabaBBDD(conn,id_serv)
            for sw in self.sws :
                sw.grabaBBDD(conn,id_serv)
            conn.commit()
        except Exception, error :
            print (error)
            conn.rollback()
        
        return