# afd_tokens.py
# Reconocimiento de tokens usando AFDs en Python
# Tokens soportados: PLUS, INCREMENT, INT, FLOAT

def afd_plus(token):
    """Reconoce + y ++"""
    state = 0
    for c in token:
        if state == 0 and c == '+':
            state = 1
        elif state == 1 and c == '+':
            state = 2
        else:
            return None
    if state == 1:
        return "PLUS"
    elif state == 2:
        return "INCREMENT"
    return None


def afd_int(token):
    """Reconoce enteros [0-9]+"""
    state = 0
    for c in token:
        if c.isdigit():
            state = 1
        else:
            return None
    return "INT" if state == 1 else None


def afd_float(token):
    """Reconoce flotantes [0-9]+\.[0-9]+"""
    state = 0
    for c in token:
        if state == 0 and c.isdigit():
            state = 1
        elif state == 1 and c.isdigit():
            state = 1
        elif state == 1 and c == '.':
            state = 2
        elif state == 2 and c.isdigit():
            state = 3
        elif state == 3 and c.isdigit():
            state = 3
        else:
            return None
    return "FLOAT" if state == 3 else None


def classify(token):
    """Prueba cada AFD en orden"""
    for afd in (afd_plus, afd_int, afd_float):
        result = afd(token)
        if result:
            return result
    return "ERROR"


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python3 afd_tokens.py archivo.txt")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "r") as f:
        for line in f:
            # Divide cada línea en tokens separados por espacios
            for token in line.strip().split():
                if token.startswith("#"):  # comentario estilo AWK
                    break
                print(f"{token:>5}  -> {classify(token)}")
