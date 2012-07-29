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

import wx
import  wx.py   as  py
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

class PanelInferior(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)
        
        self.nAuxiliar = wx.Notebook(self, -1,style =wx.BORDER_SUNKEN)
        intro = 'Bienvenido a PyShell %s ' % py.version.VERSION
        self.Shell= py.shell.Shell(self.nAuxiliar, -1, introText=intro)
        self.Layout()
        
    def Layout(self):
        sAuxiliar = wx.BoxSizer(wx.VERTICAL)
        self.sAuxiliar = sAuxiliar
        Win=[]
        NombreWin=[]
        Win.append(self.Shell)
        NombreWin.append("PyShell")
        cont=0
        for i in Win:        
            self.nAuxiliar.AddPage(i,NombreWin[cont])
            cont+=1
        self.sAuxiliar.Add(self.nAuxiliar,1,wx.EXPAND,0)        
        self.SetSizer(self.sAuxiliar)
        self.SetAutoLayout(True)
        self.sAuxiliar.Layout()
        

    def Destroy(self):
        event.Skip()    




