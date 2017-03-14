#Crear antes la BBDD sda_db y conectarte a ella

#CREATE DATABASE SDA_DB;

CREATE TABLE TB_so(
  code  character(2) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_so PRIMARY KEY(code)
);

CREATE TABLE TB_TipoDesc(
  code  character(2) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_TipoDesc PRIMARY KEY(code)
);

CREATE TABLE TB_Dispositivos(
  IP      character(15) NOT NULL,
  fecDes  DATE NOT NULL,
  id_td      character(2) NOT NULL,
  nombre  CHARACTER(25),
  id_so   CHARACTER(2), 
  Proc    CHARACTER(1) NOT NULL,
  fecProc DATE,
  CONSTRAINT pk_tb_Dispositivos PRIMARY KEY(IP),
  CONSTRAINT fk_TB_Dispositivos_so FOREIGN KEY(id_so) REFERENCES TB_so(code),
  CONSTRAINT fk_TB_Dispositivos_td FOREIGN KEY(id_td) REFERENCES TB_TipoDesc(code)
);

CREATE TABLE TB_net(
   id_net      inet NOT NULL,
   masc        inet NOT NULL,
   broadcast   inet NOT NULL,
   enlace      inet NOT NULL,
   CONSTRAINT pk_tb_net PRIMARY KEY(id_net)  
);

CREATE TABLE TB_Servidor(
   id_serv     serial NOT NULL,
   nombre      varchar NOT NULL,
   id_so       CHARACTER(2) NOT NULL,
   ram         bigint NOT NULL,
   Tipo_cpu    varchar NOT NULL,
   n_cpu       int NOT NULL,
   CONSTRAINT pk_tb_Servidor PRIMARY KEY(id_serv),
   CONSTRAINT fk_TB_Servidor_SO FOREIGN KEY(id_so) REFERENCES TB_so(code) 
);

CREATE TABLE TB_IP(
   ip          inet NOT NULL,
   mac         varchar,
   id_serv     int NOT NULL,
   id_net      inet NOT NULL,
   CONSTRAINT pk_tb_ip PRIMARY KEY(ip),
   CONSTRAINT fk_TB_IP_net FOREIGN KEY(id_net) REFERENCES TB_net(id_net),
   CONSTRAINT fk_TB_IP_Servidor FOREIGN KEY(id_serv) REFERENCES TB_Servidor(id_serv)
);

CREATE TABLE TB_FS(
   id_serv     int NOT NULL,
   montaje     varchar NOT NULL,
   size        bigint,
   tipo        varchar,
   CONSTRAINT pk_tb_fs PRIMARY KEY(id_serv,montaje),
   CONSTRAINT fk_TB_FS_Servidor FOREIGN KEY(id_serv) REFERENCES TB_Servidor(id_serv)
);

CREATE TABLE TB_INV_SOFTWARE(
   id_sw       serial NOT NULL,
   Descripcion varchar NOT NULL,
   CONSTRAINT pk_tb_inv_software PRIMARY KEY(id_sw)
);

CREATE TABLE TB_SOFT_RUNNING(
   id_sw       int NOT NULL,
   id_serv     int NOT NULL,
   CONSTRAINT pk_tb_SOFT_RUNNING PRIMARY KEY(id_sw,id_serv),
   CONSTRAINT fk_TB_SOFT_Servidor FOREIGN KEY(id_serv) REFERENCES TB_Servidor(id_serv),
   CONSTRAINT fk_TB_SOFT_INVT FOREIGN KEY(id_sw) REFERENCES TB_INV_SOFTWARE(id_SW)  
);

INSERT INTO TB_so VALUES ('LX','LINUX');
INSERT INTO TB_so VALUES ('WS','WINDOWS');

INSERT INTO TB_TipoDesc VALUES ('NM','NMAP');
