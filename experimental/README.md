# 🧪 Pasta Experimental - ULX

**⚠️ ATENÇÃO: Todo conteúdo aqui é EXPERIMENTAL e NÃO está pronto para produção.**

---

## O que é isto?

Esta pasta contém ideias e conceitos que estão em fase de **teste e pesquisa**. São funcionalidades que podem evoluir, mudar significativamente, ou até serem removidas futuramente.

---

## Conteúdo Atual

### 📦 `nfx_format/` - NEURAL.FLUX (.nfx)
Formato de armazenamento dinâmico para modelos de IA.

**Status:** Experimental
**Objetivo:** Substituir .safetensors por estruturas de grafos tensoriais indexados com:
- Bit-depth adaptativo por camada
- Memory-mapped I/O
- Sparsity nativa
- Streaming de pesos

**⚠️ NÃO PRODUÇÃO:** Requer implementação em C/CUDA para performance real.

---

### 🎯 `npx_classifier/` - NEURAL.PULSE (.npx)
Classificador semântico para IA baseada em indexação.

**Status:** Experimental
**Objetivo:** Transformar IA de "busca linear" para "acesso direto por gavetas" usando:
- DNA semântico (classificação hierárquica)
- Filtro de intenção
- Ponteiros para binários

**⚠️ NÃO PRODUÇÃO:** Conceito requer mapeamento de 100.000+ conceitos.

---

## Por que experimental?

1. **Performance não testada:** Não há benchmarks reais contra soluções atuais
2. **Implementação incompleta:** Apenas protótipos em Python
3. **Padrões não estabelecidos:** Pode mudar significativamente
4. **Sem comunidade:** Não há adoção ou feedback de outros desenvolvedores

---

## Roadmap Experimental

```
Fase 1 ✅ Conceito criado (atual)
Fase 2 ⏳ Implementar protótipos funcionais
Fase 3 ⏳ Benchmarking contra soluções atuais
Fase 4 ⏳ Implementação em C/CUDA
Fase 5 ⏳ Adoção pela comunidade
Fase 6 ⏳ Estável para produção
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
- Não há garantias de funcionamento
- Contribuições são bem-vindas mas funcionalidades podem ser removidas

---

**🧪 Experimental desde:** 2025-04-29
**📧 Mantido por:** ULX Team (DragonBRX)