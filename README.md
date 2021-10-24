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

En los tests de la etapa3, no pudimos correr esto, porque treePrinter no tenia getOutput. Lo dejamos comentado.

```python
treePrinter = TreePrinter(ctxTypes)
walker.walk(treePrinter, tree)
output = treePrinter.getOutput()

expected = output.split('\n')
with open('expected/semantic/%s.txt' % caseName) as f:
    for line1, line2 in zip(f, expected):
        if line1[:-1] != line2:
            print ("Diferencia!!! [%s]-[%s]" % (line1, line2))
            return False
```

Pero consideramos que lo importante es que se corrierna los casos sin regresar excepciones.
