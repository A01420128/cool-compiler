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

    # Tracking the necessary int constants for representing the size of the following strings
    used_int_size = dict()
    used_int_size[0] = 0
    used_int_idx = 1

    # Adding all clases names as strings
    # getting top index
    storage.all_classes_names = list(filter(lambda name: name != 'SELF_TYPE', storage.allClasses.keys())) # Remove SELF_TYPE, remnant of bad semantic?
    top_idx = (len(storage.stringConst) - 1) + len(storage.all_classes_names)
    for class_name in storage.all_classes_names:
        str_obj_size = 4 + math.ceil((len(class_name) + 1) / 4)
        str_size = len(class_name)

        # Setting the int that is saved for the string size
        this_int_idx = used_int_size[str_size] if str_size in used_int_size else used_int_idx
        if str_size not in used_int_size:
            used_int_size[str_size] = used_int_idx
            used_int_idx += 1

        o.accum += asm.cTplStr.substitute(idx=top_idx, tag=STR_TAG, size=str_obj_size, sizeIdx=this_int_idx, value=class_name)
        storage.str_const_tags.append(f'str_const{top_idx}')
        top_idx -= 1


    # Adding all strings
    for i, s in reversed(list(enumerate(storage.stringConst))):
        str_obj_size = 4 + math.ceil((len(s) + 1) / 4)
        str_size = len(s)

        # Setting the int that is saved for the string size
        this_int_idx = used_int_size[str_size] if str_size in used_int_size else used_int_idx
        if str_size not in used_int_size:
            used_int_size[str_size] = used_int_idx
            used_int_idx += 1

        o.accum += asm.cTplStr.substitute(idx=i, tag=STR_TAG, size=str_obj_size, sizeIdx=this_int_idx, value=s)
    
    # Adding all ints from storage
    for _int in storage.intConst:
        if _int not in used_int_size:
            used_int_size[_int] = used_int_idx
            used_int_idx += 1

    # Adding ints from storage and the ones used by strings
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

    # Agarrar todas las clases, guardar strings de nombres.
    # guardar en array donde quedaron esos nombres
    # for c in dict: .word all

    o.p('class_nameTab')
    for str_const in storage.str_const_tags:
        o.p('.word', str_const)

    o.p('class_objTab')
    for class_name in storage.all_classes_names:
        o.p('.word', f'{class_name}_protObj')
        o.p('.word', f'{class_name}_init') 

    for class_name in storage.all_classes_names:
        _class = storage.lookupClass(class_name)
        o.p(f'{class_name}_dispTab')
        # Get all inherited classes and methods
        inheritance_seq = [_class]
        inherit_from = _class
        while inherit_from.name != 'Object':
            inherit_from = storage.lookupClass(inherit_from.inherits)
            inheritance_seq.append(inherit_from)

        # Add all methods from the inheritance sequence
        for inherited in reversed(inheritance_seq):
            for method in inherited.methods:
                o.p('.word', f'{inherited.name}.{method}')
    
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
    class_prot_order = ['Object', 'IO', 'Main', 'Bool', 'Int', 'String']
    t = '    ' # Custom tab
    for _class_name in storage.all_classes_names:
        if _class_name not in class_prot_order:
            class_prot_order.append(_class_name)
        
    for i, _class_name in enumerate(class_prot_order):
        _class = storage.lookupClass(_class_name)
        prot_size = 3 + len(_class.attributes.keys())
        to_accum = f'{t}.word{t}-1\n{_class.name}_protObj:\n{t}.word{t}{i}\n{t}.word{t}{prot_size}\n{t}.word{t}{_class_name}_dispTab\n'
        if (_class_name == 'String'):
            to_accum += f'{t}.word{t}int_const0\n{t}.word{t}0\n'
        else:
            for _atr in _class.attributes.keys():
                to_accum += f'{t}.word{t}0\n' # Inserting void in not know attributes
    
        o.accum += to_accum


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