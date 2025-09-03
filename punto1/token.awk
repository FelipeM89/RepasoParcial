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
