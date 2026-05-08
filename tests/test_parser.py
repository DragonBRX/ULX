#!/usr/bin/env python3
"""
Testes do Parser ULX - Testes robustos e completos
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from ulx_core.lexer import Lexer
from ulx_core.parser import Parser, ASTNode, Program, NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral, Identifier, BinaryOp, UnaryOp, Assignment, VariableDecl, FunctionDef, FunctionCall, ReturnStmt, IfStmt, WhileStmt, ForStmt, BreakStmt, ContinueStmt, PrintStmt, InputStmt, ArrayLiteral, DictLiteral, IndexAccess, MemberAccess, TryExcept, ThrowStmt, ImportStmt, ClassDef, Block


class TestParserBasics(unittest.TestCase):
    """Testes básicos de parsing"""
    
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
    
    def test_if_else(self):
        program, parser = self._parse("se (x > 0) { escreva(\"positivo\") } senao { escreva(\"negativo\") }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, IfStmt)
        self.assertEqual(len(stmt.then_body), 1)
        self.assertEqual(len(stmt.else_body), 1)
    
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
        self.assertEqual(stmt.operator, '-')
    
    def test_no_errors_on_valid(self):
        program, parser = self._parse("funcao main() { escreva(\"Ola\") }")
        self.assertFalse(parser.has_errors())


class TestParserFunctions(unittest.TestCase):
    """Testes de parsing de funcoes completas"""
    
    def _parse(self, source: str) -> tuple:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source)
        return parser.parse(), parser
    
    def test_function_body_statements(self):
        """BUG CRÍTICO: corpo da funcao deve ser statements, nao expressions"""
        program, parser = self._parse("funcao dobro(x) { retorna x * 2 }")
        self.assertFalse(parser.has_errors())
        
        func = program.statements[0]
        self.assertIsInstance(func, FunctionDef)
        self.assertEqual(len(func.body), 1)
        self.assertIsInstance(func.body[0], ReturnStmt)
    
    def test_multiline_function(self):
        code = """funcao fatorial(n) {
    se (n <= 1) {
        retorna 1
    }
    retorna n * fatorial(n - 1)
}"""
        program, parser = self._parse(code)
        self.assertFalse(parser.has_errors())
        
        func = program.statements[0]
        self.assertEqual(len(func.body), 2)  # if + return
        self.assertIsInstance(func.body[0], IfStmt)
        self.assertIsInstance(func.body[1], ReturnStmt)
    
    def test_function_with_multiple_params(self):
        program, parser = self._parse("funcao calc(a, b, c) { retorna a + b + c }")
        func = program.statements[0]
        self.assertEqual(len(func.params), 3)


class TestParserClasses(unittest.TestCase):
    """Testes de parsing de classes"""
    
    def _parse(self, source: str) -> tuple:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source)
        return parser.parse(), parser
    
    def test_class_def(self):
        code = """classe Pessoa {
    funcao init(nome) {
        esta.nome = nome
    }
}"""
        program, parser = self._parse(code)
        self.assertFalse(parser.has_errors())
        
        cls = program.statements[0]
        self.assertIsInstance(cls, ClassDef)
        self.assertEqual(cls.name, "Pessoa")
        self.assertEqual(len(cls.methods), 1)


class TestParserComplete(unittest.TestCase):
    """Testes de programas completos"""
    
    def _parse(self, source: str) -> tuple:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source)
        return parser.parse(), parser
    
    def test_calculadora(self):
        code = """escreva("=== Calculadora ===")
funcao soma(a, b) {
    retorna a + b
}
funcao sub(a, b) {
    retorna a - b
}
resultado = soma(10, 5)
escreva("Resultado:", resultado)"""
        program, parser = self._parse(code)
        self.assertFalse(parser.has_errors())
        self.assertEqual(len(program.statements), 5)


if __name__ == '__main__':
    unittest.main()
