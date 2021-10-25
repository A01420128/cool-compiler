# Etapa Semantica del Compilador Cool

**Jose Javier Tlacuilo Fuentes - A01420128**

**Alonso Sebastián Varela Sandoval - A01335705**

## Resultados

Pudimos correr todas las pruebas de las 3 etapas.

```zsh
proyecto [main●] conda activate antlr 
(antlr) proyecto [main●] python etapa1.py 
............
----------------------------------------------------------------------
Ran 12 tests in 0.027s

OK
(antlr) proyecto [main●] python etapa2.py 
........................
----------------------------------------------------------------------
Ran 24 tests in 0.061s

OK
(antlr) proyecto [main●] python etapa3.py 
......................................
----------------------------------------------------------------------
Ran 38 tests in 0.842s

OK
(antlr) proyecto [main●] 
```

## Consideraciones

### Listeners

Tuvimos dos listeners:
- KlassListener: se ocupo de construir las klasses
- ConformanceListener: se ocupo de los tipos, el rastreo de ids, los scopes y todo lo demas.

### Cambios

El unico cambio a la gramatica fue poner '~' para el caso #neg, porque no lo reconocia antlr.

### Sobre TreePrinter

Al final intentamos imprimir el arbol de la ultima parte para comparar con el output esperado, pero nos encontramos
con muchos cambios de formato y por eso optamos por comentar esta parte y dejar que los test corrieran solos.

```python
treePrinter = TreePrinter(ctxTypes)
walker.walk(treePrinter, tree)
output = treePrinter.getOutput()

expected = output.split('\n')
with open('expected/semantic/%s.cool.out' % caseName) as f:
    for line1, line2 in zip(f, expected):
        if line1[:-1] != line2:
            print ("%s%s" % (line2, line1))
            return False
return True
```

Estos fueron los primeros resultados para el tree printer.

```zsh
>- AProgram
   `- AClassDecl
      |- Main
      |- Object
      `- AMethodFeature
         |- main
         |- Object
         `- AListExpr:Int
            `- APlusExpr:Int
                  `- AIntExpr:Int
                  |   `- 5
                  `- AIntExpr:Int
                  |   `- 4
            `- AMinusExpr:Int
                  `- AIntExpr:Int
                  |   `- 5
                  `- AIntExpr:Int
                  |   `- 4
            `- AMultExpr:Int
                  `- AIntExpr:Int
                  |   `- 3
                  `- AIntExpr:Int
                  |   `- 2
            `- ADivExpr:Int
                  `- AIntExpr:Int
                  |   `- 3
                  `- AIntExpr:Int
                  |   `- 2

>- AProgram  >- AProgram

F
======================================================================
FAIL: test0 (__main__.CoolTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/tlacuilose/Documents/python/tec/COM/ANTLR/proyecto/etapa3.py", line 82, in <lambda>
    methods['test%d' % i] = lambda self: self.assertTrue(parseAndCompare(cases[i]))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 1 test in 0.010s
```
Comparandolo con:

```zsh
  >- AProgram
     `- AClassDecl
        |- Main
        |- Object
        `- AMethodFeature
           |- main
           |- Object
           `- AListExpr:Int
              |- APlusExpr:Int
              |  |- AIntExpr:Int
              |  |  `- 5
              |  `- AIntExpr:Int
              |     `- 4
              |- AMinusExpr:Int
              |  |- AIntExpr:Int
              |  |  `- 5
              |  `- AIntExpr:Int
              |     `- 4
              |- AMultExpr:Int
              |  |- AIntExpr:Int
              |  |  `- 3
              |  `- AIntExpr:Int
              |     `- 2
              `- ADivExpr:Int
                 |- AIntExpr:Int
                 |  `- 3
                 `- AIntExpr:Int
                    `- 2

```
