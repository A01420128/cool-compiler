# Generated from antlr/Cool.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CoolParser import CoolParser
else:
    from CoolParser import CoolParser

# This class defines a complete listener for a parse tree produced by CoolParser.
class CoolListener(ParseTreeListener):

    # Enter a parse tree produced by CoolParser#program.
    def enterProgram(self, ctx:CoolParser.ProgramContext):
        pass

    # Exit a parse tree produced by CoolParser#program.
    def exitProgram(self, ctx:CoolParser.ProgramContext):
        pass


    # Enter a parse tree produced by CoolParser#klass.
    def enterKlass(self, ctx:CoolParser.KlassContext):
        pass

    # Exit a parse tree produced by CoolParser#klass.
    def exitKlass(self, ctx:CoolParser.KlassContext):
        pass


    # Enter a parse tree produced by CoolParser#feature.
    def enterFeature(self, ctx:CoolParser.FeatureContext):
        pass

    # Exit a parse tree produced by CoolParser#feature.
    def exitFeature(self, ctx:CoolParser.FeatureContext):
        pass


    # Enter a parse tree produced by CoolParser#formal.
    def enterFormal(self, ctx:CoolParser.FormalContext):
        pass

    # Exit a parse tree produced by CoolParser#formal.
    def exitFormal(self, ctx:CoolParser.FormalContext):
        pass


    # Enter a parse tree produced by CoolParser#expr.
    def enterExpr(self, ctx:CoolParser.ExprContext):
        pass

    # Exit a parse tree produced by CoolParser#expr.
    def exitExpr(self, ctx:CoolParser.ExprContext):
        pass



del CoolParser