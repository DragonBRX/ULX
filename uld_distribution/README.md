# ULD - Universal Language Distribution

**Quinta Base do ULX** - Sistema de distribuição e geração de executáveis nativos.

---

## O que é ULD?

ULD é o sistema que transforma código ULX/ULV em **executáveis nativos** para qualquer plataforma:

| Plataforma | Formato | Exemplo |
|------------|---------|---------|
| Windows | `.exe` | `app.exe` |
| Linux | `bin` | `app` |
| macOS | `.app` | `App.app` |
| Android | `.apk` | `app.apk` |
| Web | `.html` | `app.html` |

---

## Como Funciona

```
codigo.ulx/ulv
     │
     ▼
┌─────────────┐
│    CLX      │  Compilador ULX → C
│  Compilador │
└─────────────┘
     │
     ▼
┌─────────────┐
│     ULD     │  Build → Executavel Nativo
│   Builder   │
└─────────────┘
     │
     ▼
  app.exe
```

---

## Instalação

ULD já está incluido no CLX Compiler. Para usar:

```bash
# Via克隆
git clone https://github.com/DragonBRX/ULX.git
cd ULX

# Via Script de Instalação
./install.sh    # Linux/macOS
./install.ps1   # Windows
```

---

## Uso Rápido

### 1. Compilar para Desktop

```bash
# ULX → Executavel
python3 clx_compiler/clx_compiler.py -i meu_app.ulx -o meu_app.exe --target windows

# ULV → Executavel
python3 clx_compiler/clx_compiler.py -i interface.ulv -o interface.exe --target windows
```

### 2. Compilar para Android (experimental)

```bash
# ULX → APK
python3 uld_distribution/uld_builder.py -i app.ulx -o app.apk --target android
```

### 3. Compilar para Web

```bash
# ULX → HTML/JavaScript
python3 uld_distribution/uld_builder.py -i app.ulx -o app.html --target web
```

---

## Formatos Suportados

### Targets Disponíveis

| Target | Sistema | Arquivo |
|--------|---------|---------|
| `windows` | Windows 10/11 | `.exe` |
| `linux` | Ubuntu, Debian, Fedora | `bin` |
| `macos` | macOS 11+ | `.app` |
| `android` | Android 7+ | `.apk` |
| `ios` | iOS 14+ | `.ipa` (requer Xcode) |
| `web` | Browser | `.html` |

---

## Configuração de Build

Crie um arquivo `build.uld` para configurar seu projeto:

```json
{
    "project": "minha_aplicacao",
    "version": "1.0.0",
    "target": "windows",

    "output": {
        "name": "MeuApp",
        "icon": "assets/icon.png",
        "version": "1.0.0"
    },

    "sources": [
        "src/main.ulx",
        "src/modulos/*.ulx"
    ],

    "dependencies": [
        "ulx/stdlib"
    ],

    "build": {
        "optimize": true,
        "minify": false,
        "debug": false
    }
}
```

Execute:

```bash
ulx build --config build.uld
```

---

## API Python

```python
from uld_builder import ULDBuilder

builder = ULDBuilder()

# Build para Windows
builder.build(
    input_file="app.ulx",
    output="app.exe",
    target="windows"
)

# Build para Android
builder.build(
    input_file="app.ulx",
    output="app.apk",
    target="android"
)

# Build para Web
builder.build(
    input_file="app.ulx",
    output="app.html",
    target="web"
)
```

---

## Requisitos

| Plataforma | Requisitos |
|------------|------------|
| Windows | Python 3.8+, GCC (MinGW) |
| Linux | Python 3.8+, GCC, Android SDK (opcional) |
| macOS | Python 3.8+, Xcode Command Line Tools |
| Android | Python 3.8+, Android SDK, NDK |

---

## Status dos Targets

| Target | Status | Observação |
|--------|--------|------------|
| Windows (.exe) | Estável | GCC/MinGW |
| Linux (bin) | Estável | GCC |
| macOS (.app) | Beta | Requer Xcode |
| Android (.apk) | Experimental | Requer Android SDK |
| Web (.html) | Estável | JavaScript |
| iOS (.ipa) | Planejado | Requer Xcode |

---

## Exemplos

Veja em `../examples/` para exemplos completos.

---

## Licença

ULX ULX License - See LICENSE file
