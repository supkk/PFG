# -*- coding: utf-8 -*-
'''
Created on 8 mar. 2017

@author: jose
'''
import psycopg2
import ipcalc
import time
 
class bbdd():
    '''
    Contiene metodos de acceso a la BD de SDA
    '''

    def __init__(self, bd="sda_db",u="postgres",pw="postgres",h="192.168.1.20",p="5432"):
        
        '''
        Constructor
        
        Parametros
            bd_: nombre de BD
            u : Usuario de BD
            pw: Password del usuario de BD
            h: Ip donde escucha la BD
            p: Puerto que escucha la BD
        '''
        self.cur = None
        try :
            self.conn = psycopg2.connect(database=bd, user=u, password=pw, host=h, port=p)
        except :
            print ("Error de acceso a BBDD nn")  
        return   
    
    def confirma(self):
        
        '''
        Confirma una transaccion
        '''
        
        self.conn.commit()   
        return
    
    def deshace(self):
        '''
        Realiza el Rollback de una Transaccion
        '''
        self.conn.rollback()
        return
    
    def consulta (self,con, data=None):
        
        '''
        Ejecuta una sentencia SELECT
        
        Parametros:
        
            con: Consulta a ejecutar
            data : parametros de la consulta
        
        Salida:
            Lista de Tuplas con los valores de retorno
        '''
        
        self.cur=self.conn.cursor()
        if data is None:
            self.cur.execute(con)
        else :
            self.cur.execute(con,data)
        rows = self.cur.fetchall()
        
        return rows
    
    def apuntaApagado(self,ip):
        
        '''
        Apunta en la BBDD que el servidor está apagado
        
        Parámetros
        
            ip: IP escaneada
        
        '''
       
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
        
        '''
        Apunta en la BBDD que el servidor está se ha procesado correctamente
        
        Parámetros
        
            ip: IP escaneada
            id_Disp : identificador de Dispositivo procesado
        
        '''
        
        cur=self.conn.cursor()
        cur.execute("update tb_dispositivos  set fecproc='"+time.strftime("%c") + "' where ip='" + ip +"'")
        cur.execute("update tb_dispositivos set apagado = 0  where ip='" + ip+"'")
        cur.execute("update tb_dispositivos set id_disp ="+str(id_disp)+"  where ip='"+ ip +"'")
        cur.close()
        return
    
    def apuntaModificado (self, tabla, id_nombre, id_valor):
        
        '''
        Apunta en la BD que el CI ha sido modificado durante el inventariado
        
        Parametros
        
            tabla: Tabla deonde se guarda el objeto
            id_nombre : Nombre del atributo identicador 
            id_valor : Identificador del objeto
            
        '''
        
        sql = "update "+ tabla+ " set fsync ='"+time.strftime("%c")+"' where "+ id_nombre +"="+str(id_valor)
        self.actualizaTabla(sql)
        return
    
    def retIdFab(self,desc):
        
        '''
        Retorna el identificador del fabricante del CI 
        
        Parámetros
        
            desc : nombre del fabricante
        
        Salida
        
            Código del fabricante
        
        '''
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_MarcaDisp where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            code_retorno = 'NA'
        else :
            code_retorno = code_id[0]
            
        return code_retorno  
    
    def retIdTipoFS(self,desc):
        
        '''
        Retorna el identificador del tipo de fichero
        
        Parámetros
        
            desc : nombre del tipo de fichero
        
        Salida
        
            Código del tipo de fichero
        '''
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_fs where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            code_retorno = 'OTR'
        else :
            code_retorno = code_id[0]
        return code_retorno
    
    def retIdTipoAl(self,desc):
        
        '''
        Retorna el identificador del tipo de almacenamiento
        
        Parámetros
        
            desc : nombre del tipo de almacenamiento
        
        Salida
        
            Código del tipo de almacenamiento
        '''       
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_Almacenamiento where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            code_retorno = 'OTR'
        else :
            code_retorno = code_id[0]
        return code_retorno
    
    def retIdDesc(self,desc):
        '''
        Retorna el identificador del tipo de Descubrimiento
        
        Parámetros
        
            desc : nombre del tipo de Descubrimiento
        
        Salida
        
            Código del tipo de Descubrimiento
        '''
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_Desc where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            code_id =["OT"]
        return code_id[0]
    
    def retIdDisp(self,idServ):
        '''
        Retorna el identificador del Dispositivo
        
        Parámetros
        
            idServ : nombre del Dispositivo
        
        Salida
        
            Código del Dispositivo
        '''
        
        cur=self.conn.cursor()
        cur.execute("select id_disp from tb_Servidor where id_serv ="+str(idServ))
        code_id = cur.fetchone()
        cur.close()
        return code_id[0]
    
    def retIdserv(self,idDisp):
        '''
        Retorna el identificador del Servidor
        
        Parámetros
        
            idDisp : nombre del Servidor
        
        Salida
        
            Código del Servidor
        '''
        
        cur=self.conn.cursor()
        cur.execute("select id_serv from tb_Servidor where id_disp ="+str(idDisp))
        code_id = cur.fetchone()
        cur.close()
        return code_id[0]
    
    def retNombreServ(self,id_disp):
        
        '''
        Retorna el Nombre del Servidor
        
        Parámetros
        
            id_disp : Identificador del Servidor
        
        Salida
        
            Nombre del Servidor
        '''
        
        cur=self.conn.cursor()
        cur.execute("select nombre from tb_disp where id_disp ="+str(id_disp))
        code_id = cur.fetchone()
        cur.close()
        return code_id[0]
    
    def retIdSO(self,desc):
        '''
        Retorna el identificador del sistema Operativo
        
        Parámetros
        
            desc : nombre del Sistema Operativo
        
        Salida
        
            Código del Sistema Operativo
        '''
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_so where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_id =["ND"]
        return code_id[0]
    
    def retDescSoftware (self,idw):
        
        '''
        Retorna la Descripcion del Software
        
        Parámetros
        
            idw : Identificador del Software
        
        Salida
        
             Descipción del Software
        '''
        
        cur=self.conn.cursor()
        cur.execute("select descripcion from tb_inv_software where id_sw = " + str(idw))
        res = cur.fetchone()
        cur.close()
             
        return res[0]
    
    def retIdCatalogoSw (self,idw):
        
        '''
        Retorna el identificador  del Software en el catálogo
        
        Parámetros
        
            idsw : Identificador del Software 
        
        Salida
        
            Descipción del Software en el catálogo
        '''
        
        cur=self.conn.cursor()
        cur.execute("select _id from tb_inv_software where id_sw = " + str(idw))
        res = cur.fetchone()
        cur.close()
        
        return res[0]
    
    def retIdNet(self,desc):
        '''
        Retorna el identificador  de la red
        
        Parámetros
        
            desc : Nombre de la red
        
        Salida
        
            Identificador de la red
        '''
        
        cur=self.conn.cursor()
        cur.execute("select code from tb_lkp_Interface where descripcion ='"+desc.upper()+"'")
        code_id = cur.fetchone()
        cur.close()
            
        return code_id[0]
    
    def retCodeRed(self,idRed):
        
        '''
        Retorna el Nombre   de la red
        
        Parámetros
        
            idRed : Nombre de la red
        
        Salida
        
            Identificador de la red
        '''
        
        cur=self.conn.cursor()
        cur.execute("select _id from tb_net where id_net =" + str(idRed))
        code_id = cur.fetchone()
        cur.close()
        return code_id[0]
    
    
    def retIdSoftware(self,desc):
        '''
        Retorna el identificador  del software a partir de la cadena de busqueda
        
        Parámetros
        
            desc : Cadena de busqueda del software
        
        Salida
        
            Identificador del software
        '''
        
        cur=self.conn.cursor()
        cur.execute("select id_sw from tb_inv_software where n_proceso ='"+desc+"'")
        code_id = cur.fetchone()
        cur.close()
            
        return code_id[0]
    
    def retCadSoftware(self,desc):
        '''
        Retorna la cadena de busqueda del software a partir del identificador de este
        
        Parámetros
        
            desc : Identificador del software
        
        Salida
        
            Cadena de busqueda del software
        '''
        
        cur=self.conn.cursor()
        cur.execute("select n_proceso from tb_inv_software where id_sw =" + str(desc))
        code_id = cur.fetchone()
        cur.close()
            
        return code_id[0]
    
    def retCatSoftware(self,idsw):
        '''
        Retorna la categoria del software a partir del identificador de este
        
        Parámetros
        
            idsw : Identificador del software
        
        Salida
        
            Categoria del software
        '''
        
        cur=self.conn.cursor()
        cur.execute("select id_cat,n_proceso from tb_inv_software where id_sw =" + str(idsw))
        code_id = cur.fetchone()
        cur.close()
            
        return code_id
    
    def retEntorno(self, idServ):
        '''
        Retorna entorno de ejecución en el que se ubica un servidor
        
        Parámetros
        
            idServ : Identificador del software
        
        Salida
        
            Entorno de ejecución
        '''
        
        cur=self.conn.cursor()
        cur.execute("select id_entorno from tb_servidor where id_serv =" + str(idServ))
        code_id = cur.fetchone()
        cur.close()
        return code_id[0]
    
    def retSofInstancia(self,id_sw,id_serv):
        '''
        Retorna los atributos de una instancia de software que se ejecuta en un servidor
        
        Parámetros
        
            id_sw : Identidicador del software
            id_serv : Identificador del servidor
        
        Salida
        
            data: Atributos de la instancia
            id_si : Identificador de la instancia de software
        '''
        
        data= (id_sw,id_serv)
        sql = "select id_si from tb_softwareinstancia where id_sw=%s and id_serv=%s"
        id_si=self.consulta(sql, data)
        if len(id_si)>0:
            data = self.retInstanciaSW(id_si[0][0])
            id_si = id_si[0][0]
        else:
            data=None
            id_si=None
            
        return data,id_si
    
    def retInstanciaSW(self,id_si):
        '''
        Retorna los atributos de una instancia de software 
        
        Parámetros
        
            id_si : Identificador del software
        
        
        Salida
        
            data: Atributos de la instancia
        '''
        
        cur=self.conn.cursor()
        cur.execute("select version, home, usuario,id_entorno from  tb_softwareinstancia where id_si=" + str(id_si))
        code_id = cur.fetchone()
        cur.close()
        
        return code_id
    
    def retInstanciaBD(self,id_si):
        '''
        Retorna los atributos de una instancia de BBDD
        
        Parámetro
        
            id_si : Identificador de la instancia
        
        Salida
            code_id[0]: Administrador de la BD
            code_id[0]: Identificador de la BD
        
        '''
    
        cur=self.conn.cursor()
        cur.execute("select admin,id_db from  tb_db where id_si=" + str(id_si))
        code_id = cur.fetchone()
        cur.close()
        
        return (code_id[0]),code_id[1]
    
    def retInstanciaSA(self,id_si):
        '''
        Retorna los atributos de una instancia de Servidor de Aplicaciones
        
        Parámetro
        
            id_si : Identificador de la instancia
        
        Salida
            code_id[0]: JVM
            code_id[0]: Identificador del S.A.
        
        '''
        
        cur=self.conn.cursor()
        cur.execute("select jvm,id_sa from  tb_servaplicaciones where id_si=" + str(id_si))
        code_id = cur.fetchone()
        cur.close()
        
        return (code_id[0]),code_id[1]
    
    def retInstanciaWeb(self,id_si):
        '''
        Retorna los atributos de una instancia de Servidor WEB
        
        Parámetro
        
            id_si : Identificador de la instancia
        
        Salida
            code_id[0]: Url de admnistración
            code_id[0]: Identificador del Web.
        
        '''
        
        cur=self.conn.cursor()
        cur.execute("select urladmin,id_web from  tb_servweb where id_si=" + str(id_si))
        code_id = cur.fetchone()
        cur.close()
        
        return (code_id[0]),code_id[1]

    def retInstanciaVH(self,id_web,dns,puerto ):
        
        '''
        Retorna los atributos de una VirtualHost
        
        Parámetro
        
            id_web : Identificador del Servidor Web
            dns    : Nommbre DNS del VH
            puerto : Puerto de escucha
        
        Salida
            result: Atributos del VH
            id_vh: Identificador del VH.
        
        '''
    
        cur=self.conn.cursor()
        data =(id_web,dns,puerto)
        cur.execute("select ssl,rcert,rutacert,id_vh from tb_vhost where id_web=%s and dns=%s and puerto = %s",data)
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            result = None
            id_vh = None
        else :       
            result = (code_id[0],code_id[1],code_id[2])  
            id_vh = code_id[3]
        return result, id_vh
    
    def existeInstanciaUrl(self,id_vh, nombre):
        '''
        Indica si existe una url en un virtualhost, en caso afirmativo devuelve sus atributos
        
        Parámetro
        
            id_vh : Identificador del VirtualHost
            nombre    : Nombre del recurso URL
        
        Salida
            result: Atributos de la URL
            id_url: Identificador de la URL.
        '''
        
        cur=self.conn.cursor()
        data=(nombre,id_vh)
        cur.execute("select valor,id_tipo,id_url from  tb_url where nombre=%s and id_vh=%s",data)
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            result = None
            id_url = None
        else :       
            result = (code_id[0],code_id[1])  
            id_url = code_id[2]
        return result,id_url
    
    def existeRelacionUrl(self,data):
        
        '''
        Indica si existe la relación entre la aplicación y url especificada

        Parametro
        
            data : Datos de la relación (aplicacion, url y tipo de url)
        
        Salida
             True --> Existe 
             False --> No   
        '''
        
        dt =(data[0],data[1],data[2])
        sql="select id_apl from tb_map_url_apl where id_apl=%s and id_url=%s and tipo_url=%s"
        Correcto=(len(self.consulta(sql, data=dt))> 0)
        
        return Correcto
    
    def existeRelacionCBD(self,data):
        '''
        Indica si existe la relación entre la aplicación y y el conectorJDBC especificado

        Parametro
        
           data : Datos de la relación (aplicacion, JDBC)
        
        Salida
             True --> Existe 
             False --> No   
        '''
        
        sql="select id_cbd from tb_map_cbd_apl where id_apl=%s and id_cbd=%s"
        Correcto=(len(self.consulta(sql, data=data))> 0)
        
        return Correcto
    
    def existeRelacionSA(self,data):
        '''
        Indica si existe la relación entre la aplicación y el servidor de aplicaciones especificado

        Parametro
        
            data : Datos de la relación (aplicacion, Servidor de aplicacion)
        
        Salida
             True --> Existe 
             False --> No   
        '''
        
        sql="select id_apl from tb_map_sa_ap where id_apl=%s and id_sa=%s"
        Correcto=(len(self.consulta(sql, data=data))> 0)
        
        return Correcto
    
    def retIdUrl(self, nombre):
        
        '''
        Retorna el identificador de la url proporcionada
        
        Parametro
        
            nombre: Nombre de  la url
        
        Salida
        
            Identificador de la url
        '''
        
        cur=self.conn.cursor()
        cur.execute("select id_url from  tb_url where valor='"+nombre+"'")
        code_id = cur.fetchall()
        cur.close()
       
        return code_id
    
    def retidClassUrl(self, id_url):
        '''
        Retorna el identificador en CMDBuild de la url proporcionada
        
        Parametro
        
            id_url: Identificador de  la url
        
        Salida
        
            Identificador CMDBuild de la url
        '''
        
        cur=self.conn.cursor()
        cur.execute("select _id from  tb_url where id_url="+str(id_url))
        code_id = cur.fetchall()
        cur.close()
       
        return code_id[0]
    
    def retidClassConectorJDBC(self, id_cbd):
        
        '''
        Retorna el identificador en CMDBuild del conector JDBC proporcionada
        
        Parametro
        
            id_cbd: Identificador del Conector
        
        Salida
        
            Identificador CMDBuild del conector
        '''
        
        cur=self.conn.cursor()
        cur.execute("select _id from  tb_conectorbd where id_cbd="+str(id_cbd))
        code_id = cur.fetchall()
        cur.close()
       
        return code_id[0]
    
    def retidClassSA(self, id_SA):
        
        '''
        Retorna el identificador en CMDBuild del Servido de Aplicaciones proporcionada
        
        Parametro
        
            Id_SA: Identificador del Servidor de Aplicaciones 
        
        Salida
        
            Identificador CMDBuild del conector
        '''
        
        cur=self.conn.cursor()
        cur.execute("select _id from  tb_ServAplicaciones where id_sa="+str(id_SA))
        code_id = cur.fetchall()
        cur.close()
       
        return code_id[0]
        
    
    def retEsquemaDB(self,nombre, nombre_db):
        '''
        Retorna los atributos de un esquema de BBDD
        
        Parámetro
        
            nombre: Nombre de esquema de BD
            nombre_db: nombre de BD
        
        Salida
            result: Atributos del Esquema de BD
            id_edb: Identificador de Esquema de BD.
        
        '''
    
        cur=self.conn.cursor()
        data =(nombre,nombre_db)
        cur.execute("select propietario,id_edb from  tb_esquemabd where nombre=%s and nombre_db=%s",data)
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            result = None
            id_edb = None
        else :       
            result = (code_id[0])  
            id_edb = code_id[1]
        return result, id_edb
    
    def retidsEsquemaBD(self,id_edb):
        '''
        Retorna el nombre y la BD de  un esquema de BBDD
        
        Parámetro
        
            id_edb : Identificador de BD
        
        Salida
        
             Atributos del Esquema de BD (nombre y Nombre DB)
        
        '''
        sql="select nombre,nombre_db from tb_esquemabd where id_edb="+str(id_edb)
        result=self.consulta(sql)
        
        return result
    
    def ret_IdEsquemaBD(self,nombre,nombre_db):
        
        '''
        Retorna el identificador en CMDBUild del Esquema de BD
        
        Parámetro
        
            nombre: Nombre de esquema de BD
            nombre_db: nombre de BD
        
        Salida
        
            Identificador en CMDBUild 
        '''
        
        data =(nombre,nombre_db)
        
        sql="select _id from tb_esquemabd where nombre= %s and nombre_db=%s"
        result=self.consulta(sql,data)
        
        return result[0][0]
    
    def apuntaId(self,tabla,id_Class,clave,clave_valor):
        '''
        Apunta el identificador de CMDBUild en el registro sincronizado
        
        Parametros
        
            tabla : Tabla de SDA
            Id_CLass:Identificador en CMDBuild
            clave :Atributo primario en la tabla
            clave_valor : Valor de la clave primaria
        
        '''
    
        sql = 'update '+ tabla + ' set _id='+str(id_Class) +' where '+ clave + "="+str(clave_valor)
        self.actualizaTabla(sql)
        
        return
    
    def retTablaDB(self,nombre, id_edb):
        
        '''
        Retorna los atributos de una tabla  de BBDD
        
        Parámetro
        
            nombre: Nombre de tabla de BD
            id_edb: Identificador de esquema 
        
        Salida
            result: Atributos de la tabla de BD
            id_edb: Identificador de la tabla de BD.
        
        '''
    
        cur=self.conn.cursor()
        data =(nombre,id_edb)
        cur.execute("select id_tipo_tabla,id_tb from  tb_tabla where nombre=%s and id_edb=%s",data)
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            result = None
            id_tb = None
        else :       
            result = (code_id[0])  
            id_tb = code_id[1]
        return result, id_tb
    
    def retAttrTablaDB(self,nombre, id_tb):
        
        '''
        Retorna los atributos de los campos de una tabla   de BBDD
        
        Parámetro
        
            nombre: Nombre de atributo
            id_tb: Identificador de id_tb 
        
        Salida
            result: Atributos de campo de tabla de BD
            id_attb: Identificador de la atributos de tabla de BD.
        
        '''
    
        cur=self.conn.cursor()
        data =(nombre,id_tb)
        cur.execute("select indice,id_tb from  tb_atributotabla where nombre=%s and id_tb=%s",data)
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            result = None
            id_attb = None
        else :       
            result = (code_id[0])  
            id_attb = code_id[1]
        return result, id_attb
    
    def retInstanciaCDB(self,id_sa, nombre):
        '''
        Retorna los atributos de un conector  de BBDD 
        
        Parámetro
        
            nombre: Nombre de conector
            id_sa: Identificador del SA donde esta desplegado 
        
        Salida
            result: Atributos del conector de BD
            id_attb: Identificador del conector de BD.
        
        ''' 
        
        
        cur=self.conn.cursor()
        data=(nombre,id_sa)
        cur.execute("select usuario,id_cbd from  tb_conectorbd where nombre=%s and id_sa=%s",data)
        code_id = cur.fetchone()
        cur.close()
        if code_id is None :
            result = None
            id_cdb = None
        else :       
            result = (code_id[0])  
            id_cdb = code_id[1]
        return result,id_cdb
    
    def retInstanciaApl(self,id_apl):
        '''
        Retorna los atributos de una aplicacion
        
        Parámetro
        
            id_apl: Identificador de aplicacion 
            
        Salida
        
            Identificador de la atributos de tabla de BD.
        
        '''
        
        cur=self.conn.cursor()
        cur.execute("select acronimo,nombre,version from  tb_aplicacion where id_apl="+str(id_apl))
        data = cur.fetchone()
        cur.close()
        return data
    
    
    def existeServer(self,nombre):
        
        '''
        Si existe el servidor, retorna su identificador 
        
        Parametros
        
            nombre: Nombre del servidor
        
        Salida
        
            Identificador del servidor
        
        '''
        
        cur=self.conn.cursor()
        cur.execute("select d.id_disp,s.id_serv from tb_disp d join tb_servidor s on d.id_disp=s.id_disp where d.nombre='"+nombre+"'")
        code_id = cur.fetchone()
        cur.close()
        
        return code_id
    
    def existeNet(self,ip, mascara):
        
        '''
        Si existe la red, retorna su identificador 
        
        Parametros
        
            ip: IP base de la red
            mascara: mascara de la red
        
        Salida
        
            Identificador de la red
        
        '''
             
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
        '''
        Si existe el interfaz de red, retorna sus atributos 
        
        Parametros
        
            nombre: Nombre del interfaz
            id_disp: Identificador del dispositivo al que pertenece
            
        Salida
        
            Atributos de la interfaz
        
        '''
        cur=self.conn.cursor()
        cur.execute("select id_TipoInt,id_net,ip,mascara,mac,nombre from TB_Interface where id_disp =" + str(id_disp)+" and nombre='"+nombre+"'")
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def existeFS(self,id_serv,montaje):
        
        '''
        Si existe el sistema de ficheros, retorna sus atributos 
        
        Parametros
        
            montaje: Punto de montaje del FS
            id_serv: Identificador del dispositivo donde está montado 
        
        Salida
        
            Atributos del FS
        
        '''

        cur=self.conn.cursor()
        cur.execute("select size,id_tipofs,id_tipoAl from TB_fs where id_serv =" + str(id_serv)+ " and montaje = '" + montaje + "'")
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def _existeSw(self,id_serv,id_soft):
        
        
        cur=self.conn.cursor()
        cur.execute("select id_serv from TB_soft_running where id_serv =" + str(id_serv)+ " and id_sw="+str(id_soft))
        result = cur.fetchone()
        cur.close()
        
        return result
    
    def existeAplicacion(self,nombre,id_sa):
        
        '''
        Si existe la aplicacion, retorna su identificador 
        
        Parametros
        
            nombre: nombre de  aplicacion
            id_sa: Identificador del servidor de aplicaciones 
        
        Salida
        
            identificador de la aplicacion
        
        '''
        cur=self.conn.cursor()
        data = (id_sa,nombre)
        cur.execute("select a.id_apl from tb_aplicacion a inner join tb_map_sa_ap m on a.id_apl=m.id_apl where m.id_sa = %s and a.nombre =%s",data)
        result = cur.fetchone()
        if result is None:
            id_apl= None
        else:
            id_apl= result[0]
        cur.close()
        
        return id_apl
    
    def _borraSw(self,id_serv):
        
        if self.cur == None:
            self.cur = self.conn.cursor()

        self.cur.execute('DELETE FROM TB_soft_running WHERE id_serv = ' + str(id_serv))
        return
    
    def existeInstanciaSW(self,id_serv,id_sw,puerto,tabla):
        
        '''
        Si existe la instancia de software, retorna su identificador 
        
        Parametros
        
            id_serv : Identificador de servidor
            id_sw: Identificador de software
            puerto : Puerto en el que escucha
            tabla : Tabla de SDA donde se almancena la instancia 
        
        Salida
        
            identificador de la instancia SW
        
        '''
        
        cur=self.conn.cursor()
        data = (id_serv,id_sw,puerto)
        sql = "select i.id_si from tb_softwareInstancia i inner join "+tabla+" b on i.id_si = b.id_si  where i.id_serv=%s and i.id_sw=%s and b.puerto=%s"
        cur.execute(sql,data)
        result = cur.fetchone()
        id_si=None
        if not result is None:
            id_si = result[0]
            
        return id_si
    
    def _borraInterfacesDisp(self,id_disp):
        
        if self.cur == None:
            self.cur = self.conn.cursor()

        self.cur.execute('DELETE FROM TB_Interface WHERE id_disp = ' + str(id_disp))
        return
    
    def _borraFS(self,id_serv):
        if self.cur == None:
            self.cur = self.conn.cursor()

        self.cur.execute('DELETE FROM TB_FS WHERE id_serv = ' + str(id_serv))
        return
    
    def _ExisteIpNoSync(self,ip):
        
        existe = False
        cur=self.conn.cursor()
        cur.execute("select id_disp from tb_dispositivos where ip ='"+ip+"'")
        result = cur.fetchone()
        cur.close()
        if result <> None :
            if result[0]==0:
                existe=True
        return  existe
    
    def insertaDisp(self,s):
        '''
        Inserta los datos del la IP descubierta en la BD
        
        Parametro
        
            s: Datos de la IP descubierta
        
        Salida
        
            Indica si la operacion ha sido correcta
        '''
        
        idDes=self.retIdDesc(s.td)
        idSO=self.retIdSO(s.os)
        Correcto = True
        
        cur=self.conn.cursor()
        try :
            if self._ExisteIpNoSync(s.ip):
                data=(s.fd,idDes,idSO,"N")
                sql = "update tb_dispositivos set fecdes=%s,id_td=%s,id_so=%s,proc=%s where ip='" + s.ip + "'"
            else :
                data=(s.ip,s.fd,idDes,idSO,"N",0,0)
                sql = "INSERT INTO TB_Dispositivos(ip,fecdes,id_td,id_so,proc,apagado,id_disp) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,data)
            self.confirma()
        except Exception, error:
            Correcto = False
            self.deshace()
        
        return Correcto
        
    def grabaServidor(self,s):
    
        '''
        Graba o actualiza los datos de un servidor en la BD
        
        parametro
        
            s: servidor 
        
        Salida
        
            modificado : Indica si se han modificado los atributos en la ultima ejecucion
            code_disp : Identificador del dispositivo
            code_serv : Identificador del servidor
        '''
        
        idSO=self.retIdSO(s.so)
        modificado = True
        code = self.existeServer(s.nombre)
        if code is None :
            data_disp=(s.sn,s.nombre,s.id_marca)
            sql_disp = 'INSERT INTO tb_disp (sn,nombre, id_marca) values (%s,%s,%s)'
            if self.cur is None :
                self.cur=self.conn.cursor()
            try :
                self.cur.execute(sql_disp,data_disp)
                self.cur.execute("select currval('tb_disp_id_disp_seq')")
                result=self.cur.fetchone()
                code_disp=result[0]
            except Exception, error :
                print (time.strftime("%c")+"--"+"Error al insertar dispositivo --> "+s.nombre)
                print (time.strftime("%c")+"--",error)
            data=(code_disp,idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os,time.strftime("%c"),s.entorno,s.virtual)
            sql= "INSERT INTO TB_Servidor (id_disp,id_so,ram,tipo_cpu,n_cpu,n_cores,gw,version_os,fsync,id_entorno,virtual) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(sql,data)
            if code is None :
                self.cur.execute("select currval('tb_servidor_id_serv_seq')")
                result=self.cur.fetchone()
                code_serv=result[0]
        else :
            code_disp = code[0]
            code_serv = code[1]
            data=(idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os,s.entorno,s.virtual)
            sql="select id_so,ram,tipo_cpu,n_cpu,n_cores,gw,version_os,id_entorno,virtual from tb_servidor where id_serv="+str(code_serv)
            datos_serv = self.consulta(sql)
            if data <> datos_serv[0]:
                data=(idSO,s.ram,s.cpu,s.ncpu,s.cores,s.gw,s.v_os,time.strftime("%c"),s.entorno,s.virtual)
                sql="UPDATE TB_Servidor SET  id_so =%s ,ram =%s ,tipo_cpu =%s ,n_cpu =%s, n_cores=%s, gw=%s, version_os=%s, fsync =%s ,id_entorno=%s, virtual=%s WHERE id_serv =" +str(code_serv) 
                self.cur=self.conn.cursor()
                self.cur.execute(sql,data)      
            else :
                modificado = False
                        
        return modificado, code_disp,code_serv
    
    def creaNet(self,ip,mask):
        
        '''
        Graba la red desacubierta
        
        Parametro
        
            ip :IP Base de la red
            mask:Mascara de la red
        
        Salida 
        
           Identificador de la red
        '''
        
        address = ipcalc.Network(ip,mask)  
        red = address.network().dq
        data = ("NET_"+red,red,mask)
        sql = 'insert into tb_net (nombre,red,mask) values (%s,%s,%s)'
        try:
            self.cur=self.conn.cursor()
            self.cur.execute(sql,data)
            self.cur.execute("select currval('tb_net_id_net_seq')")
            result=self.cur.fetchone()
            id_net=result[0]
        except Exception, error :
            id_net = 0
            
            
        return id_net
    
    def grabaIPS(self,ip,id_disp):
        '''
        Graba los datos del interface en la BD de SDA
        
        Parametro
        
            ip: Objeto IP a grabar
            id_disp :Identificador del dispositivo donde se encontró
        
        Salida
        
            modificado : Indica si se ha modificado
        '''
        
        cambiado = False
        
        idNet=self.existeNet(ip.ip,ip.mascara)
        if  idNet is None :
            idNet = self.CreaNet(ip.ip,ip.mascara)
        if idNet <> 0 :
            datosInterface = self.existeInterfaceDisp(ip.nombre,id_disp)
            tipoNet=self.retIdNet(ip.tipoRed)
            data = (tipoNet,idNet,ip.ip,ip.mascara,ip.mac,ip.nombre)
            if datosInterface is None :
                data = (tipoNet,idNet,ip.ip,ip.mascara,ip.mac,ip.nombre,id_disp,time.strftime("%c"))
                sql = "INSERT INTO TB_Interface (id_TipoInt,id_net,ip,mascara, mac, nombre, id_disp,fsync) VALUES (%s,%s,%s,%s, %s, %s, %s,%s)"
                if not self.cur is None :
                    try :
                        self.cur.execute(sql,data)
                        cambiado = True
                    except Exception, error :
                        print (time.strftime("%c")+"--"+ error)
                        print (time.strftime("%c")+"--"+"Error al insertar la IP  "+ ip.ip +" con mascara " + ip.mascara)
            else :
                if data <> datosInterface :
                    data = (tipoNet,idNet,ip.ip,ip.mascara,ip.mac,ip.nombre,time.strftime("%c"))
                    sql = "UPDATE TB_Interface SET id_TipoInt=%s,id_net=%s,ip=%s,mascara=%s, mac=%s, nombre=%s, fsync=%s where id_disp="+str(id_disp) + " and nombre = '" + ip.nombre + "'"                    
                    if not self.cur is None :
                        try :
                            self.cur.execute(sql,data)
                            cambiado = True
                        except Exception, error :
                            print (time.strftime("%c")+"--"+ error)
                            print (time.strftime("%c")+"--"+"Error al actualizar la red "+ ip.ip +" con mascara " + ip.mascara)
    
        else :
            print (time.strftime("%c")+"--"+"Error al grabar la red "+ ip.ip +" con mascara " + ip.mascara)    
        return cambiado
   
    def grabaFS(self,fs,id_serv):
        
        '''
        Graba los datos del FS en la BD de SDA
        
        Parametro
        
            fs: Objeto fs a grabar
            id_serv :Identificador del servidor donde se encontró
        
        Salida
        
            modificado : Indica si se ha modificado
        '''

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

    def actualizaTabla(self,sql,data=None,confirma=True, lastval=True):
        
        '''
        Ejecuta una operación de actualización de una tabla de BD
        
        Parametros
        
            sql: Sentencia a ejecutar
            data: parametros de la sentencia
            confirma : Indica si se realiza un commit posterior
            lastval: Indica si se retorna el identificador del objeto insertado
            
        Salida 
        
            Identificador del objeto insertado
        '''
        
        cur=self.conn.cursor()
        if data is None:
            cur.execute(sql)
        else:
            cur.execute(sql,data)
        if "INSERT" in sql.upper() and lastval:
            self.cur.execute("select lastval()")
            result=self.cur.fetchone()
        else :
            result=[None]
        cur.close()
        if confirma:
            self.confirma()
        
        return result[0]
    
    
    def borraConectoresDB(self,id_si):
        '''
        Marca como Borrado el conector de la BD
        
        Parametro:
            id_si : Identificador de la instancia de BD
        '''
        
        sql='select c.id_cbd from tb_servaplicaciones s inner join tb_Conectorbd c on c.id_sa = s.id_sa where s.id_si = ' + str(id_si)
        lcon=self.consulta(sql)
        for con in lcon:
            sql = "update tb_conectorbd set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_cdb="+str(con[0])
            self.actualizaTabla(sql,confirma=False)
    
        return True
    
    def borraBD(self,id_si):

        '''
        Marca como Borradouna instancia de BD
        
        Parametro:
            id_si : Identificador de la instancia de BD
        '''
        
        sql = 'select e.id_edb from tb_db d inner join tb_esquemabd e on e.id_db = d.id_db where d.id_si='+ str(id_si)
        lcon=self.consulta(sql)
        for con in lcon:
            sql = "update tb_esquemabd set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_edb="+str(con[0])
            self.actualizaTabla(sql,confirma=False)
            sql = "update tb_tabla set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_edb="+str(con[0])
            self.actualizaTabla(sql,confirma=False)
            sql= "select id_tb from tb_tabla where id_edb="+ str(con)
            ltb= self.consulta(sql)
            for tb in ltb:
                sql = "update tb_atributotabla set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_tb="+str(tb[0])
                self.actualizaTabla(sql,confirma=False) 
        return True
    
    def borraSWeb(self,id_si):
        '''
        Marca como Borradouna instancia de Servidor WEB
        
        Parametro:
            id_si : Identificador de la instancia de Servidor WEB
        '''
        sql = "select v.id_vh from tb_servweb s inner join tb_vhost v on v.id_web = s.id_web where s.id_si="+str(id_si)
        lvh=self.consulta(sql)
        for vh in lvh:
            sql = "update tb_vhost set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_vh="+str(vh[0])
            self.actualizaTabla(sql,confirma=False)       
            sql = "update tb_url set deleted = 'True', fsync='"+time.strftime("%c")+"' where id_vh="+str(vh[0])
            self.actualizaTabla(sql,confirma=False) 
 
        return True
    
    
    def grabaSw(self,sw,id_serv):
        
        '''
        Graba los datos deluna instancia software en la BD de SDA
        
        Parametro
        
            sw: Objeto sw a grabar
            id_serv :Identificador del servidor donde se encontró
        
        Salida
        
            modificado : Indica si se ha modificado
        '''
        
        modificado = False
        id_soft=self.retIdSoftware(sw.cadRunning)
        
        if self._existeSw(id_serv,id_soft) == None:
            data=(id_soft,id_serv,time.strftime("%c"))
            sql='INSERT INTO TB_SOFT_RUNNING (id_sw,id_serv,fsync) VALUES(%s,%s,%s)'
            if self.cur <> None :
                try :
                    self.cur.execute(sql,data)
                    modificado=True
                except Exception, error :
                    print error 
        return modificado

    
    def cierraDB(self):
        
        '''
        Cierra la BD
        '''
        self.conn.close()
        
    
    
