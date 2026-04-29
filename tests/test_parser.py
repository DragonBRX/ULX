#!/usr/bin/env python3
"""
Testes do Parser ULX
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from ulx_core.lexer import Lexer
from ulx_core.parser import Parser, *


class TestParser(unittest.TestCase):
    
    def _parse(self, source: str) -> tuple:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source)
        return parser.parse(), parser
    
    def test_number_literal(self):
        program, parser = self._parse("42")
        self.assertEqual(len(program.statements), 1)
        self.assertIsInstance(program.statements[0], NumberLiteral)
        self.assertEqual(program.statements[0].value, 42)
    
    def test_string_literal(self):
        program, parser = self._parse('"hello"')
        self.assertIsInstance(program.statements[0], StringLiteral)
        self.assertEqual(program.statements[0].value, "hello")
    
    def test_binary_op(self):
        program, parser = self._parse("1 + 2")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, BinaryOp)
        self.assertEqual(stmt.operator, '+')
        self.assertEqual(stmt.left.value, 1)
        self.assertEqual(stmt.right.value, 2)
    
    def test_assignment(self):
        program, parser = self._parse("x = 10")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, Assignment)
        self.assertEqual(stmt.name, "x")
        self.assertEqual(stmt.value.value, 10)
    
    def test_print(self):
        program, parser = self._parse('escreva("Ola")')
        stmt = program.statements[0]
        self.assertIsInstance(stmt, PrintStmt)
        self.assertEqual(len(stmt.args), 1)
    
    def test_if_statement(self):
        program, parser = self._parse("se (x > 0) { escreva(\"positivo\") }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, IfStmt)
        self.assertIsInstance(stmt.condition, BinaryOp)
        self.assertEqual(len(stmt.then_body), 1)
    
    def test_while_loop(self):
        program, parser = self._parse("enquanto (x < 10) { x = x + 1 }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, WhileStmt)
        self.assertIsInstance(stmt.condition, BinaryOp)
    
    def test_for_loop(self):
        program, parser = self._parse("para (i = 0; i < 10; i = i + 1) { escreva(i) }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ForStmt)
        self.assertIsInstance(stmt.init, Assignment)
        self.assertIsInstance(stmt.condition, BinaryOp)
    
    def test_function_def(self):
        program, parser = self._parse("funcao soma(a, b) { retorna a + b }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, FunctionDef)
        self.assertEqual(stmt.name, "soma")
        self.assertEqual(len(stmt.params), 2)
    
    def test_function_call(self):
        program, parser = self._parse("soma(1, 2)")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, FunctionCall)
        self.assertEqual(stmt.name, "soma")
        self.assertEqual(len(stmt.args), 2)
    
    def test_array_literal(self):
        program, parser = self._parse("[1, 2, 3]")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ArrayLiteral)
        self.assertEqual(len(stmt.elements), 3)
    
    def test_try_except(self):
        program, parser = self._parse("tente { escreva(1) } pegue(e) { escreva(e) }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, TryExcept)
        self.assertEqual(len(stmt.try_body), 1)
        self.assertEqual(len(stmt.except_body), 1)
    
    def test_unary_op(self):
        program, parser = self._parse("-5")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, UnaryOp)
        self.assertEqual(stmt.operator, '-')
    
    def test_complex_expression(self):
        program, parser = self._parse("a + b * c - d / e")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, BinaryOp)
        # Deve ser: (a + (b * c)) - (d / e)
        self.assertEqual(stmt.operator, '-')
    
    def test_no_errors_on_valid(self):
        program, parser = self._parse("funcao main() { escreva(\"Ola\") }")
        self.assertFalse(parser.has_errors())


if __name__ == '__main__':
    unittest.main()
