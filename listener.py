from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser

import myexceptions

import structure as st

class Listener(CoolListener):

    def __init__(self):
        self.currentKlassTypes = None
        self.baseKlasses = st.SymbolTable()
        self.allKlasses = st.SymbolTable()
        self.pending_new = []
        self.setBaseClasses()

    def exitProgram(self, ctx: CoolParser.ProgramContext):
        try:
            self.allKlasses['Main'].lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException

        for pending in self.pending_new:
            to_klass = st.lookupClass(pending['to'])
            klass = st.lookupClass(pending['type'])
            if not to_klass.conforms(klass):
                raise myexceptions.DoesNotConform

    def enterKlass(self, ctx: CoolParser.KlassContext):
        types = ctx.TYPE()

        klassName = types[0].getText()
        if klassName in self.baseKlasses:
            raise myexceptions.RedefineBasicClassException

        if len(types) > 1 and types[1].getText() in ['Bool', 'SELF_TYPE', 'String'] :
            raise myexceptions.InvalidInheritsException

        klass = st.Klass(klassName) if (len(types) == 1) else st.Klass(klassName, inherits=types[1].getText())
        self.currentKlassTypes = st.SymbolTableWithScopes(klass)
        self.allKlasses[klassName] = klass
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        if id == 'self':
            raise myexceptions.SelfVariableException
        
        self.currentKlassTypes[id] = _type

    def enterMethod(self, ctx: CoolParser.MethodContext):
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        self.currentKlassTypes.klass.addMethod(name, st.Method(_type))

        self.currentKlassTypes.openScope()

    def exitMethod(self, ctx: CoolParser.MethodContext):
        self.currentKlassTypes.closeScope()
    
    def enterFormal(self, ctx: CoolParser.FormalContext):
        id = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        if id == 'self':
            raise myexceptions.SelfVariableException
        
        if _type == 'SELF_TYPE':
            raise myexceptions.SelftypeInvalidUseException
        
        self.currentKlassTypes[id] = _type

    def enterLet(self, ctx: CoolParser.LetContext):
        ids = ctx.ID()
        types = ctx.TYPE()
        for i in range(len(ids)):
            if ids[i].getText() == 'self':
                raise myexceptions.SelfVariableException
            self.currentKlassTypes[ids[i]] = types[i]
        

    def enterAssign(self, ctx: CoolParser.AssignContext):
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException

    def enterNew(self, ctx: CoolParser.NewContext):
        to_id = ctx.parentCtx.ID().getText()
        # TODO: Search in symbols table this type from formal or let. Add in let or formal.
        to_type = self.currentKlassTypes[to_id]
        _type = ctx.TYPE().getText()
        self.pending_new.append({"type": _type, "to": to_type})
    
    def setBaseClasses(self):
        k = st.Klass('Object')
        k.addMethod('abort', st.Method('Object'))
        k.addMethod('type_name', st.Method('Object'))
        k.addMethod('copy', st.Method('SELF_TYPE'))
        self.baseKlasses['Object'] = k
        k = st.Klass('IO')
        k.addMethod('out_string', st.Method('SELF_TYPE', [('x', 'String')]))
        k.addMethod('out_int', st.Method('SELF_TYPE', [('x', 'Int')]))
        k.addMethod('in_string', st.Method('String'))
        k.addMethod('in_int', st.Method('Int'))
        self.baseKlasses['IO'] = k
        k = st.Klass('Int')
        self.baseKlasses['Int'] = k
        k = st.Klass('String')
        k.addMethod('length', st.Method('Int'))
        k.addMethod('concat', st.Method('String', [('s', 'String')]))
        k.addMethod('substr', st.Method('String', [('i', 'Int'), ('l', 'Int')]))
        self.baseKlasses['String'] = k
        k = st.Klass('Bool')
        self.baseKlasses['Bool'] = k
        k = st.Klass('SELF_TYPE')
        self.baseKlasses['SELF_TYPE'] = k
