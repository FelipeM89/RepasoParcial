#include <stdio.h>
#include <string.h>
#include <time.h>

// Función que implementa el AFD: reconoce a*b
int afd(const char *cadena) {
    int estado = 0;
    for (int i = 0; cadena[i] != '\0'; i++) {
        char c = cadena[i];
        switch (estado) {
            case 0: // inicio
                if (c == 'a') estado = 0;
                else if (c == 'b') estado = 1;
                else return 0; // carácter inválido
                break;
            case 1: // estado final
                return 0; // no debe haber más caracteres después de b
        }
    }
    return (estado == 1); // válido solo si terminó en estado 1
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s archivo\n", argv[0]);
        return 1;
    }

    FILE *archivo = fopen(argv[1], "r");
    if (!archivo) {
        printf("No se pudo abrir %s\n", argv[1]);
        return 1;
    }

    char linea[1024];
    int aceptadas = 0, total = 0;

    clock_t inicio = clock();

    while (fgets(linea, sizeof(linea), archivo)) {
        // eliminar salto de línea
        linea[strcspn(linea, "\n")] = 0;
        if (afd(linea)) aceptadas++;
        total++;
    }

    clock_t fin = clock();
    double tiempo = (double)(fin - inicio) / CLOCKS_PER_SEC;

    printf("Total de cadenas: %d\n", total);
    printf("Cadenas aceptadas: %d\n", aceptadas);
    printf("Tiempo de ejecucion en C: %.6f segundos\n", tiempo);

    fclose(archivo);
    return 0;
}
