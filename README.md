# ULX - Universal Language for Everything
## Sistema Completo de Desenvolvimento

O ecossistema **ULX** é composto por **cinco bases** que trabalham em conjunto:

---

## AS CINCO BASES

### ULX - Universal Language (Linguagem de Programação)

Linguagem de programação em português, fácil e poderosa.

**Arquivos:** `.ulx`

```ulx
escreva("Olá, Mundo!")

funcao soma(a, b) {
    retorna a + b
}

resultado = soma(10, 20)
escreva("Resultado:", resultado)
```

---

### ULV - Universal Language Visual (Linguagem Visual)

Designer visual para criar interfaces, games e apps com drag & drop.

**Arquivos:** `.ulv`

```ulv
janela("Minha App") {
    titulo: "Aplicativo ULX"
    tamanho: 400x300

    texto("Olá, Mundo!")
    botao("Clique Aqui")
}
```

---

### CLX - Compiler & Language eXecutor (Compilador)

Compilador universal que processa ULX e ULV.

```bash
clx-compile programa.ulx -o app
clx-compile interface.ulv -o app
```

---

### ULQ - Universal Language for Intelligence (Interface para IAs) ⭐ NOVO

Interface JSON otimizada para **Inteligências Artificias**.

**Arquivos:** `.ulq` (JSON)

```json
{
    "type": "window",
    "name": "App",
    "children": [
        {"type": "text", "content": "Olá, IA!"},
        {"type": "button", "text": "Click", "action": "onClick"}
    ]
}
```

**Características:**
- Formato JSON padronizado
- Otimizado para IAs (Claude, GPT, Gemini, Llama, etc.)
- Zero erros de sintaxe
- Validação automática
- Conversão direta para ULX/ULV

---

### ULD - Universal Language Distribution (Distribuição)  NOVO

Sistema de **build e distribuição** que gera executáveis nativos para qualquer plataforma.

**Arquivos:** `.uld` (configuração de build)

```bash
# Gerar executavel Windows
uld-builder -i app.ulx -o app.exe --target windows

# Gerar executavel Linux
uld-builder -i app.ulx -o app --target linux

# Gerar app Android
uld-builder -i app.ulx -o app.apk --target android

# Gerar pagina web
uld-builder -i app.ulx -o app.html --target web
```

**Formatos suportados:**

| Plataforma | Formato | Status |
|------------|---------|--------|
| Windows | `.exe` | Estável |
| Linux | `bin` | Estável |
| macOS | `.app` | Beta |
| Android | `.apk` | Experimental |
| Web | `.html` | Estável |

---

## FLUXO DE TRABALHO

```
┌─────────────────────────────────────────────────────────┐
│                   ULQ (Para IAs)                       │
│  +----------------------------------------------------│
│  │ {                                                    ││
│  │   "type": "window",                                 ││
│  │   "children": [...]                                ││
│  │ }                                                    ││
│  +----------------------------------------------------│
│                      │                                 │
│                      ▼                                 │
│  ┌───────────────────────────────────────────────────┐ │
│  │           CLX Compiler (ULQ → ULX)                │ │
│  └───────────────────────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   ULV (Visual)                          │
│  +----------------------------------------------------│
│  │ janela("App") {                                     ││
│  │     texto("Olá")                                    ││
│  │     botao("Click")                                  ││
│  │ }                                                   ││
│  +----------------------------------------------------│
│                      │                                 │
│                      ▼                                 │
│  ┌───────────────────────────────────────────────────┐ │
│  │           CLX Compiler (ULV → ULX)                │ │
│  └───────────────────────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   ULX (Código)                         │
│  +----------------------------------------------------│
│  │ escreva("Olá")                                     ││
│  │ botao("Click")                                     ││
│  +----------------------------------------------------│
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
               CLX Compiler (ULX → C)
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   ULD (Distribuição)                    │
│  +----------------------------------------------------│
│  │ uld-builder -i app.ulx -o app.exe --target windows││
│  │ uld-builder -i app.ulx -o app.apk --target android││
│  │ uld-builder -i app.ulx -o app.html --target web   ││
│  +----------------------------------------------------│
│                      │                                 │
│                      ▼                                 │
│  ┌───────────────────────────────────────────────────┐ │
│  │              Executáveis Nativos                   │ │
│  │   .exe    .apk    .app    .html    bin           │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## ESTRUTURA DO PROJETO

```
ULX/
├── ulx_language/           # Linguagem de programação
│   ├── hello.ulx
│   ├── calculadora.ulx
│   └── README.md
│
├── ulv_visual/             # Linguagem visual
│   ├── calculadora.ulv
│   └── README.md
│
├── clx_compiler/           # Compilador universal
│   ├── clx_compiler.py
│   └── README.md
│
├── ulq_intelligence/       # Interface para IAs
│   ├── ulq_parser.py
│   ├── exemplo_calculadora.ulq
│   └── README.md
│
├── uld_distribution/       # Sistema de distribuição NOVO
│   ├── uld_builder.py
│   ├── exemplo_build.ulx
│   ├── exemplo_build.uld
│   └── README.md
│
└── README.md
```

---

## COMO COMEÇAR

### Instalação

```bash
git clone https://github.com/DragonBRX/ULX.git
cd ULX
chmod +x install.sh
sudo ./install.sh
```

### ULX - Hello World

```bash
echo 'escreva("Olá, Mundo!")' > hello.ulx
clx-compile hello.ulx -o hello
./hello
```

### ULQ - Para IAs

```python
from ulq_intelligence import ULQParser

parser = ULQParser()
janela = parser.create_window("Minha App")
janela["children"].append(parser.create_text("Olá, IA!"))

# Validar e converter para ULX
if parser.validate(janela):
    ulx_code = parser.to_ulx(janela)
```

### ULD - Gerar Executáveis

```bash
# Windows (.exe)
python3 uld_distribution/uld_builder.py -i app.ulx -o app.exe --target windows

# Linux (binário)
python3 uld_distribution/uld_builder.py -i app.ulx -o app --target linux

# Android (.apk)
python3 uld_distribution/uld_builder.py -i app.ulx -o app.apk --target android

# Web (.html)
python3 uld_distribution/uld_builder.py -i app.ulx -o app.html --target web
```

---

## ULQ PARA INTELIGÊNCIAS ARTIFICIAIS

ULQ foi criado para facilitar o trabalho de IAs:

| Problema | Solução ULQ |
|----------|-------------|
| Códigos com erros | JSON estruturado |
| Ambigüidade | Tipos definidos |
| IAs não visualizam | Representação visual |
| Falta de padronização | Schema único |

**ULQ funciona com qualquer IA que processa JSON!**

---

## LICENÇA

MIT License

---

**Autor:** DragonBRX
**GitHub:** https://github.com/DragonBRX/ULX
