# ULX - Universal Language for Everything v4.0
## Sistema Completo de Desenvolvimento

O ecossistema **ULX** e uma linguagem de programacao universal em portugues, facil e poderosa, composta por **cinco bases** que trabalham em conjunto, agora com **ULX Core v4.0** trazendo um lexer, parser e interpretador completos com tratamento de erros robusto.

---

## NOVIDADES v4.0

- **ULX Core**: Lexer, Parser e AST completos com suporte a todos os tipos
- **Sistema de Erros**: Tratamento estruturado com contexto, sugestoes e severidade
- **Logging Estruturado**: Sistema completo de logs com niveis e exportacao
- **REPL Interativo**: Modo interativo com auto-completar, historico e comandos
- **Debugger**: Depurador com breakpoints, watches e pilha de chamadas
- **Linter**: Analise estatica com regras configuraveis
- **Formatador**: Formatacao automatica de codigo ULX
- **Package Manager**: Gerenciamento de pacotes ULX
- **Testes**: Suite completa de testes unitarios
- **CI/CD**: GitHub Actions para testes automaticos
- **CLX Compiler v4**: Compilador melhorado com mais targets
- **Novos exemplos**: Exemplos avancados de uso

---

## AS CINCO BASES

### 1. ULX - Universal Language (Linguagem de Programacao)

Linguagem de programacao em portugues, facil e poderosa.

**Arquivos:** `.ulx`

```ulx
escreva("Ola, Mundo!")

funcao soma(a, b) {
    retorna a + b
}

resultado = soma(10, 20)
escreva("Resultado:", resultado)
```

### 2. ULV - Universal Language Visual (Linguagem Visual)

Designer visual para criar interfaces, games e apps com drag & drop.

**Arquivos:** `.ulv`

### 3. CLX - Compiler & Language eXecutor (Compilador)

Compilador universal que processa ULX e ULV.

```bash
python clx_compiler/clx_compiler_v2.py programa.ulx -o app
```

### 4. ULQ - Universal Language for Intelligence (Interface para IAs)

Interface JSON otimizada para **Inteligencias Artificiais**.

**Arquivos:** `.ulq` (JSON)

### 5. ULD - Universal Language Distribution (Distribuicao)

Sistema de **build e distribuicao** que gera executaveis nativos.

**Arquivos:** `.uld` (configuracao de build)

---

## ULX CORE v4.0

### Lexer

Analisador lexico completo com suporte a:
- Numeros inteiros, floats, notacao cientifica, separadores
- Strings com escapes e unicode
- Operadores aritmeticos, comparacao, logicos e bitwise
- Comentarios de linha e bloco
- Arrays e dicionarios

### Parser & AST

Parser com Abstract Syntax Tree suportando:
- Expressoes aritmeticas e logicas com precedencia
- Controle de fluxo (if/else, while, for, switch)
- Funcoes com parametros opcionais e retorno
- Classes com heranca
- Tratamento de excecoes (try/catch/finally)
- Modulos (import)
- Arrays e dicionarios
- Acesso por indice e membro

### Interpretador

Interpretador completo com:
- Tipos: int, float, string, bool, lista, dicionario, nulo
- Funcoes built-in: matematica, texto, arrays, utilidades
- Escopo de variaveis com closures
- Recursao com limite de profundidade
- Validacao de tipos

### Sistema de Erros

Tratamento estruturado com:
- 10+ tipos de erros especializados
- Contexto completo (arquivo, linha, coluna, snippet)
- Sugestoes de correcao automaticas
- Niveis de severidade (aviso, erro, critico, fatal)
- Stack traces

### REPL Interativo

```bash
python -m ulx_core.repl
```

Comandos disponiveis:
- `:ajuda` - Mostra ajuda
- `:vars` - Lista variaveis
- `:funcs` - Lista funcoes
- `:carregar <arquivo>` - Carrega arquivo
- `:ast <codigo>` - Mostra AST
- `:tokens <codigo>` - Mostra tokens

### Debugger

```python
from ulx_core.debugger import ULXDebugger
from ulx_core.interpreter import Interpreter

interpreter = Interpreter()
debugger = ULXDebugger(interpreter)
debugger.add_breakpoint(10)
debugger.run_with_debug(program)
```

### Linter

```python
from ulx_core.linter import ULXLinter

linter = ULXLinter()
issues = linter.lint(source_code)
linter.print_report()
```

Regras: no-unused-vars, max-line-length, indentation, trailing-whitespace, etc.

### Formatador

```python
from ulx_core.formatter import ULXFormatter

formatter = ULXFormatter()
formatted = formatter.format(source_code)
```

### Package Manager

```bash
python -m ulx_core.pkg init meu-pacote
python -m ulx_core.pkg install pacote
python -m ulx_core.pkg list
python -m ulx_core.pkg build
```

---

## INSTALACAO

### Linux/macOS

```bash
git clone https://github.com/DragonBRX/ULX.git
cd ULX
chmod +x install.sh
./install.sh
```

### Windows

```powershell
git clone https://github.com/DragonBRX/ULX.git
cd ULX
.\install.ps1
```

---

## EXEMPLOS

### Hello World

```ulx
escreva("Ola, Mundo!")
```

### Calculadora

```ulx
funcao calculadora(a, b, op) {
    se (op == "+") {
        retorna a + b
    } senao se (op == "-") {
        retorna a - b
    } senao se (op == "*") {
        retorna a * b
    } senao se (op == "/") {
        tente {
            retorna a / b
        } pegue(e) {
            escreva("Erro:", e)
            retorna 0
        }
    }
    retorna 0
}

resultado = calculadora(10, 5, "+")
escreva("Resultado:", resultado)
```

### Fatorial Recursivo

```ulx
funcao fatorial(n) {
    se (n <= 1) {
        retorna 1
    }
    retorna n * fatorial(n - 1)
}

para (i = 1; i <= 10; i = i + 1) {
    escreva(i, "! =", fatorial(i))
}
```

### Ordenacao

```ulx
funcao bubble_sort(arr) {
    n = tamanho(arr)
    para (i = 0; i < n - 1; i = i + 1) {
        para (j = 0; j < n - i - 1; j = j + 1) {
            se (arr[j] > arr[j + 1]) {
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
            }
        }
    }
    retorna arr
}

numeros = [64, 34, 25, 12, 22, 11, 90]
escreva("Ordenado:", bubble_sort(numeros))
```

---

## TESTES

```bash
# Todos os testes
python -m pytest tests/ -v

# Testes especificos
python -m pytest tests/test_lexer.py -v
python -m pytest tests/test_parser.py -v
python -m pytest tests/test_interpreter.py -v
python -m pytest tests/test_linter.py -v
```

---

## COMPILACAO

```bash
# Compilar para binario nativo
python clx_compiler/clx_compiler_v2.py programa.ulx -o app

# Gerar apenas codigo C
python clx_compiler/clx_compiler_v2.py programa.ulx -c

# Compilar para Windows
python clx_compiler/clx_compiler_v2.py programa.ulx -t windows

# Modo verbose
python clx_compiler/clx_compiler_v2.py programa.ulx -v
```

---

## FLUXO DE TRABALHO

```
[ULQ para IAs] --> [CLX Compiler] --> [ULX Codigo]
                                           |
[ULV Visual] --> [CLX Compiler] --------->|
                                           |
                                           v
                                    [ULD Builder]
                                           |
                    +----------------------+----------------------+
                    |                      |                      |
                  .exe                   .apk                   .html
               (Windows)             (Android)                  (Web)
```

---

## ESTRUTURA DO PROJETO

```
ULX/
├── ulx_core/              # NOVO: Core completo v4.0
│   ├── __init__.py
│   ├── tokens.py          # Definicoes de tokens
│   ├── errors.py          # Sistema de erros
│   ├── logger.py          # Logging estruturado
│   ├── lexer.py           # Analisador lexico
│   ├── parser.py          # Parser e AST
│   ├── interpreter.py     # Interpretador
│   ├── repl.py            # REPL interativo
│   ├── debugger.py        # Depurador
│   ├── linter.py          # Analisador estatico
│   ├── formatter.py       # Formatador de codigo
│   └── pkg.py             # Package manager
│
├── clx_compiler/           # Compilador
│   ├── clx_compiler.py
│   ├── clx_compiler_v2.py  # NOVO: Versao melhorada
│   └── clx_formats.py
│
├── ulq_intelligence/       # Interface para IAs
│   ├── ulq_parser.py
│   └── exemplo_calculadora.ulq
│
├── uld_distribution/       # Sistema de build
│   └── uld_builder.py
│
├── nfx_format/             # Formato NFX
│   └── nfx_core.py
│
├── npx_classifier/         # Classificador NPX
│   └── npx_classifier.py
│
├── ulx_language/           # Linguagem ULX
│   └── exemplos/
│
├── ulv_visual/             # Linguagem visual
│
├── tests/                  # NOVO: Testes unitarios
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_interpreter.py
│   └── test_linter.py
│
├── examples/               # Exemplos
│   ├── hello.ulx
│   ├── calculadora.ulx
│   ├── fibonacci.ulx
│   ├── tabuada.ulx
│   ├── condicoes.ulx
│   ├── fatorial.ulx
│   ├── ordenacao.ulx
│   └── excecoes.ulx
│
├── docs/                   # Documentacao
│   └── guia.md
│
├── .github/workflows/      # NOVO: CI/CD
│   └── ci.yml
│
├── install.sh
├── install.ps1
├── install.py
├── CONTRIBUTING.md         # NOVO
└── README.md
```

---

## CONTINUOUS INTEGRATION

Este projeto usa GitHub Actions para:
- Testes automaticos em Python 3.9, 3.10, 3.11, 3.12
- Execucao de todos os testes unitarios
- Validacao de exemplos
- Coverage reporting

---

## CONTRIBUINDO

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para guias de contribuicao.

---

## LICENCA

MIT License

---

**Autor:** DragonBRX
**GitHub:** https://github.com/DragonBRX/ULX
