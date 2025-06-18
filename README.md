# Compilador VLS

Este es un compilador para el lenguaje VLS (Very Light Syntax), un lenguaje de programación educativo diseñado para operaciones matemáticas básicas.

## Características

- Análisis léxico
- Análisis sintáctico
- Análisis semántico
- Soporte para operaciones aritméticas básicas
- Declaración y asignación de variables
- Impresión de resultados en consola

## Estructura del Proyecto

```
.
├── src/
│   ├── lexer.py      # Analizador léxico
│   ├── parser.py     # Analizador sintáctico
│   ├── semantic.py   # Analizador semántico
│   └── main.py       # Punto de entrada
├── tests/            # Pruebas unitarias
└── examples/         # Ejemplos de código VLS
```

## Requisitos

- Python 3.8 o superior

## Uso

```bash
python src/main.py archivo.vls
```
