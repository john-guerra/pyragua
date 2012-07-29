#! -*- coding: iso8859-1 -*-
"""ClassBrowser.py
    This file includes services to analize python source codes to extract it's
    structure, to construct a CodeBrowser


"""
__autor__="John Alexis Guerra Gómez <aguerra@utp.edu.co>"
DEBUG=False
import tokenize
from token import NAME, DEDENT, NEWLINE


import pdb

class Line :
    def __init__ ( self, val, lineno ,file, ancestors):
        self.val=val
        self.lineno=lineno
        self.file=file
        #Tell who is my ancestors
        self.ancestors=ancestors

        #self.tokens=tokenize.generate_all_tokens_by_line(self.val, self.lineno)

class Object :
    def __init__ ( self , val,  lineno):
        self.val=val
        self.lineno=lineno

class Class:
    '''Class to represent a Python class.'''
    def __init__(self, module, name, super, file, lineno):
        self.module = module
        self.name = name
        if super is None:
            super = []
        self.super = super
        self.methods = {}
        self.file = file
        self.lineno = lineno

    def _addmethod(self, name, lineno):
        self.methods[name] = lineno

    def Sort ( self, by='lineno' ):
        pass
        #if by=='lineno' :
            #self.


class Function:
    '''Class to represent a top-level Python function'''
    def __init__(self, module, name, file, lineno):
        self.module = module
        self.name = name
        self.file = file
        self.lineno = lineno

class File :
    def __init__ ( self , path, lines=[]):
        self.path=path
        #Object Dictionary
        self.objDict={}
        self.lines={}
        self.modules={}
        self.LinesToDic(lines)


    def LinesToDic ( self ,lines ):
        """Converts a list of lines to a dictionary of lines, resets the lines Dictionary"""
        self.lines={}
        for i in range(len(lines)) :
            self.AddLine(lines[i], i)

    def GetAncestors ( self, line, lineno ):
        "Returns a list of (class,indent) pairs with the ancestor information of a line"
        #Look for the ancestors of the previus line :
        if lineno==0 :
            stack=[]
        else:
            stack=self.lines[lineno-1].ancestors

        g=tokenize.generate_tokens_by_line(line, lineno)
        try:
            for tokentype, token, start, end, line in g:
                lineno, thisindent = start
                if token == DEDENT or token=='def' :
                    # close previous nested classes and defs
                    while stack and stack[-1][1] >= thisindent:
                        del stack[-1]
                if token == 'class':
                    # close previous nested classes and defs
                    while stack and stack[-1][1] >= thisindent:
                        del stack[-1]

                    tokentype, class_name, start, end, line = g.next()
                    if tokentype != NAME:
                        continue # Syntax error

                    stack.append((class_name, thisindent))
        except StopIteration:
            pass

        return stack

    def AnalizeLine ( self, line, lineno, ancestors=None ):
        """Examinee a line to generate its Browsing information"""

        #Construct a generator of tokens
        g=tokenize.generate_tokens_by_line(line, lineno)
        #Code Based in _readmodule From pyclbr.py
        module=""
        _modules=self.modules

        #Calculate the indent ancestors
        if ancestors != None:
            stack = ancestors # stack of (class, indent) pairs
        else:
            stack = self.GetAncestors(line, lineno)
        try:
            for tokentype, token, start, end, line in g:
                if token == 'def':
                    lineno, thisindent = start

                    tokentype, meth_name, start, end, line = g.next()
                    if tokentype != NAME:
                        continue # Syntax error
                    if stack:
                        class_name = stack[-1][0]
                        cur_class=self.objDict[class_name]
                        if isinstance(cur_class, Class):
                            # it's a method
                            cur_class._addmethod(meth_name, lineno)
                        # else it's a nested def
                    else:
                        # it's a function
                        #print "CB AddFunct" , meth_name, lineno
                        self.objDict[meth_name] = Function(module, meth_name, file, lineno)
                elif token == 'class':
                    lineno, thisindent = start

                    #_# close previous nested classes and defs
                    #_while stack and stack[-1][1] >= thisindent:
                        #_del stack[-1]

                    tokentype, class_name, start, end, line = g.next()
                    if tokentype != NAME:
                        continue # Syntax error
                    # parse what follows the class name
                    tokentype, token, start, end, line = g.next()
                    inherit = None
                    if token == '(':
                        names = [] # List of superclasses
                        # there's a list of superclasses
                        level = 1
                        super = [] # Tokens making up current superclass
                        while True:
                            tokentype, token, start, end, line = g.next()
                            if token in (')', ',') and level == 1:
                                n = "".join(super)
                                if n in self.objDict:
                                    # we know this super class
                                    n = self.objDict[n]
                                else:
                                    c = n.split('.')
                                    if len(c) > 1:
                                        # super class is of the form
                                        # module.class: look in module for
                                        # class
                                        m = c[-2]
                                        c = c[-1]
                                        if m in _modules:
                                            d = _modules[m]
                                            if c in d:
                                                n = d[c]
                                names.append(n)
                                super = []
                            if token == '(':
                                level += 1
                            elif token == ')':
                                level -= 1
                                if level == 0:
                                    break
                            elif token == ',' and level == 1:
                                pass
                            else:
                                super.append(token)
                        inherit = names
                    cur_class = Class(module, class_name, inherit, file, lineno)
                    self.objDict[class_name] = cur_class
                #_elif token == 'import' and start[1] == 0:
                    #_modules = _getnamelist(g)
                    #_for mod, mod2 in modules:
                        #_try:
                            #_# Recursively read the imported module
                            #_if not inpackage:
                                #__readmodule(mod, path)
                            #_else:
                                #_try:
                                    #__readmodule(mod, path, inpackage)
                                #_except ImportError:
                                    #__readmodule(mod, [])
                        #_except:
                            #_# If we can't find or parse the imported module,
                            #_# too bad -- don't die here.
                            #_pass
                #_elif token == 'from' and start[1] == 0:
                    #_mod, token = _getname(g)
                    #_if not mod or token != "import":
                        #_continue
                    #_names = _getnamelist(g)
                    #_try:
                        #_# Recursively read the imported module
                        #_d = _readmodule(mod, path, inpackage)
                    #_except:
                        #_# If we can't find or parse the imported module,
                        #_# too bad -- don't die here.
                        #_continue
                    #_# add any classes that were defined in the imported module
                    #_# to our name space if they were mentioned in the list
                    #_for n, n2 in names:
                        #_if n in d:
                            #_dict[n2 or n] = d[n]
                        #_elif n == '*':
                            #_# don't add names that start with _
                            #_for n in d:
                                #_if n[0] != '_':
                                    #_dict[n] = d[n]
        except StopIteration:
            pass
        return dict



    def AddLine ( self, val, lineNum ):
        """Adds a line to be procesed to this file"""
        if DEBUG :
            print "CB AddLine", self.path,  val, lineNum
        numLines=len(self.lines)
        ancestors=self.GetAncestors(val, lineNum)
        #Its beyond the end?
        if lineNum>=numLines :
            #Append
            self.lines[numLines]=Line(val, numLines, file=self, ancestors=ancestors)
        else:
            #Right Shift the lines
            for i in range(lineNum+1, numLines) :
                self.lines[i]=self.lines[i-1]
                self.lines[i].lineNum=i+1
            #Insert the new one
            self.lines[lineNum-1]=Line(val, numLines, file=self, ancestors=ancestors)
        self.AnalizeLine(val, lineNum, ancestors)
        #TODO INCREMENTARLAS  EN EL DICCIONARIO



class ClassBrowser :
    def __init__ ( self ):
        "File Dictionary"
        self.fileDic={}

    def AddFile ( self , file, lines=[] ):
        if DEBUG : print "CB addfile", file
        self.fileDic[file]=File(file, lines)

    def AddLine ( self , file, val, lineNum ):
        #The file is not yet in the Dictionary
        if file not in self.fileDic.keys() :
            self.AddFile(file)
        self.fileDic[file].AddLine(val, lineNum)

    def DelLine ( self ):
        pass

    def DelFile ( self, file ):
        if DEBUG : print "CB DelFile", file
        if file in self.fileDic :
            del self.fileDic[file]


    def GetObjChildrens ( self , sortBy="line"):
        pass
    def GetObjectDoc ( self , sortBy="line"):
        pass



def main ( ):
    clbr=ClassBrowser()

    txt="""
class A :
    def __init__ ( self ):
        self.line=[x for x in l]

def Ab ( ):
    pass
    """
    clbr.AddFile('hola.py', txt.split('\n'))
    #clbr.AddLine('hola.py', txt, 0)



if __name__=='__main__' :
    main()
