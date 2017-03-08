'''
Created on 4 mar. 2017

@author: jose
'''
from objetos.objDispositivo import ObjDispositivo
from objetos.bbdd  import bbdd


class listServer(object):
    '''
    classdocs
    '''


    def __init__(self, ls):
        '''
        Constructor
        '''
        self.ls=ls
        return
        
    def insert_or_update(self,server):
        if self.ls == []:
            self.ls.append(server)
        else:
            ind=0
            final=False
            while self.ls[ind].indice <= server.indice and not final:
                if  ind==len(self.ls)-1:
                    final=True
                else:
                    ind+=1
            if self.ls[ind].indice==server.indice:
                self.ls[ind].update(server)
            elif  self.ls[ind].indice<server.indice:
                self.ls.insert(ind+1,server)
            else:
                self.ls.insert(ind,server) 
    
        return
    
    def tostr(self):
        
        cad=""
        ind=""
        for x in self.ls:
            cad+=x.ip+"\n"

        return cad,ind    
     
    def grabarBBDD(self):
        c = bbdd()
        c.insertaAll(self.ls)
        c.cierraDB()
        return       
if __name__ == '__main__':
    import random
    import time

    ls=listServer([])
    for se in range(300):
        ip=str(random.randint(1, 254))+"."+str(random.randint(1, 244))+"."+str(random.randint(1, 244))+"."+str(random.randint(1, 244))
        s=ObjDispositivo(ip,time.strftime("%c"),'NMAP','','')
        ls.insert_or_update(s)
    ls.grabarBBDD()


        
            