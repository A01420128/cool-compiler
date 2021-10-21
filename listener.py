from typing import KeysView
from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser

import myexceptions

import structure as st

class Listener(CoolListener):

    def __init__(self):
        self.currentKlassTypes = None
        self.baseKlasses = st.SymbolTable()
        self.ctxTypes = st.SymbolTable()
        self.pending_new = []
        self.pending_attr = dict()
        self.pending_call = []

        # Reset st.classes so that it doesnt save other file klasses
        st._allClasses = {}
        # Add classes to st
        self.setBaseClasses()

    def exitProgram(self, ctx: CoolParser.ProgramContext):
        try:
            st.lookupClass('Main').lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException

        # Check if assignment by new conforms to inheritance.
        for pending in self.pending_new:
            to_klass = st.lookupClass(pending['to'])
            klass = st.lookupClass(pending['type'])
            if not to_klass.conforms(klass):
                raise myexceptions.DoesNotConform
            
        # Check if attributes are being overriden, attributes with same name and check klasses inheritance
        for klasses in self.pending_attr.values():
            for i in range(len(klasses)):
                for j in range(1, len(klasses)):
                    x = st.lookupClass(klasses[i])
                    y = st.lookupClass(klasses[j])
                    if x != y:
                        if x.conforms(y) or y.conforms(x):
                            raise  myexceptions.NotSupported

        # Check that parameters in calls to methods are conformant
        for call in self.pending_call:
            _klass = st.lookupClass(call['klass'])
            try:
                _method = _klass.lookupMethod(call['method'])
            except KeyError:
                raise myexceptions.MethodNotFound
            for i, _param_type in enumerate(_method.params.values()):
                _param_klass = st.lookupClass(_param_type)
                _called_klass = st.lookupClass(call['params_types'][i])
                if not _param_klass.conforms(_called_klass):
                    raise myexceptions.DoesNotConform



    def enterKlass(self, ctx: CoolParser.KlassContext):
        _types = ctx.TYPE()

        # Check if klass is redefining basic klasses
        klassName = _types[0].getText()
        if klassName in self.baseKlasses:
            raise myexceptions.RedefineBasicClassException

        # Check if klass has bad inherit type
        if len(_types) > 1 and _types[1].getText() in ['Bool', 'SELF_TYPE', 'String'] :
            raise myexceptions.InvalidInheritsException

        # Set inherits if it has two types in definition.
        klass = st.Klass(klassName) if (len(_types) == 1) else st.Klass(klassName, inherits=_types[1].getText())

        # Save klass and self
        self.currentKlassTypes = st.SymbolTableWithScopes(klass)
        self.currentKlassTypes['self'] = klassName   
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        # Attribute name cannot be self
        if id == 'self':
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

        # Save the attributes of a certain klass for future examination. (checking overriding)
        klass = self.currentKlassTypes.klass.name
        if id in self.pending_attr:
            self.pending_attr[id].append(klass)
        else:
            self.pending_attr[id] = [klass]
        
        self.currentKlassTypes[id] = _type

    def enterMethod(self, ctx: CoolParser.MethodContext):
        self.currentKlassTypes.openScope()

    def exitMethod(self, ctx: CoolParser.MethodContext):
        # Add method and its formals to the klass
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        _formals = ctx.formal()
        _params = []
        for _formal in _formals:
            _params.append((_formal.ID().getText(), self.ctxTypes[_formal]))
        self.currentKlassTypes.klass.addMethod(name, st.Method(_type, _params))
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
        self.ctxTypes[ctx] = _type
    
    def exitBase(self, ctx: CoolParser.BaseContext):
        # Type Rule: Pass child type
        _type = self.ctxTypes[ctx.getChild(0)]
        self.ctxTypes[ctx] = _type

    def enterLet(self, ctx: CoolParser.LetContext):
        ids = ctx.ID()
        types = ctx.TYPE()
        for i in range(len(ids)):
            # No id should be self
            if ids[i].getText() == 'self':
                raise myexceptions.SelfVariableException
            
            # Set expected type of id
            self.ctxTypes[ids[i]] = types[i].getText()
            # Add type of identifier for future checks
            self.currentKlassTypes[ids[i].getText()] = types[i].getText()

    def enterNew(self, ctx: CoolParser.NewContext):
        """
        # Save pending checks on assigning corresponing types
        if hasattr(ctx.parentCtx, 'ID'):
            to_id = ctx.parentCtx.ID()[0].getText()
            to_type = self.currentKlassTypes[to_id]
            _type = ctx.TYPE().getText()
            self.pending_new.append({"type": _type, "to": to_type})
        """
    
    def exitNew(self, ctx: CoolParser.NewContext):
        # Type Rule: Pass type in rule
        _type = ctx.TYPE().getText()
        self.ctxTypes[ctx] = _type

    def exitCall(self, ctx: CoolParser.CallContext):
        _id = ctx.ID().getText()
        _expr = ctx.expr()

        # If call comes from a base expression then the type can be infered from its id.
        if type(_expr[0]) is CoolParser.BaseContext:
            _klass = self.ctxTypes[_expr[0]]
            _params = []
            for i in range(1, len(_expr)):
                _param_type = self.ctxTypes[_expr[i]]
                _params.append(_param_type)
        
            self.pending_call.append({"klass": _klass, "method": _id, "params_types": _params})

        # If call comes from let ??
        if type(_expr[0]) is CoolParser.LetContext:
            _let = _expr[0]
            _caller = _let.getChild(_let.getChildCount()-1)
            _klass = self.ctxTypes[_caller]
            _params = []
            for i in range(1, len(_expr)):
                _param_type = self.ctxTypes[_expr[i]]
                _params.append(_param_type)
        
            self.pending_call.append({"klass": _klass, "method": _id, "params_types": _params})

            print(_expr[0])
        # Type Rule: TODO
        
    def enterAssign(self, ctx: CoolParser.AssignContext):
        # No id is self in assign
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException
    
    def exitAssign(self, ctx: CoolParser.AssignContext):
        # Save pending checks on assigning corresponing types
        to_id = ctx.ID().getText()
        to_type = self.currentKlassTypes[to_id]
        _expr = ctx.expr()
        _type = self.ctxTypes[_expr]
        self.pending_new.append({"type": _type, "to": to_type})

    def exitAdd(self, ctx: CoolParser.AddContext):
        # Type rule: both expr should be Int, pass Int
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (self.ctxTypes[_left] != 'Int' or self.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            self.ctxTypes[ctx] = 'Int'
    
    def exitParens(self, ctx: CoolParser.ParensContext):
        # Type rule: Pass expr context
        _type = self.ctxTypes[ctx.expr()]
        self.ctxTypes[ctx] = _type
    
    def exitInteger(self, ctx: CoolParser.IntegerContext):
        # Type rule: Pass 'Int'
        self.ctxTypes[ctx] = 'Int'
    
    def exitString(self, ctx: CoolParser.StringContext):
        # Type rule: Pass 'String'
        self.ctxTypes[ctx] = 'String'
    
    def exitBool(self, ctx: CoolParser.BoolContext):
        # Type rule: Pass 'Bool'
        self.ctxTypes[ctx] = 'Bool'
    
    def exitObject(self, ctx: CoolParser.ObjectContext):
        # Type rule: Pass type of ID
        _id = ctx.ID().getText()
        _type = self.currentKlassTypes[_id]
        # TODO: Not entered id : type
        self.ctxTypes[ctx] = _type
        
    
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
