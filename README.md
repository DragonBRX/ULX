# ULX - Universal Language for Everything
## Sistema Completo de Desenvolvimento

O ecossistema **ULX** é composto por três bases fundamentais que trabalham em conjunto:

---

## 🏗️ AS TRÊS BASES

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

**Características:**
- Sintaxe em português
- Tipagem dinâmica
- Funções de primeira classe
- Arrays e dicionários nativos

---

### 2️⃣ ULV - Universal Language Visual (Linguagem Visual)

Designer visual para criar interfaces, games e apps com drag & drop.

**Arquivos:** `.ulv`

```ulv
janela("Minha App") {
    titulo: "Aplicativo ULX"
    tamanho: 400x300

    texto("Olá, Mundo!")
        posicao: centro
        cor: azul

    botao("Clique Aqui")
        posicao: centro
        cor: verde
        acao: clique()
}
```

**Características:**
- WYSIWYG (O que você vê é o que você executa)
- Drag & Drop de componentes
- Prévia em tempo real
- Mesma base que ULX
- Compila para ULX automaticamente

---

### 3️⃣ CLX - Compiler & Language eXecutor (Compilador)

Compilador universal que processa ULX e ULV.

**Uso:**
```bash
# Compila ULX
clx-compile programa.ulx -o app

# Compila ULV
clx-compile interface.ulv -o app

# Apenas gera C
clx-compile programa.ulx --c-only
```

---

## 🔄 FLUXO DE TRABALHO

```
┌─────────────────────────────────────────────────────────┐
│                    ULV (Visual)                        │
│  +----------------------------------------------------│
│  │ janela("App") {                                    ││
│  │     texto("Olá")                                    ││
│  │     botao("Click")                                  ││
│  │ }                                                   ││
│  +----------------------------------------------------│
│                         │                              │
│                         ▼                              │
│               CLX Compiler (ULV → ULX)                 │
│                         │                              │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    ULX (Código)                         │
│  +----------------------------------------------------│
│  │ escreva("Olá")                                      ││
│  │ botao("Click", acao: clique)                        ││
│  +----------------------------------------------------│
│                         │                              │
└─────────────────────────┼───────────────────────────────┘
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
├── examples/
│   ├── games/
│   └── apps/
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

### ULV - Interface Visual

```bash
cat > minha_app.ulv << 'EOF'
janela("Minha App") {
    texto("Olá, Mundo!")
    botao("Clique Aqui")
}
EOF

clx-compile minha_app.ulv -o minha_app
./minha_app
```

---

## 📄 LICENÇA

MIT License

---

**Autor:** DragonBRX
**GitHub:** https://github.com/DragonBRX/ULX
