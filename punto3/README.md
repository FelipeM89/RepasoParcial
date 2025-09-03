README — Contador por clave (Flex)
Descripción

Programa hecho con Flex que lee un archivo de texto y cuenta cuántas veces aparece una palabra buscada.
En vez de imprimir la palabra buscada, el programa devuelve la clave asociada a esa palabra (según un diccionario definido en el código) y cuántas veces se repite en el texto.

Requisitos

flex

gcc (o cualquier compilador de C que enlace con la librería fl / lfl)

Sistema tipo Unix (Linux, macOS). Funciona en terminal.

Archivos

punto3.l — el archivo fuente de Flex (el que vas a compilar).

archivo.txt — archivo de ejemplo con el texto donde se buscará la palabra.

Compilar y ejecutar

Generar el C desde flex:
```
flex punto3.l
```

Compilar:
```
gcc lex.yy.c -lfl

```
Cómo funciona (resumen)

El programa tiene un diccionario dentro del bloque C (arreglo dic[]) que asocia palabras a claves.

Se pasa por línea de comandos la palabra a buscar (por ejemplo perro).

Antes de procesar el archivo, el programa verifica que la palabra que buscas tenga una clave en el diccionario.

El analizador léxico (rules de Flex) reconoce palabras del texto y compara cada palabra con la palabra buscada.

Cuenta coincidencias exactas (palabra completa). Al final imprime la clave y el número de repeticiones.

## Explicación línea por línea (detallada)

A continuación explico cada bloque y cada línea importante del archivo punto3.l. Para facilitar la lectura lo hago por secciones.

Bloque 1 — %{ ... %} (C que se copia al inicio del .c generado)

```c     
%{
#include <stdio.h>
#include <string.h>
#include <ctype.h>
```

%{ inicia un bloque de código C que Flex copia literalmente al principio del lex.yy.c.

#include <stdio.h> permite funciones de entrada/salida (printf, fopen, fgets, etc.).

#include <string.h> permite funciones de cadena (strcmp, strcpy, sizeof).

#include <ctype.h> se incluye por convención si quieres usar funciones de clasificación de caracteres (no usado en el código final, pero útil si normalizas mayúsculas/minúsculas).
```c     

int contador = 0;
char palabra[256];
char clave[256];

```

contador almacena el número de coincidencias encontradas.

palabra guardará la palabra que el usuario pasa por línea de comandos (ej: perro).

clave guardará la clave asociada (ej: animal) encontrada en el diccionario.

```c     

struct Diccionario {
    char palabra[50];
    char clave[50];
} dic[] = {
    {"arroz", "comida"},
    {"correr", "accion"},
    {"perro", "animal"},
    {"gato", "animal"},
    {"casa", "lugar"}
};
```

Se define una estructura Diccionario con dos campos (palabra, clave).

dic[] es un arreglo literal con entradas predefinidas. Aquí defines todas las parejas palabra → clave que quieras reconocer.

Para añadir términos sólo agrega {"nuevaPalabra", "suClave"}, dentro del arreglo.
```c     

int n_dic = sizeof(dic)/sizeof(dic[0]);

```
Calcula el número de elementos del arreglo dic de forma automática, guardándolo en n_dic. Es más robusto que poner un número fijo.

```c     

const char* buscar_clave(const char* p) {
    for (int i = 0; i < n_dic; i++) {
        if (strcmp(dic[i].palabra, p) == 0) {
            return dic[i].clave;
        }
    }
    return NULL;
}
%}
```

buscar_clave es una función auxiliar que:

Recorre dic[].

Si encuentra una entrada cuya palabra coincide exactamente con p, devuelve la clave correspondiente.

Si no encuentra coincidencias devuelve NULL.

%} cierra el bloque C que Flex pega al inicio del .c.

Línea de opción Flex
```c     

%option noyywrap

```     

Evita tener que definir la función yywrap(). Con esto, Flex terminará el análisis al final del archivo sin llamar a yywrap.

Sección de reglas — %% (primera aparición)
```c     

%%
```

Este %% separa las definiciones del bloque C de las reglas de Flex. Todo lo que venga después y antes del siguiente %% son reglas patrón { acción }.

Reglas (patrones y acciones)
```c     

[a-zA-ZáéíóúÁÉÍÓÚñÑ]+ {
    if (strcmp(yytext, palabra) == 0) {
        contador++;
    }
}

```
[a-zA-ZáéíóúÁÉÍÓÚñÑ]+ es el patrón que reconoce una palabra compuesta por letras latinas (incluye vocales con tilde y la ñ). El + significa “uno o más caracteres”.

Cuando Flex encuentra una porción del texto que coincide con ese patrón, ejecuta la acción entre { ... }.

yytext es la cadena que contiene el texto reconocido por la regla (la palabra encontrada en el archivo).

strcmp(yytext, palabra) == 0 compara si la palabra encontrada en el texto (yytext) es exactamente igual a la palabra que pasó el usuario por línea de comandos.

Si son iguales, incrementa contador.

Esta lógica hace que sólo coincidan palabras completas y exactas (por ejemplo perro coincide con perro pero no con perro. o Perro si hay diferencia en mayúsculas).
```c     

.|\n   ;

```
Regla comodín: . coincide con cualquier carácter excepto nueva línea; \n coincide con nueva línea. La acción es vacía (;) — o sea, consume todo lo demás sin hacer nada.

Esto evita que el analizador se quede atascado con otros caracteres (signos de puntuación, espacios, dígitos, etc.).

Segundo %% (fin de reglas / inicio del C final)
```c     

%%
```

Marca el fin de las reglas y el inicio del código C que va al final del archivo generado. Ahí va main() y cualquier otra función.
```
main y flujo final
int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Uso: %s archivo palabra\n", argv[0]);
        return 1;
    }
```
main toma argc y argv.

Verifica que se pasen exactamente 2 argumentos (además del nombre del programa): archivo y palabra.

Si no se pasan correctamente, muestra el uso correcto y sale con código 1.

    strcpy(palabra, argv[2]);


Copia el segundo argumento (argv[2]) dentro de la variable palabra usada por las reglas para la comparación.

    const char* c = buscar_clave(palabra);
    if (!c) {
        printf("La palabra '%s' no tiene clave definida.\n", palabra);
        return 1;
    }
    strcpy(clave, c);


Llama a buscar_clave para obtener la clave asociada a la palabra.

Si buscar_clave devuelve NULL significa que la palabra no está en el diccionario: se informa y se sale con código 1.

Si devuelve una clave válida, se copia a clave para usarla en el mensaje final.

    FILE *archivo = fopen(argv[1], "r");
    if (!archivo) {
        printf("No se pudo abrir el archivo %s\n", argv[1]);
        return 1;
    }


Abre el archivo pasado como primer argumento para lectura.

Si fopen falla (archivo no existe o permisos insuficientes) imprime error y sale.

    yyin = archivo;
    yylex();
    fclose(archivo);


yyin le dice a Flex cuál es la entrada (aquí el FILE *archivo).

yylex() inicia el análisis léxico: Flex recorrerá todo el archivo aplicando las reglas definidas arriba.

Al terminar se cierra el archivo.

    printf("%s se repite %d veces en el texto.\n", clave, contador);

    return 0;
    }


Imprime el resultado final usando la clave y el contador de coincidencias.

Devuelve 0 indicando ejecución exitosa
