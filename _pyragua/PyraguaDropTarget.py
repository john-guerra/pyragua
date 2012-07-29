#! -*- coding: iso8859-1 -*-
"""
Esta clase se encarga de administrar el arrastre de archivos al pyragua

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

class PyraguaDropTarget(wx.FileDropTarget):
    """Esta clase se encarga de administrar el arrastre de archivos al pyragua"""
    def __init__(self, pyragua):
        wx.FileDropTarget.__init__(self)
        self.pyragua=pyragua

    def OnDropFiles(self, x, y, filenames):        
        u"""Este evento es llamado al arrastrar archivos sobre el pyragua"""
        self.pyragua.finicial.AbrirArchivos(filenames)