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

import sys
"""
try:
	from xml.dom import implementation
	impl=implementation
except:
	from xml.dom.minidom import getDOMImplementation
	impl=getDOMImplementation
	
from xml.dom.ext import PrettyPrint, Print"""
from Archivo import Archivo
from WizardProyectos import WizardProyectos

class Proyecto :
    def __init__ ( self, parent ):
        self.lArchivos=[]
        self.raiz=''
        self.parent=parent
        #self.DynamicWizard()
        #self.CrearProyecto('Pyragua','pyragua.py',{'Archivos':['1','2','3','4'],'Parametros':['-p'],'Librerias':['/lib/algo.so'],'Includes':['/include/asd.al']}) 

    def AgregarArchivo ( self , ruta, padre):
        """Agrega un archivo al proyecto, retorna la instancia creada del archivo"""
        pArchivo=Archivo(ruta, padre=padre)
        self.lArchivos.append(pArchivo)
        return pArchivo  

    def CrearProyecto ( self ):
        """"""
        Selecciones= WizardProyectos(self.parent) 
        if not Selecciones.Info:
            return
        return #Para que salga mientras se termina el wizard
        doc=impl.createDocument(None,"Proyecto",None)
        self.raiz=doc.documentElement

        proyecto=doc.createElement('ProyectoPyragua')
        proyecto.setAttribute('nombre',NombreProyecto)
        self.raiz.appendChild(proyecto)

        for i in Secciones:
            if not Secciones[i] :
                continue
            Pseccion=doc.createElement(i[:(len(i)-1)])
            if i == 'Archivos':
                Pseccion.setAttribute('principal',APrincipal)
            proyecto.appendChild(Pseccion)
            for j in Secciones[i]:
                Vseccion=doc.createElement(i)
                if i =='Parametros':
                    Vseccion.setAttribute('val',j)
                else:
                    Vseccion.setAttribute('ruta',j)
                Pseccion.appendChild(Vseccion)

        PrettyPrint(doc,open(NombreProyecto+".xml","w"))

    def LeerXml ( self ):
        print 1
