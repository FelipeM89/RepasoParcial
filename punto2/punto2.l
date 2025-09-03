%{
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int encontro_lambda = 0;
int encontro_print = 0;
char nombre_lambda[128] = "";

void quitar_espacios(char *s) {
    char *inicio = s;
    while (*inicio && isspace((unsigned char)*inicio)) inicio++;
    if (inicio != s) memmove(s, inicio, strlen(inicio) + 1);

    char *fin = s + strlen(s) - 1;
    while (fin >= s && isspace((unsigned char)*fin)) {
        *fin = '\0';
        fin--;
    }
}
%}

%option noyywrap

ID       [A-Za-z_][A-Za-z0-9_]*
LINEA    [^\n]*

%%

^[ \t]*{ID}[ \t]*=[ \t]*lambda{LINEA} {
    char izquierda[128];
    char *igual = strchr(yytext, '=');

    if (igual) {
        int largo = igual - yytext;
        if (largo > (int)sizeof(izquierda)-1) largo = sizeof(izquierda)-1;
        strncpy(izquierda, yytext, largo);
        izquierda[largo] = '\0';
        quitar_espacios(izquierda);

        if (strlen(izquierda) > 0) {
            strncpy(nombre_lambda, izquierda, sizeof(nombre_lambda)-1);
            nombre_lambda[sizeof(nombre_lambda)-1] = '\0';
            encontro_lambda = 1;
        }
    }
}

^[ \t]*print[ \t]*\({LINEA}\) {
    if (encontro_lambda && nombre_lambda[0] != '\0') {
        char patron[256];
        snprintf(patron, sizeof(patron), "%s(", nombre_lambda);

        if (strstr(yytext, patron) != NULL) {
            encontro_print = 1;
        }
    }
}

[ \t\n]+    ;

.           ;

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *archivo = fopen(argv[1], "r");
        if (!archivo) {
            perror(argv[1]);
            return 1;
        }
        yyin = archivo;
    }

    yylex();

    if (encontro_lambda && encontro_print) {
        printf("ACEPTA\n");
    } else {
        printf("NO ACEPTA\n");
    }

    return 0;
}
