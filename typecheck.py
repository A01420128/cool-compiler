from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser


class Typecheck(CoolListener):
    typeTable = {}

    def exitInteger(self, ctx: CoolParser.IntegerContext):
        ctx.type = "integer"
        self.typeTable[ctx] = "integer"
    
    def exitBase(self, ctx: CoolParser.BaseContext):
        ctx.type = ctx.getChild(0).type
        self.typeTable[ctx] = "integer"

    def exitAdd(self, ctx: CoolParser.AddContext):
        #if ctx.expr(0).type == "integer" and ctx.expr(0).type == "integer":        
        #    ctx.type = "integer"
        left = ctx.expr(0)
        right = ctx.expr(1)
        if self.typeTable[ctx.expr(0)] == "integer" and self.typeTable[ctx.expr(1)] == "integer":
            self.typeTable[ctx] = "integer"
        else:
            raise Exception("Type error")
    

        