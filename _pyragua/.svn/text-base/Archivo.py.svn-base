# -*- coding: iso8859-1 -*-
"""
Este archivo es parte de Pyragua

Pyragua es software libre; lo puedes redistribuir y/o modificar
bajo los terminos de la Licencia Publica General (GNU GPL) como fue
publicada por la Free Software Foundation; cualquier version 2 de la
Licencia.

Este programa es distribuido con la esperanza de que ser útil,
pero SIN GARANTIA ALGUNA; ni con la garantía explícita de
MERCABILIDAD o de que SERVIRA PARA UN PROPOSITO EN PARTICULAR.
Mire la Licencia Pública General de la GNU para más detalles.

Debió recibir una copia de la Licencia Pública General de la GNU junto con
este programa; sino, escriba a la Free Software Foundation,
Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
DEBUG=False

import wx.stc  as  stc
import wx
import sys
import os
import os.path
#Para la ejecucción
import popen2
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

from PythonSTC import PythonSTC
from Utils import *

class Archivo(wx.Panel):
    #TODO que esto sea parametrizable
    codificacion='iso8859-1'
#    codificacion = 'utf-8'
    """Esta clase va a representar un archivo fuente abierto en el editor"""
    def __init__(self,nombre,padre):
        """El constructor, recibe el nombre del archivo a abrir y una
        referencia al Notebook padre"""
        wx.Panel.__init__(self,padre,-1, size=(80,80))
        self.padre=padre
        self.pyragua=self.padre.pyragua
        self.nombre=os.path.abspath(nombre)
        self.BusquedaActiva = False # Esto es para combrobar si hay una busqueda
        #Esta variable me indica si se ha modificado una página
        self.HideLines=[]
        self.modificado=False
        #el editor
        self.stcEditor = PythonSTC(self, -1)
        #Si el nombre es vacio es porque es un archivo nuevo
        if len(nombre)>0:
            try:
                arch=open(nombre, 'rb')
                txt=arch.read()
                #Si es None debo tomar la codificación por defecto del sistema
                #if arch.encoding:
                #    self.codificacion=arch.encoding
                #else:
                #    self.codificacion=sys.getdefaultencoding()
                #   #Codificación
                #    txt=txt.decode(self.codificacion)
                #    arch.close()
            except:
                #Falló la carga desde archivo
                Utils.MostrarError("Error cargando el archivo, usando el texto por defecto")
                txt=self.TextoNuevo()
        else :
            #El archivo es nuevo
            txt=self.TextoNuevo()
        #Cargo el contenido del archivo en el editor

        txt = txt.decode('latin-1') 
        self.stcEditor.SetText(txt)

        self.Layout()
        self.Propiedades()
        eol=self.IdentificarEOL()
        if eol!=-1:
            self.stcEditor.TIPO_EOL=eol
            self.stcEditor.SetEOLMode(eol)

        if DEBUG: print "FIN constructor archivo"


    def TextoNuevo(self):
        '''Retorna el texto que se incluye en los archivos nuevos'''
        import time
        now = time.localtime(time.time())
        if wx.Platform == '__WXMSW__':
            #Probado en WINXP
            login=os.environ['USERNAME']
        else:
            #TODO sería bueno verificar que esté en GNU/Linux, ya que este texto
            #solo ha sido probado en esa plataforma
            login=os.environ['USER']
        if self.stcEditor.TIPO_EOL==stc.STC_EOL_CRLF:
            txt='#! -*- coding: %s -*-\r\n#Nuevo Archivo.\r\n#Creado por %s.\r\n#Creado: %s\r\n'
        elif self.stcEditor.TIPO_EOL==stc.STC_EOL_CR:
            txt='#! -*- coding: %s -*-\r#Nuevo Archivo.\r#Creado por %s.\r#Creado: %s\r'
        elif self.stcEditor.TIPO_EOL==stc.STC_EOL_LF:
            txt='#! -*- coding: %s -*-\n#Nuevo Archivo.\n#Creado por %s.\n#Creado: %s\n'
        txt=txt%(self.codificacion,login, time.asctime(now))
        return txt


    def Propiedades(self):
        """Establece propiedades especiales de los widgets"""
        #self.stcEditor.SetText(u"háslña")
        self.stcEditor.EmptyUndoBuffer()
        self.stcEditor.Colourise(0, -1)

        # line numbers in the margin
        self.stcEditor.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.stcEditor.SetMarginWidth(1, 25)

    def Layout(self):
        """Organiza la ventana en sizers"""
        sArchivo=wx.BoxSizer(wx.HORIZONTAL)
        self.sArchivo=sArchivo
        sArchivo.Add(self.stcEditor,1,wx.EXPAND,0)
        self.SetSizer(sArchivo)
        self.SetAutoLayout(True)
        sArchivo.Layout()

    def ComprobarConsola(self):
        """Este método comprueba la existencia en el sistema GNU/LINUX la
        existencia de una consola (xterm, gnome-terminal) adecuada para ejecutar el programa"""
        consola=""
        for con in ["xterm","konsole","gnome-terminal"]:
            ruta=popen2.popen2("which %s"%con)[0].readline()
            ruta=EliminarEOLS(ruta)
            if os.path.isfile(ruta):
                consola=con
                break
        #Parámetros especiales de cada consola
        if consola=="xterm":
            return "%s -T Pyragua -hold -e"%ruta
        elif consola=="konsole":
            return "%s  -T Pyragua -e"%ruta #le quito el --noclose
        elif consola=="gnome-terminal":
            return "%s -t Pyragua -e"%ruta
        else:
            #No encontré consola
            return ""


    def Ejecutar(self,evento=None):
        """Ejecuta el archivo, recibe el evento que lo lanzó"""
        #guardamos primero
        salida,info=self.OnGuardar(evento)
        if not salida:
            return False,"Error guardando\n%s"%info
        #Selecciono la consola
        if wx.Platform == '__WXMSW__':
            #Si estamos en windows, mandamos a ejecutar directamente
            #sout,sin=popen2.popen2('''%s "%s" '''%(sys.executable,self.nombre))
            os.popen('start "%s" "%s"'%(sys.executable,self.nombre))
            #os.popen('start "%s" "%s"'%(sys.executable,self.nombre))
        else:
            #En otra plataforma dependemos del xterm
            consola=self.ComprobarConsola()
            if consola=="":
                MostrarError(self.padre,_(u"No puedo encontrar una consola, o no están en el path, por favor instalalas (xterm, konsole o gnome-terminal)"))
            #sout,sin=popen2.popen2('''%s "%s" '''%(sys.executable,self.nombre))
            os.popen(consola+''' "%s" "%s" '''%(sys.executable,self.nombre))


    def OnGuardar(self,evento=None):
        """Esta función solo revisa si no se ha guardado todavía
        ningúna vez y llama a GuardarComo, de lo contrario llama a
        guardar"""
        #Es un archivo nuevo
        if len(self.nombre)==0:
            salida,msg=self.GuardarComo()
            if not salida:
                #Un error guardando
                return False,msg
            else:
                return True, ""
        else:
            #Llamo el verdadero guardar
            return self.Guardar()

    def GuardarComo(self,evento=None):
        """Le permite al usuario seleccionar que nombre de archivo
        desea, luego llama a guardar"""
        dlg=wx.FileDialog(self,"Seleccione un archivo", os.getcwd(),
                          defaultFile="",
                          wildcard="*.py",
                          style=wx.SAVE | wx.CHANGE_DIR|wx.OVERWRITE_PROMPT )
        salida = dlg.ShowModal()
        if salida == wx.ID_OK:
            #Seleccionaron bien el archivo
            paths=dlg.GetPaths()
            self.nombre=paths[0]
            #Con el nuevo nombre establecido llamo a guardar
            return self.Guardar()
        else:
            #Ojo retornamos siempre el estado y luego la información
            if salida == wx.ID_CANCEL:
                return False,"Cancelado"
            return False,""



    def Guardar(self,evento=None):
        """Pasa los datos del stc al archivo físico"""
        try:
            arch=open(self.nombre,"wb")
        except:
            #Error guardando el archivo
            info=sys.exc_info()[:][1]
            if DEBUG: print 'Error guardando el archivo'+str(info)
            #Retornemos Falso y la descripción del error
            return False,info

        texto=self.stcEditor.GetText()
        try:
            #Esta línea se necesita porque o si no no guarda
            #las tíldes

            if type(texto)==type(u"unicode"):
                texto=texto.encode(self.codificacion)
            arch.write(texto)
        except:
            #Error guardando el archivo
            #La info de la exepción, hay que sacar una copia por recomendación
            # de la docu oficial de python
            info=sys.exc_info()[:][1]
            if DEBUG: print 'error en el write con la codificacion '+str(info)
            #Retornemos Falso y la descripción del error
            return False,info
        arch.close()
        #Con esto sabremos cuando lo han modificado
        self.stcEditor.SetSavePoint()
        #Cambiamos el nombre de la página para que no tenga el * de modificado
        self.padre.SetPageText(self.padre.GetSelection(),
                               str(self.padre.GetSelection()+1)+' '+os.path.basename(self.nombre))
        return True, ""



    def GotoLine ( self ):
        """Este metodo sirve para ir a una ubicacion espesifica dada por el usuario"""
        dlg=wx.TextEntryDialog(self,_("Escribe el numero de linea a la cual deseas ir:"),_("Ir a la linea"))
        if dlg.ShowModal()==wx.ID_OK:
            try:
                numero_de_linea=int(dlg.GetValue())-1
                if numero_de_linea<self.stcEditor.GetLineCount() :
                    #Expande las cabeceras en caso de ser necesario
                    self.stcEditor.EnsureVisible(numero_de_linea)
                    #LineasEscondidas= self.GetHideLines(self.stcEditor.GetCurrentLine())
                    #self.stcEditor.ScrollToLine(self.stcEditor.GetCurrentLine()-LineasEscondidas)
                    self.stcEditor.GotoLine(numero_de_linea)
                else:
                    wx.MessageBox(_(u"El numero introducido es mayor que el numero de lineas del archivo"))
            except:
                wx.MessageBox(_(u"El numero introducido no es valido"))

    def BuscarTexto(self,evento):
        """Este metodo controla que el lo que debe hacer el buscar"""
        self.BusquedaActiva = True # Garantizo que ya hay una busqueda
        TipoEvento = evento.GetEventType()
        self.Busqueda = evento.GetFindString()
        self.Flags = evento.GetFlags()
        # evento Buscar
        if TipoEvento in [wx.wxEVT_COMMAND_FIND]:
            #El stcEditor.FindText retorna la start position de la cadena encontrad, sino -1 que no fue encontrada
            StartPosicion=self.stcEditor.FindText(self.stcEditor.GetCurrentPos(),
                                            self.stcEditor.GetLineEndPosition(self.stcEditor.GetLineCount()),
                                            self.Busqueda,self.Flags) # Esto define de donde a donde va a buscar
            if StartPosicion !=-1:
                self.stcEditor.SetSelection(StartPosicion,StartPosicion+len(self.Busqueda))
                self.stcEditor.ShowLines(1,self.stcEditor.GetLineCount())
                self.stcEditor.EnsureVisible(self.stcEditor.GetCurrentLine())
                LineasEscondidas= self.GetHideLines(self.stcEditor.GetCurrentLine())
                self.stcEditor.ScrollToLine(self.stcEditor.GetCurrentLine()-LineasEscondidas)
            else:
                MostrarError(self.padre,_(u"La cadena no pudo ser encontrada"))


        # evento Buscar Siguiente
        elif TipoEvento in [wx.wxEVT_COMMAND_FIND_NEXT]:
            pos =self.stcEditor.GetSelectionEnd()
            self.stcEditor.SetCurrentPos(pos)
            self.stcEditor.GotoPos(pos)
            self.stcEditor.SearchAnchor()# El stc recomienda llamar este metodo antes de llamar a SearchNext
            if self.Flags%2 :
                if self.stcEditor.SearchNext(self.Flags,self.Busqueda) == -1:
                    if MostrarAviso(self.padre,_(u"Ha llegado al final del documento desea volver al principio")):
                        self.stcEditor.GotoPos(0)
            else:
                print self.stcEditor.GetSelectedText()
                if self.stcEditor.GetSelectedText():
                    self.stcEditor.SetCurrentPos(self.stcEditor.GetSelectionStart())
                    print self.stcEditor.GetSelectionStart()
                if self.stcEditor.SearchPrev(self.Flags,self.Busqueda)==-1:
                    if MostrarAviso(self.padre,_(u"Ha llegado al principio del documento desea volver al final")):
                        self.stcEditor.GotoPos(self.stcEditor.GetLineEndPosition(self.stcEditor.GetLineCount()))
            self.stcEditor.ShowLines(1,self.stcEditor.GetLineCount())
            self.stcEditor.EnsureVisible(self.stcEditor.GetCurrentLine())
            LineasEscondidas= self.GetHideLines(self.stcEditor.GetCurrentLine())
            self.stcEditor.ScrollToLine(self.stcEditor.GetCurrentLine()-LineasEscondidas)


        # evento Buscar Remplazar
        elif TipoEvento in [wx.wxEVT_COMMAND_FIND_REPLACE]:
            if not self.stcEditor.GetSelectedText(): # debuelve 0 si no hay nada selecionado
                self.stcEditor.SearchAnchor()# El stc recomienda llamar este metodo antes SearchNext
                self.stcEditor.SearchNext(self.Flags,self.Busqueda)
            else:
                if self.stcEditor.GetSelectedText() == self.Busqueda:
                    RemplaceString = evento.GetReplaceString()
                    self.stcEditor.ReplaceSelection(RemplaceString)
                self.stcEditor.SearchAnchor()# El stc recomienda llamar este metodo antes SearchNext
                if self.stcEditor.SearchNext(self.Flags,self.Busqueda) == -1:
                    self.stcEditor.GotoPos(0)
            self.stcEditor.ShowLines(0,self.stcEditor.GetLineCount())
            self.stcEditor.EnsureVisible(self.stcEditor.GetCurrentLine())
            LineasEscondidas= self.GetHideLines(self.stcEditor.GetCurrentLine())
            self.stcEditor.ScrollToLine(self.stcEditor.GetCurrentLine()-LineasEscondidas)

        # evento Buscar Remplazar Todo
        elif TipoEvento in [wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
            self.stcEditor.GotoPos(1)
            RemplaceString = evento.GetReplaceString()
            while  1 :
                self.stcEditor.SearchAnchor()
                if self.stcEditor.SearchNext(self.Flags,self.Busqueda) == -1:
                    break
                self.stcEditor.ReplaceSelection(RemplaceString)

    def GetHideLines ( self , pos):
        """Retorna el numero de lineas escondidad que hay hasta una posicion dada """
        HideLines=0
        linea=0
        while linea<pos:
            if not self.stcEditor.GetLineVisible(linea) :
                HideLines+=1
            if DEBUG and not self.stcEditor.GetLineVisible(linea) :print (linea+1, pos+1), "Hide line"
            if DEBUG and  self.stcEditor.GetLineVisible(linea):print (linea+1, pos+1), "visible line"
            linea+=1
        return HideLines

    def PreguntarGuardar(self):
        """Le pregunta al usuario si quiere que guarde el archivo
        porque aún no lo ha hecho"""
        dlg=wx.MessageDialog(self.padre,
                             u"El archivo %s no ha sido guardado aún, desea guardarlo ahora?"%self.nombre,
                             u"El archivo no se ha grabado aún",
                             wx.YES_NO|wx.ICON_QUESTION)

        if dlg.ShowModal()==wx.ID_YES:
            self.OnGuardar()

    def CambiarEOL(self,eol):
        """Evento que cambia el tipo de fin de línea del archivo actual"""
        self.stcEditor.TIPO_EOL=eol
        self.stcEditor.SetEOLMode(eol)
        if DEBUG: print "Cambiar EOL", eol, stc.STC_EOL_CRLF, stc.STC_EOL_LF, stc.STC_EOL_CR

    def IdentificarEOL(self):
        """Este método se encargará de retornar el tipo de EOL que utiliza un archivo"""
        txt=self.stcEditor.GetText()
        eol=stc.STC_EOL_CRLF

        if txt=="" :
            return stc.STC_EOL_CRLF
        #Busco el primer salto de línea que haya
        for i,c in enumerate(txt):
	    #if DEBUG: print "Archivo: IdentificarEOL","c", c,ord(c)
            if c=='\n' or c=='\r':
                break
        if c not in ['\n','\r']:
            #No encontré el salto de línea,
	    if DEBUG: print "Archivo: IdentificarEOL no encontre EOL"
            return -1
        #Miremos el siguiente caracter para saber si es CRLF
        if i>(len(txt)-1):
            siguiente=""
        else:
            siguiente=txt[i+1]

        if c=='\r' and siguiente=='\n':
            #CRLF
            if DEBUG: print "EOL Windows"
            return stc.STC_EOL_CRLF
        elif c=='\r':
            if DEBUG: print "EOL MAC"
            return stc.STC_EOL_CR
        elif c=='\n':
            if DEBUG: print "EOL Linux"
            return stc.STC_EOL_LF
