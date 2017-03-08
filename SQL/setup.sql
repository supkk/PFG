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

INSERT INTO TB_so VALUES ('LX','LINUX');
INSERT INTO TB_so VALUES ('WS','WINDOWS');

INSERT INTO TB_TipoDesc VALUES ('NM','NMAP');
