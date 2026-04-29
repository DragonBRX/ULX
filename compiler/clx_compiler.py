#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLX Compiler - Compilador ULX v3.0
Traduz código ULX para binário nativo otimizado
Suporta: Linux, Windows, MacOS

Uso: ulx-compile <arquivo.ulx> [-o saida] [--visual]
"""

import sys
import re
import subprocess
import os
import argparse
import json
import platform
from pathlib import Path


class HardwareDetector:
    """Detecta hardware e determina estratégia de otimização"""

    def __init__(self):
        self.cpu_cores = os.cpu_count() or 1
        self.os_type = platform.system()
        self.has_avx2 = self._check_avx2()
        self.has_avx512 = self._check_avx512()
        self.has_gpu = self._check_gpu()
        self.ram_gb = self._get_ram_gb()
        self.arch = self._detect_arch()
        self.cpu_model = self._get_cpu_model()
        self.cc_path = self._find_c_compiler()

    def _check_avx2(self):
        if self.os_type == "Windows":
            return True
        try:
            with open('/proc/cpuinfo', 'r') as f:
                return 'avx2' in f.read()
        except:
            return False

    def _check_avx512(self):
        if self.os_type == "Windows":
            return False
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                return 'avx512' in cpuinfo or 'avx512f' in cpuinfo
        except:
            return False

    def _check_gpu(self):
        if self.os_type == "Windows":
            try:
                result = subprocess.run(['nvidia-smi'], capture_output=True, timeout=2)
                return result.returncode == 0
            except:
                return False
        try:
            result = subprocess.run(['which', 'nvidia-smi'], capture_output=True, timeout=1)
            if result.returncode == 0:
                return True
            result = subprocess.run(['lspci'], capture_output=True, text=True, timeout=2)
            return any(g in result.stdout for g in ['VGA', '3D controller', 'Display'])
        except:
            return False

    def _get_ram_gb(self):
        if self.os_type == "Windows":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulong = ctypes.c_ulong
                class MEMORYSTATUS(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", c_ulong),
                        ("dwMemoryLoad", c_ulong),
                        ("dwTotalPhys", c_ulong),
                        ("dwAvailPhys", c_ulong),
                        ("dwTotalPageFile", c_ulong),
                        ("dwAvailPageFile", c_ulong),
                        ("dwTotalVirtual", c_ulong),
                        ("dwAvailVirtual", c_ulong),
                    ]
                memstatus = MEMORYSTATUS()
                memstatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
                kernel32.GlobalMemoryStatus(ctypes.byref(memstatus))
                return memstatus.dwTotalPhys / (1024**3)
            except:
                return 8
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        kb = int(line.split()[1])
                        return kb / (1024 * 1024)
        except:
            return 8

    def _detect_arch(self):
        machine = platform.machine()
        return machine

    def _get_cpu_model(self):
        if self.os_type == "Windows":
            return "Windows Host"
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        return line.split(':')[1].strip()
        except:
            return platform.processor() or "Unknown"

    def _find_c_compiler(self):
        compilers = ['gcc', 'clang', 'cc']
        if self.os_type == "Windows":
            compilers = ['gcc', 'clang-cl', 'cl']
        for cc in compilers:
            result = subprocess.run(['which', cc], capture_output=True)
            if result.returncode == 0:
                return cc
        return 'gcc'

    def get_strategy(self):
        return {
            'cpu_cores': self.cpu_cores,
            'ram_gb': self.ram_gb,
            'use_simd': self.has_avx2,
            'use_avx512': self.has_avx512,
            'use_gpu': self.has_gpu,
            'arch': self.arch,
            'cpu_model': self.cpu_model,
            'use_parallel': self.cpu_cores >= 4,
            'os_type': self.os_type,
            'cc': self.cc_path,
        }

    def print_info(self):
        s = self.get_strategy()
        print(f"[CLX] Sistema: {s['os_type']}")
        print(f"[CLX] CPU: {s['cpu_model']}")
        print(f"[CLX] Arquitetura: {s['arch']}")
        print(f"[CLX] Cores: {s['cpu_cores']}")
        print(f"[CLX] RAM: {s['ram_gb']:.1f} GB")
        print(f"[CLX] AVX2: {'Sim' if s['use_simd'] else 'Não'}")
        print(f"[CLX] AVX-512: {'Sim' if s['use_avx512'] else 'Não'}")
        print(f"[CLX] GPU: {'Detectada' if s['use_gpu'] else 'Não'}")
        print(f"[CLX] Compilador C: {s['cc']}")


class ULXParser:
    """Parser da linguagem ULX"""

    KEYWORDS = {
        'escreva': 'PRINT',
        'mostre': 'PRINT',
        'print': 'PRINT',
        'leia': 'INPUT',
        'leia_linha': 'INPUT_LINE',
        'se': 'IF',
        'senao': 'ELSE',
        'enquanto': 'WHILE',
        'para': 'FOR',
        'funcao': 'FUNC',
        'retorna': 'RETURN',
        'continua': 'CONTINUE',
        'pare': 'BREAK',
        'tenta': 'TRY',
        'captura': 'CATCH',
        'lanca': 'THROW',
        'verdadeiro': 'TRUE',
        'falso': 'FALSE',
        'nulo': 'NULL',
        'importar': 'IMPORT',
        'classe': 'CLASS',
        'novo': 'NEW',
        'isto': 'THIS',
        'verdade': 'TRUE',
        'mentira': 'FALSE',
        'nada': 'NULL',
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.pos = 0
        self.errors = []
        self.line_num = 0

    def tokenize(self):
        lines = self.source.split('\n')
        self.line_num = len(lines)

        for line_num, line in enumerate(lines, 1):
            original_line = line
            # Remove comments
            if '//' in line:
                line = line[:line.index('//')]

            line = line.strip()
            if not line:
                continue

            try:
                self._tokenize_line(line, line_num)
            except Exception as e:
                self.errors.append(f"Linha {line_num}: {e}")

        if self.errors:
            print(f"[CLX] {len(self.errors)} erro(s) encontrado(s):")
            for err in self.errors:
                print(f"  - {err}")

        return self.tokens

    def _tokenize_line(self, line, line_num):
        # Multi-statement lines (separated by ;)
        statements = [s.strip() for s in line.split(';')]

        for stmt in statements:
            if not stmt:
                continue
            self._parse_statement(stmt, line_num)

    def _parse_statement(self, line, line_num):
        # Print commands
        if line.startswith('escreva(') or line.startswith('mostre(') or line.startswith('print('):
            content = line[line.index('(')+1:]
            if content.endswith(')'):
                content = content[:-1]
            self.tokens.append({'type': 'PRINT', 'content': content, 'line': line_num})

        # Input
        elif line.startswith('leia('):
            var = line[5:-1] if line.endswith(')') else line[5:]
            self.tokens.append({'type': 'INPUT', 'var': var.strip(), 'line': line_num})

        elif line.startswith('leia_linha('):
            var = line[11:-1] if line.endswith(')') else line[11:]
            self.tokens.append({'type': 'INPUT_LINE', 'var': var.strip(), 'line': line_num})

        # If statement
        elif line.startswith('se ('):
            match = re.match(r'se\s*\((.*)\)\s*\{?', line)
            if match:
                self.tokens.append({'type': 'IF', 'condition': match.group(1).strip(), 'line': line_num})

        # Else if / Else
        elif line.startswith('senao se') or line.startswith('senao'):
            self.tokens.append({'type': 'ELSE', 'line': line_num})

        # While loop
        elif line.startswith('enquanto ('):
            match = re.match(r'enquanto\s*\((.*)\)\s*\{?', line)
            if match:
                self.tokens.append({'type': 'WHILE', 'condition': match.group(1).strip(), 'line': line_num})

        # For loop
        elif line.startswith('para ('):
            match = re.match(r'para\s*\((.*?);\s*(.*?);\s*(.*)\)\s*\{?', line)
            if match:
                self.tokens.append({
                    'type': 'FOR',
                    'init': match.group(1).strip(),
                    'condition': match.group(2).strip(),
                    'increment': match.group(3).strip(),
                    'line': line_num
                })

        # Function definition
        elif line.startswith('funcao ') or line.startswith('função '):
            match = re.match(r'funcao\s+(\w+)\s*\((.*?)\)\s*\{?', line.replace('ção', 'cao'))
            if match:
                params = match.group(2).strip()
                self.tokens.append({
                    'type': 'FUNC_DEF',
                    'name': match.group(1),
                    'params': [p.strip() for p in params.split(',')] if params else [],
                    'line': line_num
                })

        # Return
        elif line.startswith('retorna ') or line.startswith('volta '):
            value = line.split(' ', 1)[1].strip()
            self.tokens.append({'type': 'RETURN', 'value': value, 'line': line_num})

        # Continue / Break
        elif line == 'continua':
            self.tokens.append({'type': 'CONTINUE', 'line': line_num})
        elif line == 'pare':
            self.tokens.append({'type': 'BREAK', 'line': line_num})

        # Block end
        elif line == '}':
            self.tokens.append({'type': 'BLOCK_END', 'line': line_num})

        # Try / Catch
        elif line.startswith('tenta {'):
            self.tokens.append({'type': 'TRY', 'line': line_num})
        elif line.startswith('captura ('):
            match = re.match(r'captura\s*\((.*)\)\s*\{?', line)
            if match:
                self.tokens.append({'type': 'CATCH', 'var': match.group(1).strip(), 'line': line_num})
        elif line.startswith('lanca ') or line.startswith('lança '):
            value = line.split(' ', 1)[1].strip()
            self.tokens.append({'type': 'THROW', 'value': value, 'line': line_num})

        # Import
        elif line.startswith('importar ') or line.startswith('import '):
            module = line.split(' ', 1)[1].strip()
            self.tokens.append({'type': 'IMPORT', 'module': module, 'line': line_num})

        # Class definition
        elif line.startswith('classe ') or line.startswith('class '):
            match = re.match(r'classe\s+(\w+)\s*\{?', line.replace('class ', 'classe '))
            if match:
                self.tokens.append({'type': 'CLASS_DEF', 'name': match.group(1), 'line': line_num})

        # Assignment (including arrays and dicts)
        elif '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=', '+=', '-=', '*=', '/=']):
            self._parse_assignment(line, line_num)

        # Compound assignment
        elif '+=' in line:
            var = line.split('+=')[0].strip()
            val = line.split('+=', 1)[1].strip()
            self.tokens.append({'type': 'ASSIGN', 'var': var, 'value': f'{var} + {val}', 'line': line_num})
        elif '-=' in line:
            var = line.split('-=')[0].strip()
            val = line.split('-=', 1)[1].strip()
            self.tokens.append({'type': 'ASSIGN', 'var': var, 'value': f'{var} - {val}', 'line': line_num})

        # Function call (without assignment)
        elif '(' in line and line.endswith(')'):
            func_name = line[:line.index('(')]
            args = line[line.index('(')+1:-1]
            self.tokens.append({
                'type': 'FUNC_CALL',
                'name': func_name,
                'args': self._split_args(args),
                'line': line_num
            })

    def _split_args(self, content):
        """Split arguments respecting strings and nested parentheses"""
        args = []
        current = ''
        in_string = False
        paren_depth = 0

        for char in content:
            if char == '"' and (not current or current[-1] != '\\'):
                in_string = not in_string
            elif char == '(' and not in_string:
                paren_depth += 1
            elif char == ')' and not in_string:
                paren_depth -= 1
            elif char == ',' and not in_string and paren_depth == 0:
                args.append(current)
                current = ''
                continue
            current += char

        if current.strip():
            args.append(current)

        return args

    def _parse_assignment(self, line, line_num):
        parts = line.split('=', 1)
        var = parts[0].strip()
        value = parts[1].strip()

        # Check for compound assignment operators
        if len(parts[0]) > 1 and parts[0][-1] in ['+', '-', '*', '/']:
            op = parts[0][-1]
            var = parts[0][:-1].strip()
            value = f"{var} {op} {parts[1].strip()}"

        self.tokens.append({
            'type': 'ASSIGN',
            'var': var,
            'value': value,
            'line': line_num
        })

    def parse(self):
        return self.tokenize()


class CGenerator:
    """Gera código C a partir dos tokens ULX"""

    def __init__(self, tokens, strategy=None):
        self.tokens = tokens
        self.strategy = strategy or {}
        self.c_code = []
        self.indent_level = 0
        self.var_types = {}
        self.functions = []
        self.includes = set()
        self.helper_functions = []

    def _indent(self):
        return '    ' * self.indent_level

    def generate(self):
        self._generate_headers()
        self._generate_helper_functions()

        main_tokens = []
        func_tokens = []

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token['type'] == 'FUNC_DEF':
                func_block = [token]
                brace_count = 1
                i += 1
                while i < len(self.tokens) and brace_count > 0:
                    t = self.tokens[i]
                    func_block.append(t)
                    if t['type'] == 'BLOCK_END':
                        brace_count -= 1
                    elif t['type'] in ['IF', 'WHILE', 'FOR', 'FUNC_DEF', 'TRY', 'CLASS_DEF']:
                        brace_count += 1
                    i += 1
                func_tokens.extend(func_block)
            else:
                main_tokens.append(token)
                i += 1

        for token in func_tokens:
            self._generate_token(token, in_function=True)

        if main_tokens:
            self.c_code.append('\nint main(int argc, char* argv[]) {')
            self.indent_level = 1
            for token in main_tokens:
                self._generate_token(token, in_function=False)
            self.c_code.append(f'{self._indent()}return 0;')
            self.c_code.append('}')

        return '\n'.join(self.c_code)

    def _generate_headers(self):
        self.includes.add('#include <stdio.h>')
        self.includes.add('#include <stdlib.h>')
        self.includes.add('#include <string.h>')
        self.includes.add('#include <math.h>')
        self.includes.add('#include <stdbool.h>')

        if self.strategy.get('os_type') != 'Windows':
            self.includes.add('#include <unistd.h>')
            self.includes.add('#include <sys/socket.h>')
            self.includes.add('#include <netinet/in.h>')
            self.includes.add('#include <arpa/inet.h>')
            self.includes.add('#include <dirent.h>')
            self.includes.add('#include <sys/types.h>')
            self.includes.add('#include <sys/stat.h>')
            self.includes.add('#include <fcntl.h>')
            self.includes.add('#include <errno.h>')

        for inc in sorted(self.includes):
            self.c_code.append(inc)

        self.c_code.append('')

        if self.strategy.get('use_simd'):
            self.c_code.append('#pragma GCC optimize("O3,fast-math")')
            self.c_code.append('#pragma GCC target("avx2")')
        else:
            self.c_code.append('#pragma GCC optimize("O3")')

        self.c_code.append('')

    def _generate_helper_functions(self):
        self.helper_functions = [
            '''
char** ulx_split(const char* str, const char* delim, int* count) {
    char* copy = strdup(str);
    char* token = strtok(copy, delim);
    char** result = NULL;
    *count = 0;
    while (token) {
        result = realloc(result, (*count + 1) * sizeof(char*));
        result[*count] = strdup(token);
        (*count)++;
        token = strtok(NULL, delim);
    }
    free(copy);
    return result;
}

char* ulx_join(char** arr, int count, const char* delim) {
    if (count == 0) return strdup("");
    int total_len = 0;
    for (int i = 0; i < count; i++) total_len += strlen(arr[i]);
    total_len += (count - 1) * strlen(delim) + 1;
    char* result = malloc(total_len);
    result[0] = '\\0';
    for (int i = 0; i < count; i++) {
        if (i > 0) strcat(result, delim);
        strcat(result, arr[i]);
    }
    return result;
}

char* ulx_texto(int num) {
    char* buf = malloc(32);
    sprintf(buf, "%d", num);
    return buf;
}

double ulx_pow(double base, double exp) {
    return pow(base, exp);
}

double ulx_sqrt(double num) {
    return sqrt(num);
}

double ulx_sin(double num) {
    return sin(num);
}

double ulx_cos(double num) {
    return cos(num);
}

double ulx_tan(double num) {
    return tan(num);
}

double ulx_log(double num) {
    return log(num);
}

double ulx_log10(double num) {
    return log10(num);
}
'''
        ]

        for helper in self.helper_functions:
            self.c_code.append(helper)

    def _detect_type(self, value):
        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            return 'char*'
        if value.startswith("'") and value.endswith("'"):
            return 'char'
        if value in ['verdadeiro', 'verdade', 'TRUE', 'true']:
            return 'int'
        if value in ['falso', 'mentira', 'FALSE', 'false']:
            return 'int'
        if value == 'nulo' or value == 'nada' or value == 'NULL':
            return 'void*'

        if re.match(r'^\[.*\]$', value):
            return 'array'
        if re.match(r'^\{.*\}$', value):
            return 'dict'

        if '(' in value:
            func_name = value[:value.index('(')]
            string_funcs = ['le', 'texto', 'substring', 'maiuscula', 'minuscula',
                          'trim', 'split', 'join', 'tipo', 'leia_linha', 'executa']
            if func_name in string_funcs:
                return 'char*'
            int_funcs = ['tamanho', 'abs', 'sqrt', 'floor', 'ceil', 'round',
                        'inteiro', 'indice', 'cria_socket', 'aceita', 'len']
            if func_name in int_funcs:
                return 'int'
            float_funcs = ['pow', 'sen', 'cos', 'tan', 'log', 'log10', 'sin', 'seno', 'cosseno', 'tangente']
            if func_name in float_funcs:
                return 'double'

        if '+' in value and ('"' in value or "'" in value):
            return 'char*'

        if re.match(r'^-?\d+\.\d+$', value):
            return 'double'
        if re.match(r'^-?\d+$', value):
            return 'int'

        if any(op in value for op in ['+', '-', '*', '/', '%', '^']):
            return self._detect_expr_type(value)

        return 'int'

    def _detect_expr_type(self, expr):
        if '"' in expr or "'" in expr:
            return 'char*'
        if '.' in expr:
            return 'double'
        return 'int'

    def _generate_token(self, token, in_function=False):
        ttype = token['type']

        if ttype == 'PRINT':
            self._generate_print(token)
        elif ttype == 'INPUT':
            self._generate_input(token)
        elif ttype == 'INPUT_LINE':
            self._generate_input_line(token)
        elif ttype == 'ASSIGN':
            self._generate_assignment(token)
        elif ttype == 'IF':
            self._generate_if(token)
        elif ttype == 'ELSE':
            self._generate_else(token)
        elif ttype == 'WHILE':
            self._generate_while(token)
        elif ttype == 'FOR':
            self._generate_for(token)
        elif ttype == 'FUNC_DEF':
            self._generate_func_def(token)
        elif ttype == 'FUNC_CALL':
            self._generate_func_call(token)
        elif ttype == 'RETURN':
            self._generate_return(token)
        elif ttype == 'CONTINUE':
            self.c_code.append(f'{self._indent()}continue;')
        elif ttype == 'BREAK':
            self.c_code.append(f'{self._indent()}break;')
        elif ttype == 'TRY':
            self._generate_try(token)
        elif ttype == 'CATCH':
            self._generate_catch(token)
        elif ttype == 'THROW':
            self._generate_throw(token)
        elif ttype == 'IMPORT':
            self._generate_import(token)
        elif ttype == 'CLASS_DEF':
            self._generate_class_def(token)
        elif ttype == 'BLOCK_END':
            self.indent_level = max(0, self.indent_level - 1)
            self.c_code.append(f'{self._indent()}}}')

    def _generate_print(self, token):
        content = token['content']
        parts = self._split_args(content)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            if part.startswith('"') and part.endswith('"'):
                self.c_code.append(f'{self._indent()}printf({part});')
            elif part in self.var_types:
                vtype = self.var_types[part]
                if vtype == 'char*':
                    self.c_code.append(f'{self._indent()}printf("%s", {part});')
                elif vtype == 'double':
                    self.c_code.append(f'{self._indent()}printf("%g", {part});')
                else:
                    self.c_code.append(f'{self._indent()}printf("%d", {part});')
            else:
                vtype = self._detect_type(part)
                if vtype == 'char*':
                    self.c_code.append(f'{self._indent()}printf("%s", {part});')
                elif vtype == 'double':
                    self.c_code.append(f'{self._indent()}printf("%g", {part});')
                else:
                    self.c_code.append(f'{self._indent()}printf("%d", {part});')

        self.c_code.append(f'{self._indent()}printf("\\n");')

    def _split_args(self, content):
        args = []
        current = ''
        in_string = False
        paren_depth = 0

        for char in content:
            if char == '"' and (not current or current[-1] != '\\'):
                in_string = not in_string
            elif char == '(' and not in_string:
                paren_depth += 1
            elif char == ')' and not in_string:
                paren_depth -= 1
            elif char == ',' and not in_string and paren_depth == 0:
                args.append(current)
                current = ''
                continue
            current += char

        if current.strip():
            args.append(current)

        return args

    def _generate_input(self, token):
        var = token.get('var', 'input')
        self.c_code.append(f'{self._indent()}char {var}_buf[4096];')
        self.c_code.append(f'{self._indent()}if (fgets({var}_buf, sizeof({var}_buf), stdin)) {{')
        self.c_code.append(f'{self._indent()}    {var}_buf[strcspn({var}_buf, "\\n")] = 0;')
        self.c_code.append(f'{self._indent()}    {var} = strdup({var}_buf);')
        self.c_code.append(f'{self._indent()}}}')
        self.var_types[var] = 'char*'

    def _generate_input_line(self, token):
        self._generate_input(token)

    def _generate_assignment(self, token):
        var = token['var']
        value = token['value']

        vtype = self._detect_type(value)
        self.var_types[var] = vtype

        if vtype == 'array':
            items = re.findall(r'\[(.*?)\]', value)
            if items:
                item_list = [i.strip() for i in items[0].split(',')]
                self.c_code.append(f'{self._indent()}int {var}[] = {{{", ".join(item_list)}}};')
                return

        if vtype == 'dict':
            self.c_code.append(f'{self._indent()}// Dicionário: {var}')
            return

        if vtype == 'char*':
            if '"' in value and '+' in value:
                parts = re.findall(r'"[^"]*"|\w+', value)
                parts = [p for p in parts if p.strip()]
                if len(parts) >= 2:
                    self.c_code.append(f'{self._indent()}char* {var} = malloc(4096);')
                    first = True
                    for p in parts:
                        if p.startswith('"'):
                            if first:
                                self.c_code.append(f'{self._indent()}strcpy({var}, {p});')
                                first = False
                            else:
                                self.c_code.append(f'{self._indent()}strcat({var}, {p});')
                        else:
                            self.c_code.append(f'{self._indent()}strcat({var}, {p});')
                    return

            self.c_code.append(f'{self._indent()}char* {var} = {value};')
            return

        c_value = value.replace('^', '**').replace('**', '^')

        if vtype == 'double':
            self.c_code.append(f'{self._indent()}double {var} = {c_value};')
        else:
            self.c_code.append(f'{self._indent()}int {var} = {c_value};')

    def _generate_if(self, token):
        condition = token['condition']
        self.c_code.append(f'{self._indent()}if ({condition}) {{')
        self.indent_level += 1

    def _generate_else(self, token):
        self.indent_level = max(0, self.indent_level - 1)
        self.c_code.append(f'{self._indent()}}} else {{')
        self.indent_level += 1

    def _generate_while(self, token):
        condition = token['condition']
        self.c_code.append(f'{self._indent()}while ({condition}) {{')
        self.indent_level += 1

    def _generate_for(self, token):
        init = token['init']
        condition = token['condition']
        increment = token['increment']

        var_match = re.match(r'^(\w+)\s*=', init)
        if var_match:
            loop_var = var_match.group(1)
            if loop_var not in self.var_types:
                self.c_code.append(f'{self._indent()}int {init};')
                self.c_code.append(f'{self._indent()}for ({loop_var} = {init.split("=", 1)[1].strip()}; {condition}; {increment}) {{')
                self.var_types[loop_var] = 'int'
                self.indent_level += 1
                return

        self.c_code.append(f'{self._indent()}for ({init}; {condition}; {increment}) {{')
        self.indent_level += 1

    def _generate_func_def(self, token):
        name = token['name']
        params = token['params']
        c_params = ', '.join([f'int {p}' for p in params]) if params else 'void'
        self.c_code.append(f'\nint {name}({c_params}) {{')
        self.indent_level = 1
        self.functions.append(name)

    def _generate_func_call(self, token):
        name = token['name']
        args = token['args']

        func_map = {
            'tamanho': ('(int)strlen', 'char*'),
            'len': ('(int)strlen', 'char*'),
            'abs': ('abs', 'int'),
            'sqrt': ('ulx_sqrt', 'double'),
            'pow': ('ulx_pow', 'double'),
            'floor': ('floor', 'double'),
            'ceil': ('ceil', 'double'),
            'sen': ('ulx_sin', 'double'),
            'seno': ('ulx_sin', 'double'),
            'cos': ('ulx_cos', 'double'),
            'cosseno': ('ulx_cos', 'double'),
            'tan': ('ulx_tan', 'double'),
            'tangente': ('ulx_tan', 'double'),
            'log': ('ulx_log', 'double'),
            'log10': ('ulx_log10', 'double'),
            'texto': ('ulx_texto', 'char*'),
            'maiuscula': ('strupr', 'char*'),
            'minuscula': ('strlwr', 'char*'),
            'trim': ('trim', 'char*'),
            'inteiro': ('atoi', 'int'),
            'float': ('atof', 'double'),
            'split': ('ulx_split', 'char**'),
            'join': ('ulx_join', 'char*'),
            'tamanho': ('strlen', 'int'),
            'indice': ('(int)strstr', 'int'),
        }

        if name in func_map:
            c_name, _ = func_map[name]
            args_str = ', '.join(args) if args else ''
            self.c_code.append(f'{self._indent()}{c_name}({args_str});')
        else:
            args_str = ', '.join(args) if args else ''
            self.c_code.append(f'{self._indent()}{name}({args_str});')

    def _generate_return(self, token):
        value = token['value']
        self.c_code.append(f'{self._indent()}return {value};')

    def _generate_try(self, token):
        self.c_code.append(f'{self._indent()}{{ // try')
        self.indent_level += 1

    def _generate_catch(self, token):
        self.indent_level = max(0, self.indent_level - 1)
        var = token.get('var', 'e')
        self.c_code.append(f'{self._indent()}}} // catch ({var})')
        self.indent_level += 1

    def _generate_throw(self, token):
        value = token['value']
        self.c_code.append(f'{self._indent()}fprintf(stderr, "Erro: %s\\n", {value});')

    def _generate_import(self, token):
        module = token['module']
        self.c_code.append(f'{self._indent()}// import {module}')

    def _generate_class_def(self, token):
        name = token['name']
        self.c_code.append(f'// class {name}')


class CLXCompiler:
    """Compilador ULX completo"""

    def __init__(self, source_file, output=None, flags=None, strategy=None):
        self.source_file = source_file
        self.output = output or os.path.splitext(os.path.basename(source_file))[0]
        self.custom_flags = flags or []
        self.detector = strategy or HardwareDetector()
        self.strategy = self.detector.get_strategy()
        self.source = None

    def read_source(self):
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.source = f.read()
            return True
        except FileNotFoundError:
            print(f"[CLX] Erro: Arquivo '{self.source_file}' não encontrado")
            return False
        except Exception as e:
            print(f"[CLX] Erro ao ler arquivo: {e}")
            return False

    def compile(self):
        if not self.read_source():
            return False

        print("=" * 60)
        print("   ULX Compiler (CLX) v3.0")
        print("=" * 60)

        self.detector.print_info()

        print(f"\n[Fase 1] Analisando: {self.source_file}")
        parser = ULXParser(self.source)
        tokens = parser.parse()
        print(f"[Fase 1] {len(tokens)} tokens processados")

        if parser.errors:
            print("[CLX] Erros de sintaxe encontrados. Correção necessária.")
            return False

        print(f"\n[Fase 2] Gerando código C...")
        generator = CGenerator(tokens, self.strategy)
        c_code = generator.generate()

        c_file = f"{self.output}.c"
        with open(c_file, 'w', encoding='utf-8') as f:
            f.write(c_code)
        print(f"[Fase 2] Código C: {c_file}")

        print(f"\n[Fase 3] Compilando binário...")

        compile_cmd = self._build_compile_command(c_file)

        try:
            result = subprocess.run(compile_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                size = os.path.getsize(self.output)
                print(f"\n[OK] Binário: {self.output}")
                print(f"[OK] Tamanho: {size:,} bytes ({size/1024:.1f} KB)")
                print("=" * 60)
                print("   COMPILAÇÃO BEM-SUCEDIDA!")
                print("=" * 60)
                print(f"Execute: ./{self.output}")
                return True
            else:
                print(f"\n[ERRO] Falha na compilação:")
                print(result.stderr)
                return False

        except FileNotFoundError:
            print(f"[ERRO] Compilador C não encontrado: {self.strategy['cc']}")
            print("Instale com:")
            print("  Ubuntu/Debian: sudo apt install gcc")
            print("  Fedora: sudo dnf install gcc")
            print("  Windows: Instale MinGW ou MSVC")
            return False

    def _build_compile_command(self, c_file):
        flags = [
            self.strategy['cc'],
            '-O3',
            '-march=native',
            '-mtune=native',
            '-static',
            '-s',
            '-pthread',
            '-flto',
            '-ffast-math',
            '-funroll-loops',
            '-finline-functions',
            '-fomit-frame-pointer',
            '-Wall',
            '-Wextra',
        ]

        if self.strategy.get('use_simd'):
            flags.extend(['-mavx2', '-ftree-vectorize'])

        if self.strategy.get('use_avx512'):
            flags.append('-mavx512f')

        flags.extend(self.custom_flags)
        flags.extend([c_file, '-o', self.output, '-lm'])

        return flags


def main():
    parser = argparse.ArgumentParser(description='Compilador ULX (CLX) v3.0')
    parser.add_argument('source', help='Arquivo .ulx para compilar')
    parser.add_argument('-o', '--output', help='Nome do binário de saída')
    parser.add_argument('-c', '--c-only', action='store_true', help='Gerar apenas código C')
    parser.add_argument('--flags', nargs='+', help='Flags adicionais para gcc')
    parser.add_argument('--visual', action='store_true', help='Abrir visualizador após compilar')

    args = parser.parse_args()

    if not args.source.endswith('.ulx'):
        print(f"[AVISO] O arquivo não tem extensão .ulx")

    compiler = CLXCompiler(args.source, args.output, args.flags)

    if args.c_only:
        if not compiler.read_source():
            sys.exit(1)
        parser = ULXParser(compiler.source)
        tokens = parser.parse()
        generator = CGenerator(tokens, compiler.strategy)
        c_code = generator.generate()
        c_file = f"{compiler.output}.c"
        with open(c_file, 'w') as f:
            f.write(c_code)
        print(f"Código C gerado: {c_file}")
        sys.exit(0)

    success = compiler.compile()

    if success and args.visual:
        print("\n[VISUAL] Abrindo visualizador...")
        os.system(f'ulx-visual "{compiler.output}"' if os.name != 'nt' else f'ulx-visual.exe "{compiler.output}"')

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
