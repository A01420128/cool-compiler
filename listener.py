from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser

import myexceptions

from structure import Method, SymbolTable, Klass

class Listener(CoolListener):

    def __init__(self):
        self.currentKlass = None
        self.baseKlasses = SymbolTable()
        self.allKlasses = SymbolTable()
        self.setBaseClasses()

    def exitProgram(self, ctx: CoolParser.ProgramContext):
        try:
            self.allKlasses['Main'].lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException

    def enterKlass(self, ctx: CoolParser.KlassContext):
        types = ctx.TYPE()

        klassName = types[0].getText()
        if klassName in self.baseKlasses:
            raise myexceptions.RedefineBasicClassException

        if len(types) > 1 and types[1].getText() in ['Bool', 'SELF_TYPE', 'String'] :
            raise myexceptions.InvalidInheritsException

        klass = Klass(klassName)
        self.currentKlass = klass
        self.allKlasses[klassName] = klass
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfVariableException

    def enterMethod(self, ctx: CoolParser.MethodContext):
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        self.currentKlass.addMethod(name, Method(_type))
    
    def enterFormal(self, ctx: CoolParser.FormalContext):
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfVariableException
        
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise myexceptions.SelftypeInvalidUseException

    def enterLet(self, ctx: CoolParser.LetContext):
        ids = ctx.ID()
        for id  in ids:
            if id.getText() == "self":
                raise myexceptions.SelfVariableException

    def enterAssign(self, ctx: CoolParser.AssignContext):
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException
    
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
        k = Klass('SELF_TYPE')
        self.baseKlasses['SELF_TYPE'] = k
