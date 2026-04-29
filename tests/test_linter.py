#!/usr/bin/env python3
"""
Testes do Linter ULX
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from ulx_core.linter import ULXLinter, LintSeverity


class TestLinter(unittest.TestCase):
    
    def setUp(self):
        self.linter = ULXLinter()
    
    def test_no_issues_on_valid_code(self):
        code = """
funcao soma(a, b) {
    retorna a + b
}
resultado = soma(1, 2)
"""
        issues = self.linter.lint(code)
        # Pode haver warnings de formatação, mas não erros
        errors = [i for i in issues if i.severity == LintSeverity.ERROR]
        self.assertEqual(len(errors), 0)
    
    def test_line_length_warning(self):
        code = "x = " + "1" * 200  # Linha muito longa
        issues = self.linter.lint(code)
        warnings = [i for i in issues if i.rule == 'max-line-length']
        self.assertTrue(len(warnings) > 0)
    
    def test_trailing_whitespace(self):
        code = "x = 1   \ny = 2"
        issues = self.linter.lint(code)
        infos = [i for i in issues if i.rule == 'trailing-whitespace']
        self.assertTrue(len(infos) > 0)
    
    def test_detects_syntax_error(self):
        code = "funcao soma(a, b  { retorna a + b }"  # Falta )
        issues = self.linter.lint(code)
        errors = [i for i in issues if i.severity == LintSeverity.ERROR]
        self.assertTrue(len(errors) > 0)
    
    def test_empty_code(self):
        issues = self.linter.lint("")
        self.assertEqual(len(issues), 0)
    
    def test_report_contains_summary(self):
        code = "x = 1"
        self.linter.lint(code)
        # Não deve lançar exceção
        self.linter.print_report()


if __name__ == '__main__':
    unittest.main()
