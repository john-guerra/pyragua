#-*- coding:iso8859-1 -*-
"""
Este archivo es parte de Pyragua

Pyragua es software libre; lo puedes redistribuir y/o modificar
bajo los terminos de la Licencia Publica General (GNU GPL) como fue
publicada por la Free Software Foundation; cualquier versi�n 2 de la 
Licencia.

Este programa es distribuido con la esperanza de que ser� �til,
pero SIN GARANTIA ALGUNA; ni con la garant�a expl�cita de 
MERCABILIDAD o de que SERVIRA PARA UN PROPOSITO EN PARTICULAR.
Mire la Licencia P�blica General de la GNU para m�s detalles.

Debi� recibir una copia de la Licencia P�blica General de la GNU junto con
este programa; sino, escriba a la Free Software Foundation, 
Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

# El panel del navegador de c�digo

import wx
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

from ClassBrowser.BrowserTree import BrowserTree

class PanelCodigo(wx.Panel):
    """El panel del navegador de c�digo"""
    def __init__(self,*args,**kwargs):
        self.padre=kwargs['padre']
        del kwargs['padre']
        self.pyragua=self.padre.pyragua
        wx.Panel.__init__(self,*args,**kwargs)
        
        self.aCodigo=BrowserTree(self, cb=self.pyragua.cb, pyragua=self.pyragua)
        #self.codeBrowser=CodeBrowser(padre=self)
        self.archivo=""
        self.Layout()
    
        
    def Layout(self):
        self.sCodigo=wx.BoxSizer(wx.HORIZONTAL)
        self.sCodigo.Add(self.aCodigo, 1, wx.EXPAND, 0)
        
        self.SetSizerAndFit(self.sCodigo)
        
    def CambiarArchivo(self, archivo):
        u"""Navega en el c�digo del archivo que pasen como par�metro"""
        self.archivo=archivo
        self.pyragua.cb.CambiarArchivo(archivo)
        
    def __del__(self):
        """Destructor, se encarga de terminar el hilo"""
        print _(u"Terminando Hilo de navegaci�n")
        #_self.codeBrowser.Salir()
        