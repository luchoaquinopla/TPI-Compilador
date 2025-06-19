import tkinter as tk
from tkinter import ttk, scrolledtext
import time
from typing import List, Dict
from .lexer import Lexer, Token
from .parser import Parser, AST, BinOp, Num, Var, Assign, Print, VarDecl
from .semantic import SemanticAnalyzer
import threading

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador VLS - Visualizador")
        self.root.geometry("1200x800")
        
        # Variables
        self.source_code = ""
        self.tokens = []
        self.ast = None
        self.current_phase = 0
        self.is_running = False
        
        self.setup_gui()
        
    def setup_gui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Editor de código
        code_frame = ttk.LabelFrame(main_frame, text="Código Fuente", padding="5")
        code_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.code_editor = scrolledtext.ScrolledText(code_frame, width=60, height=10)
        self.code_editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.code_editor.insert(tk.END, """var x;
var y;
x = 5;
y = 3;
print(x + y);""")
        
        # Botones de control
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(control_frame, text="Compilar", command=self.start_compilation).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Paso a Paso", command=self.step_by_step).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Reiniciar", command=self.reset).grid(row=0, column=2, padx=5)
        
        # Fases del compilador
        phases_frame = ttk.Frame(main_frame, padding="5")
        phases_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Análisis Léxico
        lex_frame = ttk.LabelFrame(phases_frame, text="Análisis Léxico", padding="5")
        lex_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.lex_output = scrolledtext.ScrolledText(lex_frame, width=40, height=15)
        self.lex_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Análisis Sintáctico
        parse_frame = ttk.LabelFrame(phases_frame, text="Análisis Sintáctico", padding="5")
        parse_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.parse_output = scrolledtext.ScrolledText(parse_frame, width=40, height=15)
        self.parse_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Análisis Semántico
        sem_frame = ttk.LabelFrame(phases_frame, text="Análisis Semántico", padding="5")
        sem_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.sem_output = scrolledtext.ScrolledText(sem_frame, width=40, height=15)
        self.sem_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, length=1000, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        phases_frame.columnconfigure(0, weight=1)
        phases_frame.columnconfigure(1, weight=1)
        phases_frame.columnconfigure(2, weight=1)
        
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
            # Fase 1: Análisis Léxico
            self.update_progress(0)
            self.lex_output.delete("1.0", tk.END)
            lexer = Lexer(self.source_code)
            tokens = []
            while True:
                token = lexer.get_next_token()
                tokens.append(token)
                self.lex_output.insert(tk.END, f"{token}\n")
                self.lex_output.see(tk.END)
                self.root.update()
                time.sleep(0.1)
                if token.type.name == 'EOF':
                    break

            # Fase 2: Análisis Sintáctico
            self.update_progress(33)
            self.parse_output.delete("1.0", tk.END)
            self.parse_output.insert(tk.END, f"Código fuente recibido:\n{self.source_code}\n\n")
            self.parse_output.insert(tk.END, "Tokens generados:\n")
            for t in tokens:
                self.parse_output.insert(tk.END, f"{t}\n")
            self.parse_output.insert(tk.END, "\n")
            # Volver a crear el lexer para el parser
            lexer_for_parser = Lexer(self.source_code)
            try:
                parser = Parser(lexer_for_parser)
                self.ast = parser.program()
                self.parse_output.insert(tk.END, f"AST generado (estructura):\n")
            except Exception as e:
                self.parse_output.insert(tk.END, f"Error en el parser: {str(e)}\n")
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
                else:
                    info = f"{type(node).__name__}"
                    self.parse_output.insert(tk.END, f"{indent}{info}\n")
                    self.parse_output.see(tk.END)
                    self.root.update()
                    time.sleep(0.1)
            if isinstance(self.ast, list):
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
                
                if isinstance(node, (BinOp, Num, Var, Assign, Print, VarDecl)):
                    semantic_analyzer.visit(node)
            
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
                
                if isinstance(node, (BinOp, Num, Var, Assign, Print, VarDecl)):
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