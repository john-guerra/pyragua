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

# Archivo de utilidades
# Pyragua

import wx
# Para i18n
import gettext
gettext.install("pyragua",unicode=1)
_ = gettext.gettext


def MostrarError(padre,msg):
    """Muestra un error al usuario"""
    dlg=wx.MessageDialog(padre,msg,_("Error"),style=wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()
    
def MostrarAviso(padre,msg):
    """Muestra un aviso al usuario"""
    dlg=wx.MessageDialog(padre,msg,_("Aviso"),style=wx.ICON_INFORMATION | wx.YES_NO)
    if dlg.ShowModal() == wx.ID_YES:
        dlg.Destroy()
        return True        
    else:
        dlg.Destroy()
        return False
    
def EliminarEOLS(cad):
    """Recibe una cadena  y la retorna sin saltos de línea"""
    tmp=""
    for c in cad:
        if c not in ['\n','\r']:
            tmp+=c
    return tmp
    
def EliminaTab(TabWidth, Path,Codificacion):	
    """Recibe el tamano del tab(En espacios), el path del archivo y su codificacion
    Este metodo cambia las tabulaciones por espacios y coloca el fin de linea 
    dependiendo la arquitectura"""
    text=''
    arch=open(Path)
    #Busco la arquitectura en la cual esta corriendo
    if wx.Platform == '__WXMSW__':
        FinLinea='\r\n'
    elif wx.Platform == '__WXMAC__':
        FinLinea='\r'
    else:
        FinLinea='\n'
    for linea in arch.readlines():
        for palabra in linea:
            if palabra in ['\n','\r']:
                text+=FinLinea
                break
            if palabra=='\t':
                for i in range(TabWidth):
                    text+=' '
                    continue
            else:
                text+=palabra
                continue
    arch.close()
    text=text.decode(Codificacion)
    return text