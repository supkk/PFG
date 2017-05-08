# -*- coding: utf-8 -*-
'''
Created on 7 may. 2017

@author: jose
'''

from objetos import objSi
import time
from xdg.Locale import update

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
        
    
    def descubre(self,cnf):
        
        modulo = "from plugins import "+self.soft + " as module"
        exec modulo
        self.dic_BD = modulo.descubre(host=super(objSoftBBDD,self).ip,u=cnf['user'],p=cnf['password'],port=self.puerto)
        super(objSoftBBDD,self).version = self.dicBD['version']
        return
    
    def actualizaInstancia(self,id_si):
        di = conn.retInstanciaSW(id_si)
        data = ()
        modificado =False
        return modificado
    
    def actualizaEsquema(self,eqm):
        modificado =False
        return modificado
    
    def actualizaTabla(self,tb):
        modificado =False
        return modificado
    
    def actualizaAtrTabla(self,attb):
        modificado =False
        return modificado
    
    def apuntaModificado (self, conn,tabla, id, id_valor):
        sql = "update "+ tabla+ "set fsync ='"+time.strftime("%c")+"' where "+ id +"="+id_valor
        conn.actualizaTabla(sql)
        return
    
    def gestionaBorrados(self, conn,tabla,dic,id):
    
        return
    
    def grabaBBDD(self,conn):
        modificado = False
        id_si = conn.existeInstanciaSW(super(objSoftBBDD,self).idserv,super(objSoftBBDD,self).id_sw,self.puerto) 
        if id_si == None :
            id_si = super(objSoftBBDD,self).grabaBBDD(conn)
            data = (id_si,self.puerto,self.dicBD['admin'],time.strftime("%c"))
            sql ='insert into tb_bd (id_si,puerto,admin,fsync) values(%s,%s,%s,%s)'
            id_db=conn.actualizaTabla(sql,data)
            if id_db <> None:
                modificado = True
                for eqm in self.dic_BD['Esquema']:
                    data = (id_db, eqm['nombre'],eqm['nombre_bd'],eqm['propietario'],time.strftime("%c"))
                    sql = 'insert into tb_esquemadb (id_db,nombre, nombre_db,propietario,fsync) values (%s,%s,%s,%s,%s)'
                    id_edb=conn.actualizaTabla(sql,data)
                    if id_edb <>None:
                        for tb in eqm['Tablas']:
                            data = (id_edb,tb['nombre'],tb['tipo'],time.strftime("%c"))
                            sql = 'insert into tb_tabla (id_edb,nombre,id_tipo_tabla,fsync) values (%s,%s,%s,%s)'
                            id_tb=conn.actualizaTabla(sql,data)
                            for atb in tb['altTabla']:
                                data=(id_tb,atb['nombre'],atb['tipo'],atb['indice'],time.strftime("%c"))
                                sql ='insert into tb_atributotabla (id_tb,nombre,indice,fsync) values (%s,%s,%s,%s)'
                                conn.actualizaTabla(sql,data)
        else :
            modificado = self.actualizaInstancia(id_si)    
            for eqm in self.dic_BD['Esquema']:
                mod,id_edb = self.actualizaEsquema(eqm)    
                modificado = mod or modificado
                mod_tb=False
                for tb in eqm['Tablas']:
                    id_tb,mod = self.actualizaTabla(tb)    
                    mod_tb = mod or mod_tb
                    mod_atr=False
                    for atb in tb['altTabla']:
                        id_atr,mod = self.actualizaAtrTabla(atb)   
                        mod_atr = mod or mod_atr
                    mod_atr = self.gestionaBorrados(conn,"tb_atributoTabla",tb['altTabla'],id_tb) or mod_atr
                    if mod_atr == True:
                        modificado=True    
                        self.apuntaModificado(conn,"tb_tabla","id_tb",id_tb)
                mod_tb = self.gestionaBorrados(conn,"tb_Tabla",tb['tabla'],id_edb) or mod_tb
                if mod_tb == True :
                    modificado = True
                    self.apuntaModificado(conn, "tb_EsquemaDB","id_edb",id_edb)
            modificado = self.gestionaBorrados(conn,"tb_db","id_si") or modificado
            if modificado== True:
                self.apuntaModificado(conn, "tb_bd","id_si",id_si)
        return modificado