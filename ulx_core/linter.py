#!/usr/bin/env python3
"""
ULX Linter - Analisador estático de código ULX
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum, auto

from .lexer import Lexer
from .parser import Parser


class LintSeverity(Enum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()
    HINT = auto()


@dataclass
class LintIssue:
    """Problema encontrado pelo linter"""
    severity: LintSeverity
    message: str
    line: int
    column: int
    rule: str
    suggestion: Optional[str] = None
    
    def __str__(self):
        icons = {
            LintSeverity.ERROR: "❌",
            LintSeverity.WARNING: "⚠️",
            LintSeverity.INFO: "ℹ️",
            LintSeverity.HINT: "💡"
        }
        icon = icons.get(self.severity, "•")
        sugg = f"\n    Sugestão: {self.suggestion}" if self.suggestion else ""
        return f"{icon} [{self.line}:{self.column}] {self.message} ({self.rule}){sugg}"


class ULXLinter:
    """Linter para código ULX"""
    
    RULES = {
        'no-unused-vars': "Detecta variáveis declaradas mas não usadas",
        'no-undefined-vars': "Detecta variáveis usadas mas não declaradas",
        'consistent-naming': "Verifica convenção de nomenclatura",
        'max-line-length': "Verifica comprimento máximo da linha",
        'no-empty-block': "Detecta blocos vazios",
        'prefer-const': "Sugere const para variáveis não reatribuídas",
        'no-dead-code': "Detecta código inacessível",
        'indentation': "Verifica indentação consistente",
        'trailing-whitespace': "Detecta espaços em branco no fim da linha",
        'no-magic-numbers': "Sugere nomear números mágicos",
        'docstring': "Verifica documentação de funções",
        'complexity': "Verifica complexidade ciclomática",
        'no-global-mutable': "Evita variáveis globais mutáveis",
        'early-return': "Sugere retorno antecipado",
    }
    
    def __init__(self, rules: Optional[List[str]] = None):
        self.rules = rules or list(self.RULES.keys())
        self.issues: List[LintIssue] = []
        self.max_line_length = 100
        self.max_complexity = 10
        
    def lint(self, source: str, filename: str = None) -> List[LintIssue]:
        """Executa linting no código fonte"""
        self.issues = []
        
        # Análise léxica e sintática
        lexer = Lexer(source, filename)
        tokens = lexer.tokenize()
        
        if lexer.has_errors():
            for err in lexer.get_errors():
                self.issues.append(LintIssue(
                    severity=LintSeverity.ERROR,
                    message=str(err),
                    line=err.context.line,
                    column=err.context.column,
                    rule='syntax'
                ))
            return self.issues
        
        parser = Parser(tokens, source, filename)
        program = parser.parse()
        
        if parser.has_errors():
            for err in parser.errors.errors:
                self.issues.append(LintIssue(
                    severity=LintSeverity.ERROR,
                    message=err.message,
                    line=err.context.line,
                    column=err.context.column,
                    rule='parser'
                ))
        
        # Regras de linting
        self._check_line_length(source)
        self._check_trailing_whitespace(source)
        self._check_indentation(source)
        
        return sorted(self.issues, key=lambda i: (i.line, i.column))
    
    def _check_line_length(self, source: str):
        """Verifica comprimento das linhas"""
        if 'max-line-length' not in self.rules:
            return
            
        for i, line in enumerate(source.split('\n'), 1):
            if len(line) > self.max_line_length:
                self.issues.append(LintIssue(
                    severity=LintSeverity.WARNING,
                    message=f"Linha muito longa ({len(line)} > {self.max_line_length} chars)",
                    line=i,
                    column=self.max_line_length,
                    rule='max-line-length',
                    suggestion="Quebre a linha em múltiplas linhas"
                ))
    
    def _check_trailing_whitespace(self, source: str):
        """Verifica espaços em branco no fim das linhas"""
        if 'trailing-whitespace' not in self.rules:
            return
            
        for i, line in enumerate(source.split('\n'), 1):
            if line.rstrip() != line:
                self.issues.append(LintIssue(
                    severity=LintSeverity.INFO,
                    message="Espaços em branco no fim da linha",
                    line=i,
                    column=len(line.rstrip()),
                    rule='trailing-whitespace',
                    suggestion="Remova os espaços em branco do fim da linha"
                ))
    
    def _check_indentation(self, source: str):
        """Verifica indentação consistente"""
        if 'indentation' not in self.rules:
            return
            
        indent_sizes = []
        for i, line in enumerate(source.split('\n'), 1):
            if line.strip():
                indent = len(line) - len(line.lstrip())
                if indent > 0:
                    indent_sizes.append(indent)
        
        if indent_sizes:
            # Detecta tamanho de indentação mais comum
            from collections import Counter
            most_common = Counter(indent_sizes).most_common(1)[0][0]
            
            for i, line in enumerate(source.split('\n'), 1):
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    if indent > 0 and indent % most_common != 0:
                        self.issues.append(LintIssue(
                            severity=LintSeverity.WARNING,
                            message=f"Indentação inconsistente (esperado múltiplo de {most_common})",
                            line=i,
                            column=0,
                            rule='indentation',
                            suggestion=f"Use {most_common} espaços para indentação"
                        ))
    
    def print_report(self):
        """Imprime relatório de linting"""
        errors = [i for i in self.issues if i.severity == LintSeverity.ERROR]
        warnings = [i for i in self.issues if i.severity == LintSeverity.WARNING]
        infos = [i for i in self.issues if i.severity == LintSeverity.INFO]
        
        print(f"\n{'='*50}")
        print(f"  RELATÓRIO DE LINTING")
        print(f"{'='*50}")
        print(f"  Erros: {len(errors)}")
        print(f"  Avisos: {len(warnings)}")
        print(f"  Informações: {len(infos)}")
        print(f"{'='*50}")
        
        for issue in self.issues:
            print(f"  {issue}")
        
        print()
    
    def has_errors(self) -> bool:
        return any(i.severity == LintSeverity.ERROR for i in self.issues)
