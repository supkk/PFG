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
        data='{"Code":"'+str(red[1])+'","nombre":"'+red[2]+'","Estado":'+str(api.retIdLookup('CI-Estado','NV'))+',"IPBase":"'+red[3]+'","Mascara":"'+red[4]+'"}'
        id_class = api.creaClase('Red',data)
        if  id_class > 0:
            sql = "update tb_net set _id =" + str(id_class) + " where id_net = " + str(red[1])
            con.actualizaTabla(sql)
            con.confirma()
    return

def main ():

    conn =bbdd.bbdd()
    api = cmdbuild.cmdbuild('192.168.1.41','admin','admin')
#    sincronizaRed(conn,api)
    sql = "select d.id_disp, s.id_serv from tb_disp d inner join tb_servidor s on d.id_disp = s.id_disp where fsync ='01/01/01'"

    lServidores = conn.consulta(sql)
    for s in lServidores:
        serv = objServidor.objServidor(id_disp=s[0],id_serv=s[1])
        serv.sincroniza(api,conn)
    return

if __name__ == '__main__':
    main()
    