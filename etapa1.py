import sys
import unittest

from antlr4 import *
from antlr.CoolLexer import CoolLexer
from antlr.CoolParser import CoolParser
from myexceptions import *

from klass_listener import KlassListener
from conformance_listener import ConformanceListener

def parseCase(caseName):
    parser = CoolParser(CommonTokenStream(CoolLexer(FileStream("input/semantic/%s.cool" % caseName))))
    return parser.program()

class CoolTests(unittest.TestCase):
    def setUp(self): 
        self.walker = ParseTreeWalker()

    def test1(self): 
        tree = parseCase("nomain")
        with self.assertRaises(NoMainException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test2(self):
        tree = parseCase("badredefineint")
        with self.assertRaises(RedefineBasicClassException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test3(self):
        tree = parseCase("anattributenamedself")
        with self.assertRaises(SelfVariableException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test4(self):
        tree = parseCase("letself")
        with self.assertRaises(SelfVariableException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test5(self):
        tree = parseCase("inheritsbool")
        with self.assertRaises(InvalidInheritsException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test6(self):
        tree = parseCase("inheritsselftype")
        with self.assertRaises(InvalidInheritsException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test7(self):
        tree = parseCase("inheritsstring")
        with self.assertRaises(InvalidInheritsException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test8(self):
        tree = parseCase("redefinedobject")
        with self.assertRaises(RedefineBasicClassException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test9(self):
        tree = parseCase("self-assignment")
        with self.assertRaises(SelfAssignmentException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test10(self):
        tree = parseCase("selfinformalparameter")
        with self.assertRaises(SelfVariableException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test11(self):
        tree = parseCase("selftyperedeclared")
        with self.assertRaises(RedefineBasicClassException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

    def test12(self):
        tree = parseCase("selftypeparameterposition")
        with self.assertRaises(SelftypeInvalidUseException):
            self.walker.walk(KlassListener(), tree)
            self.walker.walk(ConformanceListener(), tree)

if __name__ == '__main__':
    unittest.main()
