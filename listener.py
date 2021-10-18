from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser

import myexceptions

from structure import Method, SymbolTable, Klass, setBaseClasses

class Listener(CoolListener):

    def __init__(self):
        self.currentKlass = None
        self.baseKlasses = SymbolTable()
        self.setBaseClasses()

    def enterKlass(self, ctx: CoolParser.KlassContext):
        className = ctx.TYPE()[0].getText()
        if className in self.baseKlasses:
            raise myexceptions.RedefineBasicClassException

        klass = Klass(className)
        self.currentKlass = klass
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfVariableException

    def enterMethod(self, ctx: CoolParser.MethodContext):
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        self.currentKlass.addMethod(name, Method(_type))

    def exitKlass(self, ctx: CoolParser.KlassContext):
        try:
            self.currentKlass.lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException()
    
    def setBaseClasses(self):
        k = Klass('Object')
        k.addMethod('abort', Method('Object'))
        k.addMethod('type_name', Method('Object'))
        k.addMethod('copy', Method('SELF_TYPE'))
        self.baseKlasses['Object'] = k
        k = Klass('IO')
        k.addMethod('out_string', Method('SELF_TYPE', [('x', 'String')]))
        k.addMethod('out_int', Method('SELF_TYPE', [('x', 'Int')]))
        k.addMethod('in_string', Method('String'))
        k.addMethod('in_int', Method('Int'))
        self.baseKlasses['IO'] = k
        k = Klass('Int')
        self.baseKlasses['Int'] = k
        k = Klass('String')
        k.addMethod('length', Method('Int'))
        k.addMethod('concat', Method('String', [('s', 'String')]))
        k.addMethod('substr', Method('String', [('i', 'Int'), ('l', 'Int')]))
        self.baseKlasses['String'] = k
        k = Klass('Bool')
        self.baseKlasses['Bool'] = k
