from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser

import myexceptions

import structure as storage

# All types should be saved in the klass listener,
# this one just checks for conformance.
class ConformanceListener(CoolListener):

    def __init__(self):
        self.idsTypes = None

    def enterKlass(self, ctx: CoolParser.KlassContext):
        _types = ctx.TYPE()

        # Start an ids symbol table in the current klass
        _klassName = ctx.TYPE()[0].getText()
        _klass = storage.lookupClass(_klassName)

        # Now we deal with inheritance
        if len(_types) > 1:
            _inherit = _types[1].getText()
            if _inherit in ['Bool', 'SELF_TYPE', 'String']:
                raise myexceptions.InvalidInheritsException
            
            # Save previous attributes and methods
            _prev_attr = _klass.attributes
            _prev_methods = _klass.methods

            # Save same klass but now with inheritance
            # Check that the inherited klass exists.
            try:
                storage.Klass(_klassName, inherits=_inherit)
            except KeyError:
                raise myexceptions.TypeNotFound

            _new_klass = storage.lookupClass(_klassName)
            _new_klass.attributes = _prev_attr
            _new_klass.methods = _prev_methods
            _klass = _new_klass

        self.idsTypes = storage.SymbolTableWithScopes(_klass)
        self.idsTypes.openScope()
    
    def exitKlass(self, ctx: CoolParser.KlassContext):
        self.idsTypes.closeScope()
    
    def enterMethod(self, ctx: CoolParser.MethodContext):
        self.idsTypes.openScope()
    
    def exitMethod(self, ctx: CoolParser.MethodContext):
        _expr = ctx.expr() 
        _type = ctx.TYPE().getText()

        # Check if methods expects a SELF_TYPE
        if _type == 'SELF_TYPE':
            # SELF_TYPE sets type to the current klass, no matter if its inherited
            _type = self.idsTypes.klass.name
            # SELF_TYPE requires a dynamic expr type
            if storage.ctxTypes[_expr] != 'self':
                raise myexceptions.TypeCheckMismatch
        else:
            # Check that the result of the method conforms to its type and that the types exist
            try:
                _exprKlass = storage.lookupClass(storage.ctxTypes[_expr])
                _typeKlass = storage.lookupClass(_type)
            except KeyError:
                raise myexceptions.TypeNotFound

            if not _typeKlass.conforms(_exprKlass):
                raise myexceptions.DoesNotConform
        
        self.idsTypes.closeScope()
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()
    
        # Check overriding super klass attributes
        try:
            _klass = self.idsTypes.klass
            _inherited = storage.lookupClass(_klass.inherits)
            _found = _inherited.lookupAttribute(_id)
            if _found != _type:
                raise myexceptions.NotSupported
        except KeyError:
            pass

        # Save id typE
        self.idsTypes[_id] = _type
    
    def exitIf(self, ctx: CoolParser.IfContext):
        # Type Rule: The union of the two branches
        _trueType = storage.ctxTypes[ctx.expr()[1]]
        _falseType = storage.ctxTypes[ctx.expr()[2]]

        _trueKlass = storage.lookupClass(_trueType)
        _falseKlass = storage.lookupClass(_falseType)
        _union = _trueKlass.union(_falseKlass)

        storage.ctxTypes[ctx] = _union

    def enterLet(self, ctx: CoolParser.LetContext):
        _types = ctx.TYPE()
        _expr = ctx.expr()

        # Check conformance of every saved expected type and its expression asigned.
        for i, _type in enumerate(_types):
            _assign = storage.lookupClass(storage.ctxTypes[_expr[i]])
            _to = storage.lookupClass(_type.getText())
            if not _to.conforms(_assign):
                raise myexceptions.DoesNotConform
    
    def exitBlock(self, ctx: CoolParser.BlockContext):
        # Type Rule: Pass type of last expr
        _expr = ctx.expr()
        _last = storage.ctxTypes[_expr[len(_expr) - 1]]
        storage.ctxTypes[ctx] = _last
        

    def exitCall(self, ctx: CoolParser.CallContext):
        _id = ctx.ID().getText()
        _expr = ctx.expr()

        # Check what type of call it is, from internal or external klass
        _klassName = None
        _starter = ctx.getChild(1).getText()
        _starter_expr = -1 # Whether the first expresion is an argument or not
        if _starter == '.':
            _starter_expr = 1

            # If it comes from a base klass only get it based on the ctx type
            if type(_expr[0]) is CoolParser.BaseContext:
                _klassName = storage.ctxTypes[_expr[0]]
            
            # If it comes from a let klass get it from the type of the last expression
            if type(_expr[0]) is CoolParser.LetContext:
                _let = _expr[0]
                _caller = _let.getChild(_let.getChildCount() - 1) # Last expr in let
                _klassName = storage.ctxTypes[_caller]
            
        elif _starter == '(':
            _starter_expr = 0
            # It is calling a method inside that klass
            _klassName = self.idsTypes.klass.name

        # Lookup klass in storage
        _klass = storage.lookupClass(_klassName)
            
        # Check that that klass has that method
        _method = None
        try:
            _method = _klass.lookupMethod(_id)
        except KeyError:
            raise myexceptions.MethodNotFound
        
        # Check that all parameters inserted conform to expected types
        _method = _klass.lookupMethod(_id)
        for i, _expected_type in enumerate(_method.params.values()):
            _inserted_type = storage.ctxTypes[_expr[_starter_expr + i]]

            # Catch self types
            if _inserted_type == 'self':
                _inserted_type = self.idsTypes.klass.name

            # Method calls with badmethodcallsitself
            # Test4 y test6 de etapa2 evaluan que los argumentos sean del mismo tipo
            # esto hace que las exceptiones arrojadas sean diferentes, por eso hacemos
            # este if para ver cuando se esta llamando el mismo methodo que da diferente tipo
            if (_inserted_type == _method.type 
                and type(_expr[_starter_expr + i]) is CoolParser.CallContext
                and _expected_type != _inserted_type):
                raise myexceptions.CallTypeCheckMismatch

            # Method calls with argument that does not conform with expected
            # Esta evaluacion es mucho mejor porque no solo evalua que sean el mismo tipo sino
            # que tambien los subtipos conforman
            if not storage.lookupClass(_expected_type).conforms(storage.lookupClass(_inserted_type)):
                raise myexceptions.DoesNotConform
        
        # Type Rule: The type for the method called
        storage.ctxTypes[ctx] = _method.type
        
    def exitAt(self, ctx: CoolParser.AtContext):
        _expr = ctx.expr()
        _type = ctx.TYPE()

        # Catch self types
        _leftType = storage.ctxTypes[_expr[0]]
        if _leftType == 'self':
            _leftType = self.idsTypes.klass.name

        _left = storage.lookupClass(_leftType)
        _right = storage.lookupClass(_type.getText())

        # Rigth should conform left.
        if not _right.conforms(_left):
            raise myexceptions.MethodNotFound


    def enterAssign(self, ctx: CoolParser.AssignContext):
        # Check conformance of types
        _idType = self.idsTypes[ctx.ID().getText()]
        _exprType = storage.ctxTypes[ctx.expr()]
        _idKlass = storage.lookupClass(_idType)
        _exprKlass = storage.lookupClass(_exprType)
        
        if not _idKlass.conforms(_exprKlass):
            raise myexceptions.DoesNotConform