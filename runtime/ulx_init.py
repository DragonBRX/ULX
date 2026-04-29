#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULX Project Init - Inicializa um novo projeto ULX
Funciona em: Linux, Windows, MacOS

Uso: ulx-init <nome_projeto> [-d descrição] [-a autor]
"""

import os
import sys
import argparse
import platform


PROJECT_README = """# {name}

{description}

## Sobre

Este projeto foi criado com **ULX** - Linguagem de Programação Universal.

## Como Compilar

```bash
ulx-compile src/main.ulx -o {name}
```

## Como Executar

```bash
./{name}
```

## Estrutura do Projeto

```
{name}/
├── src/
│   └── main.ulx    # Código principal
├── Makefile        # Automação de compilação
└── README.md       # Este arquivo
```

## Documentação ULX

Visite: https://github.com/DragonBRX/ULX
"""

MAKEFILE_TEMPLATE = """# Makefile para projeto ULX: {name}
# Plataforma: {platform}

ULX_COMPILER = ulx-compile{ext}
SOURCE = src/main.ulx
BINARY = {name}{binext}
PACKAGE = {name}.ulx

.PHONY: all compile run package clean install

all: compile

compile:
\t@echo "[Make] Compilando $(SOURCE)..."
\t$(ULX_COMPILER) $(SOURCE) -o $(BINARY)

run: compile
\t@echo "[Make] Executando $(BINARY)..."
\t./$(BINARY)

package: compile
\t@echo "[Make] Empacotando $(BINARY)..."
\tulx-pack pack $(BINARY) -o $(PACKAGE) --name "{name}" --description "{description}"

install: compile
\t@echo "[Make] Instalando $(BINARY)..."
\tcp $(BINARY) /usr/local/bin/
\tchmod +x /usr/local/bin/$(BINARY)
\t@echo "[Make] Instalado em /usr/local/bin/$(BINARY)"

clean:
\t@echo "[Make] Limpando..."
\trm -f $(BINARY) $(BINARY).c $(PACKAGE)

help:
\t@echo "Comandos disponíveis:"
\t@echo "  make compile  - Compila o projeto"
\t@echo "  make run      - Compila e executa"
\t@echo "  make package  - Cria pacote .ulx"
\t@echo "  make install  - Instala no sistema"
\t@echo "  make clean    - Remove arquivos gerados"
"""

HELLO_WORLD = """// {name} - {description}
// Autor: {author}

escreva("=" . "=" . "=" . "=" . "=" . "=" . "=" . "=" . "=" . "=")
escreva("  {name}")
escreva("  ULX - Linguagem de Programação Universal")
escreva("=" . "=" . "=" . "=" . "=" . "=" . "=" . "=" . "=" . "=")
escreva("")

// Variáveis
mensagem = "Bem-vindo ao ULX!"
escreva(mensagem)

// Loop de exemplo
escreva("")
escreva("Contando de 1 a 5:")
para (i = 1; i <= 5; i = i + 1) {
    escreva("  Iteração: ", i)
}

// Condicional
escreva("")
hora = 14
se (hora < 12) {
    escreva("Bom dia!")
} senao se (hora < 18) {
    escreva("Boa tarde!")
} senao {
    escreva("Boa noite!")
}

// Função exemplo
escreva("")
funcao saudar(nome) {
    retorna "Olá, " + nome + "!"
}

escreva(saudar("Mundo"))

escreva("")
escreva("Programa finalizado!")
"""

GITIGNORE = """# ULX
*.c
*.o
*.ulx
*.exe
!src/**/*.ulx

# Python
__pycache__/
*.pyc
*.pyo

# OS
.DS_Store
Thumbs.db
"""


def init_project(name, description, author, directory=None):
    """Inicializa um novo projeto ULX"""

    os_type = platform.system()
    comp_ext = '.py' if os_type == "Windows" else ''
    bin_ext = '.exe' if os_type == "Windows" else ''

    print("=" * 60)
    print("   ULX Project Init v3.0")
    print("=" * 60)

    if directory:
        project_dir = directory
    else:
        project_dir = name.lower().replace(' ', '_').replace('-', '_')

    if os.path.exists(project_dir):
        print(f"[ERRO] Diretório '{project_dir}' já existe")
        return False

    print(f"\nCriando projeto: {name}")
    print(f"Diretório: {project_dir}/")

    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'src'), exist_ok=True)

    readme_path = os.path.join(project_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(PROJECT_README.format(name=name, description=description))
    print(f"  [OK] README.md")

    makefile_path = os.path.join(project_dir, 'Makefile')
    with open(makefile_path, 'w', encoding='utf-8') as f:
        f.write(MAKEFILE_TEMPLATE.format(
            name=name,
            description=description,
            platform=os_type,
            ext=comp_ext,
            binext=bin_ext
        ))
    print(f"  [OK] Makefile")

    ulx_path = os.path.join(project_dir, 'src', 'main.ulx')
    with open(ulx_path, 'w', encoding='utf-8') as f:
        f.write(HELLO_WORLD.format(name=name, description=description, author=author))
    print(f"  [OK] src/main.ulx")

    gitignore_path = os.path.join(project_dir, '.gitignore')
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(GITIGNORE)
    print(f"  [OK] .gitignore")

    print("")
    print("=" * 60)
    print(f"   PROJETO '{name}' CRIADO COM SUCESSO!")
    print("=" * 60)
    print("")
    print("Para começar:")
    print(f"  cd {project_dir}")
    print(f"  make run")
    print("")
    print("Ou compile manualmente:")
    print(f"  ulx-compile src/main.ulx -o {name}")
    print(f"  ./{name}")
    print("")

    return True


def main():
    parser = argparse.ArgumentParser(description='ULX Project Init v3.0')
    parser.add_argument('name', help='Nome do projeto')
    parser.add_argument('-d', '--description', default='Projeto ULX', help='Descrição')
    parser.add_argument('-a', '--author', default='', help='Autor')
    parser.add_argument('--dir', help='Diretório (padrão: nome_do_projeto)')

    args = parser.parse_args()

    success = init_project(args.name, args.description, args.author, args.dir)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
