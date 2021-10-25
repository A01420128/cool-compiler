from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
from myexceptions import *

# Excluded
ex = {'Base'}

# Special no incluyen tipo al final
es = {'Program', 'Klass', 'Method'}

# True names
tt = {'Program': 'AProgram', 'Klass': 'AClassDecl', 'Method': 'AMethodFeature', 'Block':'AListExpr', 'Add':'APlusExpr', 'Sub':'AMinusExpr','Mult':'AMultExpr', 'Div':'ADivExpr','Integer':'AIntExpr'}

class TreePrinter(CoolListener):
    def __init__(self, types={}):
        self.depth = 0
        self.types = types
        self.output = "\n"

    def enterEveryRule(self, ctx):
        self.depth = self.depth + 1
        s = ''
        for i in range(self.depth-1):
            s += "   "
        
        _type = type(ctx).__name__[:-7]
        if _type not in ex: # There are nodes not being considered like Base
            _extra = ''
            if _type not in es:
                _extra = ":" + ctx.typename
            _real = tt[_type]
            if type(ctx) is CoolParser.ProgramContext:
                self.output += "{}>- {}\n".format(s, _real)
            else:
                self.output += "{}`- {}{}\n".format(s, _real, _extra)
            if type(ctx) is CoolParser.KlassContext:
                self.output += "{}   |- {}\n".format(s, ctx.nameklass)
                self.output += "{}   |- {}\n".format(s, ctx.nameinherits)
            if type(ctx) is CoolParser.MethodContext:
                self.output += "{}   |- {}\n".format(s, ctx.namemethod)
                self.output += "{}   |- {}\n".format(s, ctx.typemethod)
            if type(ctx) is CoolParser.IntegerContext:
                self.output += "{}|   `- {}\n".format(s, ctx.truevalue)

            

    def exitEveryRule(self, ctx):
        self.depth = self.depth - 1
    
    def getOutput(self):
        print(self.output)
        return self.output
