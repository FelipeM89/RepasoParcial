%{
#include <stdio.h>
#include <string.h>

int contador = 0;
char palabra[256];
char clave[256];


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
int n_dic = 5;


const char* buscar_clave(const char* p) {
    for (int i = 0; i < n_dic; i++) {
        if (strcmp(dic[i].palabra, p) == 0) {
            return dic[i].clave;
        }
    }
    return NULL;
}
%}

%option noyywrap

%%

[a-zA-ZáéíóúÁÉÍÓÚñÑ]+ {
    if (strcmp(yytext, palabra) == 0) {
        contador++;
    }
}
.|\n   ;

%%

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Uso: %s archivo palabra\n", argv[0]);
        return 1;
    }

    strcpy(palabra, argv[2]);

    const char* c = buscar_clave(palabra);
    if (!c) {
        printf("La palabra '%s' no tiene clave definida.\n", palabra);
        return 1;
    }
    strcpy(clave, c);

    FILE *archivo = fopen(argv[1], "r");
    if (!archivo) {
        printf("No se pudo abrir el archivo %s\n", argv[1]);
        return 1;
    }

    yyin = archivo;
    yylex();
    fclose(archivo);

    printf("%s se repite %d veces en el texto.\n", clave, contador);

    return 0;
}
