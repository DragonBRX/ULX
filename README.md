# ULX - Universal Language for Everything
## Sistema Completo de Desenvolvimento

O ecossistema **ULX** é composto por **quatro bases** que trabalham em conjunto:

---

## 🏗️ AS QUATRO BASES

### 1️⃣ ULX - Universal Language (Linguagem de Programação)

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

### 2️⃣ ULV - Universal Language Visual (Linguagem Visual)

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

### 3️⃣ CLX - Compiler & Language eXecutor (Compilador)

Compilador universal que processa ULX e ULV.

```bash
clx-compile programa.ulx -o app
clx-compile interface.ulv -o app
```

---

### 4️⃣ ULQ - Universal Language for Intelligence (Interface para IAs) ⭐ NOVO

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

## 🔄 FLUXO DE TRABALHO

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
               GCC/Clang (C → Binário)
                           │
                           ▼
                   Binário Nativo
```

---

## 📁 ESTRUTURA DO PROJETO

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
├── ulq_intelligence/       # Interface para IAs ⭐
│   ├── ulq_parser.py
│   ├── exemplo_calculadora.ulq
│   └── README.md
│
└── README.md
```

---

## 🚀 COMO COMEÇAR

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

---

## 🤖 ULQ PARA INTELIGÊNCIAS ARTIFICIAIS

ULQ foi criado para facilitar o trabalho de IAs:

| Problema | Solução ULQ |
|----------|-------------|
| Códigos com erros | JSON estruturado |
| Ambigüidade | Tipos definidos |
| IAs não visualizam | Representação visual |
| Falta de padronização | Schema único |

**ULQ funciona com qualquer IA que processa JSON!**

---

## 📄 LICENÇA

MIT License

---

**Autor:** DragonBRX
**GitHub:** https://github.com/DragonBRX/ULX