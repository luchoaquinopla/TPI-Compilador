import tkinter as tk
from tkinter import ttk, scrolledtext
import time
from typing import List, Dict
from lexer import Lexer, Token, TokenType
from parser import Parser, AST, BinOp, Num, Var, Assign, Print, VarDecl, Condition, LogicalOp, If, While
from semantic import SemanticAnalyzer
import threading
import math

class TokenCard:
    def __init__(self, canvas, token, x, y, width=140, height=60):
        self.canvas = canvas
        self.token = token
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = False
        self.animation_id = None
        
        # Colores para diferentes tipos de tokens
        self.colors = {
            TokenType.VAR: "#FF6B6B",           # Rojo claro
            TokenType.PRINT: "#4ECDC4",         # Turquesa
            TokenType.SI: "#45B7D1",            # Azul claro
            TokenType.ENTONCES: "#96CEB4",      # Verde claro
            TokenType.FIN_SI: "#FFEAA7",        # Amarillo claro
            TokenType.MIENTRAS: "#DDA0DD",      # Ciruela
            TokenType.HACER: "#98D8C8",         # Verde menta
            TokenType.FIN_MIENTRAS: "#F7DC6F",  # Amarillo
            TokenType.MAYOR: "#BB8FCE",         # Púrpura claro
            TokenType.MENOR: "#85C1E9",         # Azul cielo
            TokenType.IGUAL: "#F8C471",         # Naranja claro
            TokenType.DIFERENTE: "#F1948A",     # Rosa claro
            TokenType.MAYOR_IGUAL: "#A9CCE3",   # Azul grisáceo
            TokenType.MENOR_IGUAL: "#FAD7A0",   # Melocotón
            TokenType.Y: "#D7BDE2",             # Lavanda
            TokenType.O: "#A9DFBF",             # Verde lima
            TokenType.SUMAR: "#F9E79F",         # Amarillo crema
            TokenType.RESTAR: "#FADBD8",        # Rosa pálido
            TokenType.MULTIPLICAR: "#D5A6BD",   # Rosa grisáceo
            TokenType.DIVIDIR: "#A2D9CE",       # Verde azulado
            TokenType.POTENCIA: "#F7DC6F",      # Amarillo dorado
            TokenType.CONCATENAR: "#D2B4DE",    # Lavanda claro
            TokenType.NUMBER: "#82E0AA",        # Verde esmeralda
            TokenType.IDENTIFIER: "#F8C471",    # Naranja
            TokenType.ASSIGN: "#85C1E9",        # Azul
            TokenType.LPAREN: "#F1948A",        # Rosa
            TokenType.RPAREN: "#F1948A",        # Rosa
            TokenType.SEMICOLON: "#BB8FCE",     # Púrpura
            TokenType.STRING: "#F7DC6F",        # Amarillo
            TokenType.EOF: "#BDC3C7"            # Gris
        }
        
        self.bg_color = self.colors.get(token.type, "#BDC3C7")
        
    def create_card(self):
        # Fondo de la tarjeta
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=self.bg_color, outline="#2C3E50", width=2
        )
        # Tipo de token (centrado arriba)
        type_text = str(self.token.type).replace('TokenType.', '')
        # Hacer más descriptivos algunos tokens
        if type_text == "SEMICOLON":
            type_text = "Punto y coma"
        elif type_text == "LPAREN":
            type_text = "Paréntesis ("
        elif type_text == "RPAREN":
            type_text = "Paréntesis )"
        elif type_text == "ASSIGN":
            type_text = "Asignación"
        elif type_text == "IDENTIFIER":
            type_text = "Identificador"
        elif type_text == "NUMBER":
            type_text = "Número"
        elif type_text == "STRING":
            type_text = "Cadena"
        elif type_text == "EOF":
            type_text = "Fin de archivo"
            
        self.type_text = self.canvas.create_text(
            self.x + self.width // 2, self.y + 18,
            text=type_text,
            font=("Arial", 11, "bold"), fill="#2C3E50"
        )
        # Valor del token (centrado medio)
        value_text = str(self.token.value) if self.token.value is not None else "None"
        if len(value_text) > 15:
            value_text = value_text[:12] + "..."
        self.value_text = self.canvas.create_text(
            self.x + self.width // 2, self.y + 38,
            text=value_text,
            font=("Arial", 10), fill="#34495E"
        )

    def animate_appear(self, delay=0):
        def fade_in():
            # Aparecer gradualmente (simulado con cambios de color)
            steps = 10
            for i in range(steps):
                alpha = int(255 * (i + 1) / steps)
                # No hay alpha real en Tkinter, pero podemos simular con update y delay
                self.canvas.itemconfig(self.rect, state="normal")
                self.canvas.itemconfig(self.type_text, state="normal")
                self.canvas.itemconfig(self.value_text, state="normal")
                self.canvas.update()
                time.sleep(0.03)
            self.visible = True
        # Inicialmente oculto
        self.canvas.itemconfig(self.rect, state="hidden")
        self.canvas.itemconfig(self.type_text, state="hidden")
        self.canvas.itemconfig(self.value_text, state="hidden")
        def show():
            self.canvas.itemconfig(self.rect, state="normal")
            self.canvas.itemconfig(self.type_text, state="normal")
            self.canvas.itemconfig(self.value_text, state="normal")
            fade_in()
        if delay > 0:
            self.animation_id = self.canvas.after(int(delay * 1000), show)
        else:
            show()

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador VLS - Visualizador")
        self.root.geometry("1400x900")
        
        # Variables
        self.source_code = ""
        self.tokens = []
        self.ast = None
        self.current_phase = 0
        self.is_running = False
        self.token_cards = []
        
        self.setup_gui()
        
    def setup_gui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Editor de código
        code_frame = ttk.LabelFrame(main_frame, text="Código Fuente", padding="5")
        code_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.code_editor = scrolledtext.ScrolledText(code_frame, width=60, height=8)
        self.code_editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones de control
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(control_frame, text="Compilar", command=self.start_compilation).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Paso a Paso", command=self.step_by_step).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Reiniciar", command=self.reset).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Limpiar Tokens", command=self.clear_tokens).grid(row=0, column=3, padx=5)
        
        # Frame para ejemplos
        examples_frame = ttk.LabelFrame(main_frame, text="Ejemplos", padding="5")
        examples_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(examples_frame, text="Ejemplo Simple", command=lambda: self.load_example("examples/test_simple.vls")).grid(row=0, column=0, padx=5)
        ttk.Button(examples_frame, text="Ejemplo Completo", command=lambda: self.load_example("examples/test_tokens.vls")).grid(row=0, column=1, padx=5)
        ttk.Button(examples_frame, text="Estructuras Control", command=lambda: self.load_example("examples/estructuras_control.vls")).grid(row=0, column=2, padx=5)
        ttk.Button(examples_frame, text="Operaciones", command=lambda: self.load_example("examples/operaciones.vls")).grid(row=0, column=3, padx=5)
        
        # Fases del compilador
        phases_frame = ttk.Frame(main_frame, padding="5")
        phases_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Análisis Léxico con visualización de tokens
        lex_frame = ttk.LabelFrame(phases_frame, text="Análisis Léxico - Visualización de Tokens", padding="5")
        lex_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Canvas para tokens animados
        self.token_canvas = tk.Canvas(lex_frame, width=400, height=300, bg="white", relief="sunken", bd=2)
        self.token_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para el canvas
        token_scrollbar = ttk.Scrollbar(lex_frame, orient="vertical", command=self.token_canvas.yview)
        token_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.token_canvas.configure(yscrollcommand=token_scrollbar.set)
        
        # Output tradicional del análisis léxico
        lex_output_frame = ttk.LabelFrame(phases_frame, text="Output Léxico", padding="5")
        lex_output_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.lex_output = scrolledtext.ScrolledText(lex_output_frame, width=30, height=15)
        self.lex_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Análisis Sintáctico
        parse_frame = ttk.LabelFrame(phases_frame, text="Análisis Sintáctico", padding="5")
        parse_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.parse_output = scrolledtext.ScrolledText(parse_frame, width=40, height=15)
        self.parse_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Análisis Semántico
        sem_frame = ttk.LabelFrame(phases_frame, text="Análisis Semántico", padding="5")
        sem_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.sem_output = scrolledtext.ScrolledText(sem_frame, width=40, height=10)
        self.sem_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, length=1000, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        phases_frame.columnconfigure(0, weight=1)
        phases_frame.columnconfigure(1, weight=1)
        phases_frame.columnconfigure(2, weight=1)
        lex_frame.columnconfigure(0, weight=1)
        lex_frame.rowconfigure(0, weight=1)
        lex_output_frame.columnconfigure(0, weight=1)
        lex_output_frame.rowconfigure(0, weight=1)
        
    def clear_tokens(self):
        """Limpiar todas las tarjetas de tokens del canvas"""
        self.token_canvas.delete("all")
        self.token_cards = []
        
    def add_token_card(self, token, delay=0):
        """Agregar una nueva tarjeta de token al canvas"""
        cards_per_row = 3
        card_width = 140
        card_height = 60
        margin_x = 30
        margin_y = 20
        num_cards = len(self.token_cards)
        row = num_cards // cards_per_row
        col = num_cards % cards_per_row
        x = col * (card_width + margin_x) + margin_x
        y = row * (card_height + margin_y) + margin_y
        card = TokenCard(self.token_canvas, token, x, y, card_width, card_height)
        card.create_card()
        self.token_canvas.itemconfig(card.rect, state="hidden")
        self.token_canvas.itemconfig(card.type_text, state="hidden")
        self.token_canvas.itemconfig(card.value_text, state="hidden")
        self.token_cards.append(card)
        card.animate_appear(delay)
        total_height = (row + 1) * (card_height + margin_y) + margin_y
        self.token_canvas.configure(scrollregion=(0, 0, 500, total_height))
        return card
    
    def load_example(self, filename):
        """Cargar un ejemplo desde un archivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert("1.0", content)
            self.clear_tokens()  # Limpiar tokens anteriores
            self.lex_output.delete("1.0", tk.END)
            self.parse_output.delete("1.0", tk.END)
            self.sem_output.delete("1.0", tk.END)
            self.progress['value'] = 0
        except FileNotFoundError:
            self.lex_output.delete("1.0", tk.END)
            self.lex_output.insert(tk.END, f"Error: No se encontró el archivo {filename}\n")
        except Exception as e:
            self.lex_output.delete("1.0", tk.END)
            self.lex_output.insert(tk.END, f"Error al cargar el archivo: {str(e)}\n")
    
    def show_token_statistics(self, tokens):
        """Mostrar estadísticas de los tokens generados"""
        token_types = {}
        for token in tokens:
            type_name = str(token.type).replace('TokenType.', '')
            token_types[type_name] = token_types.get(type_name, 0) + 1
        
        self.lex_output.insert(tk.END, "\n📊 Estadísticas de Tokens:\n")
        self.lex_output.insert(tk.END, "-" * 30 + "\n")
        for token_type, count in sorted(token_types.items()):
            self.lex_output.insert(tk.END, f"{token_type:15}: {count:2d}\n")
        self.lex_output.insert(tk.END, "-" * 30 + "\n")
        self.lex_output.insert(tk.END, f"Total de tipos únicos: {len(token_types)}\n")
        self.lex_output.see(tk.END)
    
    def start_compilation(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.reset()
        self.source_code = self.code_editor.get("1.0", tk.END)
        
        # Iniciar compilación en un hilo separado
        thread = threading.Thread(target=self.run_compilation)
        thread.start()
        
    def run_compilation(self):
        try:
            # Limpiar tokens anteriores
            self.clear_tokens()
            
            # Fase 1: Análisis Léxico
            self.update_progress(0)
            self.lex_output.delete("1.0", tk.END)
            self.lex_output.insert(tk.END, "Iniciando análisis léxico...\n\n")
            self.lex_output.see(tk.END)
            self.root.update()
            
            lexer = Lexer(self.source_code)
            tokens = []
            token_count = 0
            
            while True:
                token = lexer.get_next_token()
                tokens.append(token)
                token_count += 1
                
                # Agregar token al output tradicional
                self.lex_output.insert(tk.END, f"Token {token_count}: {token}\n")
                self.lex_output.see(tk.END)
                
                # Agregar tarjeta animada al canvas
                delay = token_count * 0.3  # Delay progresivo para efecto cascada
                self.add_token_card(token, delay)
                
                self.root.update()
                time.sleep(0.2)  # Pausa para ver la animación
                
                if token.type.name == 'EOF':
                    break
            
            self.lex_output.insert(tk.END, f"\n✅ Análisis léxico completado. {token_count} tokens generados.\n")
            self.lex_output.see(tk.END)
            
            # Mostrar estadísticas de tokens
            self.show_token_statistics(tokens)

            # Fase 2: Análisis Sintáctico
            self.update_progress(33)
            self.parse_output.delete("1.0", tk.END)
            self.parse_output.insert(tk.END, f"Código fuente recibido:\n{self.source_code}\n\n")
            self.parse_output.insert(tk.END, f"Tokens generados ({token_count} tokens):\n")
            for i, t in enumerate(tokens, 1):
                self.parse_output.insert(tk.END, f"{i:2d}. {t}\n")
            self.parse_output.insert(tk.END, "\n")
            
            # Volver a crear el lexer para el parser
            lexer_for_parser = Lexer(self.source_code)
            try:
                self.parse_output.insert(tk.END, "Iniciando análisis sintáctico...\n")
                self.parse_output.see(tk.END)
                self.root.update()
                
                parser = Parser(lexer_for_parser)
                self.parse_output.insert(tk.END, "Parser creado, generando AST...\n")
                self.parse_output.see(tk.END)
                self.root.update()
                
                self.ast = parser.program()
                self.parse_output.insert(tk.END, f"AST generado exitosamente con {len(self.ast) if isinstance(self.ast, list) else 1} nodos principales\n")
                self.parse_output.insert(tk.END, f"AST generado (estructura):\n")
            except Exception as e:
                self.parse_output.insert(tk.END, f"Error en el parser: {str(e)}\n")
                self.parse_output.insert(tk.END, f"Tipo de error: {type(e).__name__}\n")
                import traceback
                self.parse_output.insert(tk.END, f"Traceback completo:\n{traceback.format_exc()}\n")
                self.is_running = False
                return
            def print_ast(node, level=0):
                if isinstance(node, list):
                    for child in node:
                        print_ast(child, level)
                    return
                indent = "  " * level
                if isinstance(node, BinOp):
                    info = f"{type(node).__name__}: {node.op.type}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.left, level + 1)
                    print_ast(node.right, level + 1)
                elif isinstance(node, Num):
                    info = f"{type(node).__name__}: {node.value}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                elif isinstance(node, Var):
                    info = f"{type(node).__name__}: {node.value}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                elif isinstance(node, Assign):
                    info = f"{type(node).__name__}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.left, level + 1)
                    print_ast(node.right, level + 1)
                elif isinstance(node, Print):
                    info = f"{type(node).__name__}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.expr, level + 1)
                elif isinstance(node, VarDecl):
                    info = f"{type(node).__name__}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.var_node, level + 1)
                elif isinstance(node, Condition):
                    info = f"{type(node).__name__}: {node.op.type}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.left, level + 1)
                    print_ast(node.right, level + 1)
                elif isinstance(node, LogicalOp):
                    info = f"{type(node).__name__}: {node.op.type}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.left, level + 1)
                    print_ast(node.right, level + 1)
                elif isinstance(node, If):
                    info = f"{type(node).__name__}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.condition, level + 1)
                    for stmt in node.then_body:
                        print_ast(stmt, level + 1)
                    if node.else_body:
                        for stmt in node.else_body:
                            print_ast(stmt, level + 1)
                elif isinstance(node, While):
                    info = f"{type(node).__name__}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
                    print_ast(node.condition, level + 1)
                    for stmt in node.body:
                        print_ast(stmt, level + 1)
                else:
                    info = f"{type(node).__name__}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
            if not self.ast:
                self.parse_output.insert(tk.END, "¡El AST está vacío!\n")
            elif isinstance(self.ast, list):
                for node in self.ast:
                    print_ast(node)
            else:
                print_ast(self.ast)
            
            # Fase 3: Análisis Semántico
            self.update_progress(66)
            self.sem_output.delete("1.0", tk.END)
            semantic_analyzer = SemanticAnalyzer()
            
            def analyze_node(node):
                if isinstance(node, list):
                    for child in node:
                        analyze_node(child)
                    return
                
                self.sem_output.insert(tk.END, f"Analizando: {type(node).__name__}\n")
                self.sem_output.see(tk.END)
                self.root.update()
                time.sleep(0.1)

                # Llama al visit y luego recorre los hijos manualmente para mostrar todos los nodos
                semantic_analyzer.visit(node)
                # Recorre hijos explícitamente para mostrar todos los nodos
                if hasattr(node, 'left'):
                    analyze_node(node.left)
                if hasattr(node, 'right'):
                    analyze_node(node.right)
                if hasattr(node, 'expr'):
                    analyze_node(node.expr)
                if hasattr(node, 'var_node'):
                    analyze_node(node.var_node)
                if hasattr(node, 'condition'):
                    analyze_node(node.condition)
                if hasattr(node, 'then_body'):
                    for stmt in node.then_body:
                        analyze_node(stmt)
                if hasattr(node, 'body'):
                    for stmt in node.body:
                        analyze_node(stmt)
            
            analyze_node(self.ast)
            
            self.update_progress(100)
            self.sem_output.insert(tk.END, "\n¡Análisis semántico completado con éxito!\n")
            
        except Exception as e:
            self.sem_output.insert(tk.END, f"\nError: {str(e)}\n")
        finally:
            self.is_running = False
    
    def step_by_step(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.reset()
        self.source_code = self.code_editor.get("1.0", tk.END)
        
        # Iniciar compilación paso a paso en un hilo separado
        thread = threading.Thread(target=self.run_step_by_step)
        thread.start()
    
    def run_step_by_step(self):
        try:
            # Fase 1: Análisis Léxico
            self.update_progress(0)
            self.lex_output.delete("1.0", tk.END)
            lexer = Lexer(self.source_code)
            
            while True:
                token = lexer.get_next_token()
                self.lex_output.insert(tk.END, f"{token}\n")
                self.lex_output.see(tk.END)
                self.root.update()
                time.sleep(0.5)  # Más lento para paso a paso
                
                if token.type.name == 'EOF':
                    break
            
            # Fase 2: Análisis Sintáctico
            self.update_progress(33)
            self.parse_output.delete("1.0", tk.END)
            parser = Parser(lexer)
            self.ast = parser.program()
            
            def print_ast_step(node, level=0):
                if isinstance(node, list):
                    for child in node:
                        print_ast_step(child, level)
                    return
                indent = "  " * level
                # Mostrar tipo y contenido relevante
                if hasattr(node, 'token') and hasattr(node.token, 'value'):
                    info = f"{type(node).__name__}: {getattr(node.token, 'value', '')}"
                elif hasattr(node, 'value'):
                    info = f"{type(node).__name__}: {getattr(node, 'value', '')}"
                elif hasattr(node, 'op') and hasattr(node.op, 'type'):
                    info = f"{type(node).__name__}: {node.op.type}"
                else:
                    info = f"{type(node).__name__}"
                self.parse_output.insert(tk.END, f"{indent}{info}\n")
                self.parse_output.see(tk.END)
                self.root.update()
                time.sleep(0.5)
                # Recorrer hijos
                if hasattr(node, 'left') and hasattr(node, 'right'):
                    print_ast_step(node.left, level + 1)
                    print_ast_step(node.right, level + 1)
                elif hasattr(node, 'expr'):
                    print_ast_step(node.expr, level + 1)
                elif hasattr(node, 'var_node'):
                    print_ast_step(node.var_node, level + 1)
            
            if isinstance(self.ast, list):
                for node in self.ast:
                    print_ast_step(node)
            else:
                print_ast_step(self.ast)
            
            # Fase 3: Análisis Semántico
            self.update_progress(66)
            self.sem_output.delete("1.0", tk.END)
            semantic_analyzer = SemanticAnalyzer()
            
            def analyze_node_step(node):
                if isinstance(node, list):
                    for child in node:
                        analyze_node_step(child)
                    return
                
                self.sem_output.insert(tk.END, f"Analizando: {type(node).__name__}\n")
                self.sem_output.see(tk.END)
                self.root.update()
                time.sleep(0.5)  # Más lento para paso a paso
                
                if isinstance(node, (BinOp, Num, Var, Assign, Print, VarDecl, Condition, LogicalOp, If, While)):
                    semantic_analyzer.visit(node)
            
            analyze_node_step(self.ast)
            
            self.update_progress(100)
            self.sem_output.insert(tk.END, "\n¡Análisis semántico completado con éxito!\n")
            
        except Exception as e:
            self.sem_output.insert(tk.END, f"\nError: {str(e)}\n")
        finally:
            self.is_running = False
    
    def reset(self):
        self.lex_output.delete("1.0", tk.END)
        self.parse_output.delete("1.0", tk.END)
        self.sem_output.delete("1.0", tk.END)
        self.progress['value'] = 0
        self.current_phase = 0
        self.tokens = []
        self.ast = None
    
    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update()

def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 