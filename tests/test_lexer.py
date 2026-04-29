#!/usr/bin/env python3
"""
Testes do Lexer ULX
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from ulx_core.lexer import Lexer
from ulx_core.tokens import TokenType


class TestLexer(unittest.TestCase):
    
    def test_hello_world(self):
        lexer = Lexer('escreva("Ola, Mundo!")')
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        self.assertEqual(types[0], TokenType.ESCREVA)
        self.assertEqual(types[1], TokenType.LPAREN)
        self.assertEqual(types[2], TokenType.STRING)
        self.assertEqual(types[3], TokenType.RPAREN)
    
    def test_numbers(self):
        lexer = Lexer("42 3.14 .5 1e10 2_000_000")
        tokens = lexer.tokenize()
        numbers = [t for t in tokens if t.type == TokenType.NUMBER]
        
        self.assertEqual(numbers[0].value, 42)
        self.assertEqual(numbers[1].value, 3.14)
        self.assertEqual(numbers[2].value, 0.5)
        self.assertEqual(numbers[3].value, 1e10)
        self.assertEqual(numbers[4].value, 2000000)
    
    def test_operators(self):
        lexer = Lexer("+ - * / % ** // == != >= <= && || ++ --")
        tokens = lexer.tokenize()
        ops = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        expected = [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
                   TokenType.DIVIDE, TokenType.MODULO, TokenType.POWER,
                   TokenType.FLOOR_DIV, TokenType.EQ, TokenType.NE,
                   TokenType.GTE, TokenType.LTE, TokenType.AND,
                   TokenType.OR, TokenType.INCREMENT, TokenType.DECREMENT]
        
        for i, exp in enumerate(expected):
            self.assertEqual(ops[i].type, exp)
    
    def test_keywords(self):
        lexer = Lexer("se senao enquanto para funcao retorna pare continua")
        tokens = lexer.tokenize()
        keywords = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        self.assertEqual(keywords[0].type, TokenType.SE)
        self.assertEqual(keywords[1].type, TokenType.SENAO)
        self.assertEqual(keywords[2].type, TokenType.ENQUANTO)
        self.assertEqual(keywords[3].type, TokenType.PARA)
        self.assertEqual(keywords[4].type, TokenType.FUNCAO)
        self.assertEqual(keywords[5].type, TokenType.RETORNA)
        self.assertEqual(keywords[6].type, TokenType.PARE)
        self.assertEqual(keywords[7].type, TokenType.CONTINUA)
    
    def test_strings(self):
        lexer = Lexer('"hello" \'world\' "esc\\"aped"')
        tokens = lexer.tokenize()
        strings = [t for t in tokens if t.type == TokenType.STRING]
        
        self.assertEqual(strings[0].value, "hello")
        self.assertEqual(strings[1].value, "world")
        self.assertEqual(strings[2].value, 'esc"aped')
    
    def test_comments(self):
        lexer = Lexer("escreva(1) // comentario\n/* bloco */ x = 2")
        tokens = lexer.tokenize()
        # Comentários são ignorados
        ids = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual(len(ids), 1)
        self.assertEqual(ids[0].value, "x")
    
    def test_booleans_and_null(self):
        lexer = Lexer("verdadeiro falso nulo")
        tokens = lexer.tokenize()
        vals = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        self.assertEqual(vals[0].type, TokenType.BOOLEAN)
        self.assertEqual(vals[0].value, True)
        self.assertEqual(vals[1].type, TokenType.BOOLEAN)
        self.assertEqual(vals[1].value, False)
        self.assertEqual(vals[2].type, TokenType.NULL)
        self.assertEqual(vals[2].value, None)
    
    def test_array(self):
        lexer = Lexer("[1, 2, 3]")
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        
        self.assertEqual(types[0], TokenType.LBRACKET)
        self.assertEqual(types[1], TokenType.NUMBER)
        self.assertEqual(types[2], TokenType.COMMA)
        self.assertEqual(types[-1], TokenType.RBRACKET)
    
    def test_no_errors_on_valid(self):
        lexer = Lexer("funcao soma(a, b) { retorna a + b }")
        tokens = lexer.tokenize()
        self.assertFalse(lexer.has_errors())
    
    def test_error_on_unterminated_string(self):
        lexer = Lexer('"unterminated')
        tokens = lexer.tokenize()
        self.assertTrue(lexer.has_errors())


if __name__ == '__main__':
    unittest.main()
