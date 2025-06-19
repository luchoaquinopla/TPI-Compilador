# Compilador VLS - Visualizador

## Definición del Lenguaje Propio: VLS

VLS (Visual Language Syntax) es un lenguaje de programación educativo, diseñado específicamente para este proyecto. Su sintaxis es simple, intuitiva y utiliza palabras en español para las operaciones aritméticas, de cadenas y estructuras de control, lo que lo hace ideal para principiantes y para la enseñanza de conceptos de compiladores.

### Características del Lenguaje VLS

- **Palabras clave**: `var` para declarar variables, `print` para imprimir resultados, `si`, `entonces`, `fin_si`, `mientras`, `hacer`, `fin_mientras` para estructuras de control.
- **Operadores en palabras**: `sumar`, `restar`, `multiplicar`, `dividir`, `potencia`, **`concatenar`** para unir cadenas.
- **Soporte para cadenas**: Se pueden usar literales de texto entre comillas dobles (`"Hola"`), asignarlas a variables y operar con ellas.
- **Operadores de comparación**: `mayor`, `menor`, `igual`, `diferente`, `mayor_igual`, `menor_igual`.
- **Operadores lógicos**: `Y`, `O` (en mayúsculas para evitar conflicto con identificadores).
- **Sintaxis clara y amigable**: Cada sentencia simple termina con punto y coma `;`. El punto y coma es opcional después de bloques de control (`fin_si`, `fin_mientras`).
- **Solo números enteros y cadenas**: Facilita el análisis y la comprensión.

#### Ejemplo de código VLS

```vls
var x;
var y;
x = 5;
y = 3;
print(x sumar y);
print(x restar y);
print(x multiplicar y);
print(x dividir y);
print(x potencia 2);

// Operaciones con cadenas
var saludo;
saludo = "Hola";
var nombre;
nombre = "Mundo";
var mensaje;
mensaje = saludo concatenar " " concatenar nombre;
print(mensaje);

// Estructura condicional
si (x mayor y) entonces
    print(x);
fin_si;

// Estructura condicional compuesta
si (x mayor 0 Y y menor 10) entonces
    print(x sumar y);
fin_si;

// Bucle while
mientras (y mayor 0) hacer
    print(y);
    y = y restar 1;
fin_mientras;
```

---

## Fases del Compilador Implementadas y Explicadas

El compilador VLS implementa y visualiza **tres fases fundamentales**:

### 1. Análisis Léxico

- Convierte el código fuente en una secuencia de tokens.
- Reconoce palabras clave, identificadores, números, **cadenas** y operadores escritos como palabras.
- Ejemplo de tokens: `VAR`, `IDENTIFIER`, `SUMAR`, `NUMBER`, `STRING`, `CONCATENAR`, `SI`, `Y`, `MAYOR`, `SEMICOLON`.
- **Visualización**: En la GUI, se muestra la lista de tokens generados.

### 2. Análisis Sintáctico

- Construye el Árbol de Sintaxis Abstracta (AST) a partir de los tokens.
- Verifica la estructura gramatical del programa.
- Implementa precedencia y agrupación de operaciones, así como estructuras de control anidadas y operaciones con cadenas.
- **Visualización**: El AST se muestra de forma jerárquica y animada en la GUI.

### 3. Análisis Semántico

- Verifica el uso correcto de variables y tipos (números y cadenas).
- Detecta errores como variables no declaradas, operaciones inválidas, condiciones incorrectas, **concatenación solo entre cadenas**, etc.
- **Visualización**: Muestra mensajes de éxito o errores semánticos en la GUI, incluyendo el análisis de condiciones, operadores lógicos y operaciones con cadenas.

---

## Creatividad y Originalidad de la Propuesta

- **Lenguaje propio y visual**: VLS es un lenguaje inventado, con operadores y estructuras en palabras y sintaxis amigable.
- **Soporte para cadenas**: Permite manipular texto, concatenar cadenas y combinarlas con variables.
- **Estructuras de control**: Permite condicionales (`si ... entonces ... fin_si`) y bucles (`mientras ... hacer ... fin_mientras`), con condiciones compuestas usando operadores lógicos y de comparación.
- **Interfaz gráfica animada**: Permite ver cada fase del compilador en tiempo real y de forma didáctica.
- **Modo paso a paso**: El usuario puede avanzar por cada fase para entender el proceso de compilación.
- **Errores explicativos**: Los errores se muestran de forma clara y contextualizada.
- **Pensado para educación**: Ideal para aprender compiladores y para quienes se inician en la programación.

---

## Aplicación de Conceptos Teóricos

Este proyecto aplica los principales conceptos de la teoría de compiladores:

- **Autómatas y análisis léxico**: El lexer implementa un autómata para reconocer tokens, incluyendo cadenas.
- **Gramáticas libres de contexto**: El parser sigue una gramática recursiva para construir el AST, incluyendo estructuras de control, expresiones lógicas y operaciones con cadenas.
- **Árbol de Sintaxis Abstracta (AST)**: Representa la estructura jerárquica del programa.
- **Tabla de símbolos**: El análisis semántico mantiene una tabla para verificar declaraciones y usos de variables, y sus tipos (número o cadena).
- **Manejo de errores**: Cada fase detecta y reporta errores propios (léxicos, sintácticos, semánticos).
- **Visualización didáctica**: La GUI permite observar cómo se aplican estos conceptos en la práctica.

---

## Ejecución de la Interfaz Gráfica

Desde la carpeta raíz del proyecto, ejecuta:

```sh
python -m src.gui
```

---

## Ejemplo de error detectado

```vls
var x;
print(x sumar y);  // Error: 'y' no está declarada

var saludo;
saludo = "Hola";
var n;
n = 5;
print(saludo concatenar n); // Error: solo se pueden concatenar cadenas

si (x mayor z) entonces
    print(x);
fin_si;  // Error: 'z' no está declarada

mientras (x menor 0 Y y mayor 10) hacer
    print(x);
fin_mientras;
```

---

**¡Explora, aprende y visualiza cómo funciona un compilador paso a paso con VLS!**
