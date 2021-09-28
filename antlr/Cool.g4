// in---->tests/input/lteassociativity.cool no hubo errores aqui y tenia que haber
grammar Cool;           

program
    : ( klass ';' )+
    ;

klass
    : KLASS TYPE (INHERITS TYPE)? '{' (feature ';' )* '}'
    ;

feature
    : ID '(' ( formal (',' formal )* )? ')' ':' TYPE '{' expr '}'
    | ID ':' TYPE ('<-' expr)?
    ;

formal : ID ':' TYPE ;

expr
    : ID '<-' expr
    | expr('@'TYPE)?'.'ID'(' (expr (',' expr)*)? ')'
    | ID'('(expr (',' expr)*)?')'
    | IF expr THEN  expr ELSE expr FI
    | WHILE expr LOOP expr POOL
    | '{' (expr ';')+ '}'
    | LET ID ':' TYPE ('<-' expr)? (',' ID ':' TYPE ('<-' expr)?)* IN expr
    | CASE expr OF ( ID ':' TYPE '=>' expr ';' )+ ESAC
    | NEW TYPE
    | ISVOID expr
    | expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | '~' expr
    | expr '<' expr
    | expr '<=' expr
    | expr '=' expr
    | NOT expr
    | '(' expr ')'
    | ID
    | INTEGER
    | STRING
    | TRUE
    | FALSE
    ;

/*
 * Aquí comenzaría el léxico
 */

KLASS : C L A S S ;
ELSE : E L S E ;
FI : F I ;
IF : I F ; 
IN : I N ; 
INHERITS : I N H E R I T S ;
ISVOID: I S V O I D ;
LET : L E T ;
LOOP : L O O P ;
POOL : P O O L ;
THEN : T H E N ; 
WHILE : W H I L E ;
CASE  : C A S E ;
ESAC : E S A C ;
NEW : N E W ;
OF : O F ;
NOT : N O T;
TRUE : 'true' ;
FALSE : 'false' ;
TYPE : [A-Z] [a-zA-Z0-9_]* ; 
ID : [a-z] [a-zA-Z0-9_]* ;
INTEGER : [0-9]+ ; 
STRING : '"' .*?  '"' ; // Escaping multiline strings, EOF
WHITESPACE : [ \t\f\n\r]+ -> skip ; // Other whitespace like v
COMMENT : '(*' .*? '*)' -> skip; // Definition of comments inline and mutliline
LINE_COMMENT : '--' .*? '\n' -> skip; // EOF?

fragment A : [aA] ;
fragment C : [cC] ;
fragment L : [lL] ;
fragment S : [sS] ;
fragment E : [eE] ;
fragment F : [fF] ;
fragment I : [iI] ;
fragment N : [nN] ;
fragment H : [hH] ;
fragment R : [rR] ;
fragment T : [tT] ;
fragment V : [vV] ;
fragment O : [oO] ;
fragment D : [dD] ;
fragment P : [pP] ;
fragment W : [wW] ;

