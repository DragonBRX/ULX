#!/usr/bin/env python3
"""
Script de testes ULX - Roda todos os testes de uma vez
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ulx_core.lexer import Lexer
from ulx_core.parser import Parser
from ulx_core.interpreter import Interpreter
from ulx_core.logger import LogLevel
from ulx_core.tokens import TokenType


def run(source: str) -> Interpreter:
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source)
    program = parser.parse()
    interp = Interpreter()
    interp.logger.level = LogLevel.CRITICAL
    interp.execute(program)
    return interp


tests_passed = 0
tests_failed = 0


def check(name, condition):
    global tests_passed, tests_failed
    if condition:
        tests_passed += 1
        print(f"  ✅ {name}")
    else:
        tests_failed += 1
        print(f"  ❌ {name}")


print("=" * 60)
print("TESTES ULX - Suite Completa")
print("=" * 60)

# ========== TESTES DO LEXER ==========
print("\n--- Lexer ---")

# Teste 1: Hello World
lexer = Lexer('escreva("Ola, Mundo!")')
tokens = lexer.tokenize()
types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
check("Hello World tokeniza", types[0] == TokenType.ESCREVA and types[2] == TokenType.STRING)

# Teste 2: Numeros
lexer = Lexer("42 3.14")
tokens = lexer.tokenize()
numbers = [t for t in tokens if t.type == TokenType.NUMBER]
check("Numeros inteiros", numbers[0].value == 42)
check("Numeros float", numbers[1].value == 3.14)

# Teste 3: Identificadores sem espacos (BUG CRITICO FIX)
lexer = Lexer("x = y")
tokens = lexer.tokenize()
idents = [t for t in tokens if t.type == TokenType.IDENTIFIER]
check("Identificadores sem espaco", all(" " not in t.value for t in idents))

# Teste 4: Keywords reconhecidas (BUG CRITICO FIX)
lexer = Lexer("funcao soma(a, b) { retorna a + b }")
tokens = lexer.tokenize()
retorna = [t for t in tokens if t.type == TokenType.RETORNA]
check("Keyword 'retorna' reconhecida", len(retorna) == 1)

# Teste 5: Funcao multilinha (BUG CRITICO FIX)
code = """funcao dobro(x) {
    retorna x * 2
}"""
lexer = Lexer(code)
tokens = lexer.tokenize()
check("Funcao multilinha sem erros", not lexer.has_errors())
retorna = [t for t in tokens if t.type == TokenType.RETORNA]
check("Funcao multilinha tem retorna", len(retorna) == 1)

# Teste 6: Strings
lexer = Lexer('"hello"')
tokens = lexer.tokenize()
strings = [t for t in tokens if t.type == TokenType.STRING]
check("Strings", strings[0].value == "hello")

# Teste 7: Comentarios
lexer = Lexer("escreva(1) // comentario\n/* bloco */ x = 2")
tokens = lexer.tokenize()
ids = [t for t in tokens if t.type == TokenType.IDENTIFIER]
check("Comentarios ignorados", len(ids) == 1 and ids[0].value == "x")

# ========== TESTES DO PARSER ==========
print("\n--- Parser ---")

# Teste 8: Expressao binaria
lexer = Lexer("1 + 2")
tokens = lexer.tokenize()
parser = Parser(tokens, "1 + 2")
program = parser.parse()
check("Expressao binaria", len(program.statements) == 1)

# Teste 9: Definicao de funcao
lexer = Lexer("funcao soma(a, b) { retorna a + b }")
tokens = lexer.tokenize()
parser = Parser(tokens, "funcao soma(a, b) { retorna a + b }")
program = parser.parse()
from ulx_core.parser import FunctionDef, ReturnStmt
check("Definicao de funcao", isinstance(program.statements[0], FunctionDef))
check("Corpo da funcao e ReturnStmt", isinstance(program.statements[0].body[0], ReturnStmt))

# Teste 10: If/Else
lexer = Lexer("se (x > 0) { escreva(1) } senao { escreva(0) }")
tokens = lexer.tokenize()
parser = Parser(tokens, "se (x > 0) { escreva(1) } senao { escreva(0) }")
program = parser.parse()
from ulx_core.parser import IfStmt
check("If/Else", isinstance(program.statements[0], IfStmt))

# Teste 11: While
lexer = Lexer("enquanto (x < 10) { x = x + 1 }")
tokens = lexer.tokenize()
parser = Parser(tokens, "enquanto (x < 10) { x = x + 1 }")
program = parser.parse()
from ulx_core.parser import WhileStmt
check("While loop", isinstance(program.statements[0], WhileStmt))

# Teste 12: For loop
lexer = Lexer("para (i = 0; i < 10; i = i + 1) { escreva(i) }")
tokens = lexer.tokenize()
parser = Parser(tokens, "para (i = 0; i < 10; i = i + 1) { escreva(i) }")
program = parser.parse()
from ulx_core.parser import ForStmt
check("For loop", isinstance(program.statements[0], ForStmt))

# ========== TESTES DO INTERPRETADOR ==========
print("\n--- Interpretador ---")

# Teste 13: Aritmetica
interp = run("x = 2 + 3")
check("Adicao", interp.environment.get("x") == 5)

interp = run("x = 10 - 4")
check("Subtracao", interp.environment.get("x") == 6)

interp = run("x = 3 * 4")
check("Multiplicacao", interp.environment.get("x") == 12)

interp = run("x = 15 / 3")
check("Divisao", interp.environment.get("x") == 5.0)

# Teste 14: Variaveis
interp = run("x = 10")
check("Atribuicao", interp.environment.get("x") == 10)

# Teste 15: If/Else
interp = run("x = 10\nse (x > 5) { y = \"maior\" } senao { y = \"menor\" }")
check("If verdadeiro", interp.environment.get("y") == "maior")

# Teste 16: While
interp = run("i = 0\nenquanto (i < 5) { i = i + 1 }")
check("While loop", interp.environment.get("i") == 5)

# Teste 17: For
interp = run("soma = 0\npara (i = 1; i <= 5; i = i + 1) { soma = soma + i }")
check("For loop", interp.environment.get("soma") == 15)

# Teste 18: Funcoes (BUG CRITICO FIX)
interp = run("funcao dobro(x) { retorna x * 2 }\nr = dobro(5)")
check("Funcao com retorno", interp.environment.get("r") == 10)

# Teste 19: Recursao
interp = run("funcao fat(n) { se (n <= 1) { retorna 1 } retorna n * fat(n - 1) }\nr = fat(5)")
check("Fatorial recursivo", interp.environment.get("r") == 120)

# Teste 20: Fibonacci
interp = run("funcao fib(n) { se (n <= 1) { retorna n } retorna fib(n - 1) + fib(n - 2) }\nr = fib(10)")
check("Fibonacci", interp.environment.get("r") == 55)

# Teste 21: Arrays
interp = run("arr = [1, 2, 3]\nprimeiro = arr[0]")
check("Arrays", interp.environment.get("primeiro") == 1)

# Teste 22: Comparacao
interp = run("a = 5 > 3\nb = 5 == 5")
check("Comparacao >", interp.environment.get("a") == True)
check("Comparacao ==", interp.environment.get("b") == True)

# Teste 23: Logicos
interp = run("a = verdadeiro && verdadeiro\nb = verdadeiro || falso\nc = !falso")
check("AND logico", interp.environment.get("a") == True)
check("OR logico", interp.environment.get("b") == True)
check("NOT logico", interp.environment.get("c") == True)

# Teste 24: Hello World
interp = run('escreva("Ola, Mundo!")')
check("Hello World", "Ola, Mundo!" in interp.output_buffer)

# Teste 25: Funcoes built-in
interp = run("resultado = sqrt(16)")
check("Built-in sqrt", interp.environment.get("resultado") == 4.0)

# Teste 26: While com If
interp = run("i = 0\nsoma = 0\nenquanto (i < 10) { se (i % 2 == 0) { soma = soma + i } i = i + 1 }")
check("While com If", interp.environment.get("soma") == 20)

# ========== RESUMO ==========
print("\n" + "=" * 60)
print(f"RESULTADO: {tests_passed} passaram, {tests_failed} falharam")
print("=" * 60)

if tests_failed > 0:
    sys.exit(1)
else:
    print("🎉 Todos os testes passaram!")
    sys.exit(0)
