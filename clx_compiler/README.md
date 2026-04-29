# CLX - Compilador Universal
## Compilador que processa ULX e ULV

**CLX** é o compilador central do ecossistema ULX. Ele compila tanto código ULX quanto ULV para binários nativos.

### Arquitetura

```
Código Fonte
    │
    ├── .ulx (ULX) ──────────┐
    │                        │
    │                        ▼
    ├── .ulv (ULV) ────► CLX Compiler ──► Código C ──► GCC ──► Binário
    │                        ▲
    │                        │
    └── .ulb (ULB) ──────────┘
```

### Como o CLX Funciona

1. **Detecta o tipo de arquivo** pela extensão
2. **ULX**: Tokeniza e gera C diretamente
3. **ULV**: Converte para ULX primeiro, depois compila
4. **ULB**: Biblioteca pré-compilada

### Compilando ULX

```bash
clx-compile programa.ulx -o app
```

### Compilando ULV

```bash
clx-compile interface.ulv -o app
```

### Flags de Compilação

| Flag | Descrição |
|------|-----------|
| `-O3` | Otimização agressiva |
| `-static` | Binário estático |
| `-native` | Otimiza para CPU atual |
| `--visual` | Abre visualizador |
| `--debug` | Inclui informações de debug |

### Otimizações

- **SIMD**: AVX2/AVX-512 quando disponível
- **LTO**: Link-Time Optimization
- **Native**: -march=native -mtune=native
- **Static**: Sem dependências externas

### Output

```
$ clx-compile hello.ulx -o hello

CLX Compiler v3.0
================

[1/4] Analisando hello.ulx...
[2/4] Gerando código C...
[3/4] Compilando com GCC (-O3 -static)...
[4/4] Binário gerado: hello (15 KB)

Sucesso! Execute ./hello
```

### API do Compilador

```python
from clx_compiler import CLXCompiler

compiler = CLXCompiler("programa.ulx", output="app")
compiler.compile()

# Para ULV
compiler = CLXCompiler("interface.ulv", output="app")
compiler.compile()
```

### Requisitos

- Python 3.8+
- GCC ou Clang
- Linux/Windows/MacOS
