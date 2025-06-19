import sys
import os
from typing import List, Dict, Any
from .parser import AST, BinOp, Num, Var, Assign, Mostrar, VarDecl
import graphviz

class DevelopmentTools:
    def __init__(self):
        self.debug_mode = False
        self.current_line = 0
        self.variables_state = {}
        self.execution_history = []

    def visualize_ast(self, ast: AST, output_file: str = "ast"):
        """Genera una visualización del AST usando graphviz."""
        dot = graphviz.Digraph(comment='AST Visualization')
        dot.attr(rankdir='TB')
        
        def add_node(node, parent_id=None):
            if isinstance(node, list):
                for child in node:
                    add_node(child, parent_id)
                return
            
            node_id = str(id(node))
            
            # Determinar el label del nodo
            if isinstance(node, BinOp):
                label = f"BinOp: {node.op.type}"
            elif isinstance(node, Num):
                label = f"Num: {node.value}"
            elif isinstance(node, Var):
                label = f"Var: {node.value}"
            elif isinstance(node, Assign):
                label = "Assign"
            elif isinstance(node, Mostrar):
                label = "Mostrar"
            elif isinstance(node, VarDecl):
                label = "VarDecl"
            else:
                label = str(type(node).__name__)
            
            dot.node(node_id, label)
            
            if parent_id:
                dot.edge(parent_id, node_id)
            
            # Agregar nodos hijos
            if isinstance(node, BinOp):
                add_node(node.left, node_id)
                add_node(node.right, node_id)
            elif isinstance(node, Assign):
                add_node(node.left, node_id)
                add_node(node.right, node_id)
            elif isinstance(node, Mostrar):
                add_node(node.expr, node_id)
            elif isinstance(node, VarDecl):
                add_node(node.var_node, node_id)
        
        add_node(ast)
        dot.render(output_file, view=True, format='png')

    def debug_step(self, node: AST, line_number: int):
        """Ejecuta un paso de depuración y registra el estado."""
        if not self.debug_mode:
            return
        
        self.current_line = line_number
        state = {
            'line': line_number,
            'node_type': type(node).__name__,
            'variables': self.variables_state.copy()
        }
        
        if isinstance(node, BinOp):
            state['operation'] = node.op.type
            state['left'] = self._get_node_value(node.left)
            state['right'] = self._get_node_value(node.right)
        elif isinstance(node, Assign):
            state['variable'] = node.left.value
            state['value'] = self._get_node_value(node.right)
        elif isinstance(node, Mostrar):
            state['value'] = self._get_node_value(node.expr)
        
        self.execution_history.append(state)
        self._print_debug_info(state)

    def _get_node_value(self, node: AST) -> Any:
        """Obtiene el valor de un nodo para depuración."""
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, Var):
            return self.variables_state.get(node.value, "undefined")
        elif isinstance(node, BinOp):
            left = self._get_node_value(node.left)
            right = self._get_node_value(node.right)
            if node.op.type == 'PLUS':
                return left + right
            elif node.op.type == 'MINUS':
                return left - right
            elif node.op.type == 'MULTIPLY':
                return left * right
            elif node.op.type == 'DIVIDE':
                return left / right
            elif node.op.type == 'POWER':
                return left ** right
        return None

    def _print_debug_info(self, state: Dict):
        """Imprime información de depuración."""
        print(f"\n=== Debug Info (Line {state['line']}) ===")
        print(f"Node Type: {state['node_type']}")
        
        if 'operation' in state:
            print(f"Operation: {state['operation']}")
            print(f"Left: {state['left']}")
            print(f"Right: {state['right']}")
        
        if 'variable' in state:
            print(f"Variable: {state['variable']}")
            print(f"Value: {state['value']}")
        
        if 'value' in state:
            print(f"Value: {state['value']}")
        
        print("\nVariables State:")
        for var, value in state['variables'].items():
            print(f"  {var} = {value}")
        print("=" * 30)

    def generate_example(self, concept: str) -> str:
        """Genera un ejemplo de código basado en un concepto específico."""
        examples = {
            'variables': """
var x;
var y;
x = 5;
y = 3;
print(x + y);
""",
            'operations': """
var resultado;
resultado = 5 + 3 * 2;
print(resultado);
""",
            'precedence': """
var a;
var b;
a = (5 + 3) * 2;
b = a ^ 2;
print(b);
"""
        }
        return examples.get(concept, "Concepto no encontrado")

    def export_execution_graph(self, output_file: str = "execution"):
        """Exporta un gráfico del flujo de ejecución."""
        if not self.execution_history:
            return
        
        dot = graphviz.Digraph(comment='Execution Flow')
        dot.attr(rankdir='TB')
        
        for i, state in enumerate(self.execution_history):
            node_id = f"step_{i}"
            label = f"Line {state['line']}\n{state['node_type']}"
            
            if 'operation' in state:
                label += f"\n{state['operation']}"
            elif 'variable' in state:
                label += f"\n{state['variable']} = {state['value']}"
            
            dot.node(node_id, label)
            
            if i > 0:
                dot.edge(f"step_{i-1}", node_id)
        
        dot.render(output_file, view=True, format='png')

    def start_debug(self):
        """Activa el modo de depuración."""
        self.debug_mode = True
        self.execution_history = []
        print("Modo de depuración activado")

    def stop_debug(self):
        """Desactiva el modo de depuración."""
        self.debug_mode = False
        print("Modo de depuración desactivado") 