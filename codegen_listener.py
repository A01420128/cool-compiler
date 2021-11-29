from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
from myexceptions import MethodNotFound

import structure as storage
import asm

class CodegenListener(CoolListener):

    def __init__(self, o) -> None:
        super().__init__()
        self.o = o
        self.num_labels = 0

    def exitMethod(self, ctx: CoolParser.MethodContext):
        # In proto
        # TODO: Get number of locals
        num_locals = 0
        ts = (3 + num_locals) * 4
        k_in = dict(klass=ctx.nameklass, method=ctx.namemethod, ts=ts, fp=ts, s0=ts-4, ra=ts-8, locals=num_locals)
        self.o.accum += asm.methodTpl_in.substitute(k_in)

        self.o.accum += ctx.expr().codegen

        # Out proto
        # TODO: Get formals
        num_formals = 0
        k_out = dict(ts=ts, fp=ts, s0=ts-4, ra=ts-8, formals=num_formals, locals=num_locals, everything=num_formals+ts) # FIXME: ts is locals frame?
        self.o.accum += asm.methodTpl_out.substitute(k_out)

    def enterFormal(self, ctx: CoolParser.FormalContext):
        # TODO something to count
        pass

    def exitBase(self, ctx: CoolParser.BaseContext):
        # Type Rule: Pass child type
        ctx.codegen = ctx.getChild(0).codegen
    
    def exitIf(self, ctx: CoolParser.IfContext):
        # TODO: If implementation
        # Type Rule: The union of the two branches
        # _trueType = storage.ctxTypes[ctx.expr()[1]]
        # _falseType = storage.ctxTypes[ctx.expr()[2]]
        pass
    
    def exitWhile(self, ctx: CoolParser.WhileContext):
        # TODO: While implementation
        # Type Rule: Pass object
        # storage.ctxTypes[ctx] = 'Object'
        # ctx.typename = 'Object'
        pass
    
    def exitLet(self, ctx: CoolParser.LetContext):
        # TODO: Let implementation
        # storage.ctxTypes[ctx] = _lastType
        pass

    def exitCase(self, ctx: CoolParser.CaseContext):
        # TODO: Case implementation
        # Type Rule: Union of all branches
        # _firstName = _types[0].getText()
        pass

    def exitNew(self, ctx: CoolParser.NewContext):
        # TODO: New implementation
        # Type Rule: Pass type in rule
        # _type = ctx.TYPE().getText()
        pass

    def exitBlock(self, ctx: CoolParser.BlockContext):
        # Block implementation: Add all code in all expressions
        ctx.codegen = ''
        for _expr in ctx.expr():
            ctx.codegen += _expr.codegen
    
    def exitCall(self, ctx: CoolParser.CallContext):
        # Call implementation
        # Write all expr inside
        ctx.codegen = ''
        for _expr in ctx.expr():
            ctx.codegen += _expr.codegen
        
        # Push Param
        ctx.codegen += asm.callParametersTpl.substitute()

        # 3 types of call, 1 with . 2 with ()
        _starter = ctx.getChild(1).getText()
        if _starter == '.':
            ctx.codegen += asm.callStr2.substitute(exp="EXPR_NEEDED_FROM_CALL_TYPE_3_AND_2")
        elif _starter == '(':
            ctx.codegen += asm.callStr1.substitute()

        line_number = ctx.start.line
        k_filename = dict(fileName=storage.str_const_dict[storage.FILENAME_STR], line=line_number, label=f'label{self.num_labels}')
        self.num_labels += 1
        ctx.codegen += asm.callTpl1.substitute(k_filename)
        
        # Call dispatch to method offset
        class_name = ctx.nameklass
        method_name = ctx.namemethod
        offset = storage.disp_methods_off[f'{class_name}.{method_name}'] * 4
        k_dispatch = dict(off=offset, method=method_name)
        ctx.codegen += asm.callTpl_instance.substitute(k_dispatch)
        
    def exitAt(self, ctx: CoolParser.AtContext):
        # TODO: At implementation
        # _expr = ctx.expr()
        _type = ctx.TYPE().getText()
        # Type Rule: Pass type of the method being called
        # _methodType = _right.lookupMethod(_id).type
        # Type Rule: Same as right side. Validate later.
        # storage.ctxTypes[ctx] = _methodType
        pass
    
    def exitNeg(self, ctx: CoolParser.NegContext):
        # TODO: Neg implementation
        # Type Rule: if expr is Int, pass Int
        # _expr = ctx.expr()
        pass
    
    def exitIsvoid(self, ctx: CoolParser.IsvoidContext):
        # TODO: Isvoid implementation
        # Type Rule: pass Bool
        # storage.ctxTypes[ctx] = 'Bool'
        # self.idsTypes.closeScope()
        pass

    def exitMult(self, ctx: CoolParser.MultContext):
        # TODO: Mult implementation
        # Type rule: both expr should be Int, pass Int
        #_left = ctx.getChild(0)
        #_right = ctx.getChild(2)
        pass

    def exitDiv(self, ctx: CoolParser.DivContext):
        # TODO: Div implementation
        # Type rule: both expr should be Int, pass Int
        # _left = ctx.getChild(0)
        # _right = ctx.getChild(2)
        pass

    def exitAdd(self, ctx: CoolParser.AddContext):
        # TODO: Add implementation
        # Type rule: both expr should be Int, pass Int
        # _left = ctx.getChild(0)
        # _right = ctx.getChild(2)
        pass

    def exitSub(self, ctx: CoolParser.SubContext):
        # TODO: Sub implementation
        # Type rule: both expr should be Int, pass Int
        # _left = ctx.getChild(0)
        # _right = ctx.getChild(2)
        pass

    def exitLt(self, ctx: CoolParser.LtContext):
        # TODO: Lt implementation
        # Type rule: both expr should be Int, pass Bool
        # _left = ctx.getChild(0)
        # _right = ctx.getChild(2)
        pass

    def exitLe(self, ctx: CoolParser.LeContext):
        # TODO: Le implementation
        # Type rule: both expr should be Int, pass Bool
        # _left = ctx.getChild(0)
        # _right = ctx.getChild(2)
        pass

    def exitEq(self, ctx: CoolParser.EqContext):
        # TODO: Eq implementation
        # Type rule: compare freely except if type Int, String or Bool, compare to same.
        # _expr = ctx.expr()
        # _left = storage.ctxTypes[_expr[0]]
        # _right = storage.ctxTypes[_expr[1]]
        pass

    def exitNot(self, ctx: CoolParser.NotContext):
        # TODO: Not implementation
        # Type Rule: expr should be Bool, pass Bool
        pass

    def exitAssign(self, ctx: CoolParser.AssignContext):
        # TODO: Assign implementation
        # Check conformance of types
        # _id = ctx.ID().getText()
        # _expr = ctx.expr()
        # _idType = self.idsTypes[ctx.ID().getText()]
        pass

    def exitParens(self, ctx: CoolParser.ParensContext):
        ctx.codegen = ctx.expr().codegen

    def exitObject(self, ctx: CoolParser.ObjectContext):
        # TODO: Object implementation
        # Type rule: Pass type of ID
        # _id = ctx.ID().getText()

        # Check if object is in scope
        # try:
            # _type = self.idsTypes[_id]
            # storage.ctxTypes[ctx] = _type
        pass
    
    def exitInteger(self, ctx: CoolParser.IntegerContext):
        # TODO: Integer implementation
        # Type Rule: Pass 'Int'
        # storage.ctxTypes[ctx] = 'Int'
        pass

    def exitString(self, ctx: CoolParser.StringContext):
        literal = storage.str_const_dict[ctx.literalval]
        k = dict(literal=literal, value=literal)
        ctx.codegen = asm.litTpl.substitute(k)
    
    def exitBool(self, ctx: CoolParser.BoolContext):
        # TODO: Bool implementation
        # Type Rule: Pass 'Bool'
        # storage.ctxTypes[ctx] = 'Bool'
        pass