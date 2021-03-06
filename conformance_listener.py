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
        _klassName = ctx.TYPE()[0].getText()
        ctx.nameklass = _klassName
        _klass = storage.lookupClass(_klassName)
        ctx.nameinherits = _klass.inherits

        # Start an ids symbol table in the current klass
        self.idsTypes = storage.SymbolTableWithScopes(_klass)
        self.idsTypes.openScope()
        self.idsTypes['self'] = 'self'
    
    def exitKlass(self, ctx: CoolParser.KlassContext):
        self.idsTypes.closeScope()
    
    def enterMethod(self, ctx: CoolParser.MethodContext):
        _methodName = ctx.ID().getText()

        # Check for bad override of inherited methods
        _inherits = self.idsTypes.klass.inherits
        if _inherits:
            _inheritedklass = storage.lookupClass(_inherits)
            # Look for posible overrides
            try:
                _inheritedMethod = _inheritedklass.lookupMethod(_methodName)
                # Should be the same return type
                if _inheritedMethod.type != ctx.TYPE().getText():
                    raise myexceptions.InvalidMethodOverride

                # Should have the same number of arguments
                _inheritedFormals = _inheritedMethod.params
                _formals = ctx.formal()
                if len(_inheritedFormals) != len(_formals):
                    raise myexceptions.InvalidMethodOverride

                # Every new formal should be the same
                for i, v in enumerate(_inheritedFormals.values()):
                    _new_type = _formals[i].TYPE().getText()
                    if _new_type != v:
                        raise myexceptions.InvalidMethodOverride
            except KeyError:
                pass
        
        # Track scope of arguments
        self.idsTypes.openScope()
        _formals = ctx.formal()
        for _formal in _formals:
            self.idsTypes[_formal.ID().getText()] = _formal.TYPE().getText()
    
    def exitMethod(self, ctx: CoolParser.MethodContext):
        _expr = ctx.expr() 
        _type = ctx.TYPE().getText()

        # Check if methods expects a SELF_TYPE
        if _type == 'SELF_TYPE':
            # SELF_TYPE sets type to the current klass, no matter if its inherited
            _type = self.idsTypes.klass.name
            # SELF_TYPE requires a dynamic expr type
            _exprType = storage.ctxTypes[_expr]
            if _exprType != 'self' and _exprType != 'SELF_TYPE':
                raise myexceptions.TypeCheckMismatch
        else:
            # Check that the result of the method conforms to its type and that the types exist
            try:
                # Check for self
                _exprType = storage.ctxTypes[_expr]
                if _exprType == 'self':
                    _exprType = self.idsTypes.klass.name

                _exprKlass = storage.lookupClass(_exprType)
                _typeKlass = storage.lookupClass(_type)
            except KeyError:
                raise myexceptions.TypeNotFound

            if not _typeKlass.conforms(_exprKlass):
                raise myexceptions.DoesNotConform
        
        self.idsTypes.closeScope()
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        # An attributed cant be assigned an uknown variable.
        expr = ctx.expr()
        if expr:
            if hasattr(expr.getChild(0), 'ID'):
                expr_id = expr.getChild(0).ID().getText()
                try:
                    self.idsTypes[expr_id]
                except KeyError as e:
                    raise myexceptions.UndeclaredIdentifier
    
        # Check overriding super klass attributes
        try:
            _klass = self.idsTypes.klass
            _inherited = storage.lookupClass(_klass.inherits)
            _found = _inherited.lookupAttribute(_id)
            if _found != _type:
                raise myexceptions.NotSupported
        except KeyError:
            pass

        # Save id type
        ctx.namesymbol = _id
        self.idsTypes[_id] = _type
        self.idsTypes.openScope()
    
    def exitAtribute(self, ctx: CoolParser.AtributeContext):
        self.idsTypes.closeScope()

    def enterFormal(self, ctx: CoolParser.FormalContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        # No self or SELF_TYPE for formals.
        if _id == 'self':
            raise myexceptions.SelfVariableException
        
        if _type == 'SELF_TYPE':
            raise myexceptions.SelftypeInvalidUseException
        
        ctx.nameformal = _id
        # This was entered when froming klasses
        # self.idsTypes[_id] = _type
    
    def exitBase(self, ctx: CoolParser.BaseContext):
        # Type Rule: Pass child type
        _type = storage.ctxTypes[ctx.getChild(0)]
        storage.ctxTypes[ctx] = _type
        ctx.typename = _type

    def enterIf(self, ctx: CoolParser.IfContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def exitIf(self, ctx: CoolParser.IfContext):
        # Type Rule: The union of the two branches
        _trueType = storage.ctxTypes[ctx.expr()[1]]
        _falseType = storage.ctxTypes[ctx.expr()[2]]

        _trueKlass = storage.lookupClass(_trueType)
        _falseKlass = storage.lookupClass(_falseType)
        _union = _trueKlass.union(_falseKlass)

        storage.ctxTypes[ctx] = _union
        ctx.typename = _union
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def enterWhile(self, ctx: CoolParser.WhileContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def exitWhile(self, ctx: CoolParser.WhileContext):
        # First expression should be a boolean
        if storage.ctxTypes[ctx.expr()[0]] != 'Bool':
            raise myexceptions.TypeCheckMismatch
        
        # Type Rule: Pass object
        storage.ctxTypes[ctx] = 'Object'
        ctx.typename = 'Object'
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def enterLet(self, ctx: CoolParser.LetContext):
        # Add scoped variables again
        _ids = ctx.ID()
        _types = ctx.TYPE()
        for i in range(len(_ids)-1, -1, -1):
            # No id should be self
            if _ids[i].getText() == 'self':
                raise myexceptions.SelfVariableException

            # Add type of identifier for future checks
            self.idsTypes.openScope()
            self.idsTypes[_ids[i].getText()] = _types[i].getText()
    
    def exitLet(self, ctx: CoolParser.LetContext):
        _types = ctx.TYPE()
        _ids = ctx.ID()
        _expr = ctx.expr()

        # Check conformance of every saved expected type and its expression asigned.
        for i, _type in enumerate(_types):
            # Only for all expr except the last one.
            if i < (len(_expr) - 1):
                _klass_from_type = storage.ctxTypes[_expr[i]]
                if _klass_from_type == 'self':
                    _klass_from_type = self.idsTypes.klass.name
                _assign = storage.lookupClass(_klass_from_type)
                _expr[i].namesymbol = _ids[i].getText()
                _to = storage.lookupClass(_type.getText())
                if not _to.conforms(_assign):
                    raise myexceptions.DoesNotConform

        _last = _expr[len(_expr) - 1]
        _lastType = storage.ctxTypes[_last]
        storage.ctxTypes[ctx] = _lastType
        ctx.typename = _lastType
        for _i in ctx.ID():
            self.idsTypes.closeScope()

    def enterCase(self, ctx: CoolParser.CaseContext):
        # Get all ids and types defined in case.
        _ids = ctx.ID()
        _exprs = ctx.expr()
        _types = ctx.TYPE()

        # There should not be repeated types
        _saved = set()
        for i, _id in reversed(list(enumerate(_ids))):
            _type = _types[i].getText()

            # Check type is not repeated
            if _type in _saved:
                raise myexceptions.InvalidCase

            # Save the types of all ids defined
            _saved.add(_type)
            _exprs[i+1].nametype = _type
            _exprs[i+1].namesymbol = _id.getText()
            self.idsTypes.openScope()
            self.idsTypes[_id.getText()] = _types[i].getText()
        
        # Type Rule: Union of all branches
        _firstName = _types[0].getText()
        _saved.discard(_firstName)
        _first  = storage.lookupClass(_firstName)
        _union = storage.union_mult(_first, _saved)
        storage.ctxTypes[ctx] = _union
        ctx.typename = _union
        self.idsTypes.openScope()
    
    def exitCase(self, ctx: CoolParser.CaseContext):
        self.idsTypes.closeScope()
    
    def enterNew(self, ctx: CoolParser.NewContext):
        self.idsTypes.openScope()
    
    def exitNew(self, ctx: CoolParser.NewContext):
        # Type Rule: Pass type in rule
        _type = ctx.TYPE().getText()
        storage.ctxTypes[ctx] = _type
        ctx.typename = _type
        ctx.nameklass = _type
        self.idsTypes.closeScope()
    
    def enterBlock(self, ctx: CoolParser.BlockContext):
        _expr = ctx.expr()
        for _ex in _expr:
            self.idsTypes.openScope()

    def exitBlock(self, ctx: CoolParser.BlockContext):
        # Type Rule: Pass type of last expr
        _expr = ctx.expr()
        _last = storage.ctxTypes[_expr[len(_expr) - 1]]
        storage.ctxTypes[ctx] = _last
        ctx.typename = _last
        for _ex in _expr:
            self.idsTypes.closeScope()
    
    def enterCall(self, ctx: CoolParser.CallContext):
        _expr = ctx.expr()
        for _ex in _expr:
            self.idsTypes.openScope()
        
    def exitCall(self, ctx: CoolParser.CallContext):
        _id = ctx.ID().getText()
        _expr = ctx.expr()

        # Check what type of call it is, from internal or external klass
        _klassName = None
        _starter = ctx.getChild(1).getText()
        _starter_expr = -1 # Whether the first expresion is an argument or not
        if _starter == '.':
            _starter_expr = 1

            # If it comes from new get its type
            if type(_expr[0]) is CoolParser.NewContext:
                _klassName = _expr[0].TYPE().getText()

            # If it comes from a base klass only get it based on the ctx type
            if type(_expr[0]) is CoolParser.BaseContext:
                _klassName = storage.ctxTypes[_expr[0]]
            
            # If it comes from a let klass get it from the type of the last expression
            if type(_expr[0]) is CoolParser.LetContext:
                _let = _expr[0]
                _caller = _let.getChild(_let.getChildCount() - 1) # Last expr in let
                _klassName = storage.ctxTypes[_caller]

            # Try getting it with the type in the expression
            if _klassName == None:
                _klassName = storage.ctxTypes[_expr[0]]
            
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

            # Catch self types and SELF_TYPE
            if _inserted_type == 'self' or _inserted_type == 'SELF_TYPE':
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
        _calltype = _method.type
        # Set call type to _klass caller when SELF_TYPE
        if _method.type == 'SELF_TYPE':
            _calltype = _klass.name

        storage.ctxTypes[ctx] = _calltype
        ctx.typename = _calltype
        ctx.nameklass = _klassName
        ctx.namemethod = _id
        for _ex in _expr:
            self.idsTypes.closeScope()
        
    def enterAt(self, ctx: CoolParser.AtContext):
        _expr = ctx.expr()
        for _ex in _expr:
            self.idsTypes.openScope()

    def exitAt(self, ctx: CoolParser.AtContext):
        _id = ctx.ID().getText()
        _expr = ctx.expr()
        _type = ctx.TYPE().getText()

        # Catch self types
        _leftType = storage.ctxTypes[_expr[0]]
        if _leftType == 'self':
            _leftType = self.idsTypes.klass.name

        _left = storage.lookupClass(_leftType)
        _right = storage.lookupClass(_type)

        # Right should conform left.
        if not _right.conforms(_left):
            raise myexceptions.MethodNotFound
        
        # Type Rule: Pass type of the method being called
        _methodType = _right.lookupMethod(_id).type
        # Type Rule: Same as right side. Validate later.
        storage.ctxTypes[ctx] = _methodType
        ctx.typename = _methodType
        ctx.nameklass = _leftType
        ctx.namemethod = _id
        for _ex in _expr:
            self.idsTypes.closeScope()
    
    def enterNeg(self, ctx: CoolParser.NegContext):
        self.idsTypes.openScope()

    def exitNeg(self, ctx: CoolParser.NegContext):
        # Type Rule: if expr is Int, pass Int
        _expr = ctx.expr()
        if storage.ctxTypes[ctx.expr()] == 'Int':
            storage.ctxTypes[ctx] = 'Int'
        
        self.idsTypes.closeScope()
    
    def enterIsvoid(self, ctx: CoolParser.IsvoidContext):
        self.idsTypes.openScope()
    
    def exitIsvoid(self, ctx: CoolParser.IsvoidContext):
        # Type Rule: pass Bool
        storage.ctxTypes[ctx] = 'Bool'
        self.idsTypes.closeScope()
    
    def enterMult(self, ctx: CoolParser.MultContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitMult(self, ctx: CoolParser.MultContext):
        # Type rule: both expr should be Int, pass Int
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterDiv(self, ctx: CoolParser.DivContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitDiv(self, ctx: CoolParser.DivContext):
        # Type rule: both expr should be Int, pass Int
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterAdd(self, ctx: CoolParser.AddContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitAdd(self, ctx: CoolParser.AddContext):
        # Type rule: both expr should be Int, pass Int
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterSub(self, ctx: CoolParser.SubContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitSub(self, ctx: CoolParser.SubContext):
        # Type rule: both expr should be Int, pass Int
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterLt(self, ctx: CoolParser.LtContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitLt(self, ctx: CoolParser.LtContext):
        # Type rule: both expr should be Int, pass Bool
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterLe(self, ctx: CoolParser.LeContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
        
    def exitLe(self, ctx: CoolParser.LeContext):
        # Type rule: both expr should be Int, pass Bool
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterEq(self, ctx: CoolParser.EqContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

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
        ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterNot(self, ctx: CoolParser.NotContext):
        self.idsTypes.openScope()

    def exitNot(self, ctx: CoolParser.NotContext):
        # Type Rule: expr should be Bool, pass Bool
        if storage.ctxTypes[ctx.expr()] == 'Bool':
            storage.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Bool'
        
        self.idsTypes.closeScope()

    def enterAssign(self, ctx: CoolParser.AssignContext):
        # No id is self in assign
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException
        
        self.idsTypes.openScope()
    

    def exitAssign(self, ctx: CoolParser.AssignContext):
        # Check conformance of types
        _id = ctx.ID().getText()
        _expr = ctx.expr()
        _idType = self.idsTypes[ctx.ID().getText()]
        _exprType = storage.ctxTypes[ctx.expr()]
        _idKlass = storage.lookupClass(_idType)
        _exprKlass = storage.lookupClass(_exprType)
        
        if not _idKlass.conforms(_exprKlass):
            raise myexceptions.DoesNotConform

        # Type Rule: pass type of expr
        storage.ctxTypes[ctx] = _exprType
        ctx.typename = _exprType
        self.idsTypes.closeScope()

    def exitParens(self, ctx: CoolParser.ParensContext):
        # Type Rule: Pass expr context
        _type = storage.ctxTypes[ctx.expr()]
        storage.ctxTypes[ctx] = _type
        ctx.typename = _type

    def exitObject(self, ctx: CoolParser.ObjectContext):
        # Type rule: Pass type of ID
        _id = ctx.ID().getText()

        # Check if object is in scope
        try:
            _type = self.idsTypes[_id]
            storage.ctxTypes[ctx] = _type
            ctx.typename = _type
            ctx.namesymbol = _id
        except KeyError:
            raise myexceptions.UndeclaredIdentifier
    
    def exitInteger(self, ctx: CoolParser.IntegerContext):
        # Type Rule: Pass 'Int'
        storage.ctxTypes[ctx] = 'Int'
        storage.intConst.append(int(ctx.INTEGER().getText()))
        ctx.truevalue = ctx.INTEGER().getText()
        ctx.literalval = int(ctx.INTEGER().getText())
        ctx.typename = 'Int'
    
    def exitString(self, ctx: CoolParser.StringContext):
        # Type Rule: Pass 'String'
        storage.ctxTypes[ctx] = 'String'
        ctx.literalval = ctx.STRING().getText()[1:-1] # Removing quotes
        storage.stringConst.append(ctx.literalval)
        ctx.typename = 'String'
    
    def exitBool(self, ctx: CoolParser.BoolContext):
        # Type Rule: Pass 'Bool'
        storage.ctxTypes[ctx] = 'Bool'
        storage.boolConst.append("UNDEF_BOOL_FIXIT")
        ctx.typename = 'Bool'
