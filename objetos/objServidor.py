# -*- coding: utf-8 -*-
'''
Created on 13 mar. 2017

@author: jose
'''
import psycopg2
from objetos import bbdd
from objetos import objIp
from objetos import objFS
from objetos import objSoft
import time


class objServidor(object):
    '''
    classdocs
    '''

    
    def __init__(self, id_disp=0,id_serv=0,nombre='',so='',ram=0,cpu='',ncpu=0,cores=0,sn='',gw='',v_os='',id_marca='',id_entorno='',virtual=False,conn=None):
        '''
        Constructor
        '''
        _id = None
        self._idDisp = None
        self.id_serv = id_serv
        self.id_disp = id_disp
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
        self.deleted = False
        self.fsync ='01/01/01'
        self.id_marca = id_marca
        self.entorno = self.recEntorno()
        self.virtual=virtual
        
        if id_serv <> 0 :
            self.cargaServidor(id_disp,id_serv,conn)
            
    def recEntorno(self):
        nombre= self.nombre.lower()
        if "des" in nombre:
            id_entorno = 'DES'
        elif 'pre' in nombre:
            id_entorno = 'PRE'
        elif 'int' in nombre:
            id_entorno = 'INT'
        else:
            id_entorno ='PRO'   
        return id_entorno
        
    def retIdDisp(self,id_disp):
        
        conn = psycopg2.connect(database="cmdbuild", user="postgres", password="postgres", host="192.168.1.20", port="5432")
        cur=conn.cursor()
        cur.execute("select \"Id\" from \"Dispositivo\" where \"Code\" = '" + str(id_disp) + "' and \"Status\" = 'A'")
        code_id = cur.fetchone()
        cur.close()
        if code_id <> None :
            code_id = code_id[0]
        return code_id
    
    def estaCargado(self):
        
        return self._id <> None
    
    def cargaServidor(self,id_disp,id_serv,c):
        
        sql = 'select s._id,d.nombre, s.ram, s.tipo_cpu, s.n_cpu, s.n_cores, d.sn, s.gw, s.version_os, s.id_so, d._id, s.deleted,s.fsync,d.id_marca,s.id_entorno,s.virtual from tb_disp d inner join tb_servidor s on d.id_disp=s.id_disp where id_serv=' + str(id_serv)
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
        self._idDisp = s[0][10]
        self.deleted = s[0][11]
        self.fsync = s[0][12]
        self.id_marca = s[0][13]
        self.entorno = s[0][14]
        self.virtual = s[0][15]
        
        sql='select _id,id_tipoint,id_net,ip,mascara,mac,nombre,deleted, fsync from tb_interface where id_disp='+str(id_disp)
        cins= c.consulta(sql)
        for i in cins:
            self.anade_IP(objIp.objIp(i[3],i[5],i[4],i[6],i[1],i[2],i[0],i[7],i[8]))
        sql='select _id,montaje,size,id_tipoFS,id_tipoAl, deleted,fsync  from tb_fs where id_serv='+str(id_serv)
        cfs= c.consulta(sql)
        for fs in cfs:
            self.anade_FS(objFS.objFS(fs[1],fs[2],fs[3],fs[4],fs[0],fs[5],fs[6]))
        
        sql='select _id,id_sw,deleted,fsync from tb_soft_running where id_serv='+str(id_serv)
        sws= c.consulta(sql)
        for sw in sws:
            self.anade_SW(objSoft.objSoft(sw[1],c.retCadSoftware(sw[1]),sw[0],sw[2],sw[3],id_serv,c))    
        
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

    def retPuntoMontaje(self):
    
        lpm =[]
        for fs in self.sfs:
            lpm.append(fs.montaje)
            
        return lpm 
    
    def retNombreInterface(self):
        lint=[]
        for i in self.ips:
            lint.append(i.nombre)
            
        return lint
    
    def retListaSoftware(self):
        
        lsws = []
        for sw in self.sws :
            lsws.append(sw.idsw)
        
        return lsws
    
    def apuntaModificado(self,conn):

        sql="update tb_Servidor set fsync ='"+time.strftime("%c")+"' where id_serv=" + str(self.id_serv)
        conn.actualizaTabla(sql)

        return
    
    def apuntafsBorrados(self,conn):
        
        cambiado = False
        sql = "select montaje from tb_fs where id_serv= " +str(self.id_serv) + " and deleted <> 'True'"
        lfs= conn.consulta(sql)
        lmontaje = self.retPuntoMontaje()
        for fs in lfs:
            if fs[0] not in lmontaje:
                sql = "update tb_fs set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_serv="+str(self.id_serv)+ " and montaje = '"+fs[0] + "'"
                conn.actualizaTabla(sql)
                cambiado = cambiado or True
        
        return cambiado
    
    def apuntaInterfacesBorrados(self,conn):
        
        cambiado =False
        sql = "select nombre from tb_Interface where id_disp= " +str(self.id_disp)+ " and deleted <> 'True'"
        lInter= conn.consulta(sql)
        lnomInt = self.retNombreInterface()
        for i in lInter:
            if i[0] not in lnomInt:
                sql = "update tb_Interface set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_disp="+str(self.id_disp)+ " and nombre = '"+ i[0] + "'"
                conn.actualizaTabla(sql)
                cambiado = cambiado or True
        return cambiado
    
    def apuntaSwBorrado(self,conn):
        
        cambiado=False
        sql = "select id_sw from tb_soft_running where id_serv= " +str(self.id_serv) + " and deleted <> 'True'"
        lsws= conn.consulta(sql)
        lnomSoft = self.retListaSoftware()
        for s in lsws:
            if s[0] not in lnomSoft:
                sql = "update tb_soft_running set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_serv="+str(self.id_serv)+ " and id_sw = "+ str(s[0]) + ""
                conn.actualizaTabla(sql)
                cambiado = cambiado or True
                
        return cambiado
    
    def grabaBBDD(self,conn,ip):

        try :
            self.modificado,self.id_disp, self.id_serv = conn.grabaServidor(self)
            for sf in self.sfs :
                cambiado = sf.grabaBBDD(conn,self.id_serv)
                self.modificado = self.modificado or cambiado
            cambiado=self.apuntafsBorrados(conn) 
            self.modificado = self.modificado or cambiado
            
            for ip in self.ips:
                cambiado=ip.grabaBBDD(conn,self.id_disp)
                self.modificado = self.modificado or cambiado
            cambiado=self.apuntaInterfacesBorrados(conn) 
            self.modificado = self.modificado or cambiado
 
            for sw in self.sws :
                self.cambiado = sw.grabaBBDD(conn,self.id_serv)
                self.modificado = self.modificado or cambiado
            cambiado=self.apuntaSwBorrado(conn) 
            self.modificado = self.modificado or cambiado
            
            if self.modificado == True :
                self.apuntaModificado(conn)

           
        except Exception, error :
            print (Exception, error)
            conn.deshace()
        
        return
    
    def borraServidor(self,api,conn):
        
        Correcto = True
        data = {'deleted':'True'}
        if self._id <> None :
            Correcto = api.actualizaClase('Servidor',data,self._id)
        if Correcto :
            for fs in self.sfs :
                ok=fs.borraFsCMDB(api,conn,self.id_serv)
                Correcto = Correcto and ok
            for i in self.ips:
                ok = i.borraIntCMDB(api,conn,self.id_disp)
                Correcto = Correcto and ok
            for s in self.sws:
                ok = s.borraSwCMDB(api,conn,self.id_serv)
                Correcto = Correcto and ok
            if Correcto :
                sql = "delete from tb_servidor where id_serv = " + str(self.id_serv)    
                conn.actualizaTabla(sql)
                sql = "delete from tb_disp where id_disp = " + str(self.id_disp)    
                conn.actualizaTabla(sql)
                sql = "delete from tb_dispositivos where id_disp = " + str(self.id_disp)    
                conn.actualizaTabla(sql)
            else:
                print "Error al borrar el servidor id="+str(self.id_serv)
        else :
            print "Error al borrar el servidor id="+str(self.id_serv)
        
    
    def sincroniza(self,api,conn,ultimaSync):
        
        
        if not self.deleted :
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
            data['Entorno'] =api.retIdLookup('CI-Entorno',self.entorno)
            data['Marca'] =api.retIdLookup('Disp-Marca',self.id_marca)
            data['Carga'] =api.retIdLookup('CI-TipoCarga',"AU")
            data['Virtual'] = str(self.virtual).lower()
            
            if not self.estaCargado():
     
                id_class = api.creaClase('Servidor',data)
                if  id_class > 0:
                    self._id=id_class
                    self._idDisp = self.retIdDisp(self.id_disp)
                    sql = "update tb_Servidor set _id =" + str(id_class) + " where id_serv = " + str(self.id_serv)
                    conn.actualizaTabla(sql) 
                    sql = "update tb_Disp set _id = " + str(self._idDisp) + " where id_disp = " + str(self.id_disp)
                    conn.actualizaTabla(sql) 
                    print (time.strftime("%c")+"-- Añadido el  servidor  "+ self.nombre)
                else :
                    print (time.strftime("%c")+"-- Error al sincronizar el   servidor  "+ self.nombre)
                    return
            else :
                if self.fsync > ultimaSync :
                    api.actualizaClase('Servidor',data,self._id)
                    print (time.strftime("%c")+"-- Actualizado el  servidor  "+ self.nombre)
    
            for fs in self.sfs:
                fs.sincroniza(api,conn,self.id_serv,self._id,ultimaSync)
            for i in self.ips :
                i.sincroniza(api,conn,self.id_disp,self._idDisp,ultimaSync)
            for sw in self.sws:
                sw.sincroniza(api,conn,self.id_serv,self._id,ultimaSync)
        else :
            self.borraServidor(api,conn)
 
        return

        
        
        