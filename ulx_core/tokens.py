#!/usr/bin/env python3
"""
ULX Token Definitions
Define todos os tipos de tokens da linguagem ULX
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Any


class TokenType(Enum):
    """Tipos de tokens ULX"""
    # Literais
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NULL = auto()
    
    # Identificadores
    IDENTIFIER = auto()
    
    # Palavras-chave
    ESCREVA = auto()      # print
    LEIA = auto()         # input
    SE = auto()           # if
    SENAO = auto()        # else
    ENQUANTO = auto()     # while
    PARA = auto()         # for
    FUNCAO = auto()       # function
    RETORNA = auto()      # return
    PARE = auto()         # break
    CONTINUA = auto()     # continue
    FACA = auto()         # do
    ESCOLHA = auto()      # switch/case
    CASO = auto()         # case
    PADRAO = auto()       # default
    TENTE = auto()        # try
    PEGUE = auto()        # catch
    FINALMENTE = auto()   # finally
    LANCA = auto()        # throw
    IMPORTE = auto()      # import
    DE = auto()           # from
    COMO = auto()         # as
    CLASSE = auto()       # class
    CONSTRUTOR = auto()   # constructor
    ESTA = auto()         # this
    SUPER = auto()        # super
    PRIVADO = auto()      # private
    PUBLICO = auto()      # public
    ESTATICO = auto()     # static
    
    # Operadores aritméticos
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    FLOOR_DIV = auto()
    
    # Operadores de atribuição
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULT_ASSIGN = auto()
    DIV_ASSIGN = auto()
    MOD_ASSIGN = auto()
    
    # Operadores de comparação
    EQ = auto()
    NE = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()
    
    # Operadores lógicos
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Operadores bitwise
    BIT_AND = auto()
    BIT_OR = auto()
    BIT_XOR = auto()
    BIT_NOT = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    
    # Pontuação
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()
    
    # Incremento/decremento
    INCREMENT = auto()
    DECREMENT = auto()
    
    # Comentários e espaços
    COMMENT = auto()
    NEWLINE = auto()
    EOF = auto()
    
    # Tipos
    TIPO_INT = auto()
    TIPO_FLOAT = auto()
    TIPO_STRING = auto()
    TIPO_BOOL = auto()
    TIPO_LISTA = auto()
    TIPO_DICT = auto()
    TIPO_VAZIO = auto()


# Palavras reservadas
KEYWORDS = {
    'escreva': TokenType.ESCREVA,
    'leia': TokenType.LEIA,
    'se': TokenType.SE,
    'senao': TokenType.SENAO,
    'enquanto': TokenType.ENQUANTO,
    'para': TokenType.PARA,
    'funcao': TokenType.FUNCAO,
    'retorna': TokenType.RETORNA,
    'pare': TokenType.PARE,
    'continua': TokenType.CONTINUA,
    'faca': TokenType.FACA,
    'escolha': TokenType.ESCOLHA,
    'caso': TokenType.CASO,
    'padrao': TokenType.PADRAO,
    'tente': TokenType.TENTE,
    'pegue': TokenType.PEGUE,
    'finalmente': TokenType.FINALMENTE,
    'lanca': TokenType.LANCA,
    'importe': TokenType.IMPORTE,
    'de': TokenType.DE,
    'como': TokenType.COMO,
    'classe': TokenType.CLASSE,
    'construtor': TokenType.CONSTRUTOR,
    'esta': TokenType.ESTA,
    'super': TokenType.SUPER,
    'privado': TokenType.PRIVADO,
    'publico': TokenType.PUBLICO,
    'estatico': TokenType.ESTATICO,
    'verdadeiro': TokenType.BOOLEAN,
    'falso': TokenType.BOOLEAN,
    'nulo': TokenType.NULL,
    'int': TokenType.TIPO_INT,
    'float': TokenType.TIPO_FLOAT,
    'string': TokenType.TIPO_STRING,
    'bool': TokenType.TIPO_BOOL,
    'lista': TokenType.TIPO_LISTA,
    'dicionario': TokenType.TIPO_DICT,
    'vazio': TokenType.TIPO_VAZIO,
}


@dataclass
class Token:
    """Representa um token na análise léxica"""
    type: TokenType
    value: Any
    line: int
    column: int
    filename: Optional[str] = None
    
    def __repr__(self):
        if self.filename:
            return f"Token({self.type.name}, {self.value!r}, linha={self.line}, col={self.column}, arquivo={self.filename})"
        return f"Token({self.type.name}, {self.value!r}, linha={self.line}, col={self.column})"
    
    def __str__(self):
        val = self.value if len(str(self.value)) < 30 else str(self.value)[:27] + "..."
        return f"[{self.line}:{self.column}] {self.type.name}: {val}"
