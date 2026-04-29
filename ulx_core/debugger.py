#!/usr/bin/env python3
"""
ULX Debugger - Depurador interativo
"""

import sys
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum, auto

from .parser import ASTNode, Program, FunctionDef, FunctionCall, Assignment
from .interpreter import Interpreter


class DebugAction(Enum):
    CONTINUE = auto()
    STEP_OVER = auto()
    STEP_INTO = auto()
    STEP_OUT = auto()
    STOP = auto()


@dataclass
class Breakpoint:
    """Ponto de interrupção"""
    line: int
    filename: Optional[str] = None
    condition: Optional[str] = None
    hit_count: int = 0
    enabled: bool = True
    
    def should_break(self, context: Dict) -> bool:
        if not self.enabled:
            return False
        self.hit_count += 1
        if self.condition:
            # Avalia condição
            try:
                return eval(self.condition, {}, context)
            except:
                return True
        return True


@dataclass
class StackFrame:
    """Frame da pilha de chamadas"""
    function_name: str
    line: int
    filename: Optional[str] = None
    locals: Dict[str, Any] = field(default_factory=dict)


class ULXDebugger:
    """Depurador ULX"""
    
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.breakpoints: Dict[int, Breakpoint] = {}
        self.call_stack: List[StackFrame] = []
        self.current_line = 0
        self.current_file = None
        self.action = DebugAction.STOP
        self.step_depth = 0
        self.watches: List[str] = []
        self.history: List[str] = []
        
    def add_breakpoint(self, line: int, filename: str = None, condition: str = None):
        """Adiciona ponto de interrupção"""
        bp = Breakpoint(line=line, filename=filename, condition=condition)
        self.breakpoints[line] = bp
        print(f"Breakpoint adicionado na linha {line}")
        
    def remove_breakpoint(self, line: int):
        """Remove ponto de interrupção"""
        if line in self.breakpoints:
            del self.breakpoints[line]
            print(f"Breakpoint removido da linha {line}")
        
    def list_breakpoints(self):
        """Lista breakpoints"""
        print("\nBreakpoints:")
        for line, bp in self.breakpoints.items():
            status = "✓" if bp.enabled else "✗"
            cond = f" (cond: {bp.condition})" if bp.condition else ""
            print(f"  [{status}] Linha {line}{cond} - hits: {bp.hit_count}")
        
    def add_watch(self, expr: str):
        """Adiciona expressão para observação"""
        self.watches.append(expr)
        print(f"Watch adicionado: {expr}")
        
    def show_watches(self):
        """Mostra valores observados"""
        print("\nWatches:")
        for watch in self.watches:
            try:
                value = self.interpreter.environment.get(watch)
                print(f"  {watch} = {value}")
            except:
                print(f"  {watch} = <undefined>")
                
    def show_stack(self):
        """Mostra pilha de chamadas"""
        print("\nCall Stack:")
        for i, frame in enumerate(reversed(self.call_stack)):
            print(f"  #{i}: {frame.function_name} (linha {frame.line})")
            
    def show_locals(self):
        """Mostra variáveis locais"""
        print("\nVariáveis Locais:")
        for name, value in self.interpreter.environment.variables.items():
            print(f"  {name} = {value}")
            
    def step(self, action: DebugAction):
        """Define ação de passo"""
        self.action = action
        
    def check_breakpoint(self, node: ASTNode) -> bool:
        """Verifica se deve parar neste nó"""
        line = getattr(node, 'line', 0)
        
        if line in self.breakpoints:
            bp = self.breakpoints[line]
            context = self.interpreter.environment.variables
            if bp.should_break(context):
                self.current_line = line
                self._show_debug_prompt(node)
                return True
        return False
        
    def _show_debug_prompt(self, node: ASTNode):
        """Mostra prompt de depuração"""
        print(f"\n[DEBUG] Linha {self.current_line}: {type(node).__name__}")
        self.show_locals()
        self.show_watches()
        
        while True:
            try:
                cmd = input("(dbg) ").strip().lower()
                
                if cmd in ('c', 'continue', 'continuar'):
                    self.action = DebugAction.CONTINUE
                    break
                elif cmd in ('n', 'next', 'proximo'):
                    self.action = DebugAction.STEP_OVER
                    break
                elif cmd in ('s', 'step', 'entrar'):
                    self.action = DebugAction.STEP_INTO
                    break
                elif cmd in ('o', 'out', 'sair'):
                    self.action = DebugAction.STEP_OUT
                    break
                elif cmd in ('q', 'quit', 'parar'):
                    self.action = DebugAction.STOP
                    sys.exit(0)
                elif cmd in ('b', 'break'):
                    line = int(input("Linha: "))
                    self.add_breakpoint(line)
                elif cmd in ('l', 'list'):
                    self.list_breakpoints()
                elif cmd in ('w', 'watch'):
                    expr = input("Expressão: ")
                    self.add_watch(expr)
                elif cmd in ('p', 'print'):
                    self.show_locals()
                elif cmd in ('s', 'stack'):
                    self.show_stack()
                elif cmd == 'help' or cmd == 'ajuda':
                    self._show_help()
                else:
                    # Tenta avaliar como expressão
                    try:
                        value = eval(cmd, {}, self.interpreter.environment.variables)
                        print(f"  => {value}")
                    except:
                        print("Comando desconhecido. Digite 'ajuda' para ajuda.")
                        
            except (EOFError, KeyboardInterrupt):
                print()
                break
                
    def _show_help(self):
        print("""
Comandos do Debugger:
  (c)ontinue  - Continua execução
  (n)ext      - Passa por cima (step over)
  (s)tep      - Entra na função (step into)
  (o)ut       - Sai da função (step out)
  (q)uit      - Para execução
  (b)reak     - Adiciona breakpoint
  (l)ist      - Lista breakpoints
  (w)atch     - Adiciona watch
  (p)rint     - Mostra variáveis
  stack       - Mostra pilha de chamadas
  <expr>      - Avalia expressão
        """)
        
    def run_with_debug(self, program: Program):
        """Executa programa com depuração"""
        print("Iniciando execução com debug...")
        self.action = DebugAction.STEP_OVER
        
        for stmt in program.statements:
            if self.check_breakpoint(stmt):
                if self.action == DebugAction.STOP:
                    break
            try:
                self.interpreter.interpret(stmt)
            except Exception as e:
                print(f"[ERRO] {e}")
                self._show_debug_prompt(stmt)
