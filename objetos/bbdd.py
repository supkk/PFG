'''
Created on 8 mar. 2017

@author: jose
'''
import psycopg2
import ipcalc
import time
 
class bbdd():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cur = None
        try :
            self.conn = psycopg2.connect(database="sda_db", user="postgres", password="postgres", host="192.168.1.41", port="5432")
        except :
            print ("Error de acceso a BBDD")  
        return   
    
    def confirma(self):
        self.conn.commit()   
        return
    
    def deshace(self):
        self.conn.rollback()
        return
    
    def consulta (self,con):
        
        self.cur=self.conn.cursor()
        self.cur.execute(con)
        rows = self.cur.fetchall()
        
        return rows
    
    def apuntaProcesado(self,ip):
        cur=self.conn.cursor()
        cur.execute("update tb_dispositivos  set fecproc='"+time.strftime("%c") + "' where ip='" + ip +"'")
        cur.execute("update tb_dispositivos set apagado = 0  where ip='" + ip+"'")
        cur.close()
        return
    
    def apuntaApagado(self,ip):
        cur=self.conn.cursor()
        cur.execute("update tb_dispositivos set apagado = COALESCE(apagado,1) +1 where ip='" + ip+"'")
        cur.close()
        return
    
    def retIdTipoFS(self,desc):
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_fs where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_retorno = 'OTR'
        else :
            code_retorno = code_id[0]
        return code_retorno
    
    def retIdTipoAl(self,desc):
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_Almacenamiento where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_retorno = 'OTR'
        else :
            code_retorno = code_id[0]
        return code_retorno
    
    def retIdDesc(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_Desc where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_id =["OT"]
        return code_id[0]
    
    def retIdDisp(self,idServ):
        
        cur=self.conn.cursor()
        cur.execute("select id_disp from tb_Servidor where id_serv ="+str(idServ))
        code_id = cur.fetchone()
        cur.close()
        return code_id[0]
    
    def retIdSO(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_so where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_id =["ND"]
        return code_id[0]
    
    def retIdNet(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_Interface where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
            
        return code_id[0]
    
    def retIdSoftware(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select id_sw from tb_inv_software where n_proceso ='"+desc+"'")
        code_id = cur.fetchone()
        cur.close()
            
        return code_id[0]
    
    def existeServer(self,nombre):
        
        cur=self.conn.cursor()
        cur.execute("select d.id_disp,s.id_serv from tb_disp d join tb_servidor s on d.id_disp=s.id_disp where d.nombre='"+nombre+"'")
        code_id = cur.fetchone()
        cur.close()
        
        return code_id
    
    def existeNet(self,ip, mascara):
             
        address = ipcalc.Network(ip,mascara)  
        red = address.network().dq
        cur=self.conn.cursor()
        cur.execute("select id_net from TB_net where ipBase ='" + red + "' and mascara = '" +mascara + "'")
        id_red = cur.fetchone()
        cur.close()
        if id_red <> None :
            id_red=id_red[0]
        return id_red
    
    def existeInterface(self,id_disp):
        
        cur=self.conn.cursor()
        cur.execute("select id_disp from TB_Interface where id_disp =" + str(id_disp))
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def existeFS(self,id_serv):
        
        cur=self.conn.cursor()
        cur.execute("select id_serv from TB_fs where id_serv =" + str(id_serv))
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def existeSw(self,id_serv):
        
        cur=self.conn.cursor()
        cur.execute("select id_serv from TB_soft_running where id_serv =" + str(id_serv))
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def borraSw(self,id_serv):
        if self.cur == None:
            self.cur = self.conn.cursor()

        self.cur.execute('DELETE FROM TB_soft_running WHERE id_serv = ' + str(id_serv))
        return
    
    def borraInterfaces(self,id_disp):
        if self.cur == None:
            self.cur = self.conn.cursor()

        self.cur.execute('DELETE FROM TB_Interface WHERE id_disp = ' + str(id_disp))
        return
    
    def borraFS(self,id_serv):
        if self.cur == None:
            self.cur = self.conn.cursor()

        self.cur.execute('DELETE FROM TB_FS WHERE id_serv = ' + str(id_serv))
        return
    
    def insertaDisp(self,s):
        
        idDes=self.retIdDesc(s.td)
        idSO=self.retIdSO(s.os)
        data=(s.ip,s.fd,idDes,s.nombre,idSO,"N")
        try :
            self.cur.execute("INSERT INTO TB_Dispositivos(ip,fecdes,id_td,nombre,id_so,proc) VALUES (%s,%s,%s,%s,%s,%s)",data)
        except Exception :
            print ("la IP "+s.ip+" ya existe")
            self.deshace()
        
        return
        
    def grabaServidor(self,s):
        
        idSO=self.retIdSO(s.so)
        
        code = self.existeServer(s.nombre)
        if code == None :
            data_disp=(s.sn,s.nombre)
            sql_disp = 'INSERT INTO tb_disp (sn,nombre) values (%s,%s)'
            if self.cur == None :
                self.cur=self.conn.cursor()
            try :
                self.cur.execute(sql_disp,data_disp)
                self.cur.execute("select currval('tb_disp_id_disp_seq')")
                result=self.cur.fetchone()
                code_disp=result[0]
            except Exception, error :
                print error
            data=(code_disp,idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os)
            sql= "INSERT INTO TB_Servidor (id_disp,id_so,ram,tipo_cpu,n_cpu,n_cores,gw,version_os) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        else :
            code_disp = code[0]
            code_serv = code[1]
            data=(idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os)
            sql="UPDATE TB_Servidor SET  id_so =%s ,ram =%s ,tipo_cpu =%s ,n_cpu =%s, n_cores=%s, gw=%s, version_os=%s WHERE id_serv =" +str(code_serv)
        if self.cur == None :
            self.cur=self.conn.cursor()
        try :
            self.cur.execute(sql,data)
            if code == None :
                self.cur.execute("select currval('tb_servidor_id_serv_seq')")
                result=self.cur.fetchone()
                code_serv=result[0]
                
        except Exception, error :
            print error
                    
        return code_disp,code_serv
    

    
    def grabaIPS(self,ip,id_disp):
        
        idNet=self.existeNet(ip.ip,ip.mascara)
        if  idNet <> None :
            tipoNet=self.retIdNet(ip.tipoRed)
            data = (tipoNet,idNet,ip.ip,ip.mascara,ip.mac,ip.nombre,id_disp)
            sql = "INSERT INTO TB_Interface (id_TipoInt,id_net,ip,mascara, mac, nombre, id_disp) VALUES (%s,%s,%s,%s, %s, %s, %s)"
            if self.cur <> None :
                try :
                    self.cur.execute(sql,data)
                except Exception, error :
                    print error      
        return
   
    def grabaFS(self,fs,id_serv):

        tipoFs = self.retIdTipoFS(fs.tipoFs)
        tipoAl = self.retIdTipoAl(fs.tipoAl)
        data = (id_serv,fs.montaje,fs.size,tipoFs,tipoAl)
        sql = "INSERT INTO TB_FS (id_serv, montaje, size, id_tipoFS,id_tipoAl) VALUES (%s,%s,%s,%s,%s)"
        if self.cur <> None :
            try :
                self.cur.execute(sql,data)
            except Exception, error :
                print error  
        return
    
    def grabaSw(self,sw,id_serv):
        id_soft=self.retIdSoftware(sw.cadRunning)
        data=(id_soft,id_serv)
        sql='INSERT INTO TB_SOFT_RUNNING (id_sw,id_serv) VALUES(%s,%s)'
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
        self.confirma()
        

        return
    
    def cierraDB(self):
        self.conn.close()
    
