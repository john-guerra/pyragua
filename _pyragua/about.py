#! -*- coding: iso8859-1 -*-
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

import  wx
import os
import os.path as path
import wx.lib.buttons as buttons
import wx.lib.hyperlink as hl
import wx.lib.dialogs
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext


class About(wx.MiniFrame):
    """Esta clase nos mostrará la información más relevante del proyecto en el aparte
    acerca de ubicada en el menú ayuda"""
    def __init__(self, parent, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.MiniFrame.__init__(self, parent, -1, title, pos, size, style)
        
        self.parent = parent
        self.title = title
        self.pos = pos
        self.size = size
        self.style = style
        
        self.pPal = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL)
        self.pAb = wx.Panel(self.pPal, -1)
        self.pPag = wx.Panel(self.pPal, -1)
        self.pLic = wx.Panel(self.pPal, -1)
        self.bLic = wx.Button(self.pPal, -1, _(u"Licencia"))
        self.bGru = wx.Button(self.pPal, -1, _(u"Pyrox"))
        self.bProy = wx.Button(self.pPal, -1, _(u"Pyragua"))
        self.bCer = wx.Button(self.pPal, -1, _(u"Cerrar"))
        
        #Muestro la imagen del proyecto por defecto
        #Me paso a la ruta del pyragua para cargar la imagen
        ruta_ant=os.getcwd()
        if parent.dir_pyragua:
            os.chdir(parent.dir_pyragua)
        bmpDef = wx.StaticBitmap(self.pAb, -1, wx.Bitmap(os.path.join("imagenes", "about_02.png"), wx.BITMAP_TYPE_ANY))
        os.chdir(ruta_ant)
        
        #Sizers
        sPal = wx.BoxSizer(wx.VERTICAL)
        sEle = wx.BoxSizer(wx.VERTICAL)
        sBot = wx.BoxSizer(wx.HORIZONTAL)
        
        sBot.Add(self.bProy, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
        sBot.Add(self.bGru, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
        sBot.Add(self.bLic, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
        sBot.Add(self.bCer, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
        sEle.Add(self.pAb, 0, wx.EXPAND | wx.ADJUST_MINSIZE, 0)
        sEle.Add(self.pLic, 0, wx.EXPAND, 0)
        sEle.Add(self.pPag, 0, wx.EXPAND, 0)
        sEle.Add(sBot, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ADJUST_MINSIZE, 0)
        
        #Propiedades
        self.pPal.SetAutoLayout(True)
        self.pPal.SetSizer(sEle)
        sEle.Fit(self.pPal)
        sEle.SetSizeHints(self.pPal)
        sPal.Add(self.pPal, 1, wx.EXPAND, 0)
        
        self.SetAutoLayout(True)
        self.SetSizer(sPal)
        sPal.Fit(self)
        sPal.SetSizeHints(self)
        
        #Hipervínculo hacia la página del grupo
        self.pagpyrox = hl.HyperLinkCtrl(self.pPag, wx.ID_ANY, _(u"Semillero de Investigación Pyrox"), URL=_(u"http://pyrox.utp.edu.co/"))
        self.pagpyrox.SetToolTip(wx.ToolTip(_(u"Conozca más sobre Pyrox y el proyecto Pyragua")))
        self.paglic = hl.HyperLinkCtrl(self.pLic, wx.ID_ANY, _(u"Licencia GPL versión 2"), URL=_(u"http://www.gnu.org/licenses/gpl.txt"))
        self.paglic.SetToolTip(wx.ToolTip(_(u"GPL v2 completa")))
        
        #Redibujo la ventana
        self.Layout()
        
        #Manejadores de eventos
        self.Bind(wx.EVT_BUTTON, self.Cerrar, self.bCer)
        self.Bind(wx.EVT_BUTTON, self.Proyecto, self.bProy)
        self.Bind(wx.EVT_BUTTON, self.Grupo, self.bGru)
        self.Bind(wx.EVT_BUTTON, self.Licencia, self.bLic)
        
    def Proyecto ( self, evento ):
        """Muestra la imagen del proyecto"""
        #Me paso a la ruta del pyragua para cargar la imagen
        ruta_ant=os.getcwd()
        if self.parent.dir_pyragua:
            os.chdir(self.parent.dir_pyragua)
        bmpProy = wx.Bitmap(os.path.join("imagenes", "pyragua_about02.png"), wx.BITMAP_TYPE_ANY)
        imagProy = wx.StaticBitmap(self.pAb, -1, bmpProy)
        imagProy.SetBitmap(bmpProy)
        os.chdir(ruta_ant)
        
        self.Layout()
        
        #Deshabilito el botón proyecto
        self.bProy.Disable()
        self.bGru.Enable()
        self.bLic.Enable()
        
    def Grupo ( self, evento ):
        """Muestra la imagen del grupo"""
        #Me paso a la ruta del pyragua para cargar la imagen
        ruta_ant=os.getcwd()
        if self.parent.dir_pyragua:
            os.chdir(self.parent.dir_pyragua)
        bmpProy = wx.Bitmap(os.path.join("imagenes", "pyrox_about02.png"), wx.BITMAP_TYPE_ANY)
        imagProy = wx.StaticBitmap(self.pAb, -1, bmpProy)
        imagProy.SetBitmap(bmpProy)
        os.chdir(ruta_ant)
        
        #Deshabilito el botón Grupo
        self.bProy.Enable()
        self.bGru.Disable()
        self.bLic.Enable()
        
    def Licencia ( self, evento ):
        """Muestra la licencia"""
        #Cargo un resumen de la licencia
        #Me paso a la ruta del pyragua para cargar la imagen
        ruta_ant=os.getcwd()
        if self.parent.dir_pyragua:
            os.chdir(self.parent.dir_pyragua)
        bmpProy = wx.Bitmap(os.path.join("imagenes", "licencia_about02.png"), wx.BITMAP_TYPE_ANY)
        imagProy = wx.StaticBitmap(self.pAb, -1, bmpProy)
        imagProy.SetBitmap(bmpProy)
        os.chdir(ruta_ant)

        #Deshabilito el botón Licencia
        self.bProy.Enable()
        self.bGru.Enable()        
        self.bLic.Disable()
    
    def Cerrar ( self, evento ):
        self.Destroy()