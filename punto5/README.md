📘 Descripción

Este proyecto implementa un intérprete interactivo que permite procesar y calcular expresiones matemáticas con números complejos.

Usamos ANTLR 4 para:

Definir la gramática de expresiones con números complejos.

Generar automáticamente el lexer y el parser en Python.

Implementar un Visitor personalizado que evalúa operaciones aritméticas con complejos.

Las operaciones soportadas son:

Suma +

Resta -

Multiplicación *

División /

Ejemplo válido:

(3+4i) + (2-5i) * (1+i)

⚙️ Instalación
1. Crear entorno virtual en Python
```
python3 -m venv venv
source venv/bin/activate
```
3. Instalar runtime de ANTLR en Python
```
pip install --upgrade antlr4-python3-runtime
```
4. Descargar ANTLR 4.13.2
```
wget https://www.antlr.org/download/antlr-4.13.2-complete.jar -O antlr-4.13.2-complete.jar
```
. Generar parser y visitor en Python
```
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor Complejo.g4
```

Esto genera:
```
ComplejoLexer.py
ComplejoParser.py
ComplejoListener.py
ComplejoVisitor.py
```
