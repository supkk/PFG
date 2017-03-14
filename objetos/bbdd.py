'''
Created on 8 mar. 2017

@author: jose
'''
import psycopg2
from libxml2 import XML_DTD_ID_REDEFINED
 
class bbdd(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cur = None
        try :
            self.conn = psycopg2.connect(database="sda_db", user="postgres", password="postgres", host="192.168.1.47", port="5432")
        except :
            print ("Error de acceso a BBDD")  
        return   
    
    def consulta (self,con):
        
        self.cur=self.conn.cursor()
        self.cur.execute(con)
        rows = self.cur.fetchall()
        self.cur.close()
        
        return rows
    
    def retIdDesc(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from TB_TipoDesc where descripcion ='"+desc+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_id =["OT"]
        return code_id[0]
    
    def retIdSO(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from TB_so where descripcion ='"+desc+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_id =["ND"]
        return code_id[0]
    
    def existeIp(self,IP):
        cur=self.conn.cursor()
        cur.execute("select ip from TB_Dispositivos where ip ='"+IP+"'")
        code_id = cur.fetchone()
        cur.close()
        
        return code_id<>None
    
    def existeServer(self,nombre):
        
        cur=self.conn.cursor()
        cur.execute("select id_serv from TB_Servidor where nombre ='"+nombre+"'")
        code_id = cur.fetchone()
        cur.close()
        
        return code_id
    
    def existeNet(self,red):
        
        cur=self.conn.cursor()
        cur.execute("select id_net from TB_net where id_net ='" + red + "'")
        id_red = cur.fetchone()
        cur.close()

        return id_red 
    
    def insertaDisp(self,s):
        
        idDes=self.retIdDesc(s.td)
        idSO=self.retIdSO(s.os)
        data=(s.ip,s.fd,idDes,s.nombre,idSO,"N")
        if not self.existeIp(s.ip) :
            try :
                self.cur.execute("INSERT INTO TB_Dispositivos(ip,fecdes,id_td,nombre,id_so,proc) VALUES (%s,%s,%s,%s,%s,%s)",data)
            except Exception, error :
                print error
                print ("la IP "+s.ip+" ya existe")
        
        return
        
    def grabaServidor(self,s):
        
        idSO=self.retIdSO(s.os)
        
        code_serv = self.existeServer(s.nombre)
        if code_serv == None :
            data=(s.nombre,idSO,s.ram,s.cpu,s.ncpu)
            sql= "INSERT INTO TB_Servidor (nombre,id_so,ram,tipo_cpu,ncpu) VALUES (%s,%s,%s,%s,%s)"
        else :
            data=(s.nombre,idSO,s.ram,s.cpu,s.ncpu,code_serv)
            sql="UPDATE TB_Servidor SET nombre =%s ,id_so =%s ,ram =%s ,tipo_cpu =%s ,ncpu =%s WHERE id_serv = %s"
        if self.cur <> None :
            try :
                self.cur.execute(sql,data)
                if code_serv == None :
                    self.cur.execute("select currval('tb_servidor_id_serv_seq')")
                    code_serv=self.cur.fechone()
            except Exception, error :
                print error
        
            
        return code_serv
    

    
    def grabaIPS(self,ip,id_serv):
        
        idNet=self.existeNet(ip.red)
        if  idNet <> None :
            dirIp=self.existeIP(ip.ip) 
            if dirIp == None:
                data = (ip.ip,ip.mac,id_serv,idNet)
                sql = "INSERT INTO TB_IP (ip, mac, id_serv, id_net) VALUES (%s,%s,%s,%s)"
            else:
                data = (ip.mac,id_serv,idNet,ip.ip)
                sql = "UPDATE TB_IP SET  mac =%s, id_serv =%s, id_net =%s WHERE ip =%s"
            if self.cur <> None :
                try :
                    self.cur.execute(sql,data)
                except Exception, error :
                    print error   
            
        return

    def grabaFS(self,fs,id_serv):
        
        if  self.existeFS(fs.montaje,id_serv) == False :
            data = (id_serv,fs.montaje,fs.size,fs.tipo)
            sql = "INSERT INTO TB_FS (id_serv, montaje, size, tipo) VALUES (%s,%s,%s,%s)"
        else:
            data = (fs.size,fs.tipo,fs.montaje,id_serv)
            sql = "UPDATE TB_FS SET size= %s, tipo = %s WHERE montaje = %s and id_serv = %s"
        if self.cur <> None :
            try :
                self.cur.execute(sql,data)
            except Exception, error :
                print error  
        return
    
    def insertaAll(self,ls):
        
        self.cur=self.conn.cursor()
        for s in ls:
            self.insertaDisp(s)
        self.commit()
        self.cur.close()

        return
    
    def cierraDB(self):
        self.conn.close()
    
