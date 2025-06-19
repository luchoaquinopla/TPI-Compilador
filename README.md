# Compilador VLS - Visualizador

## Definición del Lenguaje Propio: VLS
VLS (Visual Language Syntax) es un lenguaje de programación educativo, diseñado específicamente para este proyecto. Su sintaxis es simple, intuitiva y utiliza palabras en español para las operaciones aritméticas, lo que lo hace ideal para principiantes y para la enseñanza de conceptos de compiladores.

### Características del Lenguaje VLS
- **Palabras clave**: `var` para declarar variables, `print` para imprimir resultados.
- **Operadores en palabras**: `sumar`, `restar`, `multiplicar`, `dividir`, `potencia`.
- **Sintaxis clara y amigable**: Cada sentencia termina con punto y coma `;`.
- **Solo números enteros**: Facilita el análisis y la comprensión.

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
```

---

## Fases del Compilador Implementadas y Explicadas
El compilador VLS implementa y visualiza **tres fases fundamentales**:

### 1. Análisis Léxico
- Convierte el código fuente en una secuencia de tokens.
- Reconoce palabras clave, identificadores, números y operadores escritos como palabras.
- Ejemplo de tokens: `VAR`, `IDENTIFIER`, `SUMAR`, `NUMBER`, `SEMICOLON`.
- **Visualización**: En la GUI, se muestra la lista de tokens generados.

### 2. Análisis Sintáctico
- Construye el Árbol de Sintaxis Abstracta (AST) a partir de los tokens.
- Verifica la estructura gramatical del programa.
- Implementa precedencia y agrupación de operaciones.
- **Visualización**: El AST se muestra de forma jerárquica y animada en la GUI.

### 3. Análisis Semántico
- Verifica el uso correcto de variables y tipos.
- Detecta errores como variables no declaradas, operaciones inválidas, etc.
- **Visualización**: Muestra mensajes de éxito o errores semánticos en la GUI.

---

## Creatividad y Originalidad de la Propuesta
- **Lenguaje propio y visual**: VLS es un lenguaje inventado, con operadores en palabras y sintaxis amigable.
- **Interfaz gráfica animada**: Permite ver cada fase del compilador en tiempo real y de forma didáctica.
- **Modo paso a paso**: El usuario puede avanzar por cada fase para entender el proceso de compilación.
- **Errores explicativos**: Los errores se muestran de forma clara y contextualizada.
- **Pensado para educación**: Ideal para aprender compiladores y para quienes se inician en la programación.

---

## Aplicación de Conceptos Teóricos
Este proyecto aplica los principales conceptos de la teoría de compiladores:

- **Autómatas y análisis léxico**: El lexer implementa un autómata para reconocer tokens.
- **Gramáticas libres de contexto**: El parser sigue una gramática recursiva para construir el AST.
- **Árbol de Sintaxis Abstracta (AST)**: Representa la estructura jerárquica del programa.
- **Tabla de símbolos**: El análisis semántico mantiene una tabla para verificar declaraciones y usos de variables.
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
```

---

**¡Explora, aprende y visualiza cómo funciona un compilador paso a paso con VLS!**
