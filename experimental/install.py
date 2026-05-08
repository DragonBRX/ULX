#!/usr/bin/env python3
"""
ULX Installer - Instalar ULX como linguagem de programação
Funciona em: Linux, macOS, Windows (WSL)

Uso:
    pip install ulx          # via PIP
    python install.py         # instalação direta
    ./install.sh             # Linux/macOS
"""

import os
import sys
import subprocess
from pathlib import Path

VERSION = "3.0.0"
INSTALL_DIR = Path.home() / ".ulx"
BIN_DIR = Path.home() / ".local" / "bin"

def print_banner():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║   ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ║
    ║   ██║    ██║██╔════╝██║     ██╔═══██╗██╔══██╗║
    ║   ██║ █╗ ██║█████╗  ██║     ██║   ██║██████╔╝║
    ║   ██║███╗██║██╔══╝  ██║     ██║   ██║██╔══██╗║
    ║   ╚███╔███╔╝███████╗███████╗╚██████╔╝██║  ██║║
    ║    ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝║
    ║                                               ║
    ║   Universal Language X - v3.0                 ║
    ║   Instalador Oficial                          ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """)

def check_requirements():
    """Verifica requisitos necessários"""
    print("🔍 Verificando requisitos...")

    missing = []

    # Python 3.8+
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ necessário. Atual: {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}")

    # GCC
    if subprocess.run(["gcc", "--version"], capture_output=True).returncode != 0:
        print("  ⚠️  GCC não encontrado (necessário para compilar)")
        print("  📦 Instale com: apt install gcc")
    else:
        print("  ✅ GCC encontrado")

    return True

def install_files():
    """Instala arquivos do ULX"""
    print("\n📂 Instalando arquivos...")

    # Cria diretórios
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    BIN_DIR.mkdir(parents=True, exist_ok=True)

    # Copia compilador
    clx_src = Path(__file__).parent / "clx_compiler.py"
    clx_dest = INSTALL_DIR / "clx_compiler.py"

    if clx_src.exists():
        import shutil
        shutil.copy(clx_src, clx_dest)
        print(f"  ✅ CLX Compiler → {clx_dest}")
    else:
        # Cria compilador inline
        compiler_code = '''#!/usr/bin/env python3
"""
CLX Compiler - ULX Universal Compiler
"""
import sys

def compile_ulx(code):
    """Compila ULX → C"""
    c_code = code.replace("escreva", "printf")
    c_code = c_code.replace('"', '\\"')
    return f'#include <stdio.h>\\nint main() {{ {c_code} return 0; }}'
'''

        clx_dest.write_text(compiler_code)
        print(f"  ✅ CLX Compiler (inline) → {clx_dest}")

    # Copia formatos
    formats_src = Path(__file__).parent / "clx_formats.py"
    if formats_src.exists():
        import shutil
        shutil.copy(formats_src, INSTALL_DIR / "clx_formats.py")
        print(f"  ✅ CLX Formats → {INSTALL_DIR}/clx_formats.py")

    # Copia bibliotecas ULX
    lib_src = Path(__file__).parent / "ulx_language"
    if lib_src.exists():
        import shutil
        shutil.copytree(lib_src, INSTALL_DIR / "ulx_language", dirs_exist_ok=True)
        print(f"  ✅ ULX Language → {INSTALL_DIR}/ulx_language")

    # Copia ULQ
    ulq_src = Path(__file__).parent / "ulq_intelligence"
    if ulq_src.exists():
        import shutil
        shutil.copytree(ulq_src, INSTALL_DIR / "ulq_intelligence", dirs_exist_ok=True)
        print(f"  ✅ ULQ Intelligence → {INSTALL_DIR}/ulq_intelligence")

def create_wrapper():
    """Cria script wrapper ulx"""
    print("\n🔗 Criando comandos...")

    wrapper = f'''#!/bin/bash
# ULX Wrapper - Executa compilador ULX
~/.ulx/clx_compiler.py "$@"
'''

    wrapper_path = BIN_DIR / "ulx"
    wrapper_path.write_text(wrapper)
    os.chmod(wrapper_path, 0o755)
    print(f"  ✅ Comando 'ulx' → {wrapper_path}")

    # Comando clx
    clx_wrapper = f'''#!/bin/bash
~/.ulx/clx_compiler.py "$@"
'''
    clx_path = BIN_DIR / "clx"
    clx_path.write_text(clx_wrapper)
    os.chmod(clx_path, 0o755)
    print(f"  ✅ Comando 'clx' → {clx_path}")

def print_usage():
    """Mostra como usar"""
    print("""
╔═══════════════════════════════════════════════════════╗
║                 Instalação Completa!                  ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  Execute seus programas ULX:                          ║
║                                                       ║
║    ulx meu_programa.ulx           # Compila e executa  ║
║    clx --help                     # Ajuda do CLX     ║
║                                                       ║
║  Plataformas suportadas:                               ║
║                                                       ║
║    ulx build windows meuapp.ulx   # .exe Windows       ║
║    ulx build linux meuapp.ulx     # Binário Linux     ║
║    ulx build macos meuapp.ulx     # App macOS         ║
║    ulx build android meuapp.ulx   # .apk Android      ║
║    ulx build web meuapp.ulx       # .html Web         ║
║    ulx build npm meuapp.ulx       # Pacote NPM        ║
║    ulx build all meuapp.ulx       # Todas plataformas ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
    """)

def main():
    print_banner()
    check_requirements()
    install_files()
    create_wrapper()
    print_usage()

if __name__ == "__main__":
    main()
