# ULQ - Universal Language for Intelligence
## Quarta Base - Interface para IAs

**ULQ** é a base opcional e experimental do ecossistema ULX, projetada especificamente para **Inteligências Artificiais**.

### 🎯 Propósito

Permitir que IAs entendam, visualizem e gerem código ULX/ULV sem erros, através de uma representação padronizada e otimizada.

### 💡 Como Funciona

```
IAs → ULQ (Visualização) → ULX/ULV (Código) → CLX → Binário
```

### 📋 Estrutura ULQ

ULQ usa formato JSON otimizado para ser processado por qualquer modelo de IA:

```json
{
    "type": "window",
    "name": "App",
    "children": [
        {"type": "text", "content": "Olá, Mundo!"},
        {"type": "button", "text": "Click", "action": "onClick"}
    ]
}
```

### 🔧 API ULQ para IAs

```python
# Importar ULQ
import ulq

# Criar janela
janela = {
    "type": "window",
    "title": "Minha App",
    "children": [
        {"type": "text", "content": "Olá, IA!"},
        {"type": "button", "action": "saudar"}
    ]
}

# Converter para ULX
codigo_ulx = ulq.to_ulx(janela)

# Compilar
ulq.compile(codigo_ulx, "app")
```

### 🧠 Para IAs

ULQ foi projetado para resolver os problemas que IAs têm com código:

1. **Sem ambiguidade**: Cada comando tem um significado claro
2. **Visualização direta**: IAs podem "ver" a estrutura antes de gerar
3. **Zero erros de sintaxe**: Formato padronizado JSON
4. **Otimizado para modelos**: Tokens mínimos, meaning máximo
5. **Validação automática**: Verifica erros antes de compilar

### 📝 Exemplo ULQ

```json
{
    "project": "calculadora",
    "lang": "ulx",
    "components": [
        {
            "type": "text",
            "content": "Calculadora ULX",
            "style": {"font_size": 24, "bold": true}
        },
        {
            "type": "input",
            "name": "a",
            "label": "Número 1"
        },
        {
            "type": "input",
            "name": "b",
            "label": "Número 2"
        },
        {
            "type": "button",
            "text": "Somar",
            "on_click": "somar"
        }
    ],
    "logic": {
        "somar": "resultado = a + b"
    }
}
```

### 🔄 Conversão ULQ ↔ ULX

```
ULQ (JSON) ←→ ULX (Texto)
     ↓              ↓
   Visual        Código
```

### 🚀 Uso

```python
from ulq import ULQParser

# Parse ULQ
parser = ULQParser()
codigo = parser.parse(ulq_data)

# Validar
if parser.is_valid(ulq_data):
    # Compilar
    clx_compile(codigo)
```

### ⚙️ Para Todos os Modelos

ULQ funciona com qualquer IA que processa JSON:

- Claude
- GPT-4
- Gemini
- Llama
- MiniMax
- Qualquer outro modelo

### 📦 Implementação

```python
class ULQParser:
    """Parser ULQ - otimizado para IAs"""

    def __init__(self):
        self.valid_types = [
            "window", "text", "button", "input",
            "image", "canvas", "grid", "list"
        ]

    def parse(self, ulq_data):
        """Converte ULQ para ULX"""
        # Validação
        if not self.is_valid(ulq_data):
            raise ValueError("ULQ inválido")

        # Conversão
        return self._convert(ulq_data)

    def is_valid(self, ulq_data):
        """Verifica se ULQ é válido"""
        return (
            "type" in ulq_data and
            ulq_data["type"] in self.valid_types
        )
```

### 🎯 Benefícios

| Problema | Solução ULQ |
|----------|-------------|
| Códigos com erros de sintaxe | Formato JSON estruturado |
| Ambigüidade em comandos | Tipos definidos e claros |
| IAs não visualizam código | Representação visual em JSON |
| Falta de padronização | Schema único e consistente |
| Dificuldade em depurar | Validação automática |

### 🔮 Experimental

ULQ é uma base **opcional e experimental**. Não é obrigatório usar ULQ para criar apps ULX - você pode usar ULX ou ULV diretamente.

ULQ foi adicionado para facilitar o trabalho de IAs e permitir que elas gerem código ULX sem erros.

---

**Nota:** ULQ é experimental e pode mudar em futuras versões.