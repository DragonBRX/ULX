#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLX Compiler - Compilador Universal ULX/ULV
Compila ULX e ULV para binários nativos

Uso: clx-compile <arquivo> [-o saida] [--ulv]
"""

import sys
import os
import re
import subprocess
import argparse
import platform


class UniversalCompiler:
    """Compilador Universal - ULX + ULV"""

    def __init__(self, source_file, output=None, flags=None):
        self.source_file = source_file
        self.output = output or self._get_default_output(source_file)
        self.flags = flags or []
        self.strategy = self._detect_hardware()
        self.source = None
        self.file_type = None

    def _get_default_output(self, source_file):
        if source_file.endswith('.ulx'):
            return source_file.replace('.ulx', '')
        if source_file.endswith('.ulv'):
            return source_file.replace('.ulv', '')
        return source_file

    def _detect_hardware(self):
        return {
            'cores': os.cpu_count() or 1,
            'arch': platform.machine(),
            'os': platform.system(),
            'cc': 'gcc'
        }

    def read_source(self):
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.source = f.read()
            return True
        except FileNotFoundError:
            print(f"[CLX] Erro: Arquivo '{self.source_file}' não encontrado")
            return False

    def detect_type(self):
        if self.source_file.endswith('.ulx'):
            self.file_type = 'ULX'
        elif self.source_file.endswith('.ulv'):
            self.file_type = 'ULV'
        else:
            self.file_type = 'ULX'  # default
        return self.file_type

    def compile(self):
        if not self.read_source():
            return False

        self.detect_type()

        print("=" * 60)
        print("   CLX Compiler v3.0 - Universal")
        print("=" * 60)
        print(f"Arquivo: {self.source_file}")
        print(f"Tipo: {self.file_type}")
        print(f"Plataforma: {self.strategy['os']}")
        print("=" * 60)

        # Converte ULV para ULX se necessário
        if self.file_type == 'ULV':
            print("\n[1/4] Convertendo ULV para ULX...")
            ulx_code = self._convert_ulv_to_ulx()
            self.source = ulx_code
        else:
            print("\n[1/4] Analisando código ULX...")

        print("\n[2/4] Tokenizando...")
        tokens = self._tokenize(self.source)
        print(f"Tokens: {len(tokens)}")

        print("\n[3/4] Gerando código C...")
        c_code = self._generate_c(tokens)
        c_file = f"{self.output}.c"
        with open(c_file, 'w', encoding='utf-8') as f:
            f.write(c_code)
        print(f"Gerado: {c_file}")

        print("\n[4/4] Compilando binário...")
        success = self._compile_c(c_file)

        if success:
            size = os.path.getsize(self.output)
            print(f"\n[OK] Binário: {self.output} ({size:,} bytes)")
            print("=" * 60)
            print("   COMPILAÇÃO BEM-SUCEDIDA!")
            print("=" * 60)
        else:
            print("[ERRO] Falha na compilação")

        return success

    def _convert_ulv_to_ulx(self):
        """Converte código ULV para ULX"""
        lines = self.source.split('\n')
        ulx_lines = []
        ulx_lines.append("// ULV → ULX Convertido")
        ulx_lines.append("// Gerado automaticamente por CLX")
        ulx_lines.append("")

        in_window = False
        indent = 0

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                continue

            # Janela
            if stripped.startswith('janela(') or stripped.startswith('janela "'):
                match = re.search(r'janela\(?"([^"]+)"?\)?', stripped)
                if match:
                    window_name = match.group(1)
                    ulx_lines.append(f'// Criando janela: {window_name}')
                    in_window = True
                    indent = 1

            # Fim de janela
            elif stripped == '}':
                in_window = False
                indent = 0

            # Texto
            elif stripped.startswith('texto(') or stripped.startswith('texto "'):
                match = re.search(r'texto\(?"([^"]+)"?\)?', stripped)
                if match:
                    text = match.group(1)
                    ulx_lines.append(f'escreva("{text}");')

            # Botão
            elif stripped.startswith('botao(') or stripped.startswith('botao "'):
                match = re.search(r'botao\(?"([^"]+)"?\)?', stripped)
                if match:
                    btn_text = match.group(1)
                    ulx_lines.append(f'// Botão: {btn_text}')

            # Entrada
            elif stripped.startswith('entrada('):
                match = re.search(r'entrada\(([^)]+)\)', stripped)
                if match:
                    var_name = match.group(1)
                    ulx_lines.append(f'{var_name} = leia("Digite {var_name}: ")')

            # Ação
            elif 'acao:' in stripped:
                match = re.search(r'acao:\s*(\w+)\(', stripped)
                if match:
                    func_name = match.group(1)
                    ulx_lines.append(f'// Ação: chamar {func_name}()')

            # Posição
            elif 'posicao:' in stripped:
                pass  # Ignora, é apenas layout info

            # Tamanho
            elif 'tamanho:' in stripped:
                pass  # Ignora, é apenas layout info

            # Cor
            elif 'cor:' in stripped:
                pass  # Ignora

            # Fonte
            elif 'fonte:' in stripped:
                pass  # Ignora

        ulx_lines.append('')
        return '\n'.join(ulx_lines)

    def _tokenize(self, source):
        """Tokeniza código ULX"""
        tokens = []
        lines = source.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Remove comments
            if '//' in line:
                line = line[:line.index('//')]

            line = line.strip()
            if not line:
                continue

            # Simple tokenization
            if line.startswith('escreva('):
                content = line[8:-1] if line.endswith(')') else line[8:]
                tokens.append({'type': 'PRINT', 'content': content, 'line': line_num})
            elif line.startswith('leia('):
                var = line[5:-1] if line.endswith(')') else line[5:]
                tokens.append({'type': 'INPUT', 'var': var.strip(), 'line': line_num})
            elif line.startswith('se ('):
                match = re.match(r'se\s*\((.*)\)', line)
                if match:
                    tokens.append({'type': 'IF', 'condition': match.group(1), 'line': line_num})
            elif line.startswith('enquanto ('):
                match = re.match(r'enquanto\s*\((.*)\)', line)
                if match:
                    tokens.append({'type': 'WHILE', 'condition': match.group(1), 'line': line_num})
            elif line.startswith('para ('):
                match = re.match(r'para\s*\((.*?);\s*(.*?);\s*(.*)\)', line)
                if match:
                    tokens.append({'type': 'FOR', 'init': match.group(1), 'cond': match.group(2), 'inc': match.group(3), 'line': line_num})
            elif line.startswith('funcao '):
                match = re.match(r'funcao\s+(\w+)\s*\((.*?)\)', line)
                if match:
                    tokens.append({'type': 'FUNC', 'name': match.group(1), 'params': match.group(2), 'line': line_num})
            elif line.startswith('retorna '):
                tokens.append({'type': 'RETURN', 'value': line.split(' ', 1)[1], 'line': line_num})
            elif line == '}':
                tokens.append({'type': 'BLOCK_END', 'line': line_num})
            elif '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
                parts = line.split('=', 1)
                tokens.append({'type': 'ASSIGN', 'var': parts[0].strip(), 'value': parts[1].strip(), 'line': line_num})
            elif '(' in line and ')' in line:
                func_match = re.match(r'(\w+)\s*\((.*?)\)', line)
                if func_match:
                    tokens.append({'type': 'CALL', 'name': func_match.group(1), 'args': func_match.group(2), 'line': line_num})

        return tokens

    def _generate_c(self, tokens):
        """Gera código C a partir dos tokens"""
        lines = []
        lines.append('/* ULX Compiler Output */')
        lines.append('#include <stdio.h>')
        lines.append('#include <stdlib.h>')
        lines.append('#include <string.h>')
        lines.append('#include <stdbool.h>')
        lines.append('')
        lines.append('#pragma GCC optimize("O3")')
        lines.append('')
        lines.append('int main() {')

        for token in tokens:
            ttype = token['type']

            if ttype == 'PRINT':
                content = token['content'].strip()
                # Simple string handling
                if content.startswith('"') and content.endswith('"'):
                    lines.append(f'    printf({content});')
                elif ',' in content:
                    parts = content.split(',')
                    format_str = ''
                    for p in parts:
                        p = p.strip()
                        if p.startswith('"'):
                            format_str += p.replace('"', '')
                        else:
                            format_str += '%s'
                    lines.append(f'    printf("{format_str}\\n");')
                else:
                    lines.append(f'    printf("{content}\\n");')

            elif ttype == 'INPUT':
                var = token['var']
                lines.append(f'    char {var}[256];')
                lines.append(f'    scanf("%255s", {var});')
                lines.append(f'    // {var} lido com sucesso')

            elif ttype == 'ASSIGN':
                var = token['var']
                val = token['value'].strip()
                if val.startswith('"') and val.endswith('"'):
                    lines.append(f'    char* {var} = {val};')
                elif val.isdigit():
                    lines.append(f'    int {var} = {val};')
                elif val.replace('.', '').isdigit():
                    lines.append(f'    double {var} = {val};')
                else:
                    lines.append(f'    int {var} = {val};')

            elif ttype == 'IF':
                cond = token['condition']
                lines.append(f'    if ({cond}) {{')

            elif ttype == 'WHILE':
                cond = token['condition']
                lines.append(f'    while ({cond}) {{')

            elif ttype == 'FOR':
                init = token['init']
                cond = token['cond']
                inc = token['inc']
                lines.append(f'    for ({init}; {cond}; {inc}) {{')

            elif ttype == 'FUNC':
                name = token['name']
                params = token['params']
                lines.append(f'    int {name}({params}) {{')

            elif ttype == 'RETURN':
                lines.append(f'    return {token["value"]};')

            elif ttype == 'BLOCK_END':
                lines.append('    }')

        lines.append('    return 0;')
        lines.append('}')

        return '\n'.join(lines)

    def _compile_c(self, c_file):
        """Compila código C para binário"""
        compile_cmd = [
            'gcc', '-O3', '-march=native', '-static', '-s',
            c_file, '-o', self.output, '-lm'
        ]

        try:
            result = subprocess.run(compile_cmd, capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            print("[ERRO] GCC não encontrado")
            return False


def main():
    parser = argparse.ArgumentParser(description='CLX Compiler - Compilador Universal ULX/ULV')
    parser.add_argument('source', help='Arquivo ULX ou ULV')
    parser.add_argument('-o', '--output', help='Nome do binário de saída')
    parser.add_argument('-c', '--c-only', action='store_true', help='Gerar apenas C')
    parser.add_argument('--visual', action='store_true', help='Abrir visualizador')

    args = parser.parse_args()

    compiler = UniversalCompiler(args.source, args.output, [])

    if args.c_only:
        compiler.read_source()
        compiler.detect_type()
        if compiler.file_type == 'ULV':
            compiler.source = compiler._convert_ulv_to_ulx()
        tokens = compiler._tokenize(compiler.source)
        c_code = compiler._generate_c(tokens)
        c_file = f"{compiler.output}.c"
        with open(c_file, 'w') as f:
            f.write(c_code)
        print(f"Código C gerado: {c_file}")
        sys.exit(0)

    success = compiler.compile()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
