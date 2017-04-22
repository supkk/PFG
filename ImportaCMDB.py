'''
Created on 28 mar. 2017

@author: jose
'''
from objetos import bbdd
from objetos import objServidor
from objetos import cmdbuild
import time


def sincronizaRed(con,api):
    
    sql = 'select * from tb_net where _id is null'
    redes = con.consulta(sql)
    for red in redes:
        data='{"Code":"'+str(red[1])+'","nombre":"'+red[2]+'","Estado":'+str(api.retIdLookup('CI-Estado','NV'))+',"IPBase":"'+red[3]+'","Mascara":"'+red[4]+'"}'
        id_class = api.creaClase('Red',data)
        if  id_class > 0:
            sql = "update tb_net set _id =" + str(id_class) + " where id_net = " + str(red[1])
            con.actualizaTabla(sql)

    return

def sincronizaCatalogoSw(con,api):
    
    sql = 'select id_sw,Descripcion,id_cat,n_proceso,_id from tb_inv_software where _id is null'
    soft = con.consulta(sql)
    for sw in soft:
        data='{"Code":"'+str(sw[0])+'","Description":"'+sw[1]+'","Estado":'+str(api.retIdLookup('CI-Estado','NV'))+',"Categoria":"'+str(api.retIdLookup('Software-Tipo',sw[2]))+'","Patron":"'+sw[3]+'"}'
        id_class = api.creaClase('CatalogoSw',data)
        if  id_class > 0:
            sql = "update tb_inv_software set _id =" + str(id_class) + " where id_sw = " + str(sw[0])
            con.actualizaTabla(sql)
    return

def recuperaConfig(conn):
    
    sql = 'select * from tb_sda_config'
    config = conn.consulta(sql)
    return config

def actualizaFSync(conn):
    
    sql = "update tb_sda_config set fsync = '"+time.strftime("%c")+"'"
    conn.actualizaTabla(sql)
    
def main ():

    conn = bbdd.bbdd()
    config = recuperaConfig(conn)
    ultimaSync = config[0][1]
    api = cmdbuild.cmdbuild(config[0][2],config[0][3],config[0][4],config[0][5])
    sincronizaRed(conn,api)
    sincronizaCatalogoSw(conn,api)
    sql = "select d.id_disp, s.id_serv from tb_disp d inner join tb_servidor s on d.id_disp = s.id_disp where  s.fsync >= '" +str(config[0][1])+ "'" 
    lServidores = conn.consulta(sql)
    for s in lServidores:
        serv = objServidor.objServidor(id_disp=s[0],id_serv=s[1])
        serv.sincroniza(api,conn,ultimaSync)
    actualizaFSync(conn)
    return
    
if __name__ == '__main__':
    main()
    