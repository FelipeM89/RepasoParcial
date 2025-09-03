import time
import sys

def afd(cadena: str) -> bool:
    estado = 0
    for c in cadena:
        if estado == 0:
            if c == 'a':
                estado = 0
            elif c == 'b':
                estado = 1
            else:
                return False
        elif estado == 1:
            return False
    return estado == 1

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} archivo")
        return

    archivo = sys.argv[1]
    aceptadas = 0
    total = 0

    inicio = time.perf_counter()

    with open(archivo, "r") as f:
        for linea in f:
            linea = linea.strip()
            if afd(linea):
                aceptadas += 1
            total += 1

    fin = time.perf_counter()
    tiempo = fin - inicio

    print(f"Total de cadenas: {total}")
    print(f"Cadenas aceptadas: {aceptadas}")
    print(f"Tiempo de ejecucion en Python: {tiempo:.6f} segundos")

if __name__ == "__main__":
    main()
