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
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

class PanelProyecto(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)
        
        self.nProyecto=wx.Notebook(self, -1,style =wx.BORDER_SUNKEN)
        
        
        # oProyecto es una lista que guarda los lo que se le inserta al NoteBook
        self.oProyecto=[]
        # ProyectoName guarda los nombres de cada pestana esto es para luego darle soporte a otros idiomas
        self.ProyectoName = []
        # El agregar inserta Todo lo que va ir en el NoteBook
        self.Agregar()
        self.Layout()

        self.Proyectos.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick)

    def Layout(self):
        sProyecto = wx.BoxSizer(wx.VERTICAL)
        self.sProyecto = sProyecto
        cont = 0
        for i in self.oProyecto:
            self.nProyecto.AddPage(i,self.ProyectoName[cont])
            cont = cont +1
        self.sProyecto.Add(self.nProyecto,1,wx.EXPAND,0)        
        self.SetSizer(self.sProyecto)
        self.SetAutoLayout(True)
        self.sProyecto.Layout()

    def Destroy(self):
        event.Skip()    

    def Agregar(self):
        """Esto agrega el tree ctrl con todas sus propiedades"""
        self.Proyectos = wx.TreeCtrl(self.nProyecto, -1, style=wx.TR_HAS_BUTTONS|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER  )#|wx.TR_HIDE_ROOT

        # Creo las imagenes para los archivos del Tree Ctrl
        TamImagenes = (16,16)
        ListaImagenes = wx.ImageList(TamImagenes[0], TamImagenes[1])
        FolderIco = ListaImagenes.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, TamImagenes))
        FolderOpenIco = ListaImagenes.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, TamImagenes))
        self.ArchivosIco = ArchivosIco = ListaImagenes.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, TamImagenes))
        self.Proyectos.SetImageList(ListaImagenes)
        self.ListaImagenes = ListaImagenes

        #Aca agrega la raiz y le da la Propiedades
        self.root = self.Proyectos.AddRoot("Proyectos")
        self.Proyectos.SetPyData(self.root, None)
        self.Proyectos.SetItemImage(self.root, FolderIco, wx.TreeItemIcon_Normal)
        self.Proyectos.SetItemImage(self.root, FolderOpenIco, wx.TreeItemIcon_Expanded)
        #Aca agrego los proyectos Abiertos
        cProyectosAbiertos = self.Proyectos.AppendItem(self.root, "Proyectos Abiertos") # c es por que es un child de self.root
        self.Proyectos.SetPyData(cProyectosAbiertos, None)
        self.Proyectos.SetItemImage(cProyectosAbiertos, FolderIco, wx.TreeItemIcon_Normal)
        self.Proyectos.SetItemImage(cProyectosAbiertos, FolderOpenIco, wx.TreeItemIcon_Expanded)
        self.cProyectosAbiertos = cProyectosAbiertos
        #Aca agrego los proyectos Cerrados
        cProyectosCerrados = self.Proyectos.AppendItem(self.root, "Proyectos Cerrados")
        self.Proyectos.SetPyData(cProyectosCerrados, None)
        self.Proyectos.SetItemImage(cProyectosCerrados, FolderIco, wx.TreeItemIcon_Normal)
        self.Proyectos.SetItemImage(cProyectosCerrados, FolderOpenIco, wx.TreeItemIcon_Expanded)
        self.cProyectosCerrados = cProyectosCerrados 
        #Aca agrego para los arhivos individuales aviertos
        cArchivos = self.Proyectos.AppendItem(self.root, "Archivos")
        self.Proyectos.SetPyData(cArchivos, None)
        self.Proyectos.SetItemImage(cArchivos, FolderIco, wx.TreeItemIcon_Normal)
        self.Proyectos.SetItemImage(cArchivos, FolderOpenIco, wx.TreeItemIcon_Expanded)
        self.cArchivos = cArchivos

        self.Proyectos.Expand(self.root)   # expande el arbol
        self.ProyectoName.append("Proyectos")
        self.oProyecto.append(self.Proyectos)

        """Esto agrega el Control de Directorio y sus propiedades"""
        self.directorio = wx.GenericDirCtrl(self.nProyecto, -1,style=wx.DIRCTRL_SHOW_FILTERS,
                                filter="All files (*.*)|*.*|Python files (*.py)|*.py")
        self.ProyectoName.append("Examinar")
        self.oProyecto.append(self.directorio)

    def OnRightClick(self, event):
        """Al presionar el Click derecho desplega un menu"""
        self.popupMenuId = {}
        menu = wx.Menu()
        lista = ["Abrir","Cerrar"]
        for i in lista:
            self.popupMenuId[i] = wx.NewId()
            menu.Append(self.popupMenuId[i], i)
        
        self.Bind(wx.EVT_MENU, self.AgregarArchivo, id=self.popupMenuId["Abrir"])
        self.PopupMenu(menu)
        menu.Destroy()

    def AgregarProyecto(self,event):
        NomProyecto = wx.TextEntryDialog(self, 'Cual es el nombre del proyecto','Agregar Proyecto', '')
        if NomProyecto.ShowModal() == wx.ID_OK:
            Proyecto = self.Proyectos.AppendItem(self.cProyectosAbiertos, 'sadsadjsla')
            self.Proyectos.SetPyData(Proyecto, None)
            self.Proyectos.SetItemImage(Proyecto, FolderIco, wx.TreeItemIcon_Normal)
            self.Proyectos.SetItemImage(Proyecto, FolderOpenIco, wx.TreeItemIcon_Expanded)
            self.Proyectos.Expand(self.cProyectosAbiertos)
        NomProyecto.Destroy()

    def AgregarArchivo(self,event):
        NomArchivo = wx.TextEntryDialog(self, 'Cual es el nombre del archivo', 'Agregar Archivos', '')
        if NomArchivo.ShowModal() == wx.ID_OK:
            Archivos = self.Proyectos.AppendItem(self.cArchivos, 'sadsadjsla')
            self.Proyectos.SetPyData(Archivos, None)
            self.Proyectos.SetItemImage(Archivos, self.ArchivosIco, wx.TreeItemIcon_Normal)
            #self.Proyectos.Expand(self.cArchivos)
        NomArchivo.Destroy()

