#!/usr/bin/env python3
"""
Testes do Interpretador ULX - Testes robustos e completos
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from ulx_core.lexer import Lexer
from ulx_core.parser import Parser
from ulx_core.interpreter import Interpreter
from ulx_core.logger import LogLevel


def run(source: str) -> Interpreter:
    """Helper para executar codigo ULX"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source)
    program = parser.parse()
    interp = Interpreter()
    interp.logger.level = LogLevel.CRITICAL
    interp.execute(program)
    return interp


class TestInterpreterBasics(unittest.TestCase):
    """Testes basicos do interpretador"""
    
    def test_number_literal(self):
        interp = run("42")
        self.assertEqual(interp.output_buffer, [])
    
    def test_string_literal(self):
        interp = run('"hello"')
        self.assertEqual(interp.output_buffer, [])
    
    def test_boolean_literal(self):
        interp = run("verdadeiro")
        interp2 = run("falso")
        # Sem erros = sucesso
    
    def test_arithmetic(self):
        interp = run("x = 2 + 3")
        self.assertEqual(interp.environment.get("x"), 5)
        
        interp = run("x = 10 - 4")
        self.assertEqual(interp.environment.get("x"), 6)
        
        interp = run("x = 3 * 4")
        self.assertEqual(interp.environment.get("x"), 12)
        
        interp = run("x = 15 / 3")
        self.assertEqual(interp.environment.get("x"), 5.0)
        
        interp = run("x = 17 % 5")
        self.assertEqual(interp.environment.get("x"), 2)
        
        interp = run("x = 2 ^ 8")
        self.assertEqual(interp.environment.get("x"), 256)
    
    def test_assignment(self):
        interp = run("x = 10")
        self.assertEqual(interp.environment.get("x"), 10)
    
    def test_string_concat(self):
        interp = run('x = "Hello" + " World"')
        self.assertEqual(interp.environment.get("x"), "Hello World")
    
    def test_if_true(self):
        interp = run("x = 0\nse (1 == 1) { x = 10 }")
        self.assertEqual(interp.environment.get("x"), 10)
    
    def test_if_false(self):
        interp = run("x = 0\nse (1 == 2) { x = 10 }")
        self.assertEqual(interp.environment.get("x"), 0)
    
    def test_function_call_and_return(self):
        interp = run("funcao dobro(x) { retorna x * 2 }\nresultado = dobro(5)")
        self.assertEqual(interp.environment.get("resultado"), 10)
    
    def test_recursive_function(self):
        interp = run("funcao fat(n) { se (n <= 1) { retorna 1 } retorna n * fat(n - 1) }\nresultado = fat(5)")
        self.assertEqual(interp.environment.get("resultado"), 120)
    
    def test_while_loop(self):
        interp = run("i = 0\nenquanto (i < 5) { i = i + 1 }")
        self.assertEqual(interp.environment.get("i"), 5)
    
    def test_for_loop(self):
        interp = run("soma = 0\npara (i = 1; i <= 5; i = i + 1) { soma = soma + i }")
        self.assertEqual(interp.environment.get("soma"), 15)
    
    def test_array_literal(self):
        interp = run("arr = [1, 2, 3]")
        self.assertEqual(interp.environment.get("arr"), [1, 2, 3])
    
    def test_array_indexing(self):
        interp = run("arr = [10, 20, 30]\nprimeiro = arr[0]")
        self.assertEqual(interp.environment.get("primeiro"), 10)
    
    def test_comparison(self):
        interp = run("a = 5 > 3\nb = 5 < 3\nc = 5 == 5\nd = 5 != 3")
        self.assertEqual(interp.environment.get("a"), True)
        self.assertEqual(interp.environment.get("b"), False)
        self.assertEqual(interp.environment.get("c"), True)
        self.assertEqual(interp.environment.get("d"), True)
    
    def test_logical_ops(self):
        interp = run("a = verdadeiro && verdadeiro\nb = verdadeiro && falso\nc = verdadeiro || falso\nd = !falso")
        self.assertEqual(interp.environment.get("a"), True)
        self.assertEqual(interp.environment.get("b"), False)
        self.assertEqual(interp.environment.get("c"), True)
        self.assertEqual(interp.environment.get("d"), True)
    
    def test_unary_minus(self):
        interp = run("x = -5")
        self.assertEqual(interp.environment.get("x"), -5)
    
    def test_compound_assignment(self):
        interp = run("x = 10\nx += 5")
        self.assertEqual(interp.environment.get("x"), 15)
        
        interp = run("x = 15\nx -= 3")
        self.assertEqual(interp.environment.get("x"), 12)
    
    def test_builtin_sqrt(self):
        interp = run("resultado = sqrt(16)")
        self.assertEqual(interp.environment.get("resultado"), 4.0)
    
    def test_builtin_len(self):
        interp = run('texto = "hello"\nresultado = tamanho(texto)')
        self.assertEqual(interp.environment.get("resultado"), 5)
    
    def test_hello_world(self):
        interp = run('escreva("Ola, Mundo!")')
        self.assertIn("Ola, Mundo!", interp.output_buffer)


class TestInterpreterFunctions(unittest.TestCase):
    """Testes de funcoes completas"""
    
    def test_function_with_body(self):
        """BUG CRITICO FIX: funcoes com corpo de multiplas linhas"""
        interp = run("funcao quadrado(x) {\n    retorna x * x\n}\nresultado = quadrado(4)")
        self.assertEqual(interp.environment.get("resultado"), 16)
    
    def test_multiple_functions(self):
        interp = run("funcao soma(a, b) { retorna a + b }\nfuncao mult(a, b) { retorna a * b }\nr = mult(soma(2, 3), 4)")
        self.assertEqual(interp.environment.get("r"), 20)
    
    def test_fibonacci(self):
        interp = run("funcao fib(n) { se (n <= 1) { retorna n } retorna fib(n - 1) + fib(n - 2) }\nr = fib(10)")
        self.assertEqual(interp.environment.get("r"), 55)


class TestInterpreterControlFlow(unittest.TestCase):
    """Testes de controle de fluxo"""
    
    def test_if_else(self):
        interp = run("x = 10\nse (x > 5) { y = \"maior\" } senao { y = \"menor\" }")
        self.assertEqual(interp.environment.get("y"), "maior")
    
    def test_nested_if(self):
        interp = run("x = 10\nse (x > 5) { se (x > 8) { y = \"muito maior\" } }")
        self.assertEqual(interp.environment.get("y"), "muito maior")
    
    def test_while_with_if(self):
        interp = run("i = 0\nsoma = 0\nenquanto (i < 10) { se (i % 2 == 0) { soma = soma + i } i = i + 1 }")
        self.assertEqual(interp.environment.get("soma"), 20)  # 0+2+4+6+8


class TestInterpreterFatorial(unittest.TestCase):
    """Teste do programa de fatorial"""
    
    def test_fatorial_program(self):
        code = '''escreva("=== Fatorial ===")
funcao fatorial(n) {
    se (n <= 1) {
        retorna 1
    }
    retorna n * fatorial(n - 1)
}
para (i = 1; i <= 5; i = i + 1) {
    escreva(i, "! =", fatorial(i))
}'''
        interp = run(code)
        output = str(interp.output_buffer)
        self.assertIn("120", output)


if __name__ == '__main__':
    unittest.main()
