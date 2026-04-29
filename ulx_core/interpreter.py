#!/usr/bin/env python3
"""
ULX Interpreter - Interpretador completo com tratamento de erros
"""

import math
import random
import time
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field

from .parser import *
from .errors import (ULXRuntimeError, ULXTypeError, ULXNameError, 
                     ULXDivisionByZeroError, ULXIndexError, ErrorContext)
from .logger import ULXLogger, LogLevel


@dataclass
class Function:
    """Representa uma função ULX"""
    name: str
    params: List[Dict[str, Any]]
    body: List[ASTNode]
    return_type: Optional[str] = None
    closure: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Class:
    """Representa uma classe ULX"""
    name: str
    parent: Optional[str] = None
    methods: Dict[str, Function] = field(default_factory=dict)
    fields: Dict[str, Any] = field(default_factory=dict)


class ReturnValue(Exception):
    """Exceção para retorno de função"""
    def __init__(self, value: Any = None):
        self.value = value


class BreakLoop(Exception):
    """Exceção para break"""
    pass


class ContinueLoop(Exception):
    """Exceção para continue"""
    pass


class Environment:
    """Escopo de variáveis"""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.types: Dict[str, str] = {}  # nome -> tipo
        self.parent = parent
        self.constants: set = set()
    
    def define(self, name: str, value: Any, var_type: Optional[str] = None,
               is_const: bool = False):
        """Define uma variável"""
        self.variables[name] = value
        if var_type:
            self.types[name] = var_type
        if is_const:
            self.constants.add(name)
    
    def get(self, name: str) -> Any:
        """Obtém valor de variável"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise ULXNameError(name)
    
    def set(self, name: str, value: Any):
        """Atualiza valor de variável"""
        if name in self.constants:
            raise ULXRuntimeError(f"Cannot reassign constant '{name}'")
        if name in self.variables:
            # Verificação de tipo
            if name in self.types:
                expected = self.types[name]
                actual = self._get_type_name(value)
                if expected != actual and expected != 'any':
                    raise ULXTypeError(
                        f"Expected {expected}, got {actual}",
                        expected_type=expected, got_type=actual
                    )
            self.variables[name] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise ULXNameError(name)
    
    def exists(self, name: str) -> bool:
        """Verifica se variável existe"""
        return name in self.variables or (self.parent.exists(name) if self.parent else False)
    
    def _get_type_name(self, value: Any) -> str:
        """Obtém nome do tipo de um valor"""
        type_map = {
            int: 'int', float: 'float', str: 'string',
            bool: 'bool', list: 'lista', dict: 'dicionario',
            type(None): 'vazio'
        }
        return type_map.get(type(value), 'any')


class Interpreter:
    """Interpretador ULX completo"""
    
    MAX_RECURSION = 1000
    MAX_ITERATIONS = 1000000
    
    def __init__(self, logger: Optional[ULXLogger] = None):
        self.logger = logger or ULXLogger(level=LogLevel.INFO)
        self.globals = Environment()
        self.environment = self.globals
        self.functions: Dict[str, Function] = {}
        self.classes: Dict[str, Class] = {}
        self.call_stack: List[str] = []
        self.iteration_count = 0
        self.output_buffer: List[str] = []
        
        # Registra funções built-in
        self._register_builtins()
    
    def _register_builtins(self):
        """Registra funções built-in"""
        builtins = {
            # Matemática
            'sqrt': lambda x: math.sqrt(x) if x >= 0 else (_ for _ in ()).throw(ULXRuntimeError("Cannot sqrt negative number")),
            'pow': math.pow,
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'max': max,
            'min': min,
            'pi': math.pi,
            'e': math.e,
            
            # Texto
            'tamanho': len,
            'maiuscula': str.upper,
            'minuscula': str.lower,
            'trim': str.strip,
            'split': str.split,
            'join': lambda sep, arr: sep.join(str(x) for x in arr),
            'substitui': str.replace,
            'contem': lambda s, sub: sub in s,
            'inicia_com': str.startswith,
            'termina_com': str.endswith,
            'encontra': str.find,
            
            # Conversão
            'inteiro': int,
            'decimal': float,
            'texto': str,
            'booleano': bool,
            'lista': list,
            
            # Array
            'adiciona': lambda arr, item: arr.append(item) or arr,
            'remove': lambda arr, item: arr.remove(item) or arr,
            'insere': lambda arr, i, item: arr.insert(i, item) or arr,
            'ordena': lambda arr: sorted(arr),
            'reverte': lambda arr: list(reversed(arr)),
            'soma_array': sum,
            'media': lambda arr: sum(arr) / len(arr) if arr else 0,
            
            # Utilidades
            'tempo': time.time,
            'aleatorio': random.random,
            'aleatorio_int': random.randint,
            'escolhe': random.choice,
            'embaralha': lambda arr: random.sample(arr, len(arr)),
            'tipo': lambda x: type(x).__name__,
            'espera': time.sleep,
            
            # Assertivas
            'afirma': self._assert,
            'afirma_igual': lambda a, b: a == b or (_ for _ in ()).throw(ULXRuntimeError(f"{a} != {b}")),
        }
        
        for name, func in builtins.items():
            self.globals.define(name, func)
    
    def _assert(self, condition: bool, message: str = "Assertion failed"):
        """Asserção"""
        if not condition:
            raise ULXRuntimeError(message)
        return True
    
    def interpret(self, node: ASTNode) -> Any:
        """Interpreta um nó AST"""
        return node.accept(self)
    
    def execute(self, program: Program) -> List[Any]:
        """Executa um programa completo"""
        self.logger.info(f"Iniciando execução: {len(program.statements)} statements")
        self.iteration_count = 0
        results = []
        
        for stmt in program.statements:
            try:
                result = self.interpret(stmt)
                if result is not None:
                    results.append(result)
            except ReturnValue:
                pass  # Ignora retorno no nível global
            except (BreakLoop, ContinueLoop):
                self.logger.warning("break/continua fora de loop ignorado")
            except ULXRuntimeError as e:
                self.logger.error(str(e))
                raise
        
        self.logger.success("Execução concluída")
        return results
    
    # Visitor methods
    
    def visit_Program(self, node: Program) -> List[Any]:
        return self.execute(node)
    
    def visit_NumberLiteral(self, node: NumberLiteral) -> Union[int, float]:
        return node.value
    
    def visit_StringLiteral(self, node: StringLiteral) -> str:
        return node.value
    
    def visit_BooleanLiteral(self, node: BooleanLiteral) -> bool:
        return node.value
    
    def visit_NullLiteral(self, node: NullLiteral) -> None:
        return None
    
    def visit_Identifier(self, node: Identifier) -> Any:
        return self.environment.get(node.name)
    
    def visit_BinaryOp(self, node: BinaryOp) -> Any:
        left = self.interpret(node.left)
        
        # Short-circuit para AND/OR
        if node.operator == '&&':
            return left and self.interpret(node.right)
        if node.operator == '||':
            return left or self.interpret(node.right)
        
        right = self.interpret(node.right)
        
        # Operações aritméticas
        if node.operator == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise ULXDivisionByZeroError()
            return left / right
        elif node.operator == '%':
            return left % right
        elif node.operator == '^':
            return left ** right
        elif node.operator == '//':
            if right == 0:
                raise ULXDivisionByZeroError()
            return left // right
        
        # Comparações
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '>':
            return left > right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>=':
            return left >= right
        elif node.operator == '<=':
            return left <= right
        
        # Bitwise
        elif node.operator == '&':
            return left & right
        elif node.operator == '|':
            return left | right
        elif node.operator == '^':
            return left ^ right
        elif node.operator == '<<':
            return left << right
        elif node.operator == '>>':
            return left >> right
        
        else:
            raise ULXRuntimeError(f"Operador desconhecido: {node.operator}")
    
    def visit_UnaryOp(self, node: UnaryOp) -> Any:
        operand = self.interpret(node.operand)
        
        if node.operator == '-':
            return -operand
        elif node.operator == '!':
            return not operand
        elif node.operator == '~':
            return ~operand
        elif node.operator == '++':
            if isinstance(node.operand, Identifier):
                val = self.environment.get(node.operand.name)
                new_val = val + 1
                self.environment.set(node.operand.name, new_val)
                return new_val
        elif node.operator == '--':
            if isinstance(node.operand, Identifier):
                val = self.environment.get(node.operand.name)
                new_val = val - 1
                self.environment.set(node.operand.name, new_val)
                return new_val
        
        raise ULXRuntimeError(f"Operador unário desconhecido: {node.operator}")
    
    def visit_Assignment(self, node: Assignment) -> Any:
        value = self.interpret(node.value)
        
        if node.operator == '=':
            self.environment.set(node.name, value)
        elif node.operator == '+=':
            current = self.environment.get(node.name)
            self.environment.set(node.name, current + value)
        elif node.operator == '-=':
            current = self.environment.get(node.name)
            self.environment.set(node.name, current - value)
        elif node.operator == '*=':
            current = self.environment.get(node.name)
            self.environment.set(node.name, current * value)
        elif node.operator == '/=':
            if value == 0:
                raise ULXDivisionByZeroError()
            current = self.environment.get(node.name)
            self.environment.set(node.name, current / value)
        elif node.operator == '%=':
            current = self.environment.get(node.name)
            self.environment.set(node.name, current % value)
        
        return value
    
    def visit_VariableDecl(self, node: VariableDecl) -> Any:
        value = self.interpret(node.value) if node.value else None
        self.environment.define(node.name, value, node.var_type)
        return value
    
    def visit_FunctionDef(self, node: FunctionDef) -> None:
        func = Function(
            name=node.name,
            params=node.params,
            body=node.body,
            return_type=node.return_type
        )
        self.functions[node.name] = func
        self.globals.define(node.name, func)
    
    def visit_FunctionCall(self, node: FunctionCall) -> Any:
        args = [self.interpret(arg) for arg in node.args]
        
        # Verifica se é built-in
        if node.name in self.globals.variables and callable(self.globals.variables[node.name]):
            func = self.globals.variables[node.name]
            try:
                return func(*args)
            except TypeError as e:
                raise ULXRuntimeError(f"Erro ao chamar '{node.name}': {e}")
        
        # Verifica funções definidas pelo usuário
        if node.name not in self.functions:
            raise ULXRuntimeError(f"Função '{node.name}' não definida")
        
        func = self.functions[node.name]
        
        # Verifica recursão
        if len(self.call_stack) > self.MAX_RECURSION:
            raise ULXRuntimeError(
                f"Recursão muito profunda em '{node.name}'"
            )
        
        # Cria ambiente local
        local_env = Environment(parent=self.globals)
        
        # Vincula parâmetros
        for i, param in enumerate(func.params):
            if i < len(args):
                local_env.define(param['name'], args[i], param.get('type'))
            elif param.get('default'):
                local_env.define(param['name'], 
                               self.interpret(param['default']),
                               param.get('type'))
            else:
                raise ULXRuntimeError(
                    f"Parâmetro '{param['name']}' não fornecido para '{node.name}'"
                )
        
        # Executa corpo
        prev_env = self.environment
        self.environment = local_env
        self.call_stack.append(node.name)
        
        try:
            for stmt in func.body:
                self.interpret(stmt)
        except ReturnValue as ret:
            return ret.value
        finally:
            self.call_stack.pop()
            self.environment = prev_env
        
        return None
    
    def visit_ReturnStmt(self, node: ReturnStmt) -> None:
        value = self.interpret(node.value) if node.value else None
        raise ReturnValue(value)
    
    def visit_IfStmt(self, node: IfStmt) -> Any:
        condition = self.interpret(node.condition)
        
        if condition:
            for stmt in node.then_body:
                self.interpret(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                self.interpret(stmt)
        
        return None
    
    def visit_WhileStmt(self, node: WhileStmt) -> Any:
        while self.interpret(node.condition):
            self.iteration_count += 1
            if self.iteration_count > self.MAX_ITERATIONS:
                raise ULXRuntimeError("Número máximo de iterações excedido")
            
            try:
                for stmt in node.body:
                    self.interpret(stmt)
            except BreakLoop:
                break
            except ContinueLoop:
                continue
        
        return None
    
    def visit_ForStmt(self, node: ForStmt) -> Any:
        # Executa inicialização
        if node.init:
            self.interpret(node.init)
        
        while True:
            # Verifica condição
            if node.condition:
                if not self.interpret(node.condition):
                    break
            
            self.iteration_count += 1
            if self.iteration_count > self.MAX_ITERATIONS:
                raise ULXRuntimeError("Número máximo de iterações excedido")
            
            try:
                for stmt in node.body:
                    self.interpret(stmt)
            except BreakLoop:
                break
            except ContinueLoop:
                pass
            
            # Executa incremento
            if node.increment:
                self.interpret(node.increment)
        
        return None
    
    def visit_BreakStmt(self, node: BreakStmt) -> None:
        raise BreakLoop()
    
    def visit_ContinueStmt(self, node: ContinueStmt) -> None:
        raise ContinueLoop()
    
    def visit_PrintStmt(self, node: PrintStmt) -> None:
        values = [str(self.interpret(arg)) for arg in node.args]
        output = ' '.join(values)
        self.output_buffer.append(output)
        print(output)
        return None
    
    def visit_InputStmt(self, node: InputStmt) -> str:
        if node.prompt:
            print(node.prompt, end='')
        try:
            return input()
        except EOFError:
            return ""
    
    def visit_ArrayLiteral(self, node: ArrayLiteral) -> List[Any]:
        return [self.interpret(elem) for elem in node.elements]
    
    def visit_DictLiteral(self, node: DictLiteral) -> Dict[Any, Any]:
        result = {}
        for key, value in node.pairs:
            result[self.interpret(key)] = self.interpret(value)
        return result
    
    def visit_IndexAccess(self, node: IndexAccess) -> Any:
        obj = self.interpret(node.obj)
        index = self.interpret(node.index)
        
        if isinstance(obj, list):
            if not isinstance(index, int):
                raise ULXTypeError(f"Índice de lista deve ser inteiro, não {type(index).__name__}")
            if index < 0 or index >= len(obj):
                raise ULXIndexError(index, len(obj))
            return obj[index]
        elif isinstance(obj, str):
            if not isinstance(index, int):
                raise ULXTypeError(f"Índice de string deve ser inteiro")
            if index < 0 or index >= len(obj):
                raise ULXIndexError(index, len(obj))
            return obj[index]
        elif isinstance(obj, dict):
            return obj.get(index)
        else:
            raise ULXTypeError(f"Tipo não indexável: {type(obj).__name__}")
    
    def visit_MemberAccess(self, node: MemberAccess) -> Any:
        obj = self.interpret(node.obj)
        
        if isinstance(obj, dict):
            return obj.get(node.member)
        elif hasattr(obj, node.member):
            return getattr(obj, node.member)
        else:
            raise ULXRuntimeError(f"Objeto não tem membro '{node.member}'")
    
    def visit_TryExcept(self, node: TryExcept) -> Any:
        try:
            for stmt in node.try_body:
                self.interpret(stmt)
        except Exception as e:
            if node.except_body:
                prev_env = self.environment
                local_env = Environment(parent=self.environment)
                if node.except_var:
                    local_env.define(node.except_var, str(e))
                self.environment = local_env
                try:
                    for stmt in node.except_body:
                        self.interpret(stmt)
                finally:
                    self.environment = prev_env
        finally:
            if node.finally_body:
                for stmt in node.finally_body:
                    self.interpret(stmt)
        
        return None
    
    def visit_ThrowStmt(self, node: ThrowStmt) -> None:
        value = self.interpret(node.value)
        raise ULXRuntimeError(str(value))
    
    def visit_ImportStmt(self, node: ImportStmt) -> None:
        # Simula importação
        self.logger.info(f"Importando módulo: {node.module}")
        return None
    
    def visit_ClassDef(self, node: ClassDef) -> None:
        cls = Class(name=node.name, parent=node.parent)
        
        for method in node.methods:
            func = Function(
                name=method.name,
                params=method.params,
                body=method.body,
                return_type=method.return_type
            )
            cls.methods[method.name] = func
        
        self.classes[node.name] = cls
        self.globals.define(node.name, cls)
    
    def visit_Block(self, node: Block) -> Any:
        result = None
        for stmt in node.statements:
            result = self.interpret(stmt)
        return result
    
    def get_output(self) -> List[str]:
        """Retorna saída capturada"""
        return self.output_buffer.copy()
    
    def clear_output(self):
        """Limpa buffer de saída"""
        self.output_buffer.clear()
