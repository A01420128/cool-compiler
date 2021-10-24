from typing import KeysView
from unittest.main import main
from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser

import myexceptions

import structure as storage

class KlassListener(CoolListener):

    def __init__(self):
        self.currentKlass = None
        self.baseKlasses = storage.SymbolTable()

        # Reset st.classes so that it doesnt save other file klasses
        storage.allClasses = {}
        storage.ctxTypes = storage.SymbolTable()

        # Add classes to st
        self.setBaseClasses()

    def exitProgram(self, ctx: CoolParser.ProgramContext):
        try:
            storage.lookupClass('Main').lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException

    def enterKlass(self, ctx: CoolParser.KlassContext):
        _klassName = ctx.TYPE()[0].getText()

        # Check if klass is redefining basic klasses
        if _klassName in self.baseKlasses:
            raise myexceptions.RedefineBasicClassException

        # Check if klass is being redifined
        try:
            _klass = storage.lookupClass(_klassName)
            if _klass:
                raise myexceptions.ClassRedefinition
        except KeyError:
            pass

        # Inheritance is dealt in conformance listener
        _klass = storage.Klass(_klassName)

        # Save current klass
        self.currentKlass = _klass
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        # Attribute name cannot be self
        if _id == 'self':
            raise myexceptions.SelfVariableException

        self.currentKlass.addAttribute(_id, _type)

    def enterMethod(self, ctx: CoolParser.MethodContext):
        storage.ctxTypes[ctx] = ctx.TYPE().getText()

    def exitMethod(self, ctx: CoolParser.MethodContext):
        # Add method and its formals to the current klass
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        _formals = ctx.formal()
        _params = []
        for _formal in _formals:
            _params.append((_formal.ID().getText(), storage.ctxTypes[_formal]))
        self.currentKlass.addMethod(name, storage.Method(_type, _params))
    
    def exitFormal(self, ctx: CoolParser.FormalContext):
        # Type rule: Pass TYPE()
        _type = ctx.TYPE().getText()
        storage.ctxTypes[ctx] = _type
    
    def setBaseClasses(self):
        k = storage.Klass('Object')
        k.addMethod('abort', storage.Method('Object'))
        k.addMethod('type_name', storage.Method('Object'))
        k.addMethod('copy', storage.Method('SELF_TYPE'))
        self.baseKlasses['Object'] = k
        k = storage.Klass('IO')
        k.addMethod('out_string', storage.Method('SELF_TYPE', [('x', 'String')]))
        k.addMethod('out_int', storage.Method('SELF_TYPE', [('x', 'Int')]))
        k.addMethod('in_string', storage.Method('String'))
        k.addMethod('in_int', storage.Method('Int'))
        self.baseKlasses['IO'] = k
        k = storage.Klass('Int')
        self.baseKlasses['Int'] = k
        k = storage.Klass('String')
        k.addMethod('length', storage.Method('Int'))
        k.addMethod('concat', storage.Method('String', [('s', 'String')]))
        k.addMethod('substr', storage.Method('String', [('i', 'Int'), ('l', 'Int')]))
        self.baseKlasses['String'] = k
        k = storage.Klass('Bool')
        self.baseKlasses['Bool'] = k
        k = storage.Klass('SELF_TYPE')
        self.baseKlasses['SELF_TYPE'] = k
