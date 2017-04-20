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
            self.conn = psycopg2.connect(database="sda_db", user="postgres", password="postgres", host="192.168.1.20", port="5432")
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
    
    def apuntaApagado(self,ip):
       
        cur=self.conn.cursor()
        result = self.consulta("select apagado,id_disp from tb_dispositivos where IP='" + ip+"'")
        if result[0][0] < 3:
            cur.execute("update tb_dispositivos set apagado = COALESCE(apagado,1) +1 where ip='" + ip+"'")
        else :
            if result[0][1] <> 0:
                cur.execute("update tb_servidor set deleted ='True' where id_disp="+ str(result[0][1]))
            else :
                cur.execute("delete from tb_dispositivos where ip='"+ip+"'")
            
        cur.close()
        return
    
    def apuntaProcesado(self,ip,id_disp):
        cur=self.conn.cursor()
        cur.execute("update tb_dispositivos  set fecproc='"+time.strftime("%c") + "' where ip='" + ip +"'")
        cur.execute("update tb_dispositivos set apagado = 0  where ip='" + ip+"'")
        cur.execute("update tb_dispositivos set id_disp ="+str(id_disp)+"  where ip='"+ ip +"'")
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
    
    def retDescSoftware (self,idw):
        
        cur=self.conn.cursor()
        cur.execute("select descripcion from tb_inv_software where id_sw = " + str(idw))
        res = cur.fetchone()
        cur.close()
             
        return res[0]
    
    def retIdCatalogoSw (self,idw):
        cur=self.conn.cursor()
        cur.execute("select _id from tb_inv_software where id_sw = " + str(idw))
        res = cur.fetchone()
        cur.close()
        
        return res[0]
    
    def retIdNet(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_Interface where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
            
        return code_id[0]
    
    def retCodeRed(self,idRed):
        cur=self.conn.cursor()
        cur.execute("select _id from tb_net where id_net =" + str(idRed))
        code_id = cur.fetchone()
        cur.close()
        return code_id[0]
    
    
    def retIdSoftware(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select id_sw from tb_inv_software where n_proceso ='"+desc+"'")
        code_id = cur.fetchone()
        cur.close()
            
        return code_id[0]
    
    def retCadSoftware(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select n_proceso from tb_inv_software where id_sw =" + str(desc))
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
    
    def existeInterfaceDisp(self,nombre,id_disp):

        cur=self.conn.cursor()
        cur.execute("select id_TipoInt,id_net,ip,mascara,mac,nombre from TB_Interface where id_disp =" + str(id_disp)+" and nombre='"+nombre+"'")
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def existeFS(self,id_serv,montaje):

        cur=self.conn.cursor()
        cur.execute("select size,id_tipofs,id_tipoAl from TB_fs where id_serv =" + str(id_serv)+ " and montaje = '" + montaje + "'")
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def existeSw(self,id_serv,id_soft):
        
        cur=self.conn.cursor()
        cur.execute("select id_serv from TB_soft_running where id_serv =" + str(id_serv)+ " and id_sw="+str(id_soft))
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def borraSw(self,id_serv):
        if self.cur == None:
            self.cur = self.conn.cursor()

        self.cur.execute('DELETE FROM TB_soft_running WHERE id_serv = ' + str(id_serv))
        return
    
    def borraInterfacesDisp(self,id_disp):
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
        data=(s.ip,s.fd,idDes,idSO,"N",0,0)
        try :
            self.cur.execute("INSERT INTO TB_Dispositivos(ip,fecdes,id_td,id_so,proc,apagado,id_disp) VALUES (%s,%s,%s,%s,%s,%s,%s)",data)
            self.confirma()
        except Exception, error :
            print ("la IP "+s.ip+" ya existe")
            self.deshace()
        
        return
        
    def grabaServidor(self,s):
        
        idSO=self.retIdSO(s.so)
        modificado = True
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
            data=(code_disp,idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os,time.strftime("%c"))
            sql= "INSERT INTO TB_Servidor (id_disp,id_so,ram,tipo_cpu,n_cpu,n_cores,gw,version_os,fsync) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(sql,data)
            if code == None :
                self.cur.execute("select currval('tb_servidor_id_serv_seq')")
                result=self.cur.fetchone()
                code_serv=result[0]
        else :
            code_disp = code[0]
            code_serv = code[1]
            data=(idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os)
            sql="select id_so,ram,tipo_cpu,n_cpu,n_cores,gw,version_os from tb_servidor where id_serv="+str(code_serv)
            datos_serv = self.consulta(sql)
            if data <> datos_serv[0]:
                data=(idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os,time.strftime("%c"))
                sql="UPDATE TB_Servidor SET  id_so =%s ,ram =%s ,tipo_cpu =%s ,n_cpu =%s, n_cores=%s, gw=%s, version_os=%s, fsync =%s WHERE id_serv =" +str(code_serv) 
                self.cur=self.conn.cursor()
                self.cur.execute(sql,data)      
            else :
                modificado = False
                        
        return modificado, code_disp,code_serv
    

    
    def grabaIPS(self,ip,id_disp):
        
        cambiado = False
        
        idNet=self.existeNet(ip.ip,ip.mascara)
        if  idNet <> None :
            datosInterface = self.existeInterfaceDisp(ip.nombre,id_disp)
            tipoNet=self.retIdNet(ip.tipoRed)
            data = (tipoNet,idNet,ip.ip,ip.mascara,ip.mac,ip.nombre)
            if datosInterface == None :
                data = (tipoNet,idNet,ip.ip,ip.mascara,ip.mac,ip.nombre,id_disp,time.strftime("%c"))
                sql = "INSERT INTO TB_Interface (id_TipoInt,id_net,ip,mascara, mac, nombre, id_disp,fsync) VALUES (%s,%s,%s,%s, %s, %s, %s,%s)"
                if self.cur <> None :
                    try :
                        self.cur.execute(sql,data)
                        cambiado = True
                    except Exception, error :
                        print error
            else :
                if data <> datosInterface :
                    data = (tipoNet,idNet,ip.ip,ip.mascara,ip.mac,ip.nombre,time.strftime("%c"))
                    sql = "UPDATE TB_Interface SET id_TipoInt=%s,id_net=%s,ip=%s,mascara=%s, mac=%s, nombre=%s, fsync=%s where id_disp="+str(id_disp) + " and nombre = '" + ip.nombre + "'"                    
                    if self.cur <> None :
                        try :
                            self.cur.execute(sql,data)
                            cambiado = True
                        except Exception, error :
                            print error
        else:
            print "No existe red donde ubicar la IP "+ip.ip      
            
        return cambiado
   
    def grabaFS(self,fs,id_serv):

        modificado = False
        tipoFs = self.retIdTipoFS(fs.tipoFs)
        tipoAl = self.retIdTipoAl(fs.tipoAl)
       
        data_fs = self.existeFS(id_serv,fs.montaje)
        if data_fs == None :
            data = (id_serv,fs.montaje,fs.size,tipoFs,tipoAl,time.strftime("%c"))
            sql = "INSERT INTO TB_FS (id_serv, montaje, size, id_tipoFS,id_tipoAl,fsync) VALUES (%s,%s,%s,%s,%s,%s)"
            if self.cur <> None :
                try :
                    self.cur.execute(sql,data)
                    modificado=True
                except Exception, error :
                    print error  
        else:
            data = (fs.size,tipoFs,tipoAl)
            if data <> data_fs :
                data = (fs.size,tipoFs,tipoAl,time.strftime("%c"))
                sql = "UPDATE TB_FS SET size=%s,id_tipoFS=%s,id_tipoAl=%s,fsync=%s where id_serv= "+str(id_serv) +" and montaje ='"+fs.montaje + "'" 
                modificado = True  
                if self.cur <> None :
                    try :
                        self.cur.execute(sql,data)
                    except Exception, error :
                        print error  
    
        return modificado

    def actualizaTabla(self,sql):
        
        cur=self.conn.cursor()
        cur.execute(sql)
        cur.close()
        
        return
    
    def grabaSw(self,sw,id_serv):
        
        modificado = False
        id_soft=self.retIdSoftware(sw.cadRunning)
        
        if self.existeSw(id_serv,id_soft) == None:
            data=(id_soft,id_serv,time.strftime("%c"))
            sql='INSERT INTO TB_SOFT_RUNNING (id_sw,id_serv,fsync) VALUES(%s,%s,%s)'
            if self.cur <> None :
                try :
                    self.cur.execute(sql,data)
                    modificado=True
                except Exception, error :
                    print error 
        return modificado
    
    def insertaAll(self,ls):
        
        self.cur=self.conn.cursor()
        for s in ls:
            self.insertaDisp(s)

        return
    
    def cierraDB(self):
        self.conn.close()
    
