#! -*- coding: iso8859-1 -*- 

"""setup.py Pyragua

Con este script se podr�n crear distribuciones en diversos formatos,
como un comprimido (zip o tar.gz), una versi�n ejecutable, un instalador
para windows y un paquete rpm.

En caso de agregar un nuevo m�dulo del Pyragua se debe agregar en la lista
pyragua_modulos para que se genere la salida adecuada. 

Distribuci�n de c�digo fuente

De esta forma el script crear� un paquete comprimido en un formato que
depende del Sistema operativo (tar.gz en UNIX, zip en g�in2)

En la linea de comandos se debe ejecutar:

- python setup.py sdist

Se puede especificar el formato de salida con la opci�n --formats

- python setup.py sdist --formats=gztar,zip,bztar,ztar,tar

Claro, esta opci�n requiere tener instalado los programas correspondientes
en el sistema operativo.

**En la creaci�n de una distribuci�n de c�digo fuente es importante tener
en cuenta el archivo MANIFEST y MANIFEST.in.  El primero es generado
automaticamente por distutils al ejecutarse el comando, y en el caso de
que se modifique el script para agregar nuevos m�dulos se debe eliminar
para que este lo genere nuevamente.  El segundo archivo contiene
instrucciones para agregar a la distribuci�n de c�digo fuente archivos que
no son de extensi�n 'py', como las im�genes y docmentos de texto.
"""
from distutils.core import setup
import glob, os
try:
    import py2exe
except:
    print "no pude importar el py2exe si est� en windows esto es un error sino ign�relo"
#Aqu� se deben agregar los m�dulos nuevos del pyragua
pyragua_modulos=[
                            '_pyragua',
                            '_pyragua.ClassBrowser',
                            ] 
#Sacada del About
descripcion_larga = """Pyragua es un entorno de desarrollo para
                                 la manipulaci�n de c�digo en lenguaje Python
                                 dise�ado por los integrantes del grupo de
                                 investigaci�n Pyrox de la Universidad
                                 Tecnol�gica de Pereira, cuyo fin es explorar e
                                 implementar nuevas tecnolog�as basadas en este
                                 potente lenguaje."""
imagenes=glob.glob(os.path.join('_pyragua', 'imagenes','*.png'))+glob.glob(os.path.join('_pyragua',  'imagenes','*.ico'))
print glob.glob(os.path.join( 'imagenes','*.ico'))
print imagenes
locales=glob.glob(os.path.join('_pyragua', 'locale','es', '*.po'))
setup (name='Pyragua', 
           version='0.2.3',
           description='Entorno de Desarrollo Integrado', 
           long_description=descripcion_larga,
           author='Pyrox',
           author_email='python@gda.utp.edu.co', 
           url='http://pyrox.utp.edu.co',    
           scripts=['pyragua'],            
           packages=pyragua_modulos,
           package_dir={'_pyragua':'_pyragua'},
           package_data={'_pyragua': ['_pyragua/imagenes']} ,
           data_files= [ ( os.path.join('_pyragua', 'imagenes') , 
                                    imagenes),
                                (os.path.join('_pyragua', 'locale', 'es'), 
                                    locales)  
                                ],
           windows=[
            {
            "script": '_pyragua/pyragua.py',
            "icon_resources": [(1, os.path.join("_pyragua","imagenes", "pyragua.ico"))]  #Esto es para py2exe
            } ]                                
          )
