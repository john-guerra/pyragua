#-*- coding:iso8859-1 -*-
"""
Este archivo es parte de Pyragua

Pyragua es software libre; lo puedes redistribuir y/o modificar
bajo los terminos de la Licencia Publica General (GNU GPL) como fue
publicada por la Free Software Foundation; cualquier versión 2 de la 
Licencia.

Este programa es distribuido con la esperanza de que será útil,
pero SIN GARANTIA ALGUNA; ni con la garantía explícita de 
MERCABILIDAD o de que SERVIRA PARA UN PROPOSITO EN PARTICULAR.
Mire la Licencia Pública General de la GNU para más detalles.

Debió recibir una copia de la Licencia Pública General de la GNU junto con
este programa; sino, escriba a la Free Software Foundation, 
Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import threading
import os
import os.path as path
import pyclbr
import time
import wx
#from PanelArchivos import PanelArchivos

class ChangeBrowser(wx.Frame):
    """Esta clase es un interminiario entre el programa y el hilo"""
    def __init__(self,pArchivos):
        wx.Frame.__init__(self,None,-1,"prueba")
        self.pArchivos = pArchivos 
        self.LanzarHilo()
    #El manejador del botón
    def LanzarHilo(self):
        self.hilo=Hilo(self)

    def Anunciar(self,Posicion):
        self.pArchivos.AnunciarUser(Posicion,self.hilo) 



class Hilo(threading.Thread):
    """Esta clase servirá como demonio que estará revisando
    constantemente si un archivo es modificado y lo recarga en la aplicacion"""
    def __init__(self,ChangeBrowser):
        """Recibe una lista con las rutas a los archivos abiertos """
        threading.Thread.__init__(self)
        """En reg se gurdan los paths de los archivos abiertos y Modificaciones
        guarda el tiempo en el cual esos archivos han sido modificados por lo tanto
        la posicion en la lista nos dice tambien el tiempo de modificacion
        len(Reg)= len(Modificaciones)"""
        self.Reg=[]
        self.Modificaciones=[]
        self.salir=False
        self.ChangeBrowser=ChangeBrowser
        self.start()
        
    def Salir(self):
        self.salir=True

    def ActualizarModificaciones(self,pArchivo,NumReg):
        """Recive el path del archivo y el numero del registro 
        que se va a modificar """
        self.Modificaciones[NumReg]= os.stat(pArchivo)
        self.Reg[NumReg] =pArchivo

    def GuardarRegistro(self,pArchivo):
        """Este metodo recibe el path del archivo abierto y lo guarda en
        un registro"""
        self.Reg.append(pArchivo)
        if pArchivo == '':
            self.Modificaciones.append(pArchivo)
        else:
            self.Modificaciones.append(os.stat(pArchivo))

    def CerrarRegistro(self,nArchivo):
        """Este metodo recibe el numero del registro que se va a borrar"""
        self.Modificaciones.pop(nArchivo)
        self.Reg.pop(nArchivo)

    def run(self):
        while not self.salir:
            Valor,Posicion=self.Escanear()
            if Valor:
                self.ChangeBrowser.Anunciar(Posicion)
            #Reescaneamos código cada 2 segundo
            time.sleep(2)
            

    def Escanear(self):
        """Esta función revisa el tiempo de modificacion de un archivo y si
        ha sido modificado retorna un bool, y el numer de registro modificado """
        for i in self.Reg:
            if i != '':
                TimeModificacion = os.stat(i)
                if TimeModificacion != self.Modificaciones[self.Reg.index(i)]:
                    print self.Reg[self.Reg.index(i)] 
                    return True, self.Reg.index(i)
            else:
                continue
        return False,''
    

#if __name__=="__main__":
   # cb=ChangeBrowser()
    #while 1:
       # time.sleep(10)

