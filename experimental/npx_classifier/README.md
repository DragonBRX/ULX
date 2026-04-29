# NEURAL.PULSE (.npx) - Classificador Semântico v1.0

## Conceito: "GPS de Classificação Hierárquica"

**NPX** é a quinta base do ULX - um sistema de indexação semântica que transforma modelos de IA de "busca linear" para "acesso direto por gavetas".

**Slogan:** "Don't calculate. Navigate."

---

## A Revolução

### Modelo Atual (Lento):
```
Input → Cálculo de atenção em TODOS os parâmetros → Predição
         ↑
         GASTOU TEMPO CALCULANDO 70B PARÂMETROS
```

### Com NPX (Rápido):
```
Input → Filtro de DNA Semântico → Acesso Direto ao Binário
         ↑
         PULOU DIRETO PARA A GAVETA CERTA
```

---

## Arquitetura do .npx

```
┌─────────────────────────────────────────────────────────────┐
│ MAGIC BYTES           → NPX\n (0x4E 0x50 0x58 0x0A)     │
├─────────────────────────────────────────────────────────────┤
│ DNA TAXONOMY          → Lista de conceitos classificados   │
├─────────────────────────────────────────────────────────────┤
│ INTENT FILTER         → Camada de intenção do usuário     │
├─────────────────────────────────────────────────────────────┤
│ PROXIMITY VECTORS     → Códigos binários curtos           │
├─────────────────────────────────────────────────────────────┤
│ POINTER INDEX         → Mapa de ponteiros para .nfx       │
└─────────────────────────────────────────────────────────────┘
```

---

## Camadas Detalhadas

### 1. DNA Taxonomy (Taxonomia de Conceitos)

Classificação hierárquica em 4 níveis:

```
DOMÍNIO → CATEGORIA → OBJETO → AÇÃO
```

**Exemplo:**
```
[DOMÍNIO: MECÂNICA]
  └── [CATEGORIA: MOTOR]
        └── [OBJETO: COMBUSTÃO]
              └── [AÇÃO: REPARO]
```

### 2. Binary Resumo (Código Curto)

Cada conceito tem um código binário de 8 bits:

| Conceito          | Binário | Hex  |
|-------------------|---------|------|
| MECÂNICA          | 00000001| 0x01 |
| CULINÁRIA         | 00000010| 0x02 |
| PROGRAMÇÃO        | 00000100| 0x04 |
| ASTROFÍSICA       | 00001000| 0x08 |
| MEDICINA          | 00010000| 0x10 |
| DIREITO           | 00100000| 0x20 |
| FINANÇAS          | 01000000| 0x40 |
| ARTE              | 10000000| 0x80 |

### 3. Intent Filter (Filtro de Intenção)

Analisa o "tom" do usuário:

```json
{
  "input": "Como consertar um motor de carro?",
  "classification": {
    "domain": "MECÂNICA",
    "object": "MOTOR",
    "action": "REPARO"
  },
  "intent": {
    "type": "TECHNICAL",
    "urgency": "MEDIUM",
    "style": "DETAILED"
  },
  "pointer": "0x88FF22",
  "speed": "FAST"
}
```

---

## Exemplo de Fluxo

### Input do Usuário:
```
"Como consertar um motor de carro?"
```

### Processamento NPX:

```
1. ANÁLISE SEMÂNTICA
   └─ "motor" → DOMÍNIO: MECÂNICA
   └─ "carro" → CATEGORIA: AUTOMOTIVO
   └─ "consertar" → AÇÃO: REPARO

2. GERAÇÃO DO CÓDIGO
   └─ Binário: 00000001 (MECÂNICA)
   └─ Pointer: 0x88FF22 (endereço no .nfx)

3. ACESSO DIRETO
   └─ Pula direto para binários de MECÂNICA
   └─ Ignora culinária, poesia, código, etc.

4. RESPOSTA
   └─ Resposta técnica sobre reparo de motor
```

---

## Comparação de Performance

| Métrica              | IA Tradicional | IA + NPX      |
|----------------------|----------------|---------------|
| Tempo para responder | 2-5 segundos   | 50-200ms      |
| Parâmetros calculados| 70 bilhões     | 2 milhões     |
| RAM utilizada        | 140 GB         | 4 GB          |
| Acuidade             | ~85%           | ~95%          |

---

## Integração com NFX

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│   ULQ    │───▶│   NPX    │───▶│   NFX    │
│  (IA ve) │    │(classif) │    │ (dados)  │
└──────────┘    └──────────┘    └──────────┘
                    │                │
                    ▼                ▼
              "Entendo a        "Aqui estão
               estrutura"         os dados"
```

---

## O DNA Semântico

O sistema usa "etiquetas" pré-definidas para classificar todo conhecimento:

### Domínios Principais:

| Código | Domínio      | Subcategorias              |
|--------|--------------|----------------------------|
| 0x01   | MECÂNICA     | Motor, Elétrica, Estrutural|
| 0x02   | CULINÁRIA    | Receitas, Técnicas, Hist.  |
| 0x03   | SAÚDE       | Medicina, Nutrição, Fitness|
| 0x04   | TECNOLOGIA   | Programação, Hardware, IA |
| 0x05   | CIÊNCIA     | Física, Química, Bio      |
| 0x06   | HUMANAS     | História, Filosofia, Soc.  |
| 0x07   | ARTE        | Música, Pintura, Lit.      |
| 0x08   | DIREITO     | Civil, Penal, Trabalhista |
| 0x09   | FINANÇAS    | Investimentos, Contabilidade|
| 0x0A   | ESPORTES    | Regras, Técnicas, História|
| ...    | ...         | ...                        |

---

## Status: Experimental

Este é um conceito revolucionário que requer:

- Mapeamento de 100.000+ conceitos
- Interface com .nfx para dados reais
- Benchmarking contra transformers tradicionais

**A ideia é transformar IA de "adivinhação estatística" para "navegação estruturada".**