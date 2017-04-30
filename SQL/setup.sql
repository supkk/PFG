/*   Crear antes la BBDD sda_db y conectarte a ella  */


CREATE  TABLE tb_lkp_so(
  code  character(2) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_so PRIMARY KEY(code)
);

CREATE  TABLE tb_lkp_entorno(
  code  character(3) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_entorno PRIMARY KEY(code)
);

CREATE TABLE tb_lkp_MarcaDisp (
   code        varchar(4),
   descripcion varchar(40),
   CONSTRAINT pk_tb_lkp_MarcaDisp PRIMARY KEY(code)
);

CREATE  TABLE tb_lkp_tabla(
  code  character(3) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_tabla PRIMARY KEY(code)
);

CREATE  TABLE tb_lkp_url(
  code  character(2) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_url PRIMARY KEY(code)
);

CREATE  TABLE tb_lkp_Desc(
  code  character(2) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_Desc PRIMARY KEY(code)
);

CREATE  TABLE tb_lkp_InterFace(
  code  character(5) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_Interface PRIMARY KEY(code)
);

CREATE  TABLE tb_lkp_FS(
  code  character(4) NOT NULL,   
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_FS PRIMARY KEY(code)
);

CREATE  TABLE tb_lkp_Almacenamiento(
  code  character(3) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_Almcenamiento PRIMARY KEY(code)
);

CREATE  TABLE TB_net(
 _Id         integer,
 id_net      serial NOT NULL,
 nombre      varchar(20) NOT NULL,
 IPBase      inet NOT NULL,
 mascara     inet NOT NULL,
 CONSTRAINT pk_tb_net PRIMARY KEY(id_net)
 );

CREATE  TABLE TB_Dispositivos(
  IP      character(15) NOT NULL,
  fecDes  DATE NOT NULL,
  id_td   character(2) NOT NULL,
  id_so   CHARACTER(2), 
  Proc    CHARACTER(1) NOT NULL,
  fecProc DATE,
  apagado int,
  id_Disp int,
  CONSTRAINT pk_tb_Dispositivos PRIMARY KEY(IP),
  CONSTRAINT fk_TB_Dispositivos_so FOREIGN KEY(id_so) REFERENCES tb_lkp_so(code),
  CONSTRAINT fk_TB_Dispositivos_td FOREIGN KEY(id_td) REFERENCES tb_lkp_Desc(code)
  );

CREATE  TABLE TB_Disp(
   _id         int,
   id_disp     serial NOT NULL,
   sn          varchar(20),
   nombre      varchar(20) NOT NULL,
   fsync       date,
   deleted     boolean,
   id_marca	   varchar(10) NOT 	NULL,
   CONSTRAINT pk_tb_Disp PRIMARY KEY(id_disp),
   CONSTRAINT fk_TB_Disp_Marca FOREIGN KEY(id_marca) REFERENCES tb_lkp_MarcaDisp(code) 
   );

CREATE  TABLE TB_Servidor(
   id_disp     integer NOT NULL,
   id_serv     serial 	not NULL,
   _id         integer,
   id_so       varchar(2) NOT NULL,
   version_os  varchar(100),
   ram         integer NOT NULL,
   Tipo_cpu    varchar(100) NOT NULL,
   n_cpu       int NOT NULL,
   n_cores     int NOT NULL,
   gw          inet, 
   fsync       date,
   deleted     boolean,
   id_entorno  varchar(3),
   CONSTRAINT pk_tb_Servidor PRIMARY KEY(id_serv),
   CONSTRAINT fk_TB_Servidor_SO FOREIGN KEY(id_so) REFERENCES tb_lkp_so(code), 
   CONSTRAINT fk_TB_Servidor_Disp FOREIGN KEY(id_disp) REFERENCES tb_Disp(id_disp),
   CONSTRAINT FK_TB_Servidor_Entorno FOREIGN KEY(id_entorno) REFERENCES TB_lkp_entorno(code)
   
);

CREATE  TABLE TB_Router(
   id_disp     integer NOT NULL,
   id_router   serial 	not NULL,
   _id         integer,
   dhcp        boolean,
   dns         inet,
   puertos     integer,
   gw          inet, 
   fsync       date,
   deleted     boolean,
   CONSTRAINT pk_tb_Router PRIMARY KEY(id_router),
   CONSTRAINT fk_TB_Router_Disp FOREIGN KEY(id_disp) REFERENCES tb_Disp(id_disp) 
);

CREATE  TABLE TB_Interface(
   _id         integer,
   id_TipoInt  varchar(5),
   id_net      integer,
   ip          inet NOT NULL,
   mascara     inet NOT NULL,
   mac         varchar(20),
   nombre      varchar(30),
   id_disp     int NOT NULL,
   id_int      serial not NULL,
   fsync       date,
   deleted     boolean,
   CONSTRAINT pk_tb_Interface PRIMARY KEY(id_int),
   CONSTRAINT fk_TB_Int_Disp FOREIGN KEY(id_disp) REFERENCES TB_Disp(id_disp),
   CONSTRAINT fk_TB_Int_Net FOREIGN KEY(id_net) REFERENCES tb_net(id_net),
   CONSTRAINT fk_TB_Int_TipoInt FOREIGN KEY(id_TipoInt) REFERENCES tb_lkp_Interface(code)
);

CREATE  TABLE TB_FS(
   _id         integer,
   id_serv     int NOT NULL,
   montaje     varchar NOT NULL,
   size        bigint,
   id_tipoFS   varchar(5),
   id_tipoAl   varchar(5),
   fsync       date,
   deleted     boolean,
   CONSTRAINT pk_tb_fs PRIMARY KEY(id_serv,montaje),
   CONSTRAINT fk_TB_FS_Servidor FOREIGN KEY(id_serv) REFERENCES TB_Servidor(id_serv),
   CONSTRAINT fk_TB_FS_TipoFS FOREIGN KEY(id_tipoFS) REFERENCES tb_lkp_FS(code),
   CONSTRAINT fk_TB_FS_TipoAlmacenamiento FOREIGN KEY(id_tipoAl) REFERENCES tb_lkp_Almacenamiento(code)
);


CREATE TABLE tb_lkp_Cat_Software (
   id_cat      varchar(4),
   descripcion varchar(40),
   CONSTRAINT pk_tb_Cat_software PRIMARY KEY(id_cat)
);




CREATE  TABLE TB_INV_SOFTWARE(
   id_sw       serial NOT NULL,
   Descripcion varchar NOT NULL,
   id_cat      varchar(4) NOT NULL,
   n_proceso   varchar NOT NULL,
   _id         int,
   CONSTRAINT pk_tb_inv_software PRIMARY KEY(id_sw),
   CONSTRAINT fk_TB_FS_Sof_Cat FOREIGN KEY(id_cat) REFERENCES tb_lkp_Cat_Software(id_cat)
);


CREATE  TABLE tb_soft_running(
   _id         integer,
   id_sw       int NOT NULL,
   id_serv     int NOT NULL,
   fsync       date,
   deleted     boolean,
   CONSTRAINT pk_tb_soft_running PRIMARY KEY(id_sw,id_serv),
   CONSTRAINT fk_tb_SOFT_Servidor FOREIGN KEY(id_serv) REFERENCES TB_Servidor(id_serv),
   CONSTRAINT fk_tb_SOFT_INVT FOREIGN KEY(id_sw) REFERENCES TB_INV_SOFTWARE(id_SW)  
);

CREATE TABLE TB_SoftwareInstancia (
   _id			int,
   id_SI		serial NOT NULL,
   id_sw        int NOT NULL,
   id_serv      int NOT NULL,
   id_entorno   varchar(3),
   version      varchar(20),
   home         varchar(100),
   Usuario      varchar(10),
   fsync        date,
   CONSTRAINT PK_TB_SoftwareInstancia PRIMARY KEY(id_SI),
   CONSTRAINT fk_tb_SI_SR FOREIGN KEY(id_sw,id_serv) REFERENCES TB_soft_running(id_sw,id_serv),
   CONSTRAINT FK_TB_SofInst_Entorno FOREIGN KEY(id_entorno) REFERENCES TB_lkp_entorno(code)
);

CREATE TABLE TB_DB (
   _id			int,
   id_DB		serial NOT NULL,
   id_SI        int,
   puerto       int,
   admin		varchar(10),
   fsync       date,
   CONSTRAINT PK_TB_DB PRIMARY KEY(id_DB),
   CONSTRAINT FK_TB_DB_SoftwareInstancia FOREIGN KEY(id_SI) REFERENCES TB_SoftwareInstancia(id_SI)
);

CREATE TABLE TB_ServAplicaciones (
   _id			int,
   id_SI        int,
   id_SA		serial NOT NULL,
   JVM			varchar(100),
   puerto       int,
   fsync        date,
   id_entorno   varchar(3),
   CONSTRAINT PK_TB_ServAplicaciones PRIMARY KEY(id_SA),
   CONSTRAINT FK_TB_SA_SoftwareInstancia FOREIGN KEY(id_SI) REFERENCES TB_SoftwareInstancia(id_SI)
);

 CREATE TABLE TB_ServWeb (
   _id			int,
   id_web		serial NOT NULL,
   id_SI        int	not null,
   urlAdmin     int,
   fsync        date,
   CONSTRAINT PK_TB_ PRIMARY KEY(id_web),
   CONSTRAINT FK_TB_web_SoftwareInstancia FOREIGN KEY(id_SI) REFERENCES TB_SoftwareInstancia(id_SI)
);

CREATE TABLE TB_EsquemaBD (
   _id			int,
   id_EDB		serial NOT NULL,
   id_DB		int	NOT NULL,
   nombre		varchar(20),
   propietario  varchar(10),
   fsync       date,
   CONSTRAINT PK_TB_EsquemaDB PRIMARY KEY(id_EDB),
   CONSTRAINT FK_TB_EDB_BD FOREIGN KEY(id_DB) REFERENCES TB_DB(id_DB)
);

CREATE TABLE TB_Tabla (
   _id			   int,
   id_TB		   serial NOT NULL,
   id_EDB		   int NOT NULL,
   nombre		   varchar(50),
   id_tipo_tabla   varchar(2),
   fsync           date,
   CONSTRAINT PK_TB_Tabla PRIMARY KEY(id_TB),
   CONSTRAINT FK_TB_Tabla_EDB FOREIGN KEY(id_EDB) REFERENCES TB_EsquemaBD(id_EDB),
   CONSTRAINT FK_TB_lkp_tabla FOREIGN KEY(id_tipo_tabla) REFERENCES TB_lkp_tabla(code)
);

CREATE TABLE TB_AtributoTabla (
   _id			int,
   id_att		serial NOT NULL,
   id_TB		int NOT NULL,
   nombre       varchar(20),
   indice       boolean,
   fsync       date,
   CONSTRAINT PK_TB_AtributoTabla PRIMARY KEY(id_att),
   CONSTRAINT FK_TB_ATT_Tabla FOREIGN KEY(id_TB) REFERENCES TB_Tabla(id_TB)
);

CREATE TABLE TB_VHost (
   _id			int,
   id_VH		serial NOT NULL,
   id_web       int NOT NULL,
   DNS			varchar(50),
   puerto		int,
   SSL			boolean,
   rCert		boolean,
   rutaCert		varchar(200),
   fsync       date,
   CONSTRAINT PK_TB_VHost PRIMARY KEY(id_VH),
   CONSTRAINT FK_TB_VH_WEB FOREIGN KEY(id_web) REFERENCES TB_ServWeb(id_web)
);

CREATE TABLE TB_Aplicacion (
   _id			int,
   id_apl		serial NOT NULL,
   acronimo     varchar(10),
   nombre		varchar(20),
   version      varchar(20),
   fsync        date,
   CONSTRAINT PK_TB_Aplicacion PRIMARY KEY(id_apl)
);

CREATE TABLE TB_Map_SA_AP(
   id_apl		int not NULL,
   id_SA		int not NULL,
   CONSTRAINT PK_TB_MAP_apl_SA PRIMARY KEY(id_apl,id_SA),
   CONSTRAINT FK_TB_MAP_Apl FOREIGN KEY(id_apl) REFERENCES TB_Aplicacion(id_apl),
   CONSTRAINT FK_TB_MAP_SA FOREIGN KEY(id_SA) REFERENCES TB_ServAplicaciones(id_SA)
);

CREATE TABLE TB_url (
   _id			int,
   id_url		serial NOT NULL,
   nombre		varchar(20),
   valor		varchar(100),	
   id_VH		int NOT NULL,
   fsync       date,
   CONSTRAINT PK_TB_url PRIMARY KEY(id_url),
   CONSTRAINT FK_TB_Url_VH FOREIGN KEY(id_VH) REFERENCES TB_VHost(id_VH)
);

CREATE TABLE TB_Map_url_APL(
   id_apl		int not NULL,
   id_url		int not NULL,
   tipo_url		varchar(2) not NULL,
   CONSTRAINT PK_TB_MAP_url_apl PRIMARY KEY(id_apl,id_url),
   CONSTRAINT FK_TB_MAPua_Apl FOREIGN KEY(id_apl) REFERENCES TB_Aplicacion(id_apl),
   CONSTRAINT FK_TB_MAPua_url FOREIGN KEY(id_url) REFERENCES TB_url(id_url),
   CONSTRAINT FK_TB_MAPua_lkp_url FOREIGN KEY(tipo_url) REFERENCES TB_lkp_url(code)
);

CREATE TABLE TB_ConectorBD (
   _id			int,
   id_CBD		serial NOT NULL,
   id_EDB       int NOT NULL,
   usuario		varchar(10),
   nombre       varchar(20),
   fsync       date,
   CONSTRAINT PK_TB_CBD PRIMARY KEY(id_CBD),
   CONSTRAINT FK_TB_CBD FOREIGN KEY(id_EDB) REFERENCES TB_EsquemaBD(id_EDB)
);

CREATE TABLE TB_MAP_CBD_Apl (
   _id			int,
   id_apl		int NOT NULL,
   id_CBD	    int NOT NULL,
   CONSTRAINT PK_TB_MAP_CBD_Apl PRIMARY KEY(id_apl,id_CBD),
   CONSTRAINT FK_TB_MAPCA_Apl FOREIGN KEY(id_apl) REFERENCES TB_Aplicacion(id_apl),
   CONSTRAINT FK_TB_MAPCA_CBD FOREIGN KEY(id_CBD) REFERENCES TB_ConectorBD(id_CBD)
);

CREATE TABLE tb_sda_config (
   id               serial not null,
   fsync            date,
   host_cmdb        varchar,
   port             varchar,
   usuario_cmdb     varchar,
   password_cmdb    varchar,
   usuario_ssh      varchar,
   password_ssh     varchar,
   CONSTRAINT pk_tb_sda_config PRIMARY KEY(id)
);

INSERT INTO tb_lkp_so VALUES ('LX','LINUX');
INSERT INTO tb_lkp_so VALUES ('WS','WINDOWS');
INSERT INTO tb_lkp_so VALUES ('ND','NO DESC');
INSERT INTO tb_lkp_so VALUES ('OL','OT LINUX');
INSERT INTO tb_lkp_so VALUES ('SO','SUNOS');

INSERT INTO tb_lkp_Desc VALUES ('NM','NMAP');

INSERT INTO TB_LKP_URL VALUES('TS','TEST');
INSERT INTO TB_LKP_URL VALUES('AC','ACCESO');
INSERT INTO TB_LKP_URL VALUES('CC','COMPONENTE COMUN');
INSERT INTO TB_LKP_URL VALUES('SE','SERVICIO EXTERNO');

INSERT INTO TB_LKP_INTERFACE VALUES('ETH-V','ETHERNET VIRTUAL');
INSERT INTO TB_LKP_INTERFACE VALUES('ETH-C','ETHERNET CABLE');
INSERT INTO TB_LKP_INTERFACE VALUES('ETH-W','ETHERNET WIFI');
INSERT INTO TB_LKP_INTERFACE VALUES('OTR',  'OTRO');

INSERT INTO TB_LKP_ENTORNO VALUES('INT','INTEGRACION');
INSERT INTO TB_LKP_ENTORNO VALUES('DES','DESARROLLO');
INSERT INTO TB_LKP_ENTORNO VALUES('PRE','PREPRODUCCION');
INSERT INTO TB_LKP_ENTORNO VALUES('PRO','PRODUCCION');

INSERT INTO TB_LKP_TABLA VALUES('VIM','VISTA MATERIALIZADA');
INSERT INTO TB_LKP_TABLA VALUES('TBL','TABLA');
INSERT INTO TB_LKP_TABLA VALUES('VST','VISTA');

INSERT INTO TB_LKP_FS VALUES('NTF','NTFS');
INSERT INTO TB_LKP_FS VALUES('EX4','EXT4');
INSERT INTO TB_LKP_FS VALUES('F32','FAT32');
INSERT INTO TB_LKP_FS VALUES('BRF','BRFS');
INSERT INTO TB_LKP_FS VALUES('OTR','OTRO FS');
insert into tb_lkp_fs values ('FAT','FAT');
INSERT INTO TB_LKP_FS VALUES('ZFS','ZFS');
INSERT INTO TB_LKP_FS VALUES('TMP','TMPFS');
INSERT INTO TB_LKP_FS VALUES('ISO','ISO9660');
INSERT INTO TB_LKP_FS VALUES('VFA','VFAT');
INSERT INTO TB_LKP_FS VALUES('DTM','DEVTMPFS');
INSERT INTO TB_LKP_FS VALUES('DFS','DEVFS');
INSERT INTO TB_LKP_FS VALUES('DEV','DEV');
INSERT INTO TB_LKP_FS VALUES('CTF','CTFS');
INSERT INTO TB_LKP_FS VALUES('PRC','PROC');
INSERT INTO TB_LKP_FS VALUES('MNT','MNTFS');
INSERT INTO TB_LKP_FS VALUES('OBJ','OBJFS');
INSERT INTO TB_LKP_FS VALUES('SHR','SHAREFS');
INSERT INTO TB_LKP_FS VALUES('LOF','LOFS');
INSERT INTO TB_LKP_FS VALUES('FD','FD');


INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('NFS','NFS');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('SMB','SMB');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('SCS','ISCSI');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('INT','INTERNO');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('OTR','OTRO');


insert into tb_net (nombre,ipbase,mascara) values ('NET01','192.168.1.0','255.255.255.0');
insert into tb_net (nombre,ipbase,mascara) values ('NETLOOKUP','127.0.0.0','255.0.0.0');
insert into tb_net (nombre,ipbase,mascara) values ('NET_NO_CONFIGURADA','0.0.0.0','0.0.0.0');

INSERT INTO tb_lkp_cat_software (id_cat, Descripcion) VALUES('BBDD','BASE DATOS');
INSERT INTO tb_lkp_cat_software (id_cat, Descripcion) VALUES('SAPL','SERVIDOR DE APLICACIONES');
INSERT INTO tb_lkp_cat_software (id_cat, Descripcion) VALUES('SWEB','SERVIDOR WEB');
INSERT INTO tb_lkp_cat_software (id_cat, Descripcion) VALUES('SRMT','TERMINAL REMOTO');
INSERT INTO tb_lkp_cat_software (id_cat, Descripcion) VALUES('LDAP','SERVIDOR DE DIRECTORIO');

INSERT INTO tb_inv_software (Descripcion,id_cat,n_proceso) VALUES('SERVIDOR WEB APACHE','SWEB','httpd');
INSERT INTO tb_inv_software (Descripcion,id_cat,n_proceso) VALUES('SERVIDOR APLICACIONES TOMCAT','SAPL','tomcat');
INSERT INTO tb_inv_software (Descripcion,id_cat,n_proceso) VALUES('SERVIDOR APLICACIONES JBOSS','SAPL','jboss');
INSERT INTO tb_inv_software (Descripcion,id_cat,n_proceso) VALUES('SERVIDOR DE BBBDD MYSQL','BBDD','mysql');
INSERT INTO tb_inv_software (Descripcion,id_cat,n_proceso) VALUES('SERVIDOR DE BBDD POSTGRESQL','BBDD','postgres');
insert into tb_inv_software (descripcion,id_cat,n_proceso) values ('SERVIDOR WEB IIS WINDOWS','SWEB','iissvcs');
insert into tb_inv_software (descripcion,id_cat,n_proceso) values ('SERVIDOR DE TERMINALES','SRMT','sshd');
insert into tb_inv_software (descripcion,id_cat,n_proceso) values ('SERVIDOR WEB APACHE','SWEB','apache');
insert into tb_inv_software (descripcion,id_cat,n_proceso) values ('SERVIDOR DE APLICACIONES PHP','SAPL','php-fpm');

INSERT INTO TB_LKP_MarcaDisp VALUES('HP','HP');
INSERT INTO TB_LKP_MarcaDisp VALUES('SUN','SUN');
INSERT INTO TB_LKP_MarcaDisp VALUES('ORCL','ORACLE');
INSERT INTO TB_LKP_MarcaDisp VALUES('DELL','DELL');


insert into tb_sda_config (fsync, host_cmdb, port, usuario_cmdb, password_cmdb, usuario_ssh, password_ssh) values ('01/01/01','192.168.1.20','8080','admin','admin','user_ssh','user_ssh');
