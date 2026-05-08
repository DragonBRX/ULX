# Pasta Experimental - ULX

**ATENCAO: Todo conteudo aqui e EXPERIMENTAL e NAO esta pronto para producao.**

---

## O que e isto?

Esta pasta contem ideias e conceitos que estao em fase de **teste e pesquisa**. Sao funcionalidades que podem evoluir, mudar significativamente, ou ate serem removidas futuramente.

---

## Conteudo Atual

### `nfx_format/` - NEURAL.FLUX (.nfx)
Formato de armazenamento dinamico para modelos de IA.

**Status:** Experimental
**Objetivo:** Substituir .safetensors por estruturas de grafos tensoriais indexados com:
- Bit-depth adaptativo por camada
- Memory-mapped I/O
- Sparsity nativa
- Streaming de pesos

**NAO PRODUCAO:** Requer implementacao em C/CUDA para performance real.

---

### `npx_classifier/` - NEURAL.PULSE (.npx)
Classificador semantico para IA baseada em indexacao.

**Status:** Experimental
**Objetivo:** Transformar IA de "busca linear" para "acesso direto por gavetas" usando:
- DNA semantico (classificacao hierarquica)
- Filtro de intencao
- Ponteiros para binarios

**NAO PRODUCAO:** Conceito requer mapeamento de 100.000+ conceitos.

---

## Por que experimental?

1. **Performance nao testada:** Nao ha benchmarks reais contra solucoes atuais
2. **Implementacao incompleta:** Apenas prototipos em Python
3. **Padroes nao estabelecidos:** Pode mudar significativamente
4. **Sem comunidade:** Nao ha adotacao ou feedback de outros desenvolvedores

---

## Roadmap Experimental

```
Fase 1 [OK] Conceito criado (atual)
Fase 2 [  ] Implementar prototipos funcionais
Fase 3 [  ] Benchmarking contra solucoes atuais
Fase 4 [  ] Implementacao em C/CUDA
Fase 5 [  ] Adotacao pela comunidade
Fase 6 [  ] Estavel para producao
```

---

## Como testar

```bash
# NFX
cd nfx_format
python nfx_core.py create teste.nfx
python nfx_core.py analyze teste.nfx

# NPX
cd npx_classifier
python npx_classifier.py demo
python npx_classifier.py classify "Como consertar um motor?"
```

---

## Avisos Legais

- Use por sua conta e risco
- Nao ha garantias de funcionamento
- Contribuicoes sao bem-vindas mas funcionalidades podem ser removidas

---

**Experimental desde:** 2025-04-29
**Mantido por:** ULX Team (DragonBRX)
