'''
Created on 13 mar. 2017

@author: jose
'''
from objetos import bbdd
from objetos import objIp
from objetos import objFS
from objetos import objSoft

class objServidor(object):
    '''
    classdocs
    '''

    
    def __init__(self, id_disp=0,id_serv=0,nombre='',so='',ram=0,cpu='',ncpu=0,cores=0,sn='',gw='',v_os=''):
        '''
        Constructor
        '''
        _id = None
        self._idDisp = None
        self.id_serv = id_disp
        self.id_disp = id_serv
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
        
        if id_serv <> 0 :
            self.cargaServidor(id_disp,id_serv)
        
    def estaCargado(self):
        
        return self._id <> None
    
    def cargaServidor(self,id_disp,id_serv):
        c = bbdd.bbdd()
        sql = 'select s._id,d.nombre, s.ram, s.tipo_cpu, s.n_cpu, s.n_cores, d.sn, s.gw, s.version_os, s.id_so, d._id  from tb_disp d inner join tb_servidor s on d.id_disp=s.id_disp where id_serv=' + str(id_serv)
        s=c.consulta(sql)
        self.nombre = s[0][1]
        self.so = s[0][9]
        self.ram = s[0][2]
        self.cpu = s[0][3]
        self.ncpu = s[0][4]
        self.cores = s[0][5]
        self.sn = s[0][6]
        self.gw = s[0][7]
        self.v_os = s[0][8]
        self._id = s[0][0]
        self._idDisp = s[0][9]
        sql='select * from tb_interface where id_disp='+str(id_disp)
        cins= c.consulta(sql)
        for i in cins:
            self.anade_IP(objIp.objIp(i[0],i[3],i[5],i[4],i[6],i[1],i[2]))
        sql='select * from tb_fs where id_serv='+str(id_serv)
        cfs= c.consulta(sql)
        for fs in cfs:
            self.anade_FS(objFS.objFS(fs[0],fs[2],fs[3],fs[4],fs[5]))
        
        sql='select * from tb_soft_running where id_serv='+str(id_serv)
        sws= c.consulta(sql)
        for sw in sws:
            self.anade_SW(objSoft.objSoft(sw[0],c.retCadSoftware(sw[1])))     
        
        return 
    
    def anade_FS(self,fs):
        self.sfs.append(fs)
        return
        
    def anade_IP(self,ip):
        self.ips.append(ip)
        return
    
    def anade_SW(self,soft):
        self.sws.append(soft)
        return
    
    def grabaBBDD(self,conn,ip):

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
            if conn.existeSw(self.id_serv)<> None:
                conn.borraSw(self.id_disp)
            for sw in self.sws :
                sw.grabaBBDD(conn,self.id_serv)
            conn.apuntaProcesado(ip.ip)
            conn.confirma()
        except Exception, error :
            print (error)
            conn.deshace()
        
        return
    
    def sincroniza(self,api,conn):
        
        data = {'Code': str(self.id_disp)}
        data['Description']=self.nombre
        data['Estado']=api.retIdLookup('CI-Estado','NV')
        data['NS']=self.sn
        data['nombreDisp']=self.nombre
        data['CodeServ']= str(self.id_serv)
        data['SO'] = api.retIdLookup('DISP-SO',self.so)
        data['VersionOS'] =self.v_os.split(' ')[0]
        data['RAM'] =self.ram
        data['CPU'] =self.cpu
        data['TCPU'] =self.ncpu
        data['CPC'] =self.cores
        data['Gateway'] =self.gw
        
        if self.estaCargado()==False:
 
            id_class = api.creaClase('Servidor',data)
            if  id_class > 0:
                sql = "update tb_Servidor set _id =" + str(id_class) + " where id_serv = " + str(self.id_serv)
                conn.actualizaTabla(sql) 
            else :
                return
        else :
            api.actualizaClase('Servidor',data,self._id)

        for fs in self.sfs:
            fs.sincroniza(api,conn,self.id_serv,self._id)
        for i in self.ips :
            i.sincroniza(api,conn,self.id_disp,self._idDisp)
        conn.confirma()    
        return

        
        
        