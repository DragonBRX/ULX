#!/usr/bin/env python3
"""
ULX Formatter - Formatador de código ULX
"""

import re
from typing import Optional, List


class ULXFormatter:
    """Formatador de código ULX"""
    
    def __init__(self, indent_size: int = 4, max_line_length: int = 100):
        self.indent_size = indent_size
        self.max_line_length = max_line_length
        
    def format(self, source: str) -> str:
        """Formata código ULX"""
        lines = source.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Comentários preservados
            if stripped.startswith('//'):
                formatted_lines.append(' ' * (indent_level * self.indent_size) + stripped)
                continue
            
            # Blocos fechados
            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
            
            # Formata a linha
            if stripped:
                formatted = ' ' * (indent_level * self.indent_size) + stripped
                formatted_lines.append(formatted)
            else:
                formatted_lines.append('')
            
            # Blocos abertos
            if stripped.endswith('{') and not stripped.startswith('//'):
                indent_level += 1
        
        # Remove espaços em branco no fim das linhas
        formatted_lines = [line.rstrip() for line in formatted_lines]
        
        # Remove linhas em branco múltiplas
        result = self._remove_multiple_blank_lines('\n'.join(formatted_lines))
        
        return result
    
    def _remove_multiple_blank_lines(self, source: str) -> str:
        """Remove linhas em branco consecutivas"""
        lines = source.split('\n')
        result = []
        prev_blank = False
        
        for line in lines:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            result.append(line)
            prev_blank = is_blank
        
        return '\n'.join(result)
    
    def check_formatting(self, source: str) -> List[str]:
        """Verifica problemas de formatação sem alterar o código"""
        issues = []
        formatted = self.format(source)
        
        original_lines = source.split('\n')
        formatted_lines = formatted.split('\n')
        
        for i, (orig, fmt) in enumerate(zip(original_lines, formatted_lines), 1):
            if orig != fmt:
                issues.append(f"Linha {i}: formatação incorreta")
        
        return issues


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python formatter.py <arquivo.ulx>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        formatter = ULXFormatter()
        formatted = formatter.format(source)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        print(f"Arquivo formatado: {filename}")
        
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {filename}")


if __name__ == '__main__':
    main()
