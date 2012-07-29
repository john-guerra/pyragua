#! /usr/bin/python
#-*- coding:iso8859-1 -*-

"""Este programa es software libre; lo puedes redistribuir y/o modificar
bajo los terminos de la Licencia Publica General (GNU GPL) como fue
publicada por la Free Software Foundation; cualquier versión 2 de la licencia.

Este programa es distribuido con la esperanza de que será útil,
pero SIN GARANTIA ALGUNA; ni con la garantía explícita de
MERCABILIDAD o de que SERVIRA PARA UN PROPOSITO EN PARTICULAR.
Mire la Licencia Pública General de la GNU para más detalles.
"""
DEBUG=False


import  wx, threading
import wx.stc as stc
import os
import os.path as path
# Para llamar el about
import  wx.lib.dialogs as dialogs
#Para buscar el ejecutable del python
import sys
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

from PanelArchivos import PanelArchivos
from PanelProyecto import PanelProyecto
from PanelInferior import PanelInferior
from PanelCodigo import PanelCodigo
from ChangeBrowser import ChangeBrowser
from ClassBrowser.ClassBrowser import ClassBrowser
from PyraguaDropTarget import PyraguaDropTarget
from Utils import *
from about import About
from Proyecto import Proyecto

#La ruta en la que está actualmente el pyragua
dir_pyragua=""
pyragua_version="0.2a"
class VentanaInicial(wx.Frame):
    toolBarSize=(16,16)
    def __init__(self,*args,**kwargs):

        self.pyragua=kwargs['pyragua']
        del kwargs['pyragua']
        #Guardo la ruta del pyragua
        self.dir_pyragua=self.pyragua.dir_pyragua

        #padre es un parámetro que creo para que esta ventana pueda
        #hablar con la aplicación por eso lo saco y lo elimino de los
        #parámetros para que el constructor de frame no chille
        self.padre=kwargs["padre"]
        del kwargs["padre"]
        wx.Frame.__init__(self,*args,**kwargs)
        #El tipo de fin de línea por defecto
        self.TIPO_EOL=stc.STC_EOL_CRLF

        #Diccionario de proyectos
        self.dProyectos={}
        self.dProyectos['default']=Proyecto(self)

        self.pVentana = wx.Panel(self, -1)
        self.spVentana = wx.SplitterWindow(self.pVentana, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.pCodigo = PanelCodigo(self.spVentana, -1, padre=self)

        #Pequeño arreglo para no alterar otros archivos que usan pCodigo

        self.pNavegacion = self.pCodigo
        self.pEdicion = wx.Panel(self.spVentana, -1)
        self.spEdicion = wx.SplitterWindow(self.pEdicion, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.pArchivos = PanelArchivos(self.spEdicion,-1,padre=self)
        self.pPyShell = PanelInferior(self.spEdicion, -1)

        self.DropTarget=PyraguaDropTarget(self.pyragua)
        #self.pVentana.SetDropTarget(self.DropTarget)

        #Inicio los demonios
        #self.BuscadorCambios= ChangeBrowser(self.pArchivos)

        self.CrearMenu()
        self.CrearToolBar(self.toolBarSize)
        self.sBar=self.CreateStatusBar(3,0)

        #Banderas para los toggle menu en el men ver
        self.isNavSplit = False
        self.isInfSplit = False

        #Establece los anchos del status bar
        self.sBar.SetStatusWidths([-5,-2,-2])

        #Manejadores de los menus
        self.Bind(wx.EVT_MENU,self.Nuevo,id=self.menuArchivo.ids["Nuevo"])
        #self.Bind(wx.EVT_MENU,self.NuevoProyecto,id=self.menuArchivo.ids["Nuevo Proyecto"])
        self.Bind(wx.EVT_MENU,self.Abrir,id=self.menuArchivo.ids["Abrir"])
        self.Bind(wx.EVT_MENU,self.Guardar,id=self.menuArchivo.ids["Guardar"])
        self.Bind(wx.EVT_MENU,self.GuardarComo,id=self.menuArchivo.ids["GuardarComo"])
        self.Bind(wx.EVT_MENU,self.Cerrar,id=self.menuArchivo.ids["Cerrar"])
        self.Bind(wx.EVT_MENU,self.OnCloseWindow,id=self.menuArchivo.ids["Salir"])

        self.Bind(wx.EVT_MENU,self.Undo,id=self.menuEdicion.ids["Deshacer"])
        self.Bind(wx.EVT_MENU,self.Redo,id=self.menuEdicion.ids["Rehacer"])
        self.Bind(wx.EVT_MENU,self.Copiar,id=self.menuEdicion.ids["Copiar"])
        self.Bind(wx.EVT_MENU,self.Cortar,id=self.menuEdicion.ids["Cortar"])
        self.Bind(wx.EVT_MENU,self.Pegar,id=self.menuEdicion.ids["Pegar"])
        self.Bind(wx.EVT_MENU,self.Buscar,id = self.menuEdicion.ids["Buscar"])
        self.Bind(wx.EVT_MENU,self.GotoLine,id = self.menuEdicion.ids["Goto Line"])
        self.Bind(wx.EVT_MENU,self.BuscarSiguiente,id = self.menuEdicion.ids["BuscarSiguiente"])
        self.Bind(wx.EVT_MENU,self.BuscarAnterior,id = self.menuEdicion.ids["BuscarAnterior"])
        self.Bind(wx.EVT_MENU,self.Reemplazar,id = self.menuEdicion.ids["Reemplazar"])
        self.Bind(wx.EVT_MENU,self.ComentarBloque,id = self.menuEdicion.ids["Comentar"])
        self.Bind(wx.EVT_MENU,self.DesComentarBloque,id = self.menuEdicion.ids["DesComentar"])
        self.Bind(wx.EVT_MENU,self.CambiarEOL,id = self.menuEOL.ids["EOLWindows"])
        self.Bind(wx.EVT_MENU,self.CambiarEOL,id = self.menuEOL.ids["EOLLinux"])
        self.Bind(wx.EVT_MENU,self.CambiarEOL,id = self.menuEOL.ids["EOLMac"])
        self.Bind(wx.EVT_MENU,self.ConvertirEOLs,id = self.menuEdicion.ids["ConvertirEOLs"] )

        self.Bind(wx.EVT_MENU,self.alternarpNavegacion,id = self.menuVer.ids["Panel_Navegacion"])
        self.Bind(wx.EVT_MENU,self.alternarpInferior,id = self.menuVer.ids["Panel_Inferior"])
        self.Bind(wx.EVT_MENU,self.FinLinea,id = self.menuVer.ids["Fin_Linea"])

        self.Bind(wx.EVT_MENU,self.Ejecutar,id=self.menuEjecutar.ids["Ejecutar"])

        self.Bind(wx.EVT_MENU,self.about,id=self.menuAyuda.ids["About"])

        #self.Bind(wx.EVT_MENU,self.Split,id = self.menuAyuda.ids["About"])

        #Manejadores de la toolbar
        self.Bind(wx.EVT_TOOL,self.Nuevo,id=self.toolBar.ids["Nuevo"])
        self.Bind(wx.EVT_TOOL,self.Abrir,id=self.toolBar.ids["Abrir"])
        self.Bind(wx.EVT_TOOL,self.Guardar,id=self.toolBar.ids["Guardar"])
        self.Bind(wx.EVT_TOOL,self.GuardarComo,id=self.toolBar.ids["GuardarComo"])
        self.Bind(wx.EVT_TOOL,self.Copiar,id=self.toolBar.ids["Copiar"])
        self.Bind(wx.EVT_TOOL,self.Cortar,id=self.toolBar.ids["Cortar"])
        self.Bind(wx.EVT_TOOL,self.Pegar,id=self.toolBar.ids["Pegar"])
        self.Bind(wx.EVT_TOOL,self.Cerrar,id=self.toolBar.ids["Cerrar"])
        self.Bind(wx.EVT_TOOL,self.Ejecutar,id=self.toolBar.ids["Ejecutar"])
        self.Bind(wx.EVT_TOOL,self.Undo,id=self.toolBar.ids["Undo"])
        self.Bind(wx.EVT_TOOL,self.Redo,id=self.toolBar.ids["Redo"])

        # Manejadores de las busquedas
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)

        #Otros Manejadores
        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.onDClickSash)
        #self.Bind(wx.EVT_CONTEXT_MENU, self.MenuEmergente)

        #Icono de la ventana
        ruta_ant=os.getcwd()
        if self.dir_pyragua :
            os.chdir(self.dir_pyragua)
        PyraIcono = wx.Icon(os.path.join('imagenes','pyragua.ico'), wx.BITMAP_TYPE_ICO)
        self.SetIcon(PyraIcono)
        os.chdir(ruta_ant)

        #Sizers y demás
        self.Layout()
        self.MostrarEOL()
        #self.alternarpNavegacion()
        self.SetSize((500,500))

        #Muestro el pánel de navegación con el inicio de la aplicación
        self.alternarpNavegacion()


    def ConfirmarSalir(self):
        """Le pregunta al usuario si está seguro que desea salir, retorna True si es así False
        de lo contrario"""
        dlg=wx.MessageDialog(self, _(u"Seguro que desea salir?"),
                                                    _(u"Salir"), wx.CANCEL | wx.OK)
        return dlg.ShowModal()==wx.ID_OK

    def ComentarBloque( self,evento ):
        pag = self.pArchivos.nArchivos.GetCurrentPage()
        pag.stcEditor.STCComentarBloque()

    def DesComentarBloque( self,evento ):
        pag = self.pArchivos.nArchivos.GetCurrentPage()
        pag.stcEditor.STCDesComentarBloque()

    def OnCloseWindow(self, event):
        """Este evento captura cuando se quiere cerrar el editor"""
        #Seguro que desea salir?
        if not self.ConfirmarSalir():
            return

        #Para que salgan de los hilos
        #self.BuscadorCambios.hilo.Salir()
        #print 'Saliendo de hilo Buscador cambios'

        #Reviso que no haya archivos sin guardar

        for a in self.pArchivos.lArchivos:
            print a.stcEditor.GetModify(),a.nombre

        archivos_modificados=[x for x in self.pArchivos.lArchivos if x.stcEditor.GetModify()]

        print len(archivos_modificados)
        for archivo in archivos_modificados:
            archivo.PreguntarGuardar()

        self.Destroy()

    def Nuevo(self,evento):
        u"""Este evento es llamado al crear un nuevo archivo"""
        dlg=wx.FileDialog(self,"Seleccione el nombre del archivo", os.getcwd(),
                          defaultFile="",
                          wildcard="*.py",
                          style=wx.SAVE | wx.CHANGE_DIR|wx.OVERWRITE_PROMPT )
        salida = dlg.ShowModal()
        if salida == wx.ID_OK:
            #Seleccionaron bien el archivo
            paths=dlg.GetPaths()
            nombre=paths[0]
            self.pArchivos.AgregarNuevoArchivo(nombre)
            self.MostrarEOL()

    def NuevoProyecto(self,evento):
        self.dProyectos['default'].CrearProyecto()
        pass

    def Abrir(self,evento):
        u"""Este evento es llamado al abrir un nuevo archivo"""
        dlg=wx.FileDialog(self,_("Seleccione un archivo"), os.getcwd(),defaultFile="",
        wildcard="Python files (*.py)|*.py;*.pyw|All files (*.*)|*.*",
        style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR | wx.FILE_MUST_EXIST )

        if dlg.ShowModal()== wx.ID_OK:
        #Seleccionaron bien el archivo
            paths=dlg.GetPaths()
        #Puedo seleccionar varios archivosGetLineCount()
            if DEBUG: print  "abrir", paths

            self.AbrirArchivos(paths)

    def AbrirArchivos ( self, paths ):
        u"""Abre varios archivos en el pyragua"""
        for p in paths:
            self.pArchivos.AgregarArchivo(path.abspath(p))
            #self.pArchivos.AnalizarArchivo()
            # Agrego el archivo abierto al demonio que busca cambios
            #self.BuscadorCambios.hilo.GuardarRegistro(path)
            archivo=self.pArchivos.nArchivos.GetCurrentPage()
            self.SetTitle("Pyragua "+ path.basename(archivo.nombre))


        self.MostrarEOL(self.pArchivos.nArchivos.GetSelection())



    def Cerrar(self,evento):
        """Este método cierra la pestaña actual"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag = self.pArchivos.nArchivos.GetCurrentPage()

            # Revisa y almacena que archivos han sido modificados
            archivos_modificados=[x for x in self.pArchivos.lArchivos if x.stcEditor.GetModify()]

            # Recorre la lista de archivos modificados y la compara con la de la pestaña que se cerrará
            for archivo in archivos_modificados:
                if archivo == pag:
                    archivo.PreguntarGuardar() # Guarda el archivo

            num = self.pArchivos.Cerrar(evento)
            #self.BuscadorCambios.hilo.CerrarRegistro(num)

    def Ejecutar(self,evento):
        """Mira cual es la ventana seleccionada y ejecuta su contenido"""
        if DEBUG : print "pyragua.py: Ejecutar"
        hilo=threading.Thread(target=self.pArchivos.Ejecutar)
        hilo.start()

    def Guardar(self,evento):
        """Guarda el archivo actual"""
        estado,msg=self.pArchivos.Guardar(evento)
        if estado:
        #Todo salió bien, para la barra de tareas
            self.sBar.SetStatusText(msg)
            pag=self.pArchivos.nArchivos.GetCurrentPage()
            num=self.pArchivos.nArchivos.GetSelection()
            #self.BuscadorCambios.hilo.ActualizarModificaciones(pag.nombre,num)
        else:
            MostrarError(self,msg)

    def GuardarComo(self, evento):
        """Guarda el archivo actual"""
        estado,msg=self.pArchivos.GuardarComo(evento)
        if estado:
        #Todo salió bien, para la barra de tareas
            self.sBar.SetStatusText(msg)
            pag=self.pArchivos.nArchivos.GetCurrentPage()
            num=self.pArchivos.nArchivos.GetSelection()
            print num , pag.nombre
            #self.BuscadorCambios.z.ActualizarModificaciones(pag.nombre,num)
        else:
            MostrarError(self,msg)

    def Undo(self,evento):
        """Deshace la ultima opcion de usuario"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            pag.stcEditor.DesHacer(evento)

    def Redo(self,evento):
        """Rehace la ultima opcion de usuario"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            pag.stcEditor.ReHacer(evento)

    def Copiar(self, evento):
        """Copia el texto seleccionado en el portapapeles"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag = self.pArchivos.nArchivos.GetCurrentPage()
            pag.stcEditor.OnCopy(evento)

    def Cortar(self, evento):
        """Corta el texto seleccionado y lo almacena en el portapapeles"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag = self.pArchivos.nArchivos.GetCurrentPage()
            pag.stcEditor.OnCut(evento)

    def Pegar(self, evento):
        """Pega el texto que está contenido en el portapapeles"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag = self.pArchivos.nArchivos.GetCurrentPage()
            pag.stcEditor.OnPaste(evento)

    def GotoLine( self , evento):
        """"""
        # verifico si hay pestanas
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag = self.pArchivos.nArchivos.GetCurrentPage()
            pag.GotoLine()

    def Buscar(self, evento):
        """ Metodo que crea un dialogo de busqueda"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            data = wx.FindReplaceData()
            data.SetFlags(wx.FR_DOWN)
            if len(pag.stcEditor.GetSelectedText()) != 0:
                data.SetFindString(pag.stcEditor.GetSelectedText())
            dlg = wx.FindReplaceDialog(self, data, _("Buscar"))
            pag.data = data  # save a reference to it...
            dlg.Show(True)

    def Reemplazar(self, evento):
        """Metodo que crea un dialogo de busqueda y remplazo"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            data = wx.FindReplaceData()
            if len(pag.stcEditor.GetSelectedText()) != 0:
                data.SetFindString(pag.stcEditor.GetSelectedText())
            dlg = wx.FindReplaceDialog(self, data, _("Buscar y Remplazar"), wx.FR_REPLACEDIALOG)
            self.data = data  # save a reference to it...
            dlg.Show(True)

    def BuscarSiguiente(self, evento):
        """Busca el elemento siguente en TextCtrl"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            if pag.BusquedaActiva :
                if pag.stcEditor.GetSelectedText():
                    pag.stcEditor.SetCurrentPos(pag.stcEditor.GetSelectionEnd())
                pag.stcEditor.SearchAnchor()# El stc recomienda llamar este metodo antes de llamar a SearchNext
                pos = pag.stcEditor.SearchNext(pag.data.GetFlags(),pag.data.GetFindString())
                pag.stcEditor.EnsureVisible(pag.stcEditor.GetCurrentLine())
                LineasEscondidas= pag.GetHideLines(pag.stcEditor.GetCurrentLine())
                pag.stcEditor.ScrollToLine(pag.stcEditor.GetCurrentLine()-LineasEscondidas)
                if pos ==-1:
                    if MostrarAviso(self,_(u"Ha llegado al final del documento desea volver al principio")):
                        pag.stcEditor.GotoPos(0)

    def BuscarAnterior(self, evento):
        """Busca el elemento anterior en TextCtrl"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            if pag.BusquedaActiva :
                pag.stcEditor.SearchAnchor()# El stc recomienda llamar este metodo antes de llamar a SearchNext
                pos=pag.stcEditor.SearchPrev(pag.data.GetFlags(),pag.data.GetFindString())
                pag.stcEditor.EnsureVisible(pag.stcEditor.GetCurrentLine())
                LineasEscondidas= pag.GetHideLines(pag.stcEditor.GetCurrentLine())
                pag.stcEditor.ScrollToLine(pag.stcEditor.GetCurrentLine()-LineasEscondidas)
                if pos ==-1:
                    if MostrarAviso(self,_(u"Ha llegado al principio del documento desea volver al final")):
                        pag.stcEditor.GotoPos(pag.stcEditor.GetLineEndPosition(pag.stcEditor.GetLineCount()))

    def OnFind(self, evento):
        """Esta funcion se utiliza para buscar cadenas dentro de la pestana activa """
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            pag.BuscarTexto(evento)

    def OnFindClose(self, evento):
        """Garantiza que al cerrar el dialogo de busqueda este cierre"""
        evento.GetDialog().Destroy() #esto obtine el dialogo activo  y lo destuye

    def CrearToolBar(self,tsize):
        """Crea la barra de botones"""
        self.toolBar=self.CreateToolBar(wx.TB_HORIZONTAL)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        cut_bmp = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)
        close_bmp=wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, tsize)
        ejecutar_bmp=wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, tsize)
        guardar_bmp=wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,wx.ART_TOOLBAR,tsize)
        guardar_como_bmp=wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS,wx.ART_TOOLBAR,tsize)
        redo_bmp=wx.ArtProvider.GetBitmap(wx.ART_REDO,wx.ART_TOOLBAR,tsize)
        undo_bmp=wx.ArtProvider.GetBitmap(wx.ART_UNDO,wx.ART_TOOLBAR,tsize)

        self.toolBar.SetToolBitmapSize(tsize)

        self.toolBar.ids={}
        for i in ["Nuevo","Abrir","Guardar","GuardarComo","Copiar", "Cortar","Pegar","Cerrar","Ejecutar","Redo","Undo"]:
            self.toolBar.ids[i]=wx.NewId()

        self.toolBar.AddSimpleTool(self.toolBar.ids["Nuevo"],new_bmp,_("Nuevo"),_("Crear un nuevo archivo"))
        self.toolBar.AddSimpleTool(self.toolBar.ids["Abrir"],open_bmp,_("Abrir"),_("Abrir un archivo"))
        self.toolBar.AddSimpleTool(self.toolBar.ids["Guardar"],guardar_bmp,_("Guardar"),_("Guardar un archivo"))
        self.toolBar.AddSimpleTool(self.toolBar.ids["GuardarComo"],guardar_como_bmp,_("Guardar Como"),_("Guardar un archivo con otro nombre"))
        self.toolBar.AddSeparator()
        self.toolBar.AddSimpleTool(self.toolBar.ids["Copiar"],copy_bmp,_("Copiar"),_("Copiar al portapapeles"))
        self.toolBar.AddSimpleTool(self.toolBar.ids["Cortar"],cut_bmp,_("Cortar"),_("Corta el texto seleccionado"))
        self.toolBar.AddSimpleTool(self.toolBar.ids["Pegar"],paste_bmp,_("Pegar"),_("Pegar del cortapapeles"))
        self.toolBar.AddSeparator()
        self.toolBar.AddSimpleTool(self.toolBar.ids["Cerrar"],close_bmp,_("Cerrar"),_("Cerrar el archivo actual"))
        self.toolBar.AddSimpleTool(self.toolBar.ids["Ejecutar"],ejecutar_bmp,_("Ejecutar"),_("Ejecuta el archivo en un interprete de Python"))
        self.toolBar.AddSeparator()
        self.toolBar.AddSimpleTool(self.toolBar.ids["Undo"],undo_bmp,_("Deshacer"),_("Deshacer"))
        self.toolBar.AddSimpleTool(self.toolBar.ids["Redo"],redo_bmp,_("Rehacer"),_("Rehacer"))

        #Esto se necesita para que se muestre en windows
        self.toolBar.Realize()

    def CrearMenu(self):
        """Crea el menu"""
        self.menu = wx.MenuBar()
        self.menuArchivo = wx.Menu()
        self.menuEdicion = wx.Menu()
        self.menuVer = wx.Menu()
        self.menuEjecutar = wx.Menu()
        self.menuAyuda = wx.Menu()
        self.menuEOL=wx.Menu()

        #Creo un listado de ids para cada men
        self.menuArchivo.ids={}
        self.menuEdicion.ids={}
        self.menuVer.ids={}
        self.menuEjecutar.ids={}
        self.menuAyuda.ids={}
        self.menuEOL.ids={}

        #_for i in ["Nuevo","Nuevo Proyecto","Abrir","Guardar","GuardarComo","Cerrar","Salir"]:
        for i in ["Nuevo","Abrir","Guardar","GuardarComo","Cerrar","Salir"]:
            self.menuArchivo.ids[i]=wx.NewId()

        for i in ["Deshacer", "Rehacer", "Copiar", "Cortar", "Pegar","Goto Line", "Buscar",
        "BuscarSiguiente", "BuscarAnterior",
        "Reemplazar","CambiarEOLs" ,"ConvertirEOLs","Comentar","DesComentar"]:
            self.menuEdicion.ids[i]=wx.NewId()

        for i in ["Panel_Navegacion", "Panel_Inferior","Fin_Linea"]:
            self.menuVer.ids[i]=wx.NewId()

        for i in ["Ejecutar"]:
            self.menuEjecutar.ids[i]=wx.NewId()

        for i in ["About"]:
            self.menuAyuda.ids[i]=wx.NewId()

        #Men fin de línea
        for i in [ "EOLWindows", "EOLLinux", "EOLMac"]:
            self.menuEOL.ids[i]=wx.NewId()

        # Shortcuts y mensajes informativos para los mens
        self.menuArchivo.Append(self.menuArchivo.ids["Nuevo"], _("&Nuevo\tCtrl-N"), _("Crea un nuevo archivo"))
        #_self.menuArchivo.Append(self.menuArchivo.ids["Nuevo Proyecto"], _("&Nuevo Proyecto"), _("Crea un nuevo proyecto"))
        self.menuArchivo.Append(self.menuArchivo.ids["Abrir"], _("&Abrir\tCtrl-O"), _("Abre un archivo"))
        self.menuArchivo.Append(self.menuArchivo.ids["Guardar"], _("&Guardar\tCtrl-S"), _("Guarda los cambios del documento actual"))
        self.menuArchivo.Append(self.menuArchivo.ids["GuardarComo"], _("Guardar C&omo"), _("Posibilita el guardar en otro tipo de archivo"))
        self.menuArchivo.AppendSeparator()
        self.menuArchivo.Append(self.menuArchivo.ids["Cerrar"], _("&Cerrar\tCtrl-W"), _("Cierra el archivo actual"))
        self.menuArchivo.Append(self.menuArchivo.ids["Salir"],_("&Salir"),_("Salir de Pyragua"))

        self.menuEOL.Append(self.menuEOL.ids["EOLWindows"],_(U"Windows (CR/LF)"),_(u"Formato de fin de línea de windows CR/LF"), wx.ITEM_RADIO)
        self.menuEOL.Append(self.menuEOL.ids["EOLLinux"],_(U"GNU/Linux (LF)"),_(u"Formato de fin de línea de windows CR/LF"), wx.ITEM_RADIO)
        self.menuEOL.Append(self.menuEOL.ids["EOLMac"],_(U"Mac (CR)"),_(u"Formato de fin de línea de windows CR/LF"), wx.ITEM_RADIO)

        self.menuEdicion.Append(self.menuEdicion.ids["Deshacer"],_("&Deshacer\tCtrl-Z"),_(u"Deshace la ltima modificación"))
        self.menuEdicion.Append(self.menuEdicion.ids["Rehacer"],_("&Rehacer\tCtrl-Y"),_(u"Rehace la ltima modificación deshecha"))
        self.menuEdicion.AppendSeparator()
        self.menuEdicion.Append(self.menuEdicion.ids["Copiar"], _("&Copiar\tCtrl-C"), _(u"Copia el texto seleccionado"))
        self.menuEdicion.Append(self.menuEdicion.ids["Cortar"], _("Cor&tar\tCtrl-X"), _(u"Corta el texto seleccionado"))
        self.menuEdicion.Append(self.menuEdicion.ids["Pegar"], _("&Pegar\tCtrl-V"), _(u"Pega el texto contenido en el portapapeles"))
        self.menuEdicion.AppendSeparator()
        self.menuEdicion.Append(self.menuEdicion.ids["Goto Line"],_("&Ir a la linea...\tCtrl-G"),_(u"Posiciona el cursor en la linea que el usuario desee"))
        self.menuEdicion.Append(self.menuEdicion.ids["Buscar"],_("&Buscar...\tCtrl-B"),_(u"Busca una subcadena en el código fuente"))
        self.menuEdicion.Append(self.menuEdicion.ids["BuscarSiguiente"],_("Buscar S&iguente\tF3"),_(u"Busca la siguente coincidencia"))
        self.menuEdicion.Append(self.menuEdicion.ids["BuscarAnterior"],_("Buscar A&nterior\tF2"),_("Busca la anterior coincidencia"))
        self.menuEdicion.Append(self.menuEdicion.ids["Reemplazar"],_("&Reemplazar\tCtrl-R"),_(u"Busca una subcadena y la remplaza con otra"))
        self.menuEdicion.AppendSeparator()
        self.menuEdicion.Append(self.menuEdicion.ids["Comentar"],_("Comentar...\tAlt-3"),_(u"Comenta el bloque seleccionado"))
        self.menuEdicion.Append(self.menuEdicion.ids["DesComentar"],_("DesComentar...\tAlt-4"),_(u"DesComenta el bloque seleccionado"))
        self.menuEdicion.AppendSeparator()
        self.menuEdicion.AppendMenu(self.menuEdicion.ids["CambiarEOLs"], _(u"Cambiar fin de línea"),self.menuEOL)
        self.menuEdicion.Append(self.menuEdicion.ids["ConvertirEOLs"],_(u"&Convertir Fin de Línea"),_(u"Cambia todos los fin de línea del archivo al formato actual"))


        self.menuVer.AppendCheckItem(self.menuVer.ids["Panel_Navegacion"],_(u"&Panel de Navegación"),_(u"Muestra u oculta el panel de nevagación"))
        #Check menú -> True para el inicio de la aplicación
        self.menuVer.Check(self.menuVer.ids["Panel_Navegacion"], True)
        self.menuVer.AppendCheckItem(self.menuVer.ids["Panel_Inferior"],_(u"&Pánel inferior"),_(u"Muestra u oculta el pánel inferior"))
        self.menuVer.AppendSeparator()
        self.menuVer.AppendCheckItem(self.menuVer.ids["Fin_Linea"],_(u"&Fin de Linea"),_(u"Muestra el fin de linea del archivo"))

        self.menuEjecutar.Append(self.menuEjecutar.ids["Ejecutar"], _("&Ejecutar\tF5"), _(u"Ejecutar el archivo actual"))

        self.menuAyuda.Append(self.menuAyuda.ids["About"], _("&Acerca de..."), _(u"Algo sobre el proyecto"))

        self.menu.Append(self.menuArchivo,_(u"&Archivo"))
        self.menu.Append(self.menuEdicion,_(u"&Edición"))
        self.menu.Append(self.menuVer,_(u"&Ver"))
        self.menu.Append(self.menuEjecutar,_(u"E&jecutar"))
        self.menu.Append(self.menuAyuda,_(u"Ay&uda"))
        self.SetMenuBar(self.menu)

    def Layout(self):
        """Se encarga de crear los sizers y de insertar todos los widgets"""
        #Sizer principal
        sVentana = wx.BoxSizer(wx.HORIZONTAL)
        sPal = wx.BoxSizer(wx.HORIZONTAL)
        sNavegacion = wx.BoxSizer(wx.VERTICAL)
        sEdicion = wx.BoxSizer(wx.VERTICAL)

        #_Propiedades para los paneles, los sizers y los splitter

        self.spEdicion.SplitHorizontally(self.pArchivos, self.pPyShell)
        sEdicion.Add(self.spEdicion, 1, wx.EXPAND, 0)
        self.pEdicion.SetAutoLayout(True)
        self.pEdicion.SetSizer(sEdicion)
        sEdicion.Fit(self.pEdicion)
        sEdicion.SetSizeHints(self.pEdicion)
        self.spEdicion.Unsplit(self.pPyShell)

        self.spVentana.SplitVertically(self.pNavegacion, self.pEdicion)
        sPal.Add(self.spVentana, 1, wx.EXPAND, 0)
        self.pVentana.SetAutoLayout(True)
        self.pVentana.SetSizer(sPal)
        sPal.Fit(self.pVentana)
        sPal.SetSizeHints(self.pVentana)
        self.spVentana.Unsplit(self.pNavegacion)

        self.pVentana.SetAutoLayout(True)
        self.pVentana.SetSizer(sPal)

        sVentana.Add(self.pVentana, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sVentana)
        sVentana.Fit(self)
        sVentana.SetSizeHints(self)
        self.sVentana = sVentana

        #self.Maximize()

    def alternarpNavegacion(self, evento=None):
        """Método para mostrar u ocultar el pánel de navegación"""
        if self.isNavSplit:
            self.spVentana.Unsplit(self.pNavegacion)
            self.isNavSplit = False
        else:
            self.spVentana.SplitVertically(self.pNavegacion, self.pEdicion, 200)
            self.isNavSplit = True

    def alternarpInferior(self, evento):
        """Método para mostrar u ocultar el pánel inferior"""
        if self.isInfSplit:
            self.spEdicion.Unsplit(self.pPyShell)
            self.isInfSplit = False
        else:
            self.spEdicion.SplitHorizontally(self.pArchivos, self.pPyShell, 500)
            self.isInfSplit = True

    def FinLinea(self,evento):
        """Este metodo muestra los fines de linea"""
        if self.pArchivos.nArchivos.GetPageCount()>0:
            pag= self.pArchivos.nArchivos.GetCurrentPage()
            pag.stcEditor.SetViewEOL(not pag.stcEditor.GetViewEOL())

    def about(self, evento):
        """Acerca del proyecto"""
        win = About(self, _("Acerca de Pyragua"), style=wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ)
        win.CenterOnParent(wx.BOTH)
        win.Show(True)

    def onDClickSash(self, evento):
        self.spEdicion.SetMinimumPaneSize(20)
        self.spVentana.SetMinimumPaneSize(20)

    def CambiarEOL(self, evento):
        """Cambia el tipo de EOL del archivo actual"""
        id=evento.GetId()
        if id==self.menuEOL.ids['EOLWindows']:
            eol=stc.STC_EOL_CRLF
        elif id==self.menuEOL.ids['EOLLinux']:
            eol=stc.STC_EOL_LF
        elif id==self.menuEOL.ids['EOLMac']:
            eol=stc.STC_EOL_CR
        else:
            return
        if self.pArchivos.nArchivos.GetPageCount()==0:
            #El eol por defecto
            self.TIPO_EOL=eol
        else:
            pag= self.pArchivos.nArchivos.GetPage(self.pArchivos.nArchivos.GetSelection())
            #pag= self.pArchivos.nArchivos.GetCurrentPage()
            pag.CambiarEOL(eol)
        self.MostrarEOL(self.pArchivos.nArchivos.GetSelection())
        if DEBUG : print "Cambiar EOL Pyragua", id, "eol",eol

    def MostrarEOL(self, idPag=-1):
        """Mostrar el tipo de EOL del archivo actual (el identificado por idPag) o el por defecto"""
        if DEBUG :
            print "EOL MOSTRAR",idPag

        if idPag==-1:
            #El eol por defecto
            eol=self.TIPO_EOL
        else:
            pag= self.pArchivos.nArchivos.GetPage(idPag)
            if not pag:
                #Es un archivo nuevo
                if DEBUG : print "MostrarEOL", "archivo nuevo", pag
                eol=self.TIPO_EOL
            else:
                eol=pag.stcEditor.TIPO_EOL
        if DEBUG: print "EOL MOSTRAR",idPag, "eol",eol, stc.STC_EOL_CRLF
        if eol==stc.STC_EOL_CRLF:
            strEOL="Win (CRLF)"
            self.menuEOL.Check(self.menuEOL.ids["EOLWindows"], True)
            if DEBUG : print "CRLF"
        elif eol==stc.STC_EOL_CR:
            strEOL="Mac (CR)"
            self.menuEOL.Check(self.menuEOL.ids["EOLMac"], True)
            if DEBUG : print "LF"
        elif eol==stc.STC_EOL_LF:
            strEOL="Lin (LF)"
            self.menuEOL.Check(self.menuEOL.ids["EOLLinux"], True)
            if DEBUG : print "CR"
        self.SetStatusText(strEOL,2)

    def ConvertirEOLs(self, evento):
        pag=self.pArchivos.nArchivos.GetCurrentPage()
        pag.stcEditor.ConvertEOLs(pag.stcEditor.GetEOLMode())

class Pyragua(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()

        #Guardo la ruta del pyragua
        if wx.Platform == '__WXMSW__' :
            self.dir_pyragua=os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            self.dir_pyragua=os.path.dirname(__file__)
            if not os.path.exists(os.path.join(self.dir_pyragua, "imagenes")):
                #Necesario para cuando está instalado en linux
                self.dir_pyragua=os.path.join('/','usr','_pyragua')


        #ClassBrowser
        self.cb=ClassBrowser()

        self.finicial=VentanaInicial(None,-1,"Pyragua",padre=self, pyragua=self)
        self.finicial.Show(True)
        self.AbrirSplash()  #descomentar cuando se solucione el problema
        #self.SetTopWindow(self.splash) #descomentar cuando se solucione el problema
        self.SetTopWindow(self.finicial) #comentar cuando se solucione el problema
        if len(sys.argv)>1:
            self.finicial.AbrirArchivos(sys.argv[1:])



        return True

    def AbrirSplash(self):
        #inicio del splash
        id_splash = wx.NewId()
        #Me paso a la ruta del pyragua para cargar la imagen
        ruta_ant=os.getcwd()
        if self.finicial.dir_pyragua :
            os.chdir(self.finicial.dir_pyragua)
        self.splash = wx.SplashScreen(wx.Bitmap(os.path.join("imagenes","pyragua_splash.png")), wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 2000, self.finicial, id_splash, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        os.chdir(ruta_ant)


def main():
    #Calculo la ruta del pyragua si es diferente del dir actual me cambio
    app = Pyragua(0)
    app.MainLoop()


if __name__ == "__main__":
  main()
