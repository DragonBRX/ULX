#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULX Runtime - Executor de aplicativos .ulx
Funciona em: Linux, Windows, MacOS

Uso: ulx-run <app.ulx> [argumentos...]
"""

import sys
import os
import json
import struct
import tempfile
import subprocess
import shutil
import platform

ULX_MAGIC = b'ULX\x00'
ULX_VERSION = 2


def _read_package(ulx_path):
    """Lê um pacote .ulx e retorna (metadata, binary_data)"""
    with open(ulx_path, 'rb') as f:
        magic = f.read(4)
        if magic != ULX_MAGIC:
            return None, None

        version = struct.unpack('<H', f.read(2))[0]
        meta_len = struct.unpack('<I', f.read(4))[0]
        meta_json = f.read(meta_len).decode('utf-8')
        metadata = json.loads(meta_json)

        bin_len = struct.unpack('<Q', f.read(8))[0]
        binary_data = f.read(bin_len)

        return metadata, binary_data


def read_ulx_metadata(ulx_path):
    """Lê metadados de um arquivo .ulx sem executar"""
    meta, _ = _read_package(ulx_path)
    return meta


def execute_ulx(ulx_path, args=None):
    """Executa um arquivo .ulx"""

    if not os.path.exists(ulx_path):
        print(f"[ULX-Run] Erro: Arquivo '{ulx_path}' não encontrado")
        return 1

    metadata, binary_data = _read_package(ulx_path)

    if metadata is None:
        print(f"[ULX-Run] Erro: '{ulx_path}' não é um arquivo ULX válido")
        return 1

    print(f"[ULX-Run] Executando: {metadata.get('name', 'App')}")
    print(f"[ULX-Run] Versão: {metadata.get('version', '1.0')}")

    tmp_dir = tempfile.mkdtemp(prefix='ulx_run_')
    os_type = platform.system()

    if os_type == "Windows":
        bin_name = metadata.get('name', 'app').replace(' ', '_') + '.exe'
    else:
        bin_name = metadata.get('name', 'app').replace(' ', '_')

    bin_path = os.path.join(tmp_dir, bin_name)

    try:
        with open(bin_path, 'wb') as f:
            f.write(binary_data)

        os.chmod(bin_path, 0o755)

        run_args = [bin_path]
        if args:
            run_args.extend(args)

        result = subprocess.run(run_args)
        return result.returncode

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def create_info_display(ulx_path):
    """Mostra informações do pacote .ulx"""
    metadata = read_ulx_metadata(ulx_path)

    if not metadata:
        print("Arquivo ULX inválido")
        return False

    print("=" * 50)
    print(f"   {metadata.get('name', 'App ULX')}")
    print("=" * 50)
    print(f"Versão:      {metadata.get('version', '1.0')}")
    print(f"Descrição:   {metadata.get('description', 'N/A')}")
    print(f"Autor:       {metadata.get('author', 'N/A')}")
    print(f"Terminal:    {'Sim' if metadata.get('terminal', True) else 'Não'}")
    print(f"Categorias:  {', '.join(metadata.get('categories', []))}")
    print(f"Criado em:   {metadata.get('created', 'N/A')}")
    print(f"Formato:     ULX v{metadata.get('ulx_version', 2)}")
    print("=" * 50)

    return True


def list_ulx_packages(directory='.'):
    """Lista todos os arquivos .ulx em um diretório"""
    ulx_files = []
    for f in os.listdir(directory):
        if f.endswith('.ulx'):
            path = os.path.join(directory, f)
            ulx_files.append(path)
    return ulx_files


def main():
    print("=" * 50)
    print("   ULX Runtime v3.0")
    print(f"   Plataforma: {platform.system()}")
    print("=" * 50)
    print()

    if len(sys.argv) < 2:
        print("Uso: ulx-run <app.ulx> [argumentos...]")
        print("")
        print("Opções:")
        print("  --info          Mostrar informações do aplicativo")
        print("  --list          Listar pacotes .ulx no diretório atual")
        print("  --help          Mostrar esta ajuda")
        print("")
        print("Exemplos:")
        print("  ulx-run app.ulx")
        print("  ulx-run app.ulx arg1 arg2")
        print("  ulx-run --info app.ulx")
        sys.exit(0)

    if sys.argv[1] == '--help':
        print("Uso: ulx-run <app.ulx> [argumentos...]")
        print("")
        print("Opções:")
        print("  --info          Mostrar informações do aplicativo")
        print("  --list          Listar pacotes .ulx no diretório atual")
        sys.exit(0)

    if sys.argv[1] == '--list':
        files = list_ulx_packages()
        if files:
            print(f"Encontrados {len(files)} arquivo(s) .ulx:")
            for f in files:
                meta = read_ulx_metadata(f)
                name = meta.get('name', os.path.basename(f)) if meta else os.path.basename(f)
                version = meta.get('version', '?') if meta else '?'
                print(f"  - {os.path.basename(f)} ({name} v{version})")
        else:
            print("Nenhum arquivo .ulx encontrado no diretório atual.")
        sys.exit(0)

    ulx_file = sys.argv[1]

    if ulx_file == '--info' and len(sys.argv) > 2:
        create_info_display(sys.argv[2])
        sys.exit(0)

    if not ulx_file.endswith('.ulx'):
        print(f"[AVISO] Arquivo '{ulx_file}' não tem extensão .ulx")

    args = sys.argv[2:] if len(sys.argv) > 2 else None
    ret = execute_ulx(ulx_file, args)
    sys.exit(ret)


if __name__ == '__main__':
    main()
