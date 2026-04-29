#!/usr/bin/env python3
"""
ULX REPL - Read-Eval-Print Loop Interativo
"""

import sys
import os
from typing import Optional, List

from .lexer import Lexer
from .parser import Parser, Program
from .interpreter import Interpreter
from .logger import ULXLogger, LogLevel
from .errors import ULXError


class ULXRepl:
    """REPL interativo para ULX"""
    
    BANNER = """
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║   ██╗   ██╗██╗     ███████╗                   ║
    ║   ██║   ██║██║     ██╔════╝                   ║
    ║   ██║   ██║██║     ███████╗                   ║
    ║   ██║   ██║██║     ╚════██║                   ║
    ║   ╚██████╔╝███████╗███████║                   ║
    ║    ╚═════╝ ╚══════╝╚══════╝                   ║
    ║                                               ║
    ║   REPL Interativo v4.0                        ║
    ║   Digite 'ajuda' para comandos                ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    
    HELP_TEXT = """
Comandos do REPL:
  :ajuda, :h          - Mostra esta ajuda
  :sair, :q           - Sai do REPL
  :limpar, :c         - Limpa a tela
  :vars               - Lista variáveis definidas
  :funcs              - Lista funções definidas
  :historico          - Mostra histórico
  :carregar <arquivo> - Carrega arquivo .ulx
  :salvar <arquivo>   - Salva sessão em arquivo
  :ast <codigo>       - Mostra AST do código
  :tokens <codigo>    - Mostra tokens do código
  :modo <basico|avançado> - Altera modo
  :verbose            - Alterna modo verbose

Atalhos:
  Ctrl+D, :q          - Sair
  Tab                 - Auto-completar
  Seta cima/baixo     - Histórico
    """
    
    def __init__(self, verbose: bool = False):
        self.logger = ULXLogger(level=LogLevel.INFO if not verbose else LogLevel.DEBUG)
        self.interpreter = Interpreter(logger=self.logger)
        self.history: List[str] = []
        self.multiline_buffer: List[str] = []
        self.in_multiline = False
        self.verbose = verbose
        self.prompt = "ulx> "
        self.continue_prompt = "...> "
        
        try:
            import readline
            self.readline = readline
            readline.parse_and_bind('tab: complete')
            readline.set_completer(self._completer)
        except ImportError:
            self.readline = None
    
    def _completer(self, text, state):
        """Auto-completar para readline"""
        keywords = [
            'escreva', 'leia', 'se', 'senao', 'enquanto', 'para',
            'funcao', 'retorna', 'pare', 'continua', 'tente', 'pegue',
            'finalmente', 'lanca', 'importe', 'classe', 'verdadeiro',
            'falso', 'nulo', 'e', 'ou', 'nao'
        ]
        builtins = list(self.interpreter.globals.variables.keys())
        
        all_completions = keywords + builtins
        matches = [w for w in all_completions if w.startswith(text.lower())]
        
        if state < len(matches):
            return matches[state]
        return None
    
    def _print_banner(self):
        print(self.BANNER)
    
    def _print_result(self, result):
        if result is not None:
            print(f"  => {self._format_value(result)}")
    
    def _format_value(self, value) -> str:
        if isinstance(value, bool):
            return f"{value} (bool)"
        elif isinstance(value, (int, float)):
            return f"{value} ({type(value).__name__})"
        elif isinstance(value, str):
            return f'"{value}" (string, len={len(value)})'
        elif isinstance(value, list):
            preview = str(value[:5])[:-1] + (", ...]" if len(value) > 5 else "]")
            return f"{preview} (lista, len={len(value)})"
        elif isinstance(value, dict):
            return f"{value} (dicionario, {len(value)} items)"
        return f"{value} ({type(value).__name__})"
    
    def _handle_command(self, line: str) -> bool:
        """Processa comandos especiais do REPL. Retorna True se deve continuar."""
        line = line.strip()
        
        if not line.startswith(':'):
            return False
        
        parts = line[1:].split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if cmd in ('sair', 'q', 'quit'):
            print("Até logo!")
            return True
        
        elif cmd in ('ajuda', 'h', 'help'):
            print(self.HELP_TEXT)
        
        elif cmd in ('limpar', 'c', 'clear'):
            os.system('clear' if os.name != 'nt' else 'cls')
            self._print_banner()
        
        elif cmd == 'vars':
            self._show_vars()
        
        elif cmd == 'funcs':
            self._show_funcs()
        
        elif cmd == 'historico':
            self._show_history()
        
        elif cmd == 'carregar':
            self._load_file(arg)
        
        elif cmd == 'salvar':
            self._save_session(arg)
        
        elif cmd == 'ast':
            self._show_ast(arg)
        
        elif cmd == 'tokens':
            self._show_tokens(arg)
        
        elif cmd == 'modo':
            self._set_mode(arg)
        
        elif cmd == 'verbose':
            self.verbose = not self.verbose
            print(f"Verbose: {'ligado' if self.verbose else 'desligado'}")
        
        else:
            print(f"Comando desconhecido: {cmd}")
        
        return False
    
    def _show_vars(self):
        print(f"\n{'='*40}")
        print("Variáveis definidas:")
        print(f"{'='*40}")
        for name, value in self.interpreter.environment.variables.items():
            if not name.startswith('_'):
                print(f"  {name:20} = {self._format_value(value)}")
        print()
    
    def _show_funcs(self):
        print(f"\n{'='*40}")
        print("Funções definidas:")
        print(f"{'='*40}")
        for name, func in self.interpreter.functions.items():
            params = ", ".join(p['name'] for p in func.params)
            print(f"  {name}({params})")
        
        print("\nFunções built-in:")
        builtins = [k for k, v in self.interpreter.globals.variables.items() 
                   if callable(v) and k not in self.interpreter.functions]
        for name in sorted(builtins):
            print(f"  {name}()")
        print()
    
    def _show_history(self):
        print(f"\n{'='*40}")
        print("Histórico:")
        print(f"{'='*40}")
        for i, entry in enumerate(self.history[-20:], 1):
            print(f"  {i:3}: {entry[:60]}")
        print()
    
    def _load_file(self, filename: str):
        if not filename:
            print("Uso: :carregar <arquivo.ulx>")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                source = f.read()
            
            lexer = Lexer(source, filename)
            tokens = lexer.tokenize()
            parser = Parser(tokens, source, filename)
            program = parser.parse()
            
            if parser.has_errors():
                parser.errors.print_summary()
                return
            
            self.interpreter.execute(program)
            print(f"Arquivo '{filename}' carregado com sucesso!")
            
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {filename}")
        except Exception as e:
            print(f"Erro ao carregar: {e}")
    
    def _save_session(self, filename: str):
        if not filename:
            print("Uso: :salvar <arquivo.ulx>")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in self.history:
                    if not entry.startswith(':'):
                        f.write(entry + '\n')
            print(f"Sessão salva em '{filename}'")
        except Exception as e:
            print(f"Erro ao salvar: {e}")
    
    def _show_ast(self, code: str):
        if not code:
            print("Uso: :ast <código>")
            return
        
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens, code)
            program = parser.parse()
            
            if parser.has_errors():
                parser.errors.print_summary()
                return
            
            self._print_ast(program)
            
        except Exception as e:
            print(f"Erro: {e}")
    
    def _show_tokens(self, code: str):
        if not code:
            print("Uso: :tokens <código>")
            return
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        lexer.print_tokens()
    
    def _print_ast(self, node, indent=0):
        """Imprime AST em formato de árvore"""
        prefix = "  " * indent
        node_type = type(node).__name__
        
        if hasattr(node, 'value') and node.value is not None:
            print(f"{prefix}{node_type}: {node.value}")
        elif hasattr(node, 'name') and node.name:
            print(f"{prefix}{node_type}: {node.name}")
        else:
            print(f"{prefix}{node_type}")
        
        for field_name in ['left', 'right', 'operand', 'condition', 'value',
                          'then_body', 'else_body', 'body', 'statements',
                          'args', 'elements']:
            if hasattr(node, field_name):
                child = getattr(node, field_name)
                if isinstance(child, list):
                    for item in child:
                        if hasattr(item, 'accept'):
                            self._print_ast(item, indent + 1)
                elif hasattr(child, 'accept'):
                    self._print_ast(child, indent + 1)
    
    def _set_mode(self, mode: str):
        if mode == 'basico':
            self.verbose = False
            print("Modo básico ativado")
        elif mode == 'avancado':
            self.verbose = True
            print("Modo avançado ativado")
        else:
            print("Modos disponíveis: basico, avancado")
    
    def _execute(self, source: str):
        """Executa código ULX"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        if lexer.has_errors():
            for err in lexer.get_errors():
                print(err.format_error())
            return
        
        parser = Parser(tokens, source)
        program = parser.parse()
        
        if parser.has_errors():
            parser.errors.print_summary()
            for err in parser.errors.errors:
                print(err.format_error())
            return
        
        try:
            results = self.interpreter.execute(program)
            for result in results:
                self._print_result(result)
        except ULXError as e:
            print(e.format_error())
        except Exception as e:
            print(f"[ERRO] {e}")
    
    def run(self):
        """Executa o REPL"""
        self._print_banner()
        
        while True:
            try:
                prompt = self.continue_prompt if self.in_multiline else self.prompt
                line = input(prompt)
                
                # Comandos
                if not self.in_multiline and line.strip().startswith(':'):
                    if self._handle_command(line):
                        break
                    continue
                
                # Multiline (blocos)
                stripped = line.strip()
                if stripped.endswith('{') or self.in_multiline:
                    self.multiline_buffer.append(line)
                    self.in_multiline = True
                    
                    # Verifica se bloco foi fechado
                    open_count = sum(l.count('{') for l in self.multiline_buffer)
                    close_count = sum(l.count('}') for l in self.multiline_buffer)
                    
                    if open_count == close_count and open_count > 0:
                        full_code = '\n'.join(self.multiline_buffer)
                        self.history.append(full_code)
                        self._execute(full_code)
                        self.multiline_buffer = []
                        self.in_multiline = False
                    continue
                
                if not stripped:
                    continue
                
                self.history.append(line)
                self._execute(line)
                
            except (EOFError, KeyboardInterrupt):
                print("\nAté logo!")
                break
            except Exception as e:
                print(f"[ERRO CRÍTICO] {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='ULX REPL')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')
    parser.add_argument('-c', '--command', help='Executa comando e sai')
    parser.add_argument('file', nargs='?', help='Arquivo para carregar')
    args = parser.parse_args()
    
    repl = ULXRepl(verbose=args.verbose)
    
    if args.file:
        repl._load_file(args.file)
    
    if args.command:
        repl._execute(args.command)
    else:
        repl.run()


if __name__ == '__main__':
    main()
