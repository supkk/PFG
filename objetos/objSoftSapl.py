# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''
from objetos import objSi
import time

class objSoftSapl(objSi.objSi):
    '''
    classdocs
    '''


    def __init__( self,idserv=0,sw=0,ent='PRO',ip='',soft='',user='',port=0,home='',id_si=0,conn=None,fsync=None):
        '''
        Constructor
        '''
        super(objSoftSapl,self).__init__(id_serv=idserv,id_sw=sw,id_entorno=ent,ip=ip,user=user,home=home,id_si=id_si)
        self.soft=soft
        self.puerto=port
        self.id_sa=0
        self.id_si=0
        
        if id_si ==0:
            self.dic_SA = {}
        else:
            self.dic_SA = self.cargaSoftware(id_si,conn)
        
        return
    
    def cargaSoftware(self,id_si,conn):
        dic={}
        data=(id_si,self.fsync)
        sql= "select id_sa,jvm,puerto,id_entorno where id_si=%s and fsync >=%s" 
        data = conn.consulta(sql,data)
        dic['jvm']= data[1]
        dic['puerto']= data[2]
        dic['id_entorno']= data[3]
        data = (data[0],self.fsync)
        sql = "select id_edb,usuario,nombre where id_sa=%s and fsync >=%s"
        lcdb = conn.consulta(sql,data)
        dic['jdbc']=[]
        for cdb in lcdb:
            d_cdb={}
            d_cdb['usuario']=cdb[1]
            d_cdb['nombre']=cdb[2]
            ddb=conn.retidsEsquemaBD(cdb[0])
            d_cdb['nombre_db']=ddb[0]
            d_cdb['esquema']=ddb[1]
            dic['jdbc'].append(d_cdb.copy())
        
        return dic
    
    def descubre(self,cnf,param):
        
        cnf=cnf['conecta_probe']
        modulo = "from plugins import "+self.soft + " as module"
        exec modulo
        self.dic_SA = module.descubre(host=self.ip,user=cnf['user'],password=cnf['password'],puerto=self.puerto)
        if self.dic_SA <> None:
            self.version = self.dic_SA['version']
        
        return self.dic_SA <> None
    
    def actualizaInstancia(self, id_si,conn):
        
        modificado = super(objSoftSapl,self).actualizaInstancia(id_si, conn)
        dsa,id_sa = conn.retInstanciaSA(id_si)
        dsa=unicode(dsa,'utf-8')
        data =(self.dic_SA['jvm'])
        if data <> dsa :
            sql ="update tb_servaplicaciones set jvm=%s, fsync='"+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado = True
            
        return modificado, id_sa
    
    def actualizaConector(self,ds,conn,id_sa):
        
        modificado= False
        dcbd,id_cdb = conn.retInstanciaCDB(id_sa,ds['nombre'])
        if id_cdb == None :
            p,id_edb=conn.retEsquemaDB(ds['esquema'],ds['nombre_bd'])
            if id_edb == None :
                print (time.strftime("%c")+"-- Error el esquema al que apunta el conector no existe "+ds['esquema']+"  "+ds['nombre_bd'])
            else :
                data = (id_edb,ds['usuario'],ds['nombre'],time.strftime("%c"),self.id_sa)
                sql ="insert into tb_conectorbd (id_edb,usuario,nombre,fsync,id_sa) values (%s,%s,%s,%s,%s)"
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data =(ds['usuario'],ds['nombre'])
            if data <> dcbd :
                sql ="update tb_conectorBD set usuario=%s, nombre=%s, fsync='"+time.strftime("%c")+"' where id_cbd="+str(id_cdb)
                conn.actualizaTabla(sql,data)
                modificado = True
            
        return modificado, id_cdb
    
    def marcarCDBBorrados(self,conn,id_valor):
        
        sql = "update tb_ConectorBD set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_cdb="+str(id_valor) 
        conn.actualizaTabla(sql)
        
        return
    
    def gestionaCDBBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select nombre,id_cbd from  TB_Conectorbd where id_sa=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for ds in dic :
                if item[0]== ds['nombre'] :
                    encontrado =True
                    break
            if not encontrado :
                self.marcarCDBBorrados(conn,item[1])
                modificado =True
                
        return modificado
    
    def grabaBBDD(self,conn):
        
        mod_cdb = False
        self.id_si = conn.existeInstanciaSW(self.id_serv,self.id_sw,self.puerto,'tb_servAplicaciones') 
        if self.id_si == None :
            self.id_si = super(objSoftSapl,self).grabaBBDD(conn)
            data = (self.id_si,self.puerto,self.dic_SA['jvm'],time.strftime("%c"))
            sql ='insert into tb_servaplicaciones (id_si,puerto,jvm,fsync) values(%s,%s,%s,%s)'
            self.id_sa=conn.actualizaTabla(sql,data)
            if self.id_sa <> None:
                for ds in self.dic_SA['jdbc']:
                    p,id_edb=conn.retEsquemaDB(ds['esquema'],ds['nombre_bd'])
                    if id_edb == None :
                        print (time.strftime("%c")+"-- Error el esquema al que apunta el conector no existe "+ds['esquema']+"  "+ds['nombre_bd'])
                    else:    
                        data = (id_edb,ds['usuario'],ds['nombre'],time.strftime("%c"),self.id_sa)
                        sql ="insert into tb_conectorbd (id_edb,usuario,nombre,fsync,id_sa) values (%s,%s,%s,%s,%s)"
                        conn.actualizaTabla(sql,data)
            else:
                print (time.strftime("%c")+"-- Error al insertar la instancia de Servidor aplicaciones "+self.dic['version'])
        else:
            mod_cdb, self.id_sa = self.actualizaInstancia(self.id_si,conn)
            for ds in self.dic_SA['jdbc']: 
                mod, id_cdb = self.actualizaConector(ds,conn,self.id_sa)
                mod_cdb = mod or mod_cdb
            mod_cdb = self.gestionaCDBBorrados(conn,self.dic_SA['jdbc'],self.id_sa) or mod_cdb
            if mod_cdb == True:
                conn.apuntaModificado( "tb_servaplicaciones","id_sa",self.id_sa)
                
        return mod_cdb,self.puerto
