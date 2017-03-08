'''
Created on 8 mar. 2017

@author: jose
'''
import psycopg2
 
class bbdd(object):
    '''
    classdocs
    '''
    conn = None
    cur = None

    def __init__(self):
        '''
        Constructor
        '''
        try :
            self.conn = psycopg2.connect(database="sda_db", user="postgres", password="postgres", host="192.168.1.47", port="5432")
        except :
            print ("Error de acceso a BBDD")  
        return   
    
    def consulta (self,con):
        
        self.cur=self.conn.cursor()
        self.cur.execute(con)
        rows = self.cur.fetchall()
        self.cur.close()
        
        return rows
    
    def retIdDesc(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from TB_TipoDesc where descripcion ='"+desc+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_id =["OT"]
        return code_id[0]
    
    def retIdSO(self,desc):
        
        cur=self.conn.cursor()
        cur.execute("select code from TB_so where descripcion ='"+desc+"'")
        code_id = cur.fetchone()
        cur.close()
        if code_id == None :
            code_id =["ND"]
        return code_id[0]
    
    def insertaDisp(self,s):
        idDes=self.retIdDesc(s.td)
        idSO=self.retIdSO(s.os)
        data=(s.ip,s.fd,idDes,s.nombre,idSO,"N")
        
        try :
            self.cur.execute("INSERT INTO TB_Dispositivos(ip,fecdes,id_td,nombre,id_so,proc) VALUES (%s,%s,%s,%s,%s,%s)",data)
        except  psycopg2.DatabaseError as error:
            print error
            print ("la IP "+s.ip+" ya existe")
        return
    
    def insertaAll(self,ls):
        
        self.cur=self.conn.cursor()
        for s in ls:
            self.insertaDisp(s)
        self.conn.commit()
        self.cur.close()

        return
    def cierraDB(self):
        self.conn.close()
    
if __name__ == '__main__': 
    c = bbdd()
    c.consulta("select * from tb_so")

    
    