# Etapa de Generacion de Codigo

**Jose Javier Tlacuilo Fuentes - A01420128**

**Alonso Sebastián Varela Sandoval - A01335705**

## Resultados

Se corren todas las pruebas de la  etapa semantica pudimos correr todas las pruebas de las 3 etapas.

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

Se consideran todos los nodos en el arbol y se generan exitosamente los siguientes ejecutables.

```zsh
python codegen.py <file-name> (in resources/codegen/input/)

generated
├── abort.s
├── assignment-val.s
├── basic-init.s
├── case-order.s
├── eval-order-arith.s
├── fact.s
├── fibo.s
├── mine-div.s
├── mine-hello-sum.s
├── mine-hello.s
├── mine-loop.s
├── mine-mut.s
├── mine-sub.s
├── mine-sum-func.s
└── mine-sum.s
```

## Consideraciones

### Listeners

Tuvimos dos listeners para la etapa semantica:

- KlassListener: se ocupo de construir las klasses
- ConformanceListener: se ocupo de los tipos, el rastreo de ids, los scopes y todo lo demas.

Uno para la etapa de generacion de codigo:

- CodegenListener: inserta codigo en todos los nodos
