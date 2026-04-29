#!/usr/bin/env python3
"""
ULX Lexer - Analisador léxico completo
"""

import re
from typing import List, Optional, Tuple, Iterator
from .tokens import Token, TokenType, KEYWORDS
from .errors import ULXSyntaxError, ErrorContext


class Lexer:
    """Analisador léxico para código ULX"""
    
    def __init__(self, source: str, filename: Optional[str] = None):
        self.source = source
        self.filename = filename
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.errors: List[ULXSyntaxError] = []
        
        # Padrões regex pré-compilados
        self._patterns = {
            'number': re.compile(r'\d+\.\d+|\.\d+|\d+'),
            'identifier': re.compile(r'[a-zA-Z_áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ][a-zA-Z0-9_áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]*'),
            'string_double': re.compile(r'"([^"\\]|\\.)*"'),
            'string_single': re.compile(r"'([^'\\]|\\.)*'"),
        }
    
    def error(self, message: str, line: Optional[int] = None, 
              column: Optional[int] = None) -> ULXSyntaxError:
        """Registra um erro léxico"""
        err = ULXSyntaxError(
            message=message,
            context=ErrorContext(
                line=line or self.line,
                column=column or self.column,
                filename=self.filename,
                code_snippet=self._get_line_snippet()
            )
        )
        self.errors.append(err)
        return err
    
    def _get_line_snippet(self) -> str:
        """Obtém a linha atual do código"""
        lines = self.source.split('\n')
        if 0 <= self.line - 1 < len(lines):
            return lines[self.line - 1].strip()
        return ""
    
    def is_at_end(self) -> bool:
        """Verifica se chegou ao fim do código"""
        return self.current >= len(self.source)
    
    def peek(self, offset: int = 0) -> str:
        """Olha o caractere atual sem consumir"""
        pos = self.current + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Avança e retorna o caractere atual"""
        char = self.source[self.current]
        self.current += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def match(self, expected: str) -> bool:
        """Verifica se o próximo caractere é o esperado"""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True
    
    def add_token(self, token_type: TokenType, value=None):
        """Adiciona um token à lista"""
        text = self.source[self.start:self.current]
        self.tokens.append(Token(
            type=token_type,
            value=value if value is not None else text,
            line=self.line,
            column=self.column - len(text),
            filename=self.filename
        ))
    
    def skip_whitespace(self):
        """Ignora espaços em branco (exceto newline)"""
        while not self.is_at_end():
            char = self.peek()
            if char in ' \t\r':
                self.advance()
            else:
                break
    
    def skip_comment(self):
        """Ignora comentários"""
        if self.peek() == '/' and self.peek(1) == '/':
            # Comentário de linha
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
        elif self.peek() == '/' and self.peek(1) == '*':
            # Comentário de bloco
            self.advance()  # /
            self.advance()  # *
            while not self.is_at_end():
                if self.peek() == '*' and self.peek(1) == '/':
                    self.advance()  # *
                    self.advance()  # /
                    break
                self.advance()
    
    def read_string(self, quote: str) -> bool:
        """Lê uma string delimitada"""
        start_line = self.line
        start_col = self.column
        self.advance()  # consome a aspas inicial
        
        value = ""
        while not self.is_at_end():
            char = self.peek()
            
            if char == '\\':
                self.advance()
                escape_char = self.advance()
                escape_map = {
                    'n': '\n', 't': '\t', 'r': '\r',
                    '\\': '\\', '"': '"', "'": "'",
                    '0': '\0', 'b': '\b', 'f': '\f',
                }
                value += escape_map.get(escape_char, escape_char)
            elif char == quote:
                self.advance()  # consome aspas final
                self.add_token(TokenType.STRING, value)
                return True
            elif char == '\n':
                self.error(
                    "String não pode conter quebra de linha. "
                    "Use \\n para nova linha ou feche a string.",
                    start_line, start_col
                )
                return False
            else:
                value += self.advance()
        
        self.error(
            "String não terminada. Verifique se há aspas de fechamento.",
            start_line, start_col
        )
        return False
    
    def read_number(self) -> bool:
        """Lê um número (inteiro ou float)"""
        start_line = self.line
        start_col = self.column
        
        num_str = ""
        has_dot = False
        
        while not self.is_at_end():
            char = self.peek()
            if char.isdigit():
                num_str += self.advance()
            elif char == '.' and not has_dot and self.peek(1).isdigit():
                has_dot = True
                num_str += self.advance()
            elif char == '_' and self.peek(1).isdigit():
                # Suporta separadores: 1_000_000
                self.advance()
            elif char.lower() == 'e' and (self.peek(1) in '+-' or self.peek(1).isdigit()):
                # Notação científica
                num_str += self.advance()
                if self.peek() in '+-':
                    num_str += self.advance()
                while self.peek().isdigit():
                    num_str += self.advance()
                break
            else:
                break
        
        try:
            if has_dot or 'e' in num_str.lower():
                value = float(num_str.replace('_', ''))
            else:
                value = int(num_str.replace('_', ''))
            self.add_token(TokenType.NUMBER, value)
            return True
        except ValueError:
            self.error(f"Número inválido: '{num_str}'", start_line, start_col)
            return False
    
    def read_identifier(self) -> bool:
        """Lê um identificador ou palavra-chave"""
        while not self.is_at_end():
            char = self.peek()
            if char.isalnum() or char == '_' or char in 'áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ':
                self.advance()
            else:
                break
        
        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        
        # Verifica se é booleano
        if token_type == TokenType.BOOLEAN:
            self.add_token(token_type, text == 'verdadeiro')
        elif token_type == TokenType.NULL:
            self.add_token(token_type, None)
        else:
            self.add_token(token_type, text)
        
        return True
    
    def tokenize(self) -> List[Token]:
        """Executa a tokenização completa"""
        while not self.is_at_end():
            self.start = self.current
            self.skip_whitespace()
            
            if self.is_at_end():
                break
            
            # Verifica comentários
            if self.peek() == '/' and self.peek(1) in '/*':
                self.skip_comment()
                continue
            
            char = self.peek()
            
            # Nova linha
            if char == '\n':
                self.advance()
                self.add_token(TokenType.NEWLINE, '\\n')
                continue
            
            # Strings
            if char in '"""':
                self.read_string(char)
                continue
            
            # Números
            if char.isdigit() or (char == '.' and self.peek(1).isdigit()):
                self.read_number()
                continue
            
            # Identificadores
            if char.isalpha() or char == '_' or char in 'áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ':
                self.read_identifier()
                continue
            
            # Operadores e pontuação
            self.read_operator_or_punctuation()
        
        # Token de fim de arquivo
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.line, self.column, self.filename))
        
        return self.tokens
    
    def read_operator_or_punctuation(self):
        """Lê operadores e pontuação"""
        char = self.advance()
        
        # Operadores de 2 ou 3 caracteres
        two_char = char + self.peek() if not self.is_at_end() else char
        three_char = char + self.peek() + self.peek(1) if self.current + 1 < len(self.source) else two_char
        
        # Operadores compostos (3 caracteres)
        if three_char == '<<=':
            self.advance(); self.advance()
            self.add_token(TokenType.LSHIFT_ASSIGN, three_char)
            return
        elif three_char == '>>=':
            self.advance(); self.advance()
            self.add_token(TokenType.RSHIFT_ASSIGN, three_char)
            return
        
        # Operadores compostos (2 caracteres)
        compound_ops = {
            '+=': TokenType.PLUS_ASSIGN,
            '-=': TokenType.MINUS_ASSIGN,
            '*=': TokenType.MULT_ASSIGN,
            '/=': TokenType.DIV_ASSIGN,
            '%=': TokenType.MOD_ASSIGN,
            '**': TokenType.POWER,
            '//': TokenType.FLOOR_DIV,
            '==': TokenType.EQ,
            '!=': TokenType.NE,
            '>=': TokenType.GTE,
            '<=': TokenType.LTE,
            '&&': TokenType.AND,
            '||': TokenType.OR,
            '++': TokenType.INCREMENT,
            '--': TokenType.DECREMENT,
            '<<': TokenType.LSHIFT,
            '>>': TokenType.RSHIFT,
            '->': TokenType.ARROW,
        }
        
        if two_char in compound_ops:
            self.advance()
            self.add_token(compound_ops[two_char], two_char)
            return
        
        # Operadores simples
        single_ops = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '=': TokenType.ASSIGN,
            '>': TokenType.GT,
            '<': TokenType.LT,
            '!': TokenType.NOT,
            '&': TokenType.BIT_AND,
            '|': TokenType.BIT_OR,
            '^': TokenType.BIT_XOR,
            '~': TokenType.BIT_NOT,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            ';': TokenType.SEMICOLON,
            ':': TokenType.COLON,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
        }
        
        if char in single_ops:
            self.add_token(single_ops[char], char)
        else:
            self.error(f"Caractere inesperado: '{char}' (código: {ord(char)})")
    
    def has_errors(self) -> bool:
        """Verifica se há erros léxicos"""
        return len(self.errors) > 0
    
    def get_errors(self) -> List[ULXSyntaxError]:
        """Retorna erros léxicos"""
        return self.errors.copy()
    
    def print_tokens(self):
        """Imprime tokens para debug"""
        print(f"\n{'='*60}")
        print(f"  TOKENS ({len(self.tokens)} tokens)")
        print(f"{'='*60}")
        for token in self.tokens:
            if token.type != TokenType.NEWLINE and token.type != TokenType.EOF:
                print(f"  {token}")
        print(f"{'='*60}\n")
    
    def __iter__(self) -> Iterator[Token]:
        return iter(self.tokens)
