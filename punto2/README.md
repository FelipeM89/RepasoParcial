1) ¿Qué es lambda en Python (conceptos clave)?

Definición: lambda crea una función anónima en una sola línea:
lambda argumentos: expresión
Ejemplo: square = lambda x: x ** 2 crea una función que eleva x al cuadrado.

Características importantes:

Solo acepta una expresión (no múltiples sentencias ni return).

Se puede asignar a un nombre (square = lambda ...) y luego invocar (square(3)).

Parámetros pueden ser múltiples y separados por comas: lambda x, y: x + y.

La expresión puede contener operadores (+ - * / **) y llamadas simples, pero Python completo permite estructuras que ya no son regulares (p.ej. paréntesis anidados arbitrarios).

Para nuestro problema: vamos a aceptar una versión simplificada de lambda tipo ident = lambda params : expr donde params es lista simple de identificadores y expr es una expresión sencilla (identificadores y/o números con operadores básicos). Esto es suficiente para el enunciado de ejemplo.

2) Gramática regular vs expresiones regulares (qué necesitamos)

Gramática regular: es una descripción formal que genera lenguajes regulares (los que se pueden reconocer con autómatas finitos). En la práctica para este ejercicio usaremos una expresión regular (o conjunto de ellas) que reconozca la forma ident = lambda ....

Limitación práctica: el Python real (por ejemplo, una expresión con paréntesis anidados arbitrariamente) no es completamente regular; por eso aceptaremos un subconjunto regular suficiente para reconocer líneas del tipo del ejemplo:

LHS (identificador): [A-Za-z_][A-Za-z0-9_]*

= separado opcionalmente por espacios

la palabra clave lambda

parámetros: ident o ident, ident, ...

: y la expresión en una sola línea (no validaremos matemáticamente toda la expresió n, solo una forma razonable)

Expresión regular (conceptual) que usaremos:

^\s*IDENT\s*=\s*lambda\s*PARAMS\s*:\s*EXPR\s*$


con:

IDENT = [A-Za-z_][A-Za-z0-9_]*

PARAMS = IDENT ( \s* , \s* IDENT )* (puede ser 1 o más parámetros; también podríamos aceptar 0)

EXPR = combinación simple de IDENT o NUM y operadores (+ - * / **) (no validaremos todas las reglas de precedencia, solo presencia básica)

3) ¿Qué es LEX / flex y cómo lo vamos a usar?

LEX/flex es un generador de analizadores léxicos: tú describes patrones (expresiones regulares) y las acciones (en C) que se ejecutan cuando se reconoce cada patrón.

Estructura básica de un archivo .l (flex):

Sección C inicial (%{ ... %}) para incluir #include y declarar variables/funciones.

Definiciones/macros (opcional): ID [A-Za-z_][A-Za-z0-9_]*

Reglas: patrón { acción_en_C }

Código de usuario (main) al final (después de %%).

Funciones/variables útiles:

yytext → texto completo que coincidio con la regla actual.

yyleng → longitud de yytext.

yyin → FILE* usado como entrada (puedes asignarle fopen(argv[1],...)).

Compilación y ejecución típica:

flex archivo.l → genera lex.yy.c

gcc lex.yy.c -lfl -o mi_chequeador

./mi_chequeador archivo.txt

Cómo vamos a decidir "ACEPTA" / "NO ACEPTA":
Asumiré (para coincidir con el ejemplo del enunciado) que un archivo se ACEPTA si contiene al menos:

Una asignación válida de lambda (p.ej. square = lambda x: x ** 2), y

Una llamada que use el identificador asignado (p.ej. print(square(3))) — esto valida que la lambda fue definida y utilizada.
Si prefieres otra regla (p. ej. aceptar sólo la asignación), lo ajustamos, pero esto coincide con el ejemplo mostrado en el enunciado.

4) Diseño del analizador LEX que te doy (resumen)

Buscará líneas que parezcan ident = lambda ... y guardará el ident (nombre de la función).

Buscará líneas print(...) y verificará si dentro del print hay una llamada a ese ident (p.ej. ident().

Si se detectan ambos (definición + llamada a la misma función) -> imprimirá ACEPTA, sino NO ACEPTA.

Notas de robustez: el scanner es pragmático: acepta diferentes espacios y formas simples; no pretende validar el Python completo (si necesitas una verificación completa de expresiones, habría que usar Yacc/Bison o un parser más poderoso).
