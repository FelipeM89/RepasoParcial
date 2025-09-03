import sys
from antlr4 import *
from ComplejoLexer import ComplejoLexer
from ComplejoParser import ComplejoParser
from EvalVisitor import EvalVisitor

def evaluar_expresion(expresion: str):
    entrada = InputStream(expresion)
    lexer = ComplejoLexer(entrada)
    tokens = CommonTokenStream(lexer)
    parser = ComplejoParser(tokens)
    tree = parser.expr()

    visitor = EvalVisitor()
    return visitor.visit(tree)

def main():
    print("=== Calculadora de números complejos (ANTLR + Python) ===")
    print("Escribe expresiones como (3+4i) + (2-5i) * (1+i)")
    print("Escribe 'exit' para salir.\n")

    while True:
        try:
            expr = input(">> ").strip()
            if expr.lower() in ["exit", "salir", "quit"]:
                print("Saliendo...")
                break
            if not expr:
                continue
            resultado = evaluar_expresion(expr)
            print("Resultado:", resultado)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
