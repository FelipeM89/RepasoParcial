📘 README — Reconocimiento de Tokens con AWK
📌 Descripción

Este proyecto implementa un reconocedor de tokens usando AWK.
El programa toma un archivo de entrada con posibles lexemas (secuencias de caracteres) y los clasifica según un autómata finito determinista (AFD) definido en el enunciado del parcial.

Los tokens a reconocer son:

+ → PLUS

++ → INCREMENT

[0-9]+ → INT (números enteros positivos, incluye 0)

[0-9]+"."[0-9]+ → FLOAT (números reales con punto decimal, al menos un dígito antes y después del punto)

Si el lexema no coincide con ninguno, se etiqueta como ERROR.

📂 Archivos del proyecto

token.awk → Script en AWK que implementa el reconocedor.

tokens.txt → Archivo de prueba con ejemplos de entrada.

⚙️ Requisitos

Sistema operativo: Linux (Kali en este caso, pero vale cualquier distro)

AWK instalado (ya viene en la mayoría de distribuciones, puedes verificar con):

awk --version



▶️ Uso

Guarda el script en un archivo llamado token.awk:

#!/usr/bin/awk -f

function classify(tok) {
    if (tok ~ /^\+\+$/)        return "INCREMENT";
    else if (tok ~ /^\+$/)     return "PLUS";
    else if (tok ~ /^[0-9]+$/) return "INT";
    else if (tok ~ /^[0-9]+\.[0-9]+$/) return "FLOAT";
    else return "ERROR";
}

{
    for (i = 1; i <= NF; i++) {
        tok = $i;
        if (tok ~ /^#/) break;   # Permite comentarios en el archivo de entrada
        print classify(tok);
    }
}


Crea un archivo de entrada, por ejemplo tokens.txt:

+
++
0
12345
9.0
12.34
12.
.34
a
+++
42 + ++ 3.14


Ejecuta el reconocedor:

awk -f token.awk tokens.txt

Casos especiales

12. → ERROR (falta un dígito después del punto)

.34 → ERROR (falta un dígito antes del punto)

007 → INT (válido, ceros a la izquierda aceptados)

++ → INCREMENT

+++ → ERROR (no definido en el lenguaje)

📝 Notas

Los lexemas deben estar separados por espacios o saltos de línea.

Se permiten comentarios en el archivo de entrada, empezando con #.

El orden en el que se valida es importante: primero ++, luego +, después enteros y finalmente flotantes. Esto evita que ++ sea interpretado como dos +.

🚀 Conclusión

Este proyecto demuestra cómo usar AWK para implementar un reconocedor léxico simple basado en un AFD. Es un ejemplo básico pero muy útil para entender la relación entre expresiones regulares, autómatas y procesamiento de texto.


