#!/usr/bin/env python3
"""
ULD Builder - Universal Language Distribution
Quinta Base do ULX - Sistema de Build e Distribuicao

Transforma codigo ULX/ULV em executaveis nativos
para Windows, Linux, macOS, Android e Web.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Cores para terminal
class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class ULDBuilder:
    """Construtor de executaveis ULD"""

    TARGETS = {
        'windows': {
            'extension': '.exe',
            'compiler': 'gcc',
            'platform': 'win32',
            'template': 'window_c'
        },
        'linux': {
            'extension': '',
            'compiler': 'gcc',
            'platform': 'linux',
            'template': 'window_c'
        },
        'macos': {
            'extension': '.app',
            'compiler': 'clang',
            'platform': 'darwin',
            'template': 'window_c'
        },
        'android': {
            'extension': '.apk',
            'compiler': 'ndk',
            'platform': 'android',
            'template': 'android_java'
        },
        'web': {
            'extension': '.html',
            'compiler': None,
            'platform': 'web',
            'template': 'web_js'
        }
    }

    def __init__(self):
        self.verbose = False
        self.project_dir = Path(__file__).parent.parent

    def log(self, mensagem: str, tipo: str = "info"):
        """Log colorizado"""
        cores = {
            'info': Cores.AZUL,
            'sucesso': Cores.VERDE,
            'aviso': Cores.AMARELO,
            'erro': Cores.VERMELHO
        }
        print(f"{cores.get(tipo, '')}{mensagem}{Cores.RESET}")

    def verbose_log(self, mensagem: str):
        """Log detalhado se verbose=True"""
        if self.verbose:
            self.log(f"  [DEBUG] {mensagem}", "info")

    def check_dependencies(self, target: str) -> bool:
        """Verifica dependencias necessarias"""
        self.log(f"Verificando dependencias para {target}...", "info")

        if target == 'web':
            self.log("  Web nao requer compilador nativo", "sucesso")
            return True

        # Verifica GCC
        try:
            result = subprocess.run(
                ['gcc', '--version'],
                capture_output=True,
                text=True
            )
            self.verbose_log(f"GCC encontrado: {result.stdout.split()[0]}")
        except FileNotFoundError:
            if target != 'android':
                self.log("ERRO: GCC nao encontrado. Instale GCC primeiro.", "erro")
                return False

        # Verifica Android SDK se target=android
        if target == 'android':
            if not os.environ.get('ANDROID_HOME'):
                self.log("AVISO: ANDROID_HOME nao definido. APK nao sera gerado.", "aviso")
                return False

        return True

    def parse_ulx(self, input_file: str) -> str:
        """Converte ULX para C usando CLX"""
        self.log("Convertendo ULX → C...", "info")

        clx_path = self.project_dir / 'clx_compiler' / 'clx_compiler.py'

        if not clx_path.exists():
            self.log("ERRO: CLX Compiler nao encontrado", "erro")
            sys.exit(1)

        try:
            result = subprocess.run(
                ['python3', str(clx_path), '-i', input_file, '-o', '/tmp/output.c'],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                self.log(f"ERRO no CLX: {result.stderr}", "erro")
                sys.exit(1)

            self.log("  ULX convertido para C", "sucesso")
            return '/tmp/output.c'

        except Exception as e:
            self.log(f"ERRO: {e}", "erro")
            sys.exit(1)

    def compile_c(self, c_file: str, output: str, target: str) -> bool:
        """Compila C para executavel nativo"""
        self.log(f"Compilando para {target}...", "info")

        compiler = self.TARGETS[target]['compiler']

        # Flags de compilacao
        flags = ['-Wall', '-Wextra', '-O2']

        if target == 'windows':
            flags.extend(['-mwindows', '-mconsole'])
            output = output.replace('/', '\\') if '\\' in output else output
        elif target == 'linux':
            flags.extend(['-no-pie'])
            if not output.startswith('/'):
                output = './' + output

        try:
            result = subprocess.run(
                [compiler, c_file, '-o', output] + flags,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                self.log(f"ERRO de compilacao:\n{result.stderr}", "erro")
                return False

            # Torna executavel no Linux
            if target == 'linux':
                os.chmod(output, 0o755)

            self.log(f"  Executavel gerado: {output}", "sucesso")
            return True

        except FileNotFoundError:
            self.log(f"ERRO: {compiler} nao encontrado", "erro")
            return False

    def generate_web(self, input_file: str, output: str) -> bool:
        """Gera HTML/JavaScript para web"""
        self.log("Gerando aplicacao web...", "info")

        # Simula conversao ULX → JS
        template = self.get_web_template()

        try:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(template)

            self.log(f"  HTML gerado: {output}", "sucesso")
            return True

        except Exception as e:
            self.log(f"ERRO: {e}", "erro")
            return False

    def get_web_template(self) -> str:
        """Template basico para web"""
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App ULX</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 {
            color: #00d4ff;
            margin-bottom: 20px;
        }
        .powered {
            margin-top: 30px;
            color: #888;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ULX App</h1>
        <p>Executando em navegador via ULD Web</p>
        <div class="powered">Powered by ULX Language</div>
    </div>
</body>
</html>'''

    def build(self, input_file: str, output: str, target: str = 'windows',
              config: Optional[Dict] = None) -> bool:
        """
        Funcao principal de build

        Args:
            input_file: Arquivo ULX/ULV de entrada
            output: Nome do arquivo de saida
            target: Plataforma alvo (windows, linux, macos, android, web)
            config: Configuracoes opcionais de build
        """
        self.log(f"{Cores.BOLD}{'='*50}{Cores.RESET}", "info")
        self.log(f"{Cores.BOLD}ULD Builder - {target.upper()}{Cores.RESET}", "info")
        self.log(f"{Cores.BOLD}{'='*50}{Cores.RESET}", "info")

        # Valida target
        if target not in self.TARGETS:
            self.log(f"ERRO: Target '{target}' nao suportado", "erro")
            self.log(f"Targets disponiveis: {', '.join(self.TARGETS.keys())}", "info")
            return False

        # Verifica arquivo de entrada
        if not Path(input_file).exists():
            self.log(f"ERRO: Arquivo '{input_file}' nao encontrado", "erro")
            return False

        # Verifica dependencias
        if not self.check_dependencies(target):
            return False

        # Adiciona extensao se necessario
        if not output:
            ext = self.TARGETS[target]['extension']
            output = Path(input_file).stem + ext

        self.verbose_log(f"Input: {input_file}")
        self.verbose_log(f"Output: {output}")
        self.verbose_log(f"Target: {target}")

        # Executa build
        if target == 'web':
            success = self.generate_web(input_file, output)
        else:
            # ULX → C → Executavel
            c_file = self.parse_ulx(input_file)
            success = self.compile_c(c_file, output, target)

            # Limpa arquivo C temporario
            if os.path.exists(c_file):
                os.remove(c_file)

        if success:
            self.log(f"{Cores.BOLD}{'='*50}{Cores.RESET}", "sucesso")
            self.log(f"Build concluido com sucesso!", "sucesso")
            self.log(f"  Arquivo: {output}", "sucesso")
            self.log(f"{Cores.BOLD}{'='*50}{Cores.RESET}", "sucesso")
        else:
            self.log("Build falhou!", "erro")

        return success


def main():
    """Interface de linha de comando"""
    parser = argparse.ArgumentParser(
        description='ULD Builder - Compila ULX para executaveis nativos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  uld_builder.py -i app.ulx -o app.exe --target windows
  uld_builder.py -i app.ulx -o app --target linux
  uld_builder.py -i app.ulx -o app.html --target web

Targets disponiveis: windows, linux, macos, android, web
        '''
    )

    parser.add_argument('-i', '--input', required=True,
                       help='Arquivo ULX/ULV de entrada')
    parser.add_argument('-o', '--output', required=True,
                       help='Arquivo de saida (.exe, .apk, .html, etc)')
    parser.add_argument('-t', '--target', default='windows',
                       choices=['windows', 'linux', 'macos', 'android', 'web'],
                       help='Plataforma alvo (default: windows)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Modo detalhado')
    parser.add_argument('-c', '--config',
                       help='Arquivo de configuracao JSON')

    args = parser.parse_args()

    # Configuracoes
    config = None
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    # Executa build
    builder = ULDBuilder()
    builder.verbose = args.verbose

    success = builder.build(
        input_file=args.input,
        output=args.output,
        target=args.target,
        config=config
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
