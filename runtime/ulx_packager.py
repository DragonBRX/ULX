#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULX Packager - Empacota binários em formato .ulx
Funciona em: Linux, Windows, MacOS

Uso: ulx-pack pack <binario> -o app.ulx
"""

import sys
import os
import json
import struct
import argparse
from datetime import datetime
import platform

ULX_MAGIC = b'ULX\x00'
ULX_VERSION = 2


def create_ulx_package(binary_path, output, metadata=None):
    """Cria um pacote .ulx a partir de um binário"""

    if not os.path.exists(binary_path):
        print(f"[ERRO] Binário '{binary_path}' não encontrado")
        return False

    print("=" * 60)
    print("   ULX Packager v3.0")
    print("=" * 60)

    with open(binary_path, 'rb') as f:
        binary_data = f.read()

    bin_size = len(binary_data)
    print(f"Binário: {binary_path}")
    print(f"Tamanho: {bin_size:,} bytes ({bin_size/1024:.1f} KB)")

    default_meta = {
        'name': os.path.basename(binary_path),
        'version': '1.0.0',
        'description': f'Aplicativo ULX - {os.path.basename(binary_path)}',
        'author': '',
        'icon': '',
        'categories': ['Utility'],
        'terminal': True,
        'created': datetime.now().isoformat(),
        'ulx_version': ULX_VERSION,
        'platform': platform.system(),
    }

    if metadata:
        default_meta.update(metadata)

    meta_json = json.dumps(default_meta, ensure_ascii=False).encode('utf-8')

    print(f"\nCriando pacote: {output}")
    print(f"Nome: {default_meta['name']}")
    print(f"Versão: {default_meta['version']}")
    print(f"Descrição: {default_meta['description']}")

    with open(output, 'wb') as f:
        f.write(ULX_MAGIC)
        f.write(struct.pack('<H', ULX_VERSION))
        f.write(struct.pack('<I', len(meta_json)))
        f.write(meta_json)
        f.write(struct.pack('<Q', len(binary_data)))
        f.write(binary_data)

    output_size = os.path.getsize(output)
    print(f"\n[OK] Pacote criado: {output}")
    print(f"[OK] Tamanho final: {output_size:,} bytes ({output_size/1024:.1f} KB)")
    print("=" * 60)
    print("   EMPACOTAMENTO CONCLUÍDO!")
    print("=" * 60)
    print(f"Execute com: ulx-run {output}")

    return True


def extract_ulx(ulx_path, output_dir=None):
    """Extrai o conteúdo de um pacote .ulx"""

    if not os.path.exists(ulx_path):
        print(f"[ERRO] Arquivo '{ulx_path}' não encontrado")
        return False

    with open(ulx_path, 'rb') as f:
        magic = f.read(4)
        if magic != ULX_MAGIC:
            print("[ERRO] Arquivo não é um pacote ULX válido")
            return False

        version = struct.unpack('<H', f.read(2))[0]
        print(f"Formato ULX versão {version}")

        meta_len = struct.unpack('<I', f.read(4))[0]
        meta_json = f.read(meta_len).decode('utf-8')
        metadata = json.loads(meta_json)

        print(f"Nome: {metadata.get('name', 'Desconhecido')}")
        print(f"Versão: {metadata.get('version', '?')}")
        print(f"Plataforma: {metadata.get('platform', '?')}")

        bin_len = struct.unpack('<Q', f.read(8))[0]
        binary_data = f.read(bin_len)

        out_dir = output_dir or os.path.dirname(ulx_path) or '.'
        os.makedirs(out_dir, exist_ok=True)

        os_type = platform.system()
        bin_name = metadata.get('name', 'app')
        if os_type == "Windows" and not bin_name.endswith('.exe'):
            bin_name += '.exe'

        bin_path = os.path.join(out_dir, bin_name)

        with open(bin_path, 'wb') as bf:
            bf.write(binary_data)

        os.chmod(bin_path, 0o755)
        print(f"\n[OK] Extraído: {bin_path}")
        print(f"[OK] Tamanho: {bin_size:,} bytes" if (bin_size := len(binary_data)) else "")

        return True


def main():
    parser = argparse.ArgumentParser(description='ULX Packager v3.0')
    subparsers = parser.add_subparsers(dest='command', help='Comando')

    pack_parser = subparsers.add_parser('pack', help='Empacotar binário')
    pack_parser.add_argument('binary', help='Binário para empacotar')
    pack_parser.add_argument('-o', '--output', required=True, help='Arquivo .ulx de saída')
    pack_parser.add_argument('--name', help='Nome do aplicativo')
    pack_parser.add_argument('--version', default='1.0.0', help='Versão')
    pack_parser.add_argument('--description', help='Descrição')
    pack_parser.add_argument('--author', help='Autor')
    pack_parser.add_argument('--icon', help='Caminho do ícone')
    pack_parser.add_argument('--terminal', type=bool, default=True, help='Requer terminal?')

    extract_parser = subparsers.add_parser('extract', help='Extrair pacote')
    extract_parser.add_argument('ulx_file', help='Arquivo .ulx')
    extract_parser.add_argument('-o', '--output', help='Diretório de saída')

    args = parser.parse_args()

    if args.command == 'pack':
        metadata = {
            'name': args.name or os.path.basename(args.binary),
            'version': args.version,
            'description': args.description or f'Aplicativo ULX',
            'author': args.author or '',
            'icon': args.icon or '',
            'terminal': args.terminal,
        }
        success = create_ulx_package(args.binary, args.output, metadata)
        sys.exit(0 if success else 1)

    elif args.command == 'extract':
        success = extract_ulx(args.ulx_file, args.output)
        sys.exit(0 if success else 1)

    else:
        print("ULX Packager v3.0")
        print("")
        print("Uso:")
        print("  ulx-pack pack <binario> -o app.ulx [opções]")
        print("  ulx-pack extract <app.ulx> [-o diretório]")
        print("")
        print("Opções de empacotamento:")
        print("  --name        Nome do aplicativo")
        print("  --version     Versão (padrão: 1.0.0)")
        print("  --description Descrição do app")
        print("  --author      Autor")
        sys.exit(1)


if __name__ == '__main__':
    main()
