# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''

from objetos import objSi
import time



class objSoftBBDD(objSi.objSi):
    '''
    classdocs
    '''

    def __init__(self, idserv=0, sw=0, ent='PRO',ip='',soft='',user='',port=0,home=''):
        '''
        Constructor
        '''
        super(objSoftBBDD,self).__init__(id_serv=idserv,id_sw=sw,id_entorno=ent,ip=ip,user=user,home=home)
        self.soft=soft
        self.puerto=port
        self.dic_BD={}
        self.id_db = 0
        self.id_si = 0
        
    
    def descubre(self,cnf,param):
        
        modulo = "from plugins import "+self.soft + " as module"
        exec modulo
        cnf=cnf['conecta_bd']
        self.dic_BD = module.descubre(ip=self.ip,user=cnf['user'],password=cnf['password'],port=self.puerto)
        if self.dic_BD <> None:
            self.version = self.dic_BD['version']

        return self.dic_BD <> None
    
    def actualizaInstancia(self,id_si,conn):
        
        modificado = super(objSoftBBDD,self).actualizaInstancia(id_si, conn)
        dbd,id_db= conn.retInstanciaBD(id_si)
        data =(self.dic_BD['admin'])
        if data <> dbd :
            sql ="update tb_bd set admin=%s, fsync="+time.strftime("%c")+"' where id_si="+str(id_si)
            conn.actualizaTabla(sql,data)
            modificado = True
        
        return modificado,id_db
    
    def actualizaEsquema(self,eqm,conn,id_db):
        
        modificado =False
        de,id_edb = conn.retEsquemaDB(eqm['nombre'],eqm['nombre_db'])
        data = (eqm['propietario'])
        if id_edb <> None :
            if de <> data :
                sql ="update tb_bd set propietario=%s, fsync="+time.strftime("%c")+"' where id_si="+str(id_edb)
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data = (self.id_db,eqm['nombre'],eqm['propietario'],time.strftime("%c"),eqm['nombre_db'])
            sql ="insert into tb_esquemabd (id_db,nombre,propietario,fsync,nombre_db) values (%s,%s,%s,%s,%s)"
            id_edb=conn.actualizaTabla(sql,data)
            print (time.strftime("%c")+"-- Actualizada esquema BBDD "+eqm['nombre']+ " en BD "+eqm['nombre_db'])
            modificado =True
    
 
        return modificado,id_edb
    
    def actualizaTabla(self,tb,conn,id_edb):
        
        modificado =False
        dt,id_tb = conn.retTablaDB(tb['nombre'],id_edb)
        data = (tb['tipo'])
        if id_tb <> None :
            if dt <> data :
                sql ="update tb_tabla set id_tipo_tabla=%s, fsync="+time.strftime("%c")+"' where id_si="+str(id_tb)
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data = (id_edb,tb['nombre'],tb['tipo'],time.strftime("%c"))
            sql ="insert into tb_tabla (id_edb,nombre,id_tipo_tabla,fsync) values (%s,%s,%s,%s)"
            id_tb=conn.actualizaTabla(sql,data)
            modificado =True
 
        return modificado,id_tb
    
    def actualizaAtrTabla(self,attb,conn,id_tb):
        
        modificado =False
        datt,id_atr = conn.retAttrTablaDB(attb['nombre'],id_tb)
        data = (attb['indice']=="True")
        if id_atr <> None :
            if datt <> data :
                sql ="update tb_atributotabla set indice=%s, fsync='"+time.strftime("%c")+"' where id_si="+str(id_atr)
                conn.actualizaTabla(sql,data)
                modificado =True
        else:
            data = (id_tb,attb['nombre'],attb['indice'],time.strftime("%c"))
            sql ="insert into tb_atributotabla (id_tb,nombre,indice,fsync) values (%s,%s,%s,%s)"
            id_tb=conn.actualizaTabla(sql,data)
            modificado =True
 
        return modificado,id_tb
    
    
    def marcarAttrTablaBorrados(self,conn,id_valor):
        
        sql = "update tb_AtributoTabla set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_att="+str(id_valor) 
        conn.actualizaTabla(sql)
        return
    
    def gestionaAttrTablaBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select id_att,nombre from  TB_atributoTabla where id_tb=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for Attr in dic :
                if item[1]== Attr['nombre'] :
                    encontrado =True
                    break
            if not encontrado :
                self.marcarAttrTablaBorrados(conn,item[0])
                modificado = True         
                
        return modificado
    
    def marcarTablaBorrados(self,conn,id_valor):
        
        sql = "update tb_Tabla set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_tb="+str(id_valor) 
        conn.actualizaTabla(sql)
        sql = "select id_att from tb_atributoTabla where id_tb="+str(id_valor)
        lattrtablas =conn.consulta(sql)
        for attb in lattrtablas :
            self.marcarAttrTablaBorrados(conn,attb[0])
        
        return
    
    def gestionaTablaBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select id_tb,nombre from  TB_Tabla where id_edb=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for tabla in dic :
                if item[1]== tabla['nombre'] :
                    encontrado =True
                    break
            if not encontrado :
                self.marcarTablaBorrados(conn,item[0])
                modificado = True         
                
        return modificado
    
    def marcarEqmBorrados(self,conn,id_valor):
        
        sql = "update tb_EsquemaBD set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_edb="+str(id_valor) 
        conn.actualizaTabla(sql)
        sql = "select id_tb from tb_Tabla where id_edb="+str(id_valor)
        ltablas =conn.consulta(sql)
        for tb in ltablas :
            self.marcarTablaBorrados(conn,tb[0])
        
        return
    
    def gestionaEqmBorrados(self, conn,dic, id_valor):
        
        modificado =False
        sql= "select id_edb,nombre,nombre_db from  TB_EsquemaBD where id_db=" + str(id_valor)
        litem = conn.consulta(sql)
        for item in litem:
            encontrado = False
            for eqm in dic :
                if item[1]== eqm['nombre'] and item[2] == eqm['nombre_db']:
                    encontrado =True
                    break
            if not encontrado :
                self.marcarEqmBorrados(conn,item[0])
                modificado =True
                
        return modificado
    
    def grabaBBDD(self,conn):
        
        modificado = False
        id_si = conn.existeInstanciaSW(self.id_serv,self.id_sw,self.puerto,'tb_db') 
        if id_si == None :
            id_si = super(objSoftBBDD,self).grabaBBDD(conn)
            data = (id_si,self.puerto,self.dic_BD['admin'],time.strftime("%c"))
            sql ='insert into tb_db (id_si,puerto,admin,fsync) values(%s,%s,%s,%s)'
            id_db=conn.actualizaTabla(sql,data)
            if id_db <> None:
                modificado = True
                for eqm in self.dic_BD['Esquema']:
                    data = (id_db, eqm['nombre'],eqm['nombre_db'],eqm['propietario'],time.strftime("%c"))
                    sql = 'insert into tb_esquemabd (id_db,nombre, nombre_db,propietario,fsync) values (%s,%s,%s,%s,%s)'
                    id_edb=conn.actualizaTabla(sql,data)
                    print (time.strftime("%c")+"-- Insertada instancia BBDD "+eqm['nombre_db']+ " con esquema "+eqm['nombre'])
                    if id_edb <>None:
                        for tb in eqm['Tablas']:
                            data = (id_edb,tb['nombre'],tb['tipo'],time.strftime("%c"))
                            print (time.strftime("%c")+"-- Insertada Tabla BBDD "+tb['nombre']+ " en esquema "+eqm['nombre'])
                            sql = 'insert into tb_tabla (id_edb,nombre,id_tipo_tabla,fsync) values (%s,%s,%s,%s)'
                            id_tb=conn.actualizaTabla(sql,data)
                            for atb in tb['attTabla']:
                                data=(id_tb,atb['nombre'],atb['indice'],time.strftime("%c"))
                                sql ='insert into tb_atributotabla (id_tb,nombre,indice,fsync) values (%s,%s,%s,%s)'
                                conn.actualizaTabla(sql,data)
        else :
            modificado, self.id_db = self.actualizaInstancia(id_si,conn)    
            for eqm in self.dic_BD['Esquema']:
                mod,id_edb = self.actualizaEsquema(eqm,conn,self.id_db)    
                modificado = mod or modificado
                mod_tb=False
                for tb in eqm['Tablas']:
                    mod, id_tb = self.actualizaTabla(tb,conn,id_edb)    
                    mod_tb = mod or mod_tb
                    mod_atr=False
                    for atb in tb['attTabla']:
                        mod = self.actualizaAtrTabla(atb,conn,id_tb)   
                        mod_atr = mod or mod_atr
                    mod_atr = self.gestionaAttrTablaBorrados(conn,tb['attTabla'],id_tb) or mod_atr
                    if mod_atr == True:
                        modificado=True    
                        conn.apuntaModificado("tb_tabla","id_tb",id_tb)
                mod_tb = self.gestionaTablaBorrados(conn,eqm['Tablas'],id_edb) or mod_tb
                if mod_tb == True :
                    modificado = True
                    conn.apuntaModificado("tb_EsquemaBD","id_edb",id_edb)
            modificado = self.gestionaEqmBorrados(conn,self.dic_BD['Esquema'], self.id_db) or modificado
            if modificado== True:
                conn.apuntaModificado( "tb_db","id_si",id_si)
        return modificado,self.puerto
    
    
    
    
    