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

import os
import wx
import gettext
import  wx.wizard as wiz
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

class WizardProyectos :
    def __init__ ( self, parent ):
        self.parent=parent
        self.Info= self.WizardCrearProyecto()
        
        self.wizard.Bind(wiz.EVT_WIZARD_PAGE_CHANGING,self.Guardar) 

    def WizardCrearProyecto(self):
        """Crea un wizard para crear un proyecto, recoge la informacion necesaria y la debuelve"""
        Imagen=wx.Image(os.path.join("imagenes", "bmppyragua.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.wizard = wiz.Wizard(self.parent, -1, _("Asistente de Proyectos"),Imagen)

        page1 = TituloPagina(self.wizard, _("Nombre y Descripcion del Proyecto"))
        page2 = TituloPagina(self.wizard, _("Page 2"))
        page3 = TituloPagina(self.wizard, _("Page 3"))
        page4 = TituloPagina(self.wizard, _("Page 4"))
        self.page1 = page1

        #Pagina 1 sizer y demas
        self.StaticboxP = wx.StaticBox(page1, -1, "Nombre del Proyecto")
        self.StaticboxD = wx.StaticBox(page1, -1, "Descripcion del Proyecto")
        self.NombreProyecto = wx.TextCtrl(page1, -1, "")
        self.DecripcionProyecto = wx.TextCtrl(page1, -1, "", style=wx.TE_MULTILINE)
        sizerP1= wx.BoxSizer(wx.VERTICAL)
        sizerProyecto = wx.StaticBoxSizer(self.StaticboxP, wx.VERTICAL)
        sizerDescripcion = wx.StaticBoxSizer(self.StaticboxD, wx.HORIZONTAL)
        sizerProyecto.Add(self.NombreProyecto, 0, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 2)
        sizerP1.Add(sizerProyecto, 0, wx.ALL|wx.EXPAND, 6)
        sizerDescripcion.Add(self.DecripcionProyecto, 1, wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE, 2)
        sizerP1.Add(sizerDescripcion, 1, wx.ALL|wx.EXPAND, 6)
        sizerP1.Fit(page1)
        sizerP1.SetSizeHints(page1)

        #page1.sizer.Add(wx.StaticText(page1, -1, "Este es el asistente de proyectos"))

        self.wizard.FitToPage(page1)
        page1.sizer.Add(sizerP1,1,wx.EXPAND)

        
        wiz.WizardPageSimple_Chain(page1, page2)
        wiz.WizardPageSimple_Chain(page2, page3)
        wiz.WizardPageSimple_Chain(page3, page4)

        if self.wizard.RunWizard(page1):
            wx.MessageBox("Wizard completed successfully", "That's all folks!")
        else:
            wx.MessageBox("Wizard was cancelled", "That's all folks!")
        return {}

    def Guardar(self, evento):
        print 1

class TituloPagina(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = self.makePageTitle(self, title)

    def makePageTitle(self,wizPg, title):
        sizer = wx.BoxSizer(wx.VERTICAL)
        wizPg.SetSizer(sizer)
        title = wx.StaticText(wizPg, -1, title)
        title.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
        return sizer