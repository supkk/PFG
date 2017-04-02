'''
Created on 28 mar. 2017

@author: jose
'''
from objetos import bbdd
from objetos import objServidor
from objetos import cmdbuild

def sincronizaRed(con,api):
    
    sql = 'select * from tb_net where _id is null'
    redes = con.consulta(sql)
    for red in redes:
        data='{"Code":"'+str(red[1])+'","Descripcion":"'+red[2]+'","Estado":1,"IPBase":"'+red[3]+'","mascara":"'+red[4]+'"}'
        id_class = api.creaClase('Red',data)
        if "Error" not in id_class:
            sql = "update tb_net set _id =" + id_class + " where id_red = " + chr(red[1])
            con.actualizaTabla(sql)
    return

def main ():

    conn =bbdd.bbdd()
    api = cmdbuild.cmdbuild('192.168.1.41','admin','admin')
    sincronizaRed(conn,api)
    sql = "select d.id_disp, s.id_serv from tb_disp d inner join tb_servidor s on d.id_disp = s.id_disp where fsync ='01/01/01'"

    lServidores = conn.consulta(sql)
    for s in lServidores:
        serv = objServidor.objServidor(id_disp=s[0],id_serv=s[1])
        serv.sincroniza(api)
    return

if __name__ == '__main__':
    main()
    