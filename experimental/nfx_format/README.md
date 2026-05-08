# NEURAL.FLUX (.nfx) - Especificacao Tecnica v1.0

## Visao Geral

**NEURAL.FLUX** e um formato de armazenamento dinamico para modelos de IA que substitui arquivos binarios estaticos (.safetensors) por estruturas de grafos tensoriais indexados.

**Slogan:** "Don't just store weights. Stream intelligence."

---

## Estrutura do Arquivo

```
+-------------------------------------------------------------+
| MAGIC BYTES (4 bytes)          -> 4E 46 58 0A              |
+-------------------------------------------------------------+
| HEADER JSON (variavel)       -> Metadados + Topologia      |
+-------------------------------------------------------------+
| SPARSE INDEX MAP (bitfield)  -> Mapa de pesos nao-zero    |
+-------------------------------------------------------------+
| BIT-PLANE LAYER 0            -> Bits mais significativos   |
+-------------------------------------------------------------+
| BIT-PLANE LAYER 1            -> ...                         |
+-------------------------------------------------------------+
| ...                                                        |
+-------------------------------------------------------------+
| BIT-PLANE LAYER N            -> Bits menos significativos |
+-------------------------------------------------------------+
| INDEX TABLE                  -> Ponteiros para blocos       |
+-------------------------------------------------------------+
```

---

## Componentes Tecnicos

### 1. Magic Bytes (4 bytes)
```
N F X \n (0x4E 0x46 0x58 0x0A)
```

### 2. Semantic Header (JSON)

```json
{
    "version": "1.0",
    "model_name": "llama_70b",
    "total_params": 70000000000,
    "layers": [
        {
            "name": "attention_qkv",
            "shape": [4096, 4096],
            "quant_bits": 4,
            "block_size": 65536,
            "sparse_ratio": 0.72
        },
        {
            "name": "mlp_fc",
            "shape": [4096, 11008],
            "quant_bits": 1.58,
            "block_size": 32768,
            "sparse_ratio": 0.85
        }
    ],
    "hip": {
        "prefetch_sequence": ["qkv", "attn", "ffn"],
        "hardware_hint": "cuda_a100"
    },
    "encryption": {
        "enabled": false,
        "algorithm": "AES-256-GCM"
    }
}
```

### 3. Sparse Index Map

Mapa de bits indicando pesos nao-zero:
- Bit = 1: peso significativo (armazenar)
- Bit = 0: peso zero (pular)

### 4. Bit-Plane Storage

Organizacao em planos de bits para carregamento progressivo:
- Layer 0: Bits mais significativos (importancia maxima)
- Layer N: Bits menos significativos (detalhes finos)

---

## Diferenciais Tecnicos

### Bit-Depth Adaptativo

Cada camada pode ter precisao diferente:

| Tipo de Camada     | Precisao  | Razao                        |
|--------------------|-----------|------------------------------|
| Attention QKV      | 4-bit     | Alta precisao necessaria    |
| MLP Feed-forward   | 1.58-bit  | Pode usar baixa precisao     |
| Embeddings         | 8-bit     | Precisao moderada            |
| Layer Norm         | 16-bit    | Precisao total               |

### Paging Granular (mmap)

```
# Sem mmap (safetensors):
model = load_tensor("model.safetensors")  # 70GB em RAM

# Com mmap (nfx):
model = mmap_tensor("model.nfx")  # 0GB em RAM, carrega sob demanda
```

### HIP (Header de Inferencia Preditiva)

```python
# O header sugere pre-carregamento baseado no contexto
hip = {
    "task_type": "chat",
    "expected_tokens": 2048,
    "critical_layers": ["attention_qkv", "mlp_fc"]
}
```

---

## Conversao .safetensors -> .nfx

### Algoritmo de Destilacao

1. **Analise de Importancia**: Identificar pesos redundantes
2. **Quantizacao Adaptativa**: Aplicar precisao por camada
3. **Sparsity Extraction**: Criar mapa de zeros
4. **Bit-Plane Slicing**: Organizar em camadas de bits
5. **Compressao Final**: Reducao de ~60% no tamanho

```python
# Exemplo de conversao
from nfx_converter import SafeToNFX

converter = SafeToNFX()
converter.load("model.safetensors")
converter.analyze_sparsity(threshold=0.001)
converter.quantize(layers={
    "attention": 4,
    "mlp": 1.58,
    "embed": 8
})
converter.export("model.nfx")
```

---

## Benchmark Esperado

| Metrica              | .safetensors  | .nfx          | Melhoria    |
|----------------------|---------------|---------------|-------------|
| Tamanho arquivo      | 140 GB        | 56 GB         | -60%        |
| Memoria RAM (load)   | 140 GB        | 0 GB          | mmap        |
| Tempo primeira token | 45s           | 2s            | 22x         |
| Streaming_tokens/s   | 0             | 120           | infinito    |

---

## Casos de Uso

1. **Modelos grandes**: LLM 7B+ em dispositivos com RAM limitada
2. **Edge Computing**: IA em IoT/mobile com cache dinamico
3. **Streaming de modelos**: Modelo "chega" conforme necessidade
4. **Edicao de pesos**: Alterar camada sem recarregar modelo inteiro

---

## Integracao ULQ

O formato .nfx pode ser descrito em ULQ para IAs:

```json
{
    "project": "model_nfx",
    "type": "file",
    "format": "nfx",
    "properties": {
        "model_name": "llama_70b",
        "size": "56GB",
        "quantization": "mixed",
        "sparsity": 0.78,
        "layers": 80,
        "streaming": true
    },
    "description": "Modelo neural em formato NEURAL.FLUX com streaming dinamico"
}
```

---

## Status: Experimental

Este e um formato experimental que requer:

- Implementacao em C/CUDA para maxima performance
- Testes de benchmark contra safetensors
- Suporte de frameworks (PyTorch, TensorFlow)

**Pull requests bem-vindos!**
