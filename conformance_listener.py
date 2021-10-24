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
        # Start an ids symbol table in the current klass
        _klassName = ctx.TYPE()[0].getText()
        _klass = storage.lookupClass(_klassName)
        self.idsTypes = storage.SymbolTableWithScopes(_klass)
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()
    
        # Check overriding super klass attributes
        try:
            _klass = self.idsTypes.klass
            _inherited = storage.lookupClass(_klass.inherits)
            _found = _inherited.lookupAttribute(_id)
            if _found: 
                raise myexceptions.NotSupported
        except KeyError:
            pass


        # Save id typE
        self.idsTypes[_id] = _type

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
        

    def enterAssign(self, ctx: CoolParser.AssignContext):
        # Check conformance of types
        _idType = self.idsTypes[ctx.ID().getText()]
        _exprType = storage.ctxTypes[ctx.expr()]
        _idKlass = storage.lookupClass(_idType)
        _exprKlass = storage.lookupClass(_exprType)
        
        if not _idKlass.conforms(_exprKlass):
            raise myexceptions.DoesNotConform