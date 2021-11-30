from typing import Literal
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
        self.num_formals = 0
        self.idx_stack = -1

    def enterMethod(self, ctx: CoolParser.MethodContext):
        self.num_formals = 0
        self.idx_stack = -1

    def exitMethod(self, ctx: CoolParser.MethodContext):
        # In proto
        # TODO: Get number of locals
        num_locals = 0
        ts = (3 + num_locals) * 4
        k_in = dict(klass=ctx.nameklass, method=ctx.namemethod, ts=ts, fp=ts, s0=ts-4, ra=ts-8, locals=num_locals)
        self.o.accum += asm.methodTpl_in.substitute(k_in)

        self.o.accum += ctx.expr().codegen

        # Out proto
        formals = self.num_formals * 4
        k_out = dict(ts=ts, fp=ts, s0=ts-4, ra=ts-8, formals=formals, locals=num_locals, everything=formals+ts) # FIXME: ts is locals frame?
        self.o.accum += asm.methodTpl_out.substitute(k_out)

    def exitFormal(self, ctx: CoolParser.FormalContext):
        self.num_formals += 1
        self.idx_stack += 1

    def exitBase(self, ctx: CoolParser.BaseContext):
        # Type Rule: Pass child type
        ctx.codegen = ctx.getChild(0).codegen
    
    def exitIf(self, ctx: CoolParser.IfContext):
        _test = ctx.expr()[0].codegen
        _true = ctx.expr()[1].codegen
        _false = ctx.expr()[2].codegen
        label_false = f'label{self.num_labels}'
        self.num_labels += 1
        label_exit = f'label{self.num_labels}'
        self.num_labels += 1
        k = dict(test_subexp=_test, true_subexp=_true, false_subexp=_false, label_false=label_false, label_exit=label_exit)
        ctx.codegen = asm.ifTpl.substitute(k)
    
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
        _left = ctx.getChild(0).codegen
        _right = ctx.getChild(2).codegen
        k = dict(left_subexp=_left, right_subexp=_right, op='mul')
        ctx.codegen = asm.arithTpl.substitute(k)

    def exitDiv(self, ctx: CoolParser.DivContext):
        _left = ctx.getChild(0).codegen
        _right = ctx.getChild(2).codegen
        k = dict(left_subexp=_left, right_subexp=_right, op='div')
        ctx.codegen = asm.arithTpl.substitute(k)

    def exitAdd(self, ctx: CoolParser.AddContext):
        _left = ctx.getChild(0).codegen
        _right = ctx.getChild(2).codegen
        k = dict(left_subexp=_left, right_subexp=_right, op='add')
        ctx.codegen = asm.arithTpl.substitute(k)

    def exitSub(self, ctx: CoolParser.SubContext):
        _left = ctx.getChild(0).codegen
        _right = ctx.getChild(2).codegen
        k = dict(left_subexp=_left, right_subexp=_right, op='sub')
        ctx.codegen = asm.arithTpl.substitute(k)

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
        _left = ctx.expr()[0].codegen
        _right = ctx.expr()[1].codegen
        k = dict(left_subexp=_left, right_subexp=_right, label=f'label{self.num_labels}')
        self.num_labels += 1
        ctx.codegen = asm.eqTpl.substitute(k)

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
        # Pop from idx_stack on load
        off = (3 + self.idx_stack) * 4
        self.idx_stack -= 1
        address = f'{off}($fp)'
        k = dict(address=address, symbol=ctx.namesymbol, klass=ctx.typename)
        ctx.codegen = asm.varTpl.substitute(k)
    
    def exitInteger(self, ctx: CoolParser.IntegerContext):
        literal = storage.int_const_dict[ctx.literalval]
        k = dict(literal=literal, value=ctx.literalval)
        ctx.codegen = asm.litTpl.substitute(k)

    def exitString(self, ctx: CoolParser.StringContext):
        literal = storage.str_const_dict[ctx.literalval]
        k = dict(literal=literal, value=ctx.literalval)
        ctx.codegen = asm.litTpl.substitute(k)
    
    def exitBool(self, ctx: CoolParser.BoolContext):
        # TODO: Bool implementation
        # Type Rule: Pass 'Bool'
        # storage.ctxTypes[ctx] = 'Bool'
        pass