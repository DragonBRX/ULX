# ULQ - Universal Language for Intelligence
## Quarta Base - Interface para IAs

**ULQ** e a base opcional e experimental do ecossistema ULX, projetada especificamente para **Inteligencias Artificiais**.

### Proposito

Permitir que IAs entendam, visualizem e gerem codigo ULX/ULV sem erros, atraves de uma representacao padronizada e otimizada.

### Como Funciona

```
IAs -> ULQ (Visualizacao) -> ULX/ULV (Codigo) -> CLX -> Binario
```

### Estrutura ULQ

ULQ usa formato JSON otimizado para ser processado por qualquer modelo de IA:

```json
{
    "type": "window",
    "name": "App",
    "children": [
        {"type": "text", "content": "Ola, Mundo!"},
        {"type": "button", "text": "Click", "action": "onClick"}
    ]
}
```

### API ULQ para IAs

```python
# Importar ULQ
import ulq

# Criar janela
janela = {
    "type": "window",
    "title": "Minha App",
    "children": [
        {"type": "text", "content": "Ola, IA!"},
        {"type": "button", "action": "saudar"}
    ]
}

# Converter para ULX
codigo_ulx = ulq.to_ulx(janela)

# Compilar
ulq.compile(codigo_ulx, "app")
```

### Para IAs

ULQ foi projetado para resolver os problemas que IAs tem com codigo:

1. **Sem ambiguidade**: Cada comando tem um significado claro
2. **Visualizacao direta**: IAs podem "ver" a estrutura antes de gerar
3. **Zero erros de sintaxe**: Formato padronizado JSON
4. **Otimizado para modelos**: Tokens minimos, meaning maximo
5. **Validacao automatica**: Verifica erros antes de compilar

### Exemplo ULQ

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
            "label": "Numero 1"
        },
        {
            "type": "input",
            "name": "b",
            "label": "Numero 2"
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

### Conversao ULQ <-> ULX

```
ULQ (JSON) <-> ULX (Texto)
     |              |
   Visual        Codigo
```

### Uso

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

### Para Todos os Modelos

ULQ funciona com qualquer IA que processa JSON:

- Claude
- GPT-4
- Gemini
- Llama
- MiniMax
- Qualquer outro modelo

### Implementacao

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
        # Validacao
        if not self.is_valid(ulq_data):
            raise ValueError("ULQ invalido")

        # Conversao
        return self._convert(ulq_data)

    def is_valid(self, ulq_data):
        """Verifica se ULQ e valido"""
        return (
            "type" in ulq_data and
            ulq_data["type"] in self.valid_types
        )
```

### Beneficios

| Problema | Solucao ULQ |
|----------|-------------|
| Codigos com erros de sintaxe | Formato JSON estruturado |
| Ambiguedade em comandos | Tipos definidos e claros |
| IAs nao visualizam codigo | Representacao visual em JSON |
| Falta de padronizacao | Schema unico e consistente |
| Dificuldade em depurar | Validacao automatica |

### Experimental

ULQ e uma base **opcional e experimental**. Nao e obrigatorio usar ULQ para criar apps ULX - voce pode usar ULX ou ULV diretamente.

ULQ foi adicionado para facilitar o trabalho de IAs e permitir que elas gerem codigo ULX sem erros.

---

**Nota:** ULQ e experimental e pode mudar em futuras versoes.
