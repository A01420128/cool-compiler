import enum
import math
from antlr4 import *
from antlr.CoolLexer import *
from antlr.CoolParser import *
from antlr.CoolListener import *

import sys
from string import Template
import asm

from klass_listener import KlassListener
from conformance_listener import ConformanceListener
import structure as storage

BOO_TAG = 3
INT_TAG = 4
STR_TAG = 5

class Output:
    def __init__(self):
        self.accum = ''

    def p(self, *args):
        '''
        Si tiene un argumento es una etiqueta
        '''
        if len(args) == 1:
            self.accum += '%s:\n' % args[0]
            return

        '''
        Si tiene más, indenta el primero y los demás los separa con espacios
        '''
        r = '    %s    ' % args[0]        
        for a in args[1:-1]:
            r += ' %s' % str(a)

        if type(args[-1]).__name__ != 'int' and args[-1][0] == '#':
            for i in range(64 - len(r)):
                r += ' '
        r += str(args[-1])

        self.accum += r + '\n'

    def out(self):
        return self.accum

def global_data(o):
        k = dict(intTag=INT_TAG, boolTag=BOO_TAG, stringTag=STR_TAG)
        o.accum = asm.gdStr1 + asm.gdTpl1.substitute(k) + asm.gdStr2

def constants(o):
    """
    1. Determinar literales string
        1.1 Obtener lista de literales (a cada una asignar un índice) + nombres de las clases
        1.2 Determinar constantes numéricas necesarias
        1.3 Reemplazar en el template:
            - tag
            - tamanio del objeto: [tag, tamanio, ptr al dispTab, ptr al int, (len(contenido)+1)%4] = ? 
                (el +1 es por el 0 en que terminan siempre)
            - índice del ptr al int
            - valor (el string)
    2. Determinar literales enteras
        2.1 Literales necesarias en el punto 1
        2.2 + constantes en el código fuente
        2.3 Remplazar en el template:
            - tag
            - tamanio del objeto: [tag, tamanio, ptr al dispTab y contenido] = 4 words
            - valor
    """

    ### POR EJEMPLO (CAMBIAR)
    # o.accum += asm.cTplStr.substitute(idx=3, tag=2, size=23, sizeIdx=2, value='hola mundo')
    # o.accum += asm.cTplInt.substitute(idx=5, tag=12, value=340)

    used_int_size = dict()
    used_int_idx = 0
    for i, s in enumerate(reversed(storage.stringConst)):
        str_obj_size = 4 + math.ceil((len(s) + 1) / 4)
        str_size = len(s)

        # Setting the int that is saved for the string size
        this_int_idx = used_int_size[str_size] if str_size in used_int_size else used_int_idx
        if str_size not in used_int_size:
            used_int_size[str_size] = used_int_idx
            used_int_idx += 1

        o.accum += asm.cTplStr.substitute(idx=i, tag=STR_TAG, size=str_obj_size, sizeIdx=this_int_idx, value=s)
    
    for _int in storage.intConst:
        if _int not in used_int_size:
            used_int_idx += 1
            used_int_size[_int] = used_int_idx

    for k, v in used_int_size.items():
        o.accum += asm.cTplInt.substitute(idx=v, tag=INT_TAG, value=k)

    # Siempre incluir los bool
    o.accum += asm.boolStr


def tables(o):
    """
    1. class_nameTab: tabla para los nombres de las clases en string
        1.1 Los objetos ya fueron generados arriba
        1.2 El tag de cada clase indica el desplazamiento desde la etiqueta class_nameTab
    2. class_objTab: prototipos (templates) y constructores para cada objeto
        2.1 Indexada por tag: en 2*tag está el protObj, en 2*tag+1 el init
    3. dispTab para cada clase
        3.1 Listado de los métodos en cada clase considerando herencia
"""
    #Ejemplo (REEMPLAZAR):

    o.p('class_nameTab')
    o.p('.word', 'str_const3')

    o.p('class_objTab')
    o.p('.word', 'Object_protObj')
    o.p('.word', 'Object_init') 

    o.p('Object_dispTab')
    o.p('.word', 'Object.abort')
    o.p('.word', 'Object.type_name')
    o.p('.word', 'Object.copy')
    
def templates(o):
    """
    El template o prototipo para cada objeto (es decir, de donde new copia al instanciar)
    1. Para cada clase generar un objeto, poner atención a:
        - nombre
        - tag
        - tamanio [tag, tamanio, dispTab, atributos ... ] = ?
            Es decir, el tamanio se calcula en base a los atributos + 3, por ejemplo 
                Int tiene 1 atributo (el valor) por lo que su tamanio es 3+1
                String tiene 2 atributos (el tamanio y el valor (el 0 al final)) por lo que su tamanio es 3+2
        - dispTab
        - atributos
"""
    # Ejemplo: nombre=Object, tag->0, tamanio=3, atributos=no tiene
    o.accum += """
    .word   -1 
Object_protObj:
    .word   0 
    .word   3 
    .word   Object_dispTab 
"""
    # Ejemplo: nombre=String, tag->4, tamanio=5, atributos=int ptr, 0
    o.accum += """
    .word   -1 
String_protObj:
    .word   4 
    .word   5 
    .word   String_dispTab 
    .word   int_const0 
    .word   0 
"""

def heap(o):
    o.accum += asm.heapStr

def global_text(o):
    o.accum += asm.textStr

def class_inits(o):
    pass


def genCode():
    o = Output()
    global_data(o)
    constants(o)
    tables(o)
    templates(o)
    heap(o)
    global_text(o)

    # Aquí enviar a un archivo, etc.
    print(o.out())
    
if __name__ == '__main__':
    # Ejecutar como: "python codegen.py <filename>" donde filename es el nombre de alguna de las pruebas
    parser = CoolParser(CommonTokenStream(CoolLexer(FileStream("resources/codegen/input/fact.cool"))))
    #parser = CoolParser(CommonTokenStream(CoolLexer(FileStream("resources/codegen/input/%s.cool" % sys.argv[1]))))
    # parser = CoolParser(CommonTokenStream(CoolLexer(FileStream("resources/codegen/input/%s.cool" % ("abort")))))
    walker = ParseTreeWalker()
    tree = parser.program()

    walker.walk(KlassListener(), tree)
    walker.walk(ConformanceListener(), tree)

    # Poner aquí los listeners necesarios para reeorrer el árbol y obtener los datos
    # que requiere el generador de código
    #walker.walk(Listener1(), tree)
    #walker.walk(Listener2(), tree)

    # Pasar parámetros al generador de código 
    genCode()