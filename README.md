# ULX - Linguagem de Programacao em Portugues v4.0

> Uma linguagem de programacao em portugues, feita para quem fala portugues.
> Nao tenta ser universal. E focada, simples e acessivel.

## Status do Projeto

| Componente | Status | Descricao |
|-----------|--------|-----------|
| Lexer | ✅ Funcional | Analisador lexico completo |
| Parser | ✅ Funcional | Parser com AST completo |
| Interpretador | ✅ Funcional | Interpretador com tipos, funcoes, controle de fluxo |
| REPL | ✅ Funcional | Modo interativo |
| Testes | ✅ Melhorados | Suite de testes robusta |
| Linter | ⚠️ Basico | Analise estatica simples |
| Formatador | ⚠️ Basico | Formatacao por regex |
| Debugger | ⚠️ Scaffold | Estrutura inicial |
| Compilador CLX | ⚠️ Experimental | Gera C, nao completo |
| Package Manager | ❌ Nao funcional | Apenas scaffold |
| ULD (Distribuicao) | ❌ Nao funcional | Apenas scaffold |
| ULV (Visual) | ❌ Nao existe | Apenas ideia |

## O Que Funciona Agora

- ✅ Variaveis e atribuicao
- ✅ Tipos: int, float, string, bool, lista, dicionario, nulo
- ✅ Operadores aritmeticos, comparacao, logicos
- ✅ Controle de fluxo: se/senao, enquanto, para
- ✅ Funcoes com parametros e retorno
- ✅ Recursao
- ✅ Arrays e indexacao
- ✅ Classes (basico)
- ✅ Tratamento de excecoes (tente/pegue)
- ✅ REPL interativo
- ✅ Funcoes built-in (matematica, texto, arrays)

## O Que Ainda Nao Funciona

- ❌ Imports/modulos (parser reconhece, interpreter nao implementa)
- ❌ Package manager (nao ha registry)
- ❌ Compilador para binario nativo (gera C basico)
- ❌ Interface visual (ULV)
- ❌ Distribuicao multiplataforma (ULD)

## Quickstart

### Requisitos
- Python 3.8+
- Git

### Instalacao

```bash
git clone https://github.com/DragonBRX/ULX.git
cd ULX
python -m ulx_core.repl
```

### Primeiro Programa

Crie um arquivo `hello.ulx`:

```ulx
// Meu primeiro programa ULX
escreva("Ola, Mundo!")

funcao soma(a, b) {
    retorna a + b
}

resultado = soma(10, 20)
escreva("Resultado:", resultado)
```

Execute:
```bash
python -c "from ulx_core.lexer import Lexer; from ulx_core.parser import Parser; from ulx_core.interpreter import Interpreter; import sys; code=open(sys.argv[1]).read(); l=Lexer(code); p=Parser(l.tokenize(),code); Interpreter().execute(p.parse())" hello.ulx
```

Ou use o REPL:
```bash
python -m ulx_core.repl
```

### Exemplos

Veja a pasta `examples/` para mais programas de exemplo:
- `hello.ulx` - Ola mundo
- `fatorial.ulx` - Calculo de fatorial com recursao
- `fibonacci.ulx` - Sequencia de Fibonacci
- `calculadora.ulx` - Calculadora simples
- `ordenacao.ulx` - Algoritmo de ordenacao

## Arquitetura

```
Codigo Fonte (.ulx)
      |
      v
   Lexer  --> Tokens
      |
      v
   Parser  --> AST (Abstract Syntax Tree)
      |
      v
Interpretador  --> Resultado
```

## Estrutura do Projeto

```
ULX/
├── ulx_core/          # Nucleo da linguagem (Lexer, Parser, Interpreter)
│   ├── lexer.py       # Analisador lexico
│   ├── parser.py      # Parser com AST
│   ├── interpreter.py # Interpretador
│   ├── tokens.py      # Definicoes de tokens
│   ├── errors.py      # Sistema de erros
│   ├── repl.py        # REPL interativo
│   ├── debugger.py    # Depurador (basico)
│   ├── linter.py      # Analisador estatico (basico)
│   ├── formatter.py   # Formatador (basico)
│   ├── logger.py      # Sistema de logs
│   └── pkg.py         # Package manager (nao funcional)
├── clx_compiler/      # Compilador experimental
│   ├── clx_compiler_v2.py  # Versao mais recente
│   └── README.md
├── examples/          # Exemplos de programas ULX
├── tests/             # Testes unitarios
├── experimental/      # Codigo experimental (NFX, NPX)
├── nfx_format/        # Formato NFX (experimental)
├── npx_classifier/    # Classificador NPX (experimental)
├── uld_distribution/  # Sistema de distribuicao (nao funcional)
├── ulv_visual/        # Linguagem visual (apenas ideia)
├── ulq_intelligence/  # Interface para IAs (JSON)
└── ulx_language/      # Exemplos adicionais
```

## Rodando Testes

```bash
python -m unittest discover tests/ -v
```

Ou individualmente:
```bash
python -m unittest tests.test_lexer -v
python -m unittest tests.test_parser -v
python -m unittest tests.test_interpreter -v
```

## Filosofia de Design

1. **Portugues primeiro**: Tudo em portugues - keywords, erros, documentacao
2. **Simplicidade**: Sintaxe familiar para quem ja programou em Python/JavaScript
3. **Acessibilidade**: Feita para estudantes e iniciantes que falam portugues
4. **Honestidade**: Documentamos o que funciona e o que nao funciona

## Roadmap

### v4.1 (Curto prazo)
- [x] Corrigir bug critico no lexer
- [x] Corrigir atribuicao de variaveis
- [x] Melhorar testes
- [ ] Implementar imports
- [ ] Melhorar suporte a classes

### v4.2 (Medio prazo)
- [ ] Package manager funcional
- [ ] Biblioteca padrao completa
- [ ] Compilador CLX funcional

### v5.0 (Longo prazo)
- [ ] Suporte a modulos nativos
- [ ] ULD - distribuicao multiplataforma
- [ ] ULV - interface visual

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

Areas que precisam de ajuda:
- Melhorar cobertura de testes
- Implementar sistema de imports
- Melhorar o compilador CLX
- Documentacao

## Licenca

MIT License - veja LICENSE para detalhes.

---

**Nota**: Este projeto esta em desenvolvimento ativo. A API pode mudar.
Documentamos honestamente o que funciona e o que nao funciona.
