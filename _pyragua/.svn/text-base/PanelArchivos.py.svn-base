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

from Archivo import Archivo
import wx
import os.path as path
import os
import sys
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

class PanelArchivos(wx.Panel):
    def __init__(self,*args,**kwargs):
        self.padre=kwargs['padre']
        self.vInicial=self.padre
        self.pyragua=self.vInicial.pyragua
        del kwargs['padre']

        wx.Panel.__init__(self,*args,**kwargs)
        self.nArchivos=wx.Notebook(self, -1,style =wx.BORDER_SUNKEN)
        self.nArchivos.pyragua=self.pyragua
        #La lista de los archivos
        self.lArchivos=[]
        self.PathArchivos=[]
        self.Layout()

        self.nArchivos.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.OnCambiarPagina)
        self.nArchivos.Bind(wx.EVT_RIGHT_UP,self.PopUpPestana)


    def Layout(self):
        """Se encarga de posicionar los sizer"""
        sArchivos=wx.BoxSizer(wx.VERTICAL)
        self.sArchivos=sArchivos
        sArchivos.Add(self.nArchivos,1,wx.EXPAND,0)
        self.SetSizer(sArchivos)
        self.SetAutoLayout(True)
        sArchivos.Layout()

    def AnunciarUser(self,Posicion,hilo):
        """"""
        dlg = wx.MessageDialog(self, _(u'EL archivo '+self.nArchivos.GetPageText(Posicion).split(' ')[1] +' sido modificado en otra parte,\n Desea recargarlo'),
                               _(u'Aviso'),
                               #wx.OK | wx.ICON_INFORMATION
                               wx.YES_NO | wx.NO_DEFAULT  | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal()==wx.ID_YES:
            codificacion='iso8859-1'
            arch=open(self.PathArchivos[Posicion])
            txt=arch.read()
            txt=txt.decode(codificacion)
            arch.close()
            self.nArchivos.SetSelection(Posicion)
            pag= self.lArchivos[Posicion]
            pag.stcEditor.ClearAll()
            pag.stcEditor.SetText(txt)
            self.nArchivos.SetPageText(Posicion, str(self.nArchivos.GetSelection()+1)+' '+self.nArchivos.GetPageText(Posicion).split(' ')[1]+' '+'*')
            #pag.stcEditor.ConvertEOLs(self.stcEditor.TIPO_EOL)
        hilo.ActualizarModificaciones(self.PathArchivos[Posicion],Posicion)
        dlg.Destroy()

    def AnalizarArchivo(self):
        """Analiza los fines de linea de un archivo y si hay errores muestra posibles soluciones"""
        NumTab=0
        NumEOL_CR=NumEOL_LF=NumEOL_CRLF=0
        pag=self.nArchivos.GetCurrentPage()
        TabWidth=pag.stcEditor.GetTabWidth()
        arch=open(pag.nombre)
        for linea in arch.readlines():
            Cont=0
            for palabra in linea:
                Cont+=1
                if palabra=='	':
                    NumTab+=1
                if palabra in ['\n','\r']:
                    if len(linea)!=Cont:
                        NumEOL_CRLF+=1
                        break
                    elif palabra in ['\n']:
                        NumEOL_LF+=1
                        continue
                    elif palabra in ['\r']:
                        NumEOL_CR+=1
                        continue
        arch.close()
        if pag.stcEditor.GetUseTabs():
            MsgTab='Es archivo esta usando Tab'
        else:
            if NumTab:
                MsgTab='El archivo esta usando una combinacion de '+str(NumTab)+' Tab y espacios'
            else:
                MsgTab='No esta usando Tabs'
        ListaFinLinea=[]
        ListaFinLinea.extend([NumEOL_CR,NumEOL_CRLF,NumEOL_LF])
        ListaFinLinea.sort() # organizo la lista
        # Miramos en que plataforma esta corriendo
        if wx.Platform == '__WXMSW__':
            Plataforma='Win'
        elif wx.Platform == '__WXMAC__':
            Plataforma= 'Mac'
        else:
            Plataforma='Linux'
        # Ahora miramos que si el achivo usa solo un fin de linea
        if not (ListaFinLinea[0]==0 and ListaFinLinea[1]==0):
            MsgNumEOL='Esta usando diversos tipos de linea en el docunemto recomendamos que solo use uno'
        else:
            if ListaFinLinea[2]==NumEOL_CRLF:
                if Plataforma == 'Win':
                    MsgNumEOL=''
                else:
                    MsgNumEOL='Esta usando fines de linea que no son propios de la arquitectura en la cual trabaja'
            if ListaFinLinea[2]==NumEOL_CR:
                if Plataforma == 'Mac':
                    MsgNumEOL=''
                else:
                    MsgNumEOL='Esta usando fines de linea que no son propios de la arquitectura en la cual trabaja'
            if ListaFinLinea[2]==NumEOL_LF:
                if Plataforma == 'Linux':
                    MsgNumEOL=''
                else:
                    MsgNumEOL='Esta usando fines de linea que no son propios de la arquitectura en la cual trabaja'
        print NumEOL_CR, NumEOL_LF,NumEOL_CRLF
        if MsgNumEOL=='':
            Msg='Se ha detectado en el siguiente archivo:\n- '+MsgTab+'\nQue desea hacer:'
        else:
            Msg='Se ha detectado en el siguiente archivo:\n- '+MsgTab+'\n- '+MsgNumEOL+'\nQue desea hacer:'
        dlg = wx.SingleChoiceDialog(
                self, Msg ,'Aviso',
                ['uno','dos'],
                wx.CHOICEDLG_STYLE
                )

        if dlg.ShowModal() == wx.ID_OK:
            Seleccion=dlg.GetStringSelection()

        dlg.Destroy()

    def AgregarNuevoArchivo ( self , nombre):
        open(nombre, "wb").close()
        self.AgregarArchivo(nombre)

    def AgregarArchivo(self,nombre):
        """Recibe el nombre de un archivo y lo abre en un stc, luego lo mete dentro del panel"""

        # Comprueva si el archivo esta abierto y si lo esta se sale del metodo
        for i in self.PathArchivos:
            if i == '':
                continue
            else:
                if i == nombre:
                    self.nArchivos.SetSelection(self.PathArchivos.index(i))
                    return
        self.PathArchivos.append(nombre)
        pArchivo=self.vInicial.dProyectos['default'].AgregarArchivo(nombre, padre=self.nArchivos)
        self.lArchivos.append(pArchivo)
        num =str(self.nArchivos.GetPageCount()+1)
        if len(nombre)==0:
            #Un archivo nuevo
            self.nArchivos.AddPage(pArchivo,num+' '+_('Nuevo'),select = True)
        else :
            self.nArchivos.AddPage(pArchivo,num+' '+path.basename(nombre),select = True)
        #Copio la coficación en la barra de estado
        self.padre.sBar.SetStatusText(pArchivo.codificacion,1)

        #Dejo el cursor listo para empezar a escribir
        pArchivo.stcEditor.SetFocus()
        if len(nombre)!=0:
            self.pyragua.cb.AddFile(nombre, open(nombre).readlines())
            self.pyragua.finicial.pCodigo.aCodigo.CambiarArchivo(nombre)

    def Cerrar(self,evento):
        """Este metodo cierra la pestaña y debuelve el numero del la pestaña que se esta cerrando"""
        #Miro si hay archivos para cerrar
        if self.nArchivos.GetPageCount()>0:
            pag=self.nArchivos.GetCurrentPage()
            num=self.nArchivos.GetSelection()
            pag.stcEditor.EmptyUndoBuffer()
            #self.pyragua.cb.DelFile(pag.nombre)
            self.pyragua.finicial.pCodigo.aCodigo.EliminarArchivo(pag.nombre)
            self.nArchivos.DeletePage(num)
            self.lArchivos.remove(pag)
            self.PathArchivos.pop(num)
            self.ActualizarPaginas()
            self.OnCambiarPagina()

        self.pyragua.finicial.SetTitle("Pyragua")
        return num

    def ActualizarPaginas(self):
        """ Actualiza la numeracion de las ventanas al cerrarlas"""
        NumeroPestanas= self.nArchivos.GetPageCount()
        for i in range(1,int(NumeroPestanas)+1):
            # separo el nombre del numero de la pagina
            lista = self.nArchivos.GetPageText(i-1).split(' ')[1:len(self.nArchivos.GetPageText(i-1))]
            cadena=''
            # Uno la cadena
            for j in lista:
                if j == '*':
                    cadena=cadena+' '+j
                    break
                cadena=cadena+j
            # Coloco el nombre con la nueva numeracion en la ventana
            self.nArchivos.SetPageText(i -1, str(i)+' '+cadena)

    def Ejecutar(self,evento=None):
        #La ruta del ejecutable se puede obtener con sys.executable
        if self.nArchivos.GetPageCount()>0:# Esto es para comprovar si hay pestañas abiertas
            self.nArchivos.GetCurrentPage().Ejecutar(evento)

    def Guardar(self,evento):
        """Guarda el archivo de la pestaña actual, retorna un booleano con que pasó y un
        mensaje informativo"""
        #La página actual seleccionada
        pag=self.nArchivos.GetCurrentPage()
        if self.nArchivos.GetPageCount()==0:# Esto es para comprovar si hay pestañas abiertas
            return False,_("No ha abierto ningún Archivo")
        else:
            salida,info=pag.OnGuardar(evento)
            if salida:
                return True,_(u"Archivo %s guardado")%(path.basename(pag.nombre))
            else:
                if info =="Cancelado":
                    return True,_(u"Cancelado %s\n%s"%(path.basename(pag.nombre)),"")
                return False,_(u"Problemas guardando %s\n%s"%(path.basename(pag.nombre),info))

    def GuardarComo(self,evento):
        """Lo mismo que guardar pero cambia el nombre del archivo"""
        #La página actual seleccionada
        pag=self.nArchivos.GetCurrentPage()
        if self.nArchivos.GetPageCount()==0:# Esto es para comprovar si hay pestañas abiertas
            return False,_(u"No ha abierto ningun Arhivo")
        else:
            salida,info=pag.GuardarComo(evento)
            if salida:
                self.PathArchivos[self.nArchivos.GetSelection()]=pag.nombre
                return True,_(u"Archivo %s guardado"%(path.basename(pag.nombre)))
            else:
                if info =="Cancelado":
                    return True,_(u"Cancelado %s\n%s"%(path.basename(pag.nombre),""))
                return False,_(u"Problemas guardando %s\n%s"%(path.basename(pag.nombre),info))

    def Modificado(self, evento):
        evento.Skip()

    def OnCambiarPagina(self,evento=None):
        """Este evento se llamará cuando cambien de página, por el momento
        se encarga de cambiar la codificacion en la barra de estado"""
        if not evento :
            pagina_actual=self.nArchivos.GetCurrentPage()
        else:
            pagina_actual=self.nArchivos.GetPage(evento.GetSelection())
        if pagina_actual:
            self.padre.sBar.SetStatusText(pagina_actual.codificacion,1)
            self.pyragua.finicial.pCodigo.aCodigo.CambiarArchivo(pagina_actual.nombre)
            self.padre.MostrarEOL( self.nArchivos.GetSelection())
            self.pyragua.finicial.SetTitle("Pyragua " + path.basename(pagina_actual.nombre))
        if evento: evento.Skip()


    def PopUpPestana ( self, evento ):
        """Este método nos permite dar click derecho sobre la pestaña del notebook
        para desplegar un menú"""
        pos= evento.GetPosition()
        self.IDcerrar = wx.NewId()
        self.IndexPestana=self.nArchivos.HitTest(pos)
        print self.IndexPestana
        if  self.IndexPestana:
            # Hacemos un menú
            menu = wx.Menu()

            # Mostramos íconos en las opciones
            Size=(16,16)
            item = wx.MenuItem(menu, self.IDcerrar,"Cerrar")
            close_bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, Size)
            item.SetBitmap(close_bmp)
            menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.PopUpClose, id=self.IDcerrar)
            # Otros items
            #_menu.Append(self.popupID2, "Two")
            #_menu.Append(self.popupID3, "Three")
            #_menu.Append(self.popupID4, "Four")
            #_menu.Append(self.popupID5, "Five")
            #_menu.Append(self.popupID6, "Six")

            # Para un submenú
            #_sm = wx.Menu()
            #_sm.Append(self.popupID8, "sub item 1")
            #_sm.Append(self.popupID9, "sub item 1")
            #_menu.AppendMenu(self.popupID7, "Test Submenu", sm)

            # Al dar click derecho sobre el popup se destruirá
            self.PopupMenu(menu)
            menu.Destroy()

    def PopUpClose ( self, evento):
            pag=self.nArchivos.GetPage(self.IndexPestana[0])
            pag.stcEditor.EmptyUndoBuffer()
            self.pyragua.cb.DelFile(self.nArchivos.GetPageText(self.IndexPestana[0]))
            self.nArchivos.DeletePage(self.IndexPestana[0])
            self.lArchivos.remove(pag)
            self.PathArchivos.pop(self.IndexPestana[0])
            self.ActualizarPaginas()
            self.OnCambiarPagina()
