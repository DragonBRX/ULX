#!/usr/bin/env python3
"""
ULX Error System - Sistema de tratamento de erros completo
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import traceback
import sys


class ErrorSeverity(Enum):
    """Níveis de severidade de erro"""
    AVISO = auto()        # Warning - não impede execução
    ERRO = auto()         # Error - impede execução do bloco atual
    CRITICO = auto()      # Critical - impede execução completa
    FATAL = auto()        # Fatal - impede execução do programa


class ErrorCategory(Enum):
    """Categorias de erro para melhor diagnóstico"""
    SINTAXE = "Sintaxe"
    TIPO = "Tipo"
    NOME = "Nome"
    RUNTIME = "Execução"
    IMPORT = "Importação"
    IO = "Entrada/Saída"
    MEMORIA = "Memória"
    DIVISAO_ZERO = "Divisão por Zero"
    INDICE = "Índice"
    ATRIBUICAO = "Atribuição"
    CHAMADA = "Chamada de Função"
    RETORNO = "Retorno"
    ESCOPO = "Escopo"
    RECURSÃO = "Recursão"
    SISTEMA = "Sistema"
    ASSERTIVA = "Asserção"
    DEPRECATED = "Depreciado"
    EXPERIMENTAL = "Experimental"


@dataclass
class ErrorContext:
    """Contexto de um erro para melhor diagnóstico"""
    line: int
    column: int
    filename: Optional[str] = None
    code_snippet: Optional[str] = None
    function_name: Optional[str] = None
    stack_trace: Optional[List[str]] = None
    
    def __str__(self):
        parts = []
        if self.filename:
            parts.append(f"Arquivo: {self.filename}")
        parts.append(f"Linha: {self.line}, Coluna: {self.column}")
        if self.function_name:
            parts.append(f"Função: {self.function_name}")
        if self.code_snippet:
            parts.append(f"\n  >>> {self.code_snippet}")
        return "\n".join(parts)


@dataclass
class ErrorSuggestion:
    """Sugestão de correção para um erro"""
    message: str
    replacement: Optional[str] = None
    confidence: float = 1.0  # 0.0 a 1.0
    
    def __str__(self):
        return f"💡 {self.message}" + (f" -> '{self.replacement}'" if self.replacement else "")


class ULXError(Exception):
    """Exceção base para todos os erros ULX"""
    
    def __init__(self, message: str, 
                 category: ErrorCategory = ErrorCategory.RUNTIME,
                 severity: ErrorSeverity = ErrorSeverity.ERRO,
                 context: Optional[ErrorContext] = None,
                 suggestions: Optional[List[ErrorSuggestion]] = None,
                 code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.context = context or ErrorContext(line=0, column=0)
        self.suggestions = suggestions or []
        self.error_code = code or "ULX-000"
        self._formatted = False
    
    def add_suggestion(self, message: str, replacement: Optional[str] = None, confidence: float = 1.0):
        """Adiciona uma sugestão de correção"""
        self.suggestions.append(ErrorSuggestion(message, replacement, confidence))
    
    def format_error(self, verbose: bool = False) -> str:
        """Formata o erro para exibição amigável"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"  ❌ ERRO ULX - {self.category.value}")
        lines.append(f"{'='*60}")
        lines.append(f"  Código: {self.error_code}")
        lines.append(f"  Severidade: {self.severity.name}")
        lines.append(f"  Mensagem: {self.message}")
        lines.append(f"{'='*60}")
        
        if self.context:
            lines.append(f"\n  📍 Localização:")
            lines.append(f"  {self.context}")
        
        if self.suggestions:
            lines.append(f"\n  💡 Sugestões:")
            for i, sugg in enumerate(self.suggestions, 1):
                lines.append(f"    {i}. {sugg}")
        
        if verbose and self.context and self.context.stack_trace:
            lines.append(f"\n  🔍 Stack Trace:")
            for frame in self.context.stack_trace:
                lines.append(f"    {frame}")
        
        lines.append(f"\n{'='*60}\n")
        return "\n".join(lines)
    
    def __str__(self):
        if not self._formatted:
            return self.format_error()
        return super().__str__()


class ULXSyntaxError(ULXError):
    """Erro de sintaxe no código ULX"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None, 
                 expected: Optional[str] = None, found: Optional[str] = None):
        suggestions = []
        if expected and found:
            suggestions.append(ErrorSuggestion(
                f"Esperado '{expected}', mas encontrado '{found}'",
                replacement=expected
            ))
        
        super().__init__(
            message=message,
            category=ErrorCategory.SINTAXE,
            severity=ErrorSeverity.CRITICO,
            context=context,
            suggestions=suggestions,
            code="ULX-001"
        )
        self.expected = expected
        self.found = found


class ULXTypeError(ULXError):
    """Erro de tipo em tempo de execução"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None,
                 expected_type: Optional[str] = None, got_type: Optional[str] = None):
        suggestions = []
        if expected_type and got_type:
            suggestions.append(ErrorSuggestion(
                f"Converta o valor para '{expected_type}' usando a função apropriada",
                replacement=f"{expected_type}(valor)"
            ))
        
        super().__init__(
            message=message,
            category=ErrorCategory.TIPO,
            severity=ErrorSeverity.ERRO,
            context=context,
            suggestions=suggestions,
            code="ULX-002"
        )
        self.expected_type = expected_type
        self.got_type = got_type


class ULXNameError(ULXError):
    """Erro quando um nome não é encontrado"""
    
    def __init__(self, name: str, context: Optional[ErrorContext] = None):
        suggestions = [
            ErrorSuggestion(f"Verifique se a variável '{name}' foi declarada"),
            ErrorSuggestion(f"Verifique se há erros de digitação no nome"),
        ]
        
        super().__init__(
            message=f"Nome não definido: '{name}'",
            category=ErrorCategory.NOME,
            severity=ErrorSeverity.ERRO,
            context=context,
            suggestions=suggestions,
            code="ULX-003"
        )
        self.name = name


class ULXRuntimeError(ULXError):
    """Erro em tempo de execução"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.RUNTIME,
            severity=ErrorSeverity.CRITICO,
            context=context,
            code="ULX-004"
        )


class ULXDivisionByZeroError(ULXError):
    """Erro de divisão por zero"""
    
    def __init__(self, context: Optional[ErrorContext] = None):
        super().__init__(
            message="Divisão por zero não é permitida",
            category=ErrorCategory.DIVISAO_ZERO,
            severity=ErrorSeverity.ERRO,
            context=context,
            suggestions=[
                ErrorSuggestion("Verifique se o divisor é zero antes da divisão"),
                ErrorSuggestion("Use uma condicional para tratar o caso de divisor zero"),
            ],
            code="ULX-005"
        )


class ULXIndexError(ULXError):
    """Erro de índice fora dos limites"""
    
    def __init__(self, index: Any, size: int, context: Optional[ErrorContext] = None):
        super().__init__(
            message=f"Índice {index} fora dos limites (tamanho: {size})",
            category=ErrorCategory.INDICE,
            severity=ErrorSeverity.ERRO,
            context=context,
            suggestions=[
                ErrorSuggestion(f"Use um índice entre 0 e {size-1}"),
                ErrorSuggestion("Verifique o tamanho da lista antes de acessar"),
            ],
            code="ULX-006"
        )
        self.index = index
        self.size = size


class ULXImportError(ULXError):
    """Erro ao importar módulo"""
    
    def __init__(self, module: str, context: Optional[ErrorContext] = None):
        super().__init__(
            message=f"Não foi possível importar o módulo '{module}'",
            category=ErrorCategory.IMPORT,
            severity=ErrorSeverity.ERRO,
            context=context,
            suggestions=[
                ErrorSuggestion(f"Verifique se o módulo '{module}' existe"),
                ErrorSuggestion("Verifique se o caminho do módulo está correto"),
            ],
            code="ULX-007"
        )
        self.module = module


class ULXIOError(ULXError):
    """Erro de entrada/saída"""
    
    def __init__(self, message: str, filename: Optional[str] = None, 
                 context: Optional[ErrorContext] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.IO,
            severity=ErrorSeverity.ERRO,
            context=context,
            code="ULX-008"
        )
        self.filename = filename


class ULXRecursionError(ULXError):
    """Erro de recursão muito profunda"""
    
    def __init__(self, function_name: str, depth: int, 
                 context: Optional[ErrorContext] = None):
        super().__init__(
            message=f"Recursão muito profunda em '{function_name}' (profundidade: {depth})",
            category=ErrorCategory.RECURSÃO,
            severity=ErrorSeverity.FATAL,
            context=context,
            suggestions=[
                ErrorSuggestion("Verifique se há um caso base para a recursão"),
                ErrorSuggestion("Considere usar uma abordagem iterativa"),
            ],
            code="ULX-009"
        )
        self.function_name = function_name
        self.depth = depth


class ULXAssertionError(ULXError):
    """Erro de asserção falhou"""
    
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(
            message=f"Asserção falhou: {message}",
            category=ErrorCategory.ASSERTIVA,
            severity=ErrorSeverity.ERRO,
            context=context,
            code="ULX-010"
        )


class ErrorHandler:
    """Gerenciador de erros ULX"""
    
    MAX_ERRORS = 100
    
    def __init__(self):
        self.errors: List[ULXError] = []
        self.warnings: List[ULXError] = []
        self.error_count = 0
        self.warning_count = 0
        self.strict_mode = False
        self._exit_on_error = False
    
    def add_error(self, error: ULXError):
        """Adiciona um erro à lista"""
        if error.severity == ErrorSeverity.AVISO:
            self.warnings.append(error)
            self.warning_count += 1
        else:
            self.errors.append(error)
            self.error_count += 1
        
        if self.error_count >= self.MAX_ERRORS:
            raise ULXRuntimeError(
                f"Número máximo de erros ({self.MAX_ERRORS}) atingido. "
                "Interrompendo a compilação."
            )
        
        if self.strict_mode and error.severity in (ErrorSeverity.ERRO, ErrorSeverity.CRITICO):
            raise error
    
    def has_errors(self) -> bool:
        """Verifica se há erros"""
        return self.error_count > 0
    
    def has_warnings(self) -> bool:
        """Verifica se há avisos"""
        return self.warning_count > 0
    
    def get_errors(self, severity: Optional[ErrorSeverity] = None) -> List[ULXError]:
        """Retorna erros filtrados por severidade"""
        if severity is None:
            return self.errors
        return [e for e in self.errors if e.severity == severity]
    
    def print_summary(self):
        """Imprime resumo de erros e avisos"""
        print(f"\n{'='*60}")
        print(f"  RESUMO DE COMPILAÇÃO")
        print(f"{'='*60}")
        print(f"  Erros: {self.error_count}")
        print(f"  Avisos: {self.warning_count}")
        if self.error_count == 0:
            print(f"  ✅ Compilação bem-sucedida!")
        else:
            print(f"  ❌ Compilação falhou com {self.error_count} erro(s)")
        print(f"{'='*60}\n")
    
    def clear(self):
        """Limpa todos os erros"""
        self.errors.clear()
        self.warnings.clear()
        self.error_count = 0
        self.warning_count = 0
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.has_errors():
            self.print_summary()
