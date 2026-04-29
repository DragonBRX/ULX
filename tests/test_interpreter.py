#!/usr/bin/env python3
"""
Testes do Interpretador ULX
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from ulx_core.lexer import Lexer
from ulx_core.parser import Parser
from ulx_core.interpreter import Interpreter
from ulx_core.errors import ULXDivisionByZeroError, ULXIndexError


class TestInterpreter(unittest.TestCase):
    
    def setUp(self):
        self.interpreter = Interpreter()
    
    def _run(self, source: str):
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source)
        program = parser.parse()
        return self.interpreter.execute(program)
    
    def test_number_literal(self):
        results = self._run("42")
        self.assertEqual(results[0], 42)
    
    def test_string_literal(self):
        results = self._run('"hello"')
        self.assertEqual(results[0], "hello")
    
    def test_boolean_literal(self):
        results = self._run("verdadeiro")
        self.assertEqual(results[0], True)
        results = self._run("falso")
        self.assertEqual(results[0], False)
    
    def test_arithmetic(self):
        results = self._run("2 + 3")
        self.assertEqual(results[0], 5)
        
        results = self._run("10 - 4")
        self.assertEqual(results[0], 6)
        
        results = self._run("3 * 4")
        self.assertEqual(results[0], 12)
        
        results = self._run("15 / 3")
        self.assertEqual(results[0], 5.0)
        
        results = self._run("17 % 5")
        self.assertEqual(results[0], 2)
        
        results = self._run("2 ^ 8")
        self.assertEqual(results[0], 256)
    
    def test_assignment(self):
        self._run("x = 10")
        results = self._run("x")
        self.assertEqual(results[0], 10)
    
    def test_string_concat(self):
        results = self._run('"Hello" + " World"')
        self.assertEqual(results[0], "Hello World")
    
    def test_if_true(self):
        self._run("x = 0")
        self._run("se (1 == 1) { x = 10 }")
        results = self._run("x")
        self.assertEqual(results[0], 10)
    
    def test_if_false(self):
        self._run("x = 0")
        self._run("se (1 == 2) { x = 10 }")
        results = self._run("x")
        self.assertEqual(results[0], 0)
    
    def test_function_call_and_return(self):
        self._run("funcao dobro(x) { retorna x * 2 }")
        results = self._run("dobro(5)")
        self.assertEqual(results[0], 10)
    
    def test_recursive_function(self):
        self._run("funcao fat(n) { se (n <= 1) { retorna 1 } retorna n * fat(n - 1) }")
        results = self._run("fat(5)")
        self.assertEqual(results[0], 120)
    
    def test_while_loop(self):
        self._run("i = 0")
        self._run("enquanto (i < 5) { i = i + 1 }")
        results = self._run("i")
        self.assertEqual(results[0], 5)
    
    def test_for_loop(self):
        self._run("soma = 0")
        self._run("para (i = 1; i <= 5; i = i + 1) { soma = soma + i }")
        results = self._run("soma")
        self.assertEqual(results[0], 15)
    
    def test_array_literal(self):
        results = self._run("[1, 2, 3]")
        self.assertEqual(results[0], [1, 2, 3])
    
    def test_array_indexing(self):
        self._run("arr = [10, 20, 30]")
        results = self._run("arr[0]")
        self.assertEqual(results[0], 10)
        results = self._run("arr[1]")
        self.assertEqual(results[0], 20)
    
    def test_comparison(self):
        results = self._run("5 > 3")
        self.assertTrue(results[0])
        
        results = self._run("5 < 3")
        self.assertFalse(results[0])
        
        results = self._run("5 == 5")
        self.assertTrue(results[0])
        
        results = self._run("5 != 3")
        self.assertTrue(results[0])
    
    def test_logical_ops(self):
        results = self._run("verdadeiro && verdadeiro")
        self.assertTrue(results[0])
        
        results = self._run("verdadeiro && falso")
        self.assertFalse(results[0])
        
        results = self._run("verdadeiro || falso")
        self.assertTrue(results[0])
        
        results = self._run("!falso")
        self.assertTrue(results[0])
    
    def test_unary_minus(self):
        results = self._run("-5")
        self.assertEqual(results[0], -5)
    
    def test_compound_assignment(self):
        self._run("x = 10")
        self._run("x += 5")
        results = self._run("x")
        self.assertEqual(results[0], 15)
        
        self._run("x -= 3")
        results = self._run("x")
        self.assertEqual(results[0], 12)
    
    def test_builtin_sqrt(self):
        self._run("resultado = sqrt(16)")
        results = self._run("resultado")
        self.assertEqual(results[0], 4.0)
    
    def test_builtin_len(self):
        self._run("texto = \"hello\"")
        results = self._run("tamanho(texto)")
        self.assertEqual(results[0], 5)
    
    def test_print_output(self):
        self.interpreter.clear_output()
        self._run('escreva("Hello, World!")')
        output = self.interpreter.get_output()
        self.assertEqual(output, ["Hello, World!"])
    
    def test_division_by_zero(self):
        with self.assertRaises(ULXDivisionByZeroError):
            self._run("10 / 0")
    
    def test_index_out_of_bounds(self):
        self._run("arr = [1, 2, 3]")
        with self.assertRaises(ULXIndexError):
            self._run("arr[10]")


if __name__ == '__main__':
    unittest.main()
