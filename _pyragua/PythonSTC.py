#!-*- coding:iso8859-1 -*-
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
DEBUG=False
import wx.stc  as  stc
import wx
import keyword
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext

from Utils import *

#Este módulo sirve para buscar cuales son los módulos de una variable
import wx.py

import os,sys

if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

class PythonSTC(stc.StyledTextCtrl):
    fold_symbols = 3

    def __init__(self, archivo, ID,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        self.archivo=archivo
        self.pyragua=self.archivo.pyragua
        stc.StyledTextCtrl.__init__(self, archivo, ID, pos, size, style)
        self.Configurar()
        self.SetModEventMask(stc.STC_MOD_INSERTTEXT | stc.STC_MOD_DELETETEXT | stc.STC_PERFORMED_USER )
        #Utilizaremos este diccionario para llevar un registro del espacio
        #de nombres de cada variable para el autocompletar
        self.namespace={}

    def Configurar(self):
        u"""Establece los parámetros de configuración del stc"""
        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.CmdKeyAssign(ord('K'), stc.STC_SCMOD_CTRL, stc.STC_CMD_LINEDELETE)
        self.CmdKeyAssign(ord('Z'), stc.STC_SCMOD_CTRL, stc.STC_CMD_UNDO)

        self.SetLexer(stc.STC_LEX_PYTHON)
        keyword .kwlist+=['True','False','self']
        self.SetKeyWords(0, " ".join(keyword.kwlist))
        # esto sirve para resaltar estas palabras ademas de las que estan ya en keyword.kwlist
        self.CadenaParaComentar='#_'

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0,0)

        self.SetViewWhiteSpace(False)
        #self.SetBufferedDraw(False)
        #self.SetViewEOL(True)
        #self.SetEOLMode(stc.STC_EOL_CRLF)
        #self.SetUseAntiAliasing(True)
        self.TIPO_EOL=stc.STC_EOL_CRLF  #Variable que contiene el tipo de EOL
        '''stc.STC_EOL_CRLF
        stc.STC_EOL_CR
        stc.STC_EOL_LF'''
        self.SetEOLMode(self.TIPO_EOL)
        #self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        #self.SetEdgeColumn(78)
        self.TAMESPC=4#tamaño de cada tabulacion
        self.SetTabWidth(self.TAMESPC)
        # Setup a margin to hold fold markers
        #self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY,     "white", "black")

        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")

        self.Bind(stc.EVT_STC_MODIFIED,self.ChangeText)
        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(wx.EVT_CHAR, self.OnChar)

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        #Copiado del editor del demo de wxpy
        # Indentation and tab stuff
        self.SetIndent(self.TAMESPC)               # Proscribed indent size for wx
        self.SetIndentationGuides(True) # Show indent guides
        self.SetBackSpaceUnIndents(True)# Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)        # Tab key indents
        #self.SetTabWidth(4)             # Proscribed tab size for wx
        self.SetUseTabs(False)          # Use spaces rather than tabs, or

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")
        # Indentation guide
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        # Python styles
        # Default
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        self.SetCaretForeground("BLUE")
    def DesHacer(self,evento):
        if self.CanUndo()==1 :
            self.Undo()
        else:
            self.DesAcusarModificacion()

    def ReHacer(self,evento):
        if self.CanRedo() :
            self.Redo()
            self.AcusarModificacion()

    def OnCopy(self, evento):
        self.Copy()

    def OnCut(self, evento):
        self.Cut()

    def OnPaste(self, evento):
        self.Paste()

    def Tabular(self,linea):
        """Determina si la linea de texto debe ser tabulada y cuantos caracteres
        extras debe poner para completar la tabulación.
        Tabular(str) --> bool, int"""
        band=False #Determina si la linea debe ser tabulada
        m=0#cantidad de espacios extras a colocar en caso de ser necesario
        ban=True
        balp=0#balance de parantesis
        i=0
        while i<len(linea):#bucle para quitar las cadenas para no confundir algun comentario
            j=i
            if linea[i]=='"' and not linea[i:i+3]=='"""':#para quitar las cadenas en comillas dobles
                j=j+1
                while j<len(linea) and linea[j]!='"':
                    j=j+1
                #if j>=len(linea):
                    #print 'se salio'#se salio
                linea= linea[:i]+linea[j+1:]
                i=i-1
            elif linea[i:i+3]=='"""':#para quitar las cadenas en triple comilla doble
                j=j+3
                while j<len(linea) and linea[j:j+3]!='"""':
                    j=j+1
                #print 'i = %d, j = %d'%(i,j)
                #if j>=len(linea):
                    #print 'se salio'#se salio
                linea= linea[:i]+linea[j+3:]
                i=i-1
            elif linea[i]=="'" and not linea[i:i+3]=="'''":#para quitar las cadenas en comilla sencilla
                j=j+1
                while j<len(linea) and linea[j]!="'":
                    j=j+1
                #if j>=len(linea):
                    #print 'se salio'#se salio
                linea= linea[:i]+linea[j+1:]
                i=i-1
            elif linea[i:i+3]=="'''":#tpara quitar las cadenas en riple comilla sencilla
                j=j+3
                while j<len(linea) and linea[j:j+3]!="'''":
                    j=j+1
                #print 'i = %d, j = %d'%(i,j)
                #if j>=len(linea):
                    #print 'se salio'#se salio
                linea= linea[:i]+linea[j+3:]
                i=i-1
            i=i+1
        pos=linea.find('#')#se le borran los comentarios #xxxxx
        if pos >=0:
            linea=linea[:pos]
        ppal=(linea.split(' '))[0]#ppal contiene la primera palabra de la linea
        linea=linea.strip()
        band=linea.endswith(':')
        i=len(linea)-1
        while i>=0:#este ciclo es para saber si quedo algun parentesis abierto sin cerrar al final de la linea
            x=linea[i]
            if x=='(':
                balp=balp-1
            if x==')':
                balp=balp+1
            if balp==-1:
                band=False
                m=i
                break
            i=i-1
        palabras=['if', 'while', 'for', 'class', 'try','else','except','def','elif']#las palabras reservadas que llevan tabulacion
        if m >0:
            band=False
        bandera=False
        for x in palabras:#para determinar si la linea comienza con una palabra correcta para indentar
            if linea.startswith(x):
                bandera=True
        if not bandera and m==0:
            band=False
        return band,m

    def NuevaLinea ( self ):
        """Inserta una nueva linea segun la plataforma
        """
        if DEBUG : print "Nueva Línea", self.GetEOLMode()
        if self.GetEOLMode()==stc.STC_EOL_CRLF:
            self.AddTextRaw('\r\n')
        elif self.GetEOLMode()==stc.STC_EOL_CR:
            self.AddTextRaw('\r')
        elif self.GetEOLMode()==stc.STC_EOL_LF:
            self.AddTextRaw('\n')

    def CalcularTab( self ):
        """Funcion que calcula si al recibir un enter debe hacer una tabulacion extra e inserta la nueva linea.
        """
        ESP=' '#un caracter espacio, cuidado al modificar
        TAB='    '#un caracter tab, cuidado al modificar
        espacio=' '#el caracter por defecto de la tabulacion
        m=0#cantidad de espacios extras a colocar en la tabulacion
        numtabs=0#numero de tabulaciones
        (linea,pos)=self.GetCurLine()
        numtabs=self.GetLineIndentation(self.GetCurrentLine())
        linea=linea[:pos]
        if pos>=numtabs:
            if numtabs>0:
                if len(linea)!=0 :
                    espacio=linea[0]
                    if espacio==TAB:#si es una caracter tab?
                        numtabs=numtabs/self.GetTabWidth()
            linea=linea.strip()
            if  len(linea)>0:
                ban,m=self.Tabular(linea)
            else:
                ban=False
                m=0
            if ban:
                if espacio==TAB:
                    numtabs=numtabs+1
                else:
                    numtabs=numtabs+self.GetTabWidth()
            self.NuevaLinea()
            self.AddText( ((espacio*numtabs)+(ESP*m)) )
        else  :
            self.NuevaLinea()
            self.AddText( ((espacio*pos)+(ESP*m)) )

    def OnKeyPressed(self, event):
        """
        Funcion sobrecargada que se ejecuta cuando alguna tecla es presionada
        """
        if self.CallTipActive():
            self.CallTipCancel()

        #Para que funcione en el wx2.7
        if callable(event.KeyCode):
            key = event.KeyCode()
        else:
            key = event.KeyCode
        band=True

        if key == wx.WXK_RETURN and not self.AutoCompActive():
            #Estamos creando una nueva línea agreguémosla al ClassBrowser
            #self.AgregarLineaAlClassBrowser()
            band=False
            self.CalcularTab()
        if key == wx.WXK_SPACE and event.ControlDown():
            pos = self.GetCurrentPos()
            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("white")
                self.CallTipShow(pos, 'El editor del Pyragua\n\n'
                                 'Desarrollado por Pyrhox\n'
                                 'UTP.')
            # Code completion
            else:
                self.AutoCompletar(event)
        else:
            if band:
                event.Skip()

    def CompletarDosPuntos(self):
        """Metodo que pone el caracter ':' como ayuda
        """
        palabras=['if', 'while', 'for', 'class', 'try','else','except','elif']#las palabras reservadas usadas al antes de ':'
        (linea,pos)=self.GetCurLine()#devuelve la linea actual y la posicion del cursor en esta linea
        #Quito la basura
        linea=linea.strip()
        if len(linea)==0:
            return
        token=self.GetTokens(linea)[-1]#Se toma el ultima palabra de la linea
        #Vuelvo a quitar la basura
        token=token.strip()
        if token=='def':
            numtabs=self.GetLineIndentation(self.GetCurrentLine())
            if numtabs>=1:#Esto es un machetazo para saber si la declaracion esta dentro de una clase
           #si tiene tabulaciones la funcion deberia estar en una clase  por eso el self   (Ley de Charles)
               pos=self.GetCurrentPos()
               self.AddText(' ( self ):')
               self.SetCurrentPos(pos)
            else:
               pos=self.GetCurrentPos()
               self.AddText(' ( ):')
               self.SetCurrentPos(pos)
        if token in palabras:
            pos=self.GetCurrentPos()
            self.AddText(' :')
            self.SetCurrentPos(pos)
    def  TomarTamIdentacion( self, numLinea ):
        linea=self.GetLine(numLinea)
        aux_linea=linea.lstrip()
        tam=len(linea) - len(aux_linea)
        return tam

    def  STCComentarBloque( self ):
        """
        Metodo que comenta agregando el caracter '#_' al inicio de cada linea seleccionada
        """
        cad=self.CadenaParaComentar
        a,b=self.GetSelection()#se toma la posicion inicial y final de la seleccion
        #a=posicion inicial de la seleccion
        #b=posicion final de la seleccion
        A=self.LineFromPosition(a)#se toma el numero de la linea donde inicia la seleccion
        B=self.LineFromPosition(b)#se toma el numero de la linea donde finaliza la seleccion
        for x in range(A,B+1) :#recorre las lineas seleccionadas
            pos=self.PositionFromLine(x)#toma la posicion al inicio de cada linea
            numtabs=self.TomarTamIdentacion(x)
            #numtabs=self.GetLineIndentation(x)
            tamLinea=len( self.GetLine(x).strip() )
            if tamLinea > 0:
                if len(cad) > tamLinea:
                    self.InsertText(pos+numtabs,cad)
                else:
                    text=self.GetTextRange( pos+numtabs , pos+numtabs+len(cad) )
                    if len(text)>0 and (not text==cad) :
                        self.InsertText(pos+numtabs,cad)

    def  STCDesComentarBloque( self ):
        """
        Metodo que descomenta removiendo el caracter '#_' al inicio de cada linea seleccionada
        """
        cad=self.CadenaParaComentar
        a,b=self.GetSelection()#se toma la posicion inicial y final de la seleccion
        #a=posicion inicial de la seleccion
        #b=posicion final de la seleccion
        A=self.LineFromPosition(a)#se toma el numero de la linea donde inicia la seleccion
        B=self.LineFromPosition(b)#se toma el numero de la linea donde finaliza la seleccion
        targetstart=self.GetTargetStart()
        targetend=self.GetTargetEnd()
        for x in range(A,B+1) :#recorre las lineas seleccionadas
            pos=self.PositionFromLine(x)#toma la posicion al inicio de cada linea
            numtabs=self.TomarTamIdentacion(x)
            #numtabs=self.GetLineIndentation(x)
            tamLinea=len(self.GetLine(x).strip())
            if tamLinea>=len(cad) :
                text=self.GetTextRange(pos+numtabs,pos+numtabs+len(cad))
                if text==cad :#esta comentada al inicio?
                    self.SetTargetStart(pos+numtabs)
                    self.SetTargetEnd(pos+numtabs+len(cad))
                    self.ReplaceTarget('')#reemplaza el caracter '#_' por el caracter ''
        self.SetTargetStart(targetstart)
        self.SetTargetEnd(targetend)

    def ChangeText ( self , evento):
        #self.AcusarModificacion()
        evento.Skip()

    def OnChar(self,event):
        """Evento disparado cuando se recibe un caracter"""
        #Para que funcione en el wx2.7
        if callable(event.KeyCode):
            key = event.KeyCode()
        else:
            key = event.KeyCode
        pos=self.GetCurrentPos()
        self.AcusarModificacion()
        if key==ord(' '):#pregunta si escribio un espacio
            self.CompletarDosPuntos()
            self.AddText(' ')
        elif key==ord("."):
            if not self.AutoCompletar(event):
                #Un error en el autocompletar
                #Para que se agregue el caracter presionado
                event.Skip()
        else:
            #Procesar normalmente
            event.Skip()

    def OnUpdateUI(self, evt):
        """
        Reviza si hay parentesis, llaves o corchetes para resaltar.
        """
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            #pt = self.PointFromPosition(braceOpposite)
            #self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            #print pt
            #self.Refresh(False)


    def OnMarginClick(self, evt):
        """
        Muestra o esconde el texto de los bloques.
        """
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)


    def FoldAll(self):
        """
        Esconde todos bloques.
        """
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1



    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        """
        Muestra el texto de un bloque.
        """
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1

        return line



    def AcusarModificacion(self):
        """Esta función se encarga de dibujar un * en el nombre de la
        pestaña del panel para avisar que se ha modificado el archivo"""
        #La instancia de archivo que me contiene
        archivo=self.archivo
        #Este es el notebook donde estoy metido
        note_book=archivo.padre
        #Cuando es un archivo nuevo sin guardar no pongo nada
        if archivo.nombre!="":
            note_book.SetPageText(note_book.GetSelection(),
                                  str(note_book.GetSelection()+1)+' '+os.path.basename(archivo.nombre)+' '+"*")
        #Código para agregar un * cuando se modifica el archivo

    def DesAcusarModificacion(self):
        """Esta función se encarga de quitar el  * del nombre de la
        pestaña del panel para avisar que no se ha modificado el archivo"""
        #La instancia de archivo que me contiene
        archivo=self.archivo
        #Este es el notebook donde estoy metido
        note_book=archivo.padre
        #Cuando es un archivo nuevo sin guardar no pongo nada
        if archivo.nombre!="":
            note_book.SetPageText(note_book.GetSelection(),
                                  str(note_book.GetSelection()+1)+' '+os.path.basename(archivo.nombre))
        #Código para quitar el * cuando no se modifica el archivo

    def GetTokens(self,linea):
        """Toma una cadena de código python y la parte por tokens"""
        seps=[" ",",","=","(","|"]
        pal=""
        tokens=[]
        for c in linea:
            if c in seps:
                tokens.append(pal)
                pal=""
            else:
                pal+=c
        if pal!="":
            tokens.append(pal)
        return tokens

    def AgregarLineaAlClassBrowser ( self ):
            nombreArchivo=self.archivo.nombre
            linea=self.GetCurLine()[0]
            lineaNum=self.GetCurrentLine()
            self.pyragua.cb.AddLine( nombreArchivo, linea , lineaNum)
            self.pyragua.finicial.pCodigo.aCodigo.Actualizar()

    ########AUTOCOMPLETAR
    def ACLimpiarGetToken( self , linea):
        """Mira la línea actual, la parte por tokens y retorna solo
        el último token"""
        #Quito la basura
        linea.strip()
        linea=EliminarEOLS(linea)
        if len(linea)==0 :
            return False

        #Parto la línea por tokens, y tomo solo el último elemento
        token=self.GetTokens(linea)[-1]
        #Vuelvo a quitar la basura
        token.strip()
        return token

    def ACQuitarPunto( self, cadena ):
        "Elimina el el punto final de una cadena"
        if cadena[-1:]=='.':
            #Elimino el punto
            cadena=cadena[:-1]
        return cadena

    def AutoCompletar(self,evento):

        """Este método se encargará de autocompletar según lo que esté
        escrito, retorna True si fue capaz de realizarlo"""
        self.AutoCompSetIgnoreCase(False)
        (linea,pos)=self.GetCurLine()
        token=self.ACLimpiarGetToken(linea)
        token=self.ACQuitarPunto(token)

        objeto=self.ACEvaluar(token,linea)

        if not objeto:
            return False
        listaOps=dir(objeto)
        #Le adiciono a cada elemento el token
        #listaOps=[token+"."+x for x in listaOps]
        #self.autoComplete(object=1)
        if listaOps!=[]:
            self.AddText(".")
            self.AutoCompShow(0," ".join(listaOps))
            return True
        else:
            return False

    def ACEvaluar(self,word, linea):
        """Código tomado del spe, retorna un objeto obtenido con eval,
        modificado"""
        #Ya existe la palabra en el namespace, retornar lo que tenemos
        if word in self.namespace.keys():
            return self.namespace[word]
        #Si aún no está evaluar
        try:
            objeto=eval(word,self.namespace)
        except:
            try:
                #Aún no ha sido importado, lo importo
                objeto=__import__(word)
            except ImportError:
                #El módulo aún no existe, busco a ver si es uno de los que
                #se están escribiendo en este momento
                objeto=None
            except :
                print "Error en autocompletar", sys.exc_info
                return None

        #Agrego el objeto a mi lista
        self.namespace[word]=objeto
        return self.namespace[word]


    ########FIN AUTOCOMPLETAR
