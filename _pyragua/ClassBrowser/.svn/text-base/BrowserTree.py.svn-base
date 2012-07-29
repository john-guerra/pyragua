#! -*- coding: iso8859-1 -*-


__autor__="John Alexis Guerra Gómez <aguerra@utp.edu.co>"
DEBUG=False

import wx

import os.path as path
import time
import os

class BrowserTree ( wx.TreeCtrl ):
    #El árbol del navegador de código
    def __init__ ( self , padre, cb, pyragua):
        "cb: a ClassBrowser instance"


        wx.TreeCtrl.__init__(self, padre, -1)
        self.cb=cb
        self.pyragua=pyragua
        self.iconos={}
        #TODO Validar que no existan los íconos
        ruta_ant=os.getcwd()
        if pyragua.dir_pyragua:
            os.chdir(pyragua.dir_pyragua)
        self.imageList=wx.ImageList(10,10)
        self.iconos["clase"]=self.imageList.Add(wx.Bitmap(os.path.join("imagenes","clase.png")))
        self.iconos["archivo"]=self.imageList.Add(wx.Bitmap(os.path.join("imagenes","archivo.png")))
        self.iconos["metodo"]=self.imageList.Add(wx.Bitmap(os.path.join("imagenes","metodo.png")))
        os.chdir(ruta_ant)
        self.SetImageList(self.imageList)

        self.ruta=""
        self.archivo=None
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.Activar)
        self.Bind(wx.EVT_RIGHT_DOWN, self.MenuDerecha)
        self.arbolCodAnt={}
        self.indexArbol={}
        self.rutaCompleta=""

    def CambiarArchivo(self,nombre):
        #Elimino la parte .py
        if DEBUG: print "BT cambiar archivo", nombre
        self.nombre=path.basename(nombre).split(".")[0]
        self.ruta=path.dirname(nombre)
        self.rutaCompleta=path.abspath(nombre)
        self.Actualizar()

    def Actualizar(self):
        """Esta función revisa el diccionario del classBrowser para buscar que clases y
        funciones hay disponibles"""
        cambio=False
        if not self.rutaCompleta in self.cb.fileDic.keys() :
            self.Limpiar()
            #print "ERROR BROWSER TREE Acutalizar a un archivo que no estA en el classBrowser", self.rutaCompleta
            return
        arbolCod=self.cb.fileDic[self.rutaCompleta].objDict
        if DEBUG: print "BT: nombre", "Arbolcod",arbolCod.keys(), "ANTERIOR", self.arbolCodAnt.keys(), "index", self.indexArbol.keys()

        #Saco el nombre del archivo actualmente mostrado
        try:
            root=self.GetRootItem()
            nombre=self.GetPyData(root)
        except:
            nombre=""
        if self.nombre != nombre :
            #Cambio de Arbol
            self.DeleteAllItems()
            del self.indexArbol
            self.indexArbol={}
            self.arbolCodAnt={}
            root=self.AgregarRoot()
            cambio=True

        self.BorrarNodosViejos(arbolCod)
        if DEBUG: print "BT: AgregarNODOSNUEVOS nombre", "Arbolcod",arbolCod.keys(), "ANTERIOR", self.arbolCodAnt.keys(), "index", self.indexArbol.keys()
        self.AgregarNodosNuevos(arbolCod)

        if cambio :
            self.Expand(root)
        self.arbolCodAnt.update(arbolCod)

        self.UpdateWindowUI()


    def AgregarNodosNuevos ( self, arbolCod ):
        """Revisa que nodos deben agregarse al árbol, recibiendo un nuevo árbol generado por el
        pyclbr"""
        ant=self.arbolCodAnt
        root=self.GetRootItem()
        nombre=self.GetPyData(root)
        #Creo los nodos nuevos
        objs=arbolCod.keys()
        objs.sort()

        if DEBUG : print "BT: AgregarNodosNuevos",objs
        for clase in objs:
            val=arbolCod[clase]
            if not ant.has_key(clase) :
                #Es nuevo
                if hasattr(val,"methods"):
                    if DEBUG: print "BT: Agregar Clase", clase, val.lineno
                    hojaClase=self.AgregarClase(root,nombre,val, val.lineno)
                else:
                    #Es una función
                    if DEBUG: print "BT: Agregar Función", clase, val.lineno
                    hojaMetodo=self.AgregarFuncion(root,nombre,clase, val.lineno)
            if hasattr(val, "methods") :
                methods_keys=val.methods.keys()
                methods_keys.sort()
                if DEBUG : print "BT: ", clase, "MEtodos", methods_keys
                for met in methods_keys:
                    hojaClase=self.indexArbol[nombre].clases[clase]
                    if ant.has_key(clase):
                        if not met in ant[clase].methods :
                            if DEBUG: print "BT: Agregar Metodo", clase, met, val.lineno
                            self.AgregarMetodo(hojaClase, nombre,clase,met,val.methods[met])
                    else:
                        if DEBUG: print "BT: Agregar Metodo1", clase, met, val.lineno
                        self.AgregarMetodo(hojaClase, nombre,clase,met,val.methods[met])

    def BorrarNodosViejos ( self,  arbolCod):
        """Elimina del árbol los nodos viejos, recibiendo un nuevo árbol generado por el
        pyclbr"""
        root=self.GetRootItem()
        ant=self.arbolCodAnt
        nombre=self.GetPyData(root)
        #Borro los nodos viejos
        for clase,val in ant.iteritems():
            if not clase in arbolCod.keys() :
                if hasattr(val,"methods"):
                    #Es clase y ya no está
                    if DEBUG : print "CB: Borrar Clase", nombre, clase
                    self.Delete( self.indexArbol[nombre].clases[clase] )
                    #Elimino también del índice
                    del  self.indexArbol[nombre].clases[clase]
                    #TODO borrar todos los hijos
                else:
                    #Es función y no está
                    if DEBUG : print "CB: Borrar Función", nombre, clase
                    self.Delete(self.indexArbol[nombre].funciones[clase])
                    #Elimino también del índice
                    del self.indexArbol[nombre].funciones[clase]
            else:
                #Reviso los hijos de las clases
                if hasattr(val,"methods"):
                    for func in val.methods:
                        if not func in arbolCod[clase].methods :
                            #Un método desapareció
                            if DEBUG : print "CB: Borrar método", nombre, clase, func
                            self.Delete(self.indexArbol[nombre].clases[clase].metodos[func])
                            del self.indexArbol[nombre].clases[clase].metodos[func]

    def AgregarRoot ( self ):
        if DEBUG: print "BT AgregarRoot", self.nombre
        root=self.AddRoot(self.nombre)
        self.indexArbol[self.nombre]=root
        self.indexArbol[self.nombre].clases={}
        self.indexArbol[self.nombre].funciones={}
        self.SetItemImage(root,self.iconos["archivo"])
        self.SetPyData(root, self.nombre)

        #self.arbolCodAnt[self.nombre]=self.cb.fileDic[self.rutaCompleta].objDict[self.nombre]
        return root

    def AgregarClase ( self , root, archivo,clase,linea):
        nombre=clase.name
        hojaClase=self.AppendItem(root,nombre)
        self.indexArbol[archivo].clases[nombre]=hojaClase
        self.indexArbol[archivo].clases[nombre].metodos={}
        self.indexArbol[archivo].clases[nombre].data=clase
        self.SetItemImage(hojaClase,self.iconos["clase"])
        self.SetPyData(hojaClase, linea)

        return hojaClase

    def AgregarMetodo ( self , hojaClase, archivo,clase,func,linea):
        hojaMetodo=self.AppendItem(hojaClase,func)
        self.indexArbol[archivo].clases[clase].metodos[func]=hojaMetodo
        self.SetItemImage(hojaMetodo,self.iconos["metodo"])
        self.SetPyData(hojaMetodo, linea)

        return hojaMetodo

    def AgregarFuncion( self , root, archivo,func, linea):
        hojaFuncion=self.AppendItem(root,func)
        self.indexArbol[archivo].funciones[func]=hojaFuncion
        self.SetItemImage(hojaFuncion,self.iconos["metodo"])
        self.SetPyData(hojaFuncion, linea)

        return hojaFuncion

    def Activar ( self , evento):
        """Manejador de Evento de activar un elemento del árbol"""
        linea=self.GetItemPyData(evento.GetItem())
        #Si no es un número me salgo
        if type(linea)!=type(1) :
            return
        pyragua=self.pyragua
        pag=pyragua.finicial.pArchivos.nArchivos.GetCurrentPage()
        if DEBUG: print "CB: Ir a ", linea
        LineasEscondidas= pag.GetHideLines(linea)
        pag.stcEditor.ScrollToLine(linea-LineasEscondidas)

    def MenuDerecha(self, evt=None):
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity.
        if not hasattr(self, "idActualizar"):
            self.idActualizar = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnActualizar, id=self.idActualizar)

        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.idActualizar,"Actualizar")
        menu.AppendItem(item)
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnActualizar(self, evt=None):
        self.cb.AddFile(self.rutaCompleta, open(self.rutaCompleta).readlines())
        self.Actualizar()

    def EliminarArchivo(self, nombre):
        self.cb.DelFile(nombre)
        self.Actualizar()

    def Limpiar(self):
        self.DeleteAllItems()
        self.UpdateWindowUI()


