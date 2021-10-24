from typing import KeysView
from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser

import myexceptions

import structure as storage

class KlassListener(CoolListener):

    def __init__(self):
        self.currentKlassTypes = None
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
        _types = ctx.TYPE()

        # Check if klass is redefining basic klasses
        klassName = _types[0].getText()
        if klassName in self.baseKlasses:
            raise myexceptions.RedefineBasicClassException

        # Check if klass inherits or not
        _klass = None
        if len(_types) > 1:
            _inherit= _types[1].getText()
            if _inherit in ['Bool', 'SELF_TYPE', 'String']:
                raise myexceptions.InvalidInheritsException
            
            # Save klass in store
            _klass =storage.Klass(klassName, inherits=_inherit)
        else:
            _klass = storage.Klass(klassName)
        
        # Save current klass
        self.currentKlassTypes = storage.SymbolTableWithScopes(_klass)
        self.currentKlassTypes['self'] = klassName   
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        # Attribute name cannot be self
        if _id == 'self':
            raise myexceptions.SelfVariableException

        # An attributed cant be assigned an uknown variable.
        expr = ctx.expr()
        if expr:
            if hasattr(expr.getChild(0), 'ID'):
                expr_id = expr.getChild(0).ID().getText()
                try:
                    self.currentKlassTypes[expr_id]
                except KeyError as e:
                    raise myexceptions.UndeclaredIdentifier

        self.currentKlassTypes.klass.addAttribute(_id, _type)
        self.currentKlassTypes[_id] = _type

    def enterMethod(self, ctx: CoolParser.MethodContext):
        storage.ctxTypes[ctx] = ctx.TYPE().getText()
        self.currentKlassTypes.openScope()

    def exitMethod(self, ctx: CoolParser.MethodContext):
        # Add method and its formals to the current klass
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        _formals = ctx.formal()
        _params = []
        for _formal in _formals:
            _params.append((_formal.ID().getText(), storage.ctxTypes[_formal]))
        self.currentKlassTypes.klass.addMethod(name, storage.Method(_type, _params))
        self.currentKlassTypes.closeScope()
    
    def enterFormal(self, ctx: CoolParser.FormalContext):
        id = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        if id == 'self':
            raise myexceptions.SelfVariableException
        
        if _type == 'SELF_TYPE':
            raise myexceptions.SelftypeInvalidUseException
        
        self.currentKlassTypes[id] = _type
    
    def exitFormal(self, ctx: CoolParser.FormalContext):
        # Type rule: Pass TYPE()
        _type = ctx.TYPE().getText()
        storage.ctxTypes[ctx] = _type
    
    def exitBase(self, ctx: CoolParser.BaseContext):
        # Type Rule: Pass child type
        _type = storage.ctxTypes[ctx.getChild(0)]
        storage.ctxTypes[ctx] = _type

    def enterLet(self, ctx: CoolParser.LetContext):
        _ids = ctx.ID()
        _types = ctx.TYPE()
        for i in range(len(_ids)):

            # No id should be self
            if _ids[i].getText() == 'self':
                raise myexceptions.SelfVariableException
            
            # Set expected type of id
            storage.ctxTypes[_ids[i]] = _types[i].getText()
            # Add type of identifier for future checks
            self.currentKlassTypes[_ids[i].getText()] = _types[i].getText()
    
    def exitNew(self, ctx: CoolParser.NewContext):
        # Type Rule: Pass type in rule
        _type = ctx.TYPE().getText()
        storage.ctxTypes[ctx] = _type
        
    def exitEq(self, ctx: CoolParser.EqContext):
        # Type rule: compare freely except if type Int, String or Bool, compare to same.
        _expr = ctx.expr()
        _left = storage.ctxTypes[_expr[0]]
        _right = storage.ctxTypes[_expr[1]]
        _except = ['Int', 'String', 'Bool']
        if _left in _except or _right in _except:
            if _left != _right:
                raise myexceptions.TypeCheckMismatch

        storage.ctxTypes[ctx] = 'Bool'

    def exitAdd(self, ctx: CoolParser.AddContext):
        # Type rule: both expr should be Int, pass Int
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'

    def enterAssign(self, ctx: CoolParser.AssignContext):
        # No id is self in assign
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException
    
    def exitParens(self, ctx: CoolParser.ParensContext):
        # Type rule: Pass expr context
        _type = storage.ctxTypes[ctx.expr()]
        storage.ctxTypes[ctx] = _type
    
    def exitInteger(self, ctx: CoolParser.IntegerContext):
        # Type rule: Pass 'Int'
        storage.ctxTypes[ctx] = 'Int'
    
    def exitString(self, ctx: CoolParser.StringContext):
        # Type rule: Pass 'String'
        storage.ctxTypes[ctx] = 'String'
    
    def exitBool(self, ctx: CoolParser.BoolContext):
        # Type rule: Pass 'Bool'
        storage.ctxTypes[ctx] = 'Bool'
    
    def exitObject(self, ctx: CoolParser.ObjectContext):
        # Type rule: Pass type of ID
        _id = ctx.ID().getText()
        _type = self.currentKlassTypes[_id]
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
