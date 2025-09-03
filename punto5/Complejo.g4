grammar Complejo;

expr
    : expr '+' term   # Suma
    | expr '-' term   # Resta
    | term            # Termino
    ;

term
    : term '*' factor # Multiplicacion
    | term '/' factor # Division
    | factor          # TerminoFactor
    ;

factor
    : complejo        # ComplejoFactor
    | '(' expr ')'    # Parentesis
    ;

complejo
    : REAL (('+'|'-') REAL)? 'i'?   # NumeroComplejo
    ;

REAL
    : '-'? [0-9]+ ('.' [0-9]+)?
    ;

WS
    : [ \t\r\n]+ -> skip
    ;

