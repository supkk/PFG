/*   Crear antes la BBDD sda_db y conectarte a ella  */


CREATE  TABLE tb_lkp_so(
  code  character(2) NOT NULL,
  descripcion  character(20) NOT NULL,
  CONSTRAINT pk_tb_lkp_so PRIMARY KEY(code)
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
  nombre  CHARACTER(25),
  id_so   CHARACTER(2), 
  Proc    CHARACTER(1) NOT NULL,
  fecProc DATE,
  CONSTRAINT pk_tb_Dispositivos PRIMARY KEY(IP),
  CONSTRAINT fk_TB_Dispositivos_so FOREIGN KEY(id_so) REFERENCES tb_lkp_so(code),
  CONSTRAINT fk_TB_Dispositivos_td FOREIGN KEY(id_td) REFERENCES tb_lkp_Desc(code)
);

CREATE  TABLE TB_Disp(
   id_disp     serial NOT NULL,
   sn          varchar(20),
   nombre      varchar(20) NOT NULL,
   CONSTRAINT pk_tb_Disp PRIMARY KEY(id_disp)
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
   CONSTRAINT pk_tb_Servidor PRIMARY KEY(id_serv),
   CONSTRAINT fk_TB_Servidor_SO FOREIGN KEY(id_so) REFERENCES tb_lkp_so(code), 
   CONSTRAINT fk_TB_Servidor_Disp FOREIGN KEY(id_disp) REFERENCES tb_Disp(id_disp) 
);

CREATE  TABLE TB_Router(
   id_disp     integer NOT NULL,
   id_router   serial 	not NULL,
   _id         integer,
   dhcp        boolean,
   dns         inet,
   puertos     integer,
   gw          inet, 
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
   nombre      varchar(10),
   id_disp     int NOT NULL,
   CONSTRAINT pk_tb_Interface PRIMARY KEY(ip),
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
   CONSTRAINT pk_tb_fs PRIMARY KEY(id_serv,montaje),
   CONSTRAINT fk_TB_FS_Servidor FOREIGN KEY(id_serv) REFERENCES TB_Servidor(id_serv),
   CONSTRAINT fk_TB_FS_TipoFS FOREIGN KEY(id_tipoFS) REFERENCES tb_lkp_FS(code),
   CONSTRAINT fk_TB_FS_TipoAlmacenamiento FOREIGN KEY(id_tipoAl) REFERENCES tb_lkp_Almacenamiento(code)
);

CREATE  TABLE TB_INV_SOFTWARE(
   id_sw       serial NOT NULL,
   Descripcion varchar NOT NULL,
   CONSTRAINT pk_tb_inv_software PRIMARY KEY(id_sw)
);

CREATE  TABLE tb_lkp_SOFT_RUNNING(
   id_sw       int NOT NULL,
   id_serv     int NOT NULL,
   CONSTRAINT pk_tb_lkp_SOFT_RUNNING PRIMARY KEY(id_sw,id_serv),
   CONSTRAINT fk_tb_lkp_SOFT_Servidor FOREIGN KEY(id_serv) REFERENCES TB_Servidor(id_serv),
   CONSTRAINT fk_tb_lkp_SOFT_INVT FOREIGN KEY(id_sw) REFERENCES TB_INV_SOFTWARE(id_SW)  
);

INSERT INTO tb_lkp_so VALUES ('LX','LINUX');
INSERT INTO tb_lkp_so VALUES ('WS','WINDOWS');
INSERT INTO tb_lkp_so VALUES ('ND','NO DESC');
INSERT INTO tb_lkp_so VALUES ('OL','OT LINUX');

INSERT INTO tb_lkp_Desc VALUES ('NM','NMAP');


INSERT INTO TB_LKP_INTERFACE VALUES('ETH-V','ETHERNET VIRTUAL');
INSERT INTO TB_LKP_INTERFACE VALUES('ETH-C','ETHERNET CABLE');
INSERT INTO TB_LKP_INTERFACE VALUES('ETH-W','ETHERNET WIFI');
INSERT INTO TB_LKP_INTERFACE VALUES('OTR',  'OTRO');

INSERT INTO TB_LKP_FS VALUES('NTF','NTFS');
INSERT INTO TB_LKP_FS VALUES('EX4','EXT4');
INSERT INTO TB_LKP_FS VALUES('F32','FAT32');
INSERT INTO TB_LKP_FS VALUES('BRF','BRFS');
INSERT INTO TB_LKP_FS VALUES('OTR','OTRO FS');

INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('NFS','NFS');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('SMB','SMB');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('SCS','ISCSI');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('INT','INTERNO');
INSERT INTO TB_LKP_ALMACENAMIENTO VALUES('OTR','OTRO');


insert into tb_net (nombre,ipbase,mascara) values ('NET01','192.168.1.0','255.255.255.0');



