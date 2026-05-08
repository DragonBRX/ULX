# ULV - Universal Language Visual
## Linguagem Visual de Design

**ULV** é a linguagem visual do ecossistema ULX. Permite criar interfaces gráficas arrastando e soltando componentes, como um HTML visual.

### Conceito

- **WYSIWYG**: O que você vê é o que você executa
- **Drag & Drop**: Arraste componentes para criar interfaces
- **Prévia em Tempo Real**: Veja o resultado instantaneamente
- **Mesma Base**: Compila para o mesmo binário que ULX

### Arquivos ULV

Arquivos `.ulv` contêm código visual que é convertido para ULX:

```
botao("Click Me!")
    posicao: centro
    cor: azul
    tamanho: 200x50

texto("Olá, Mundo!")
    fonte: Arial
    tamanho: 24
```

### Componentes Visuais

| Componente | Descrição |
|-----------|-----------|
| `texto()` | Textolabel |
| `botao()` | Botão clicável |
| `caixa_texto()` | Campo de entrada |
| `imagem()` | Exibe imagem |
| `janela()` | Janela/container |
| `grade()` | Layout em grade |
| `linha()` | Linha horizontal |

### Exemplo Completo

```
janela("Minha App") {
    titulo: "Calculadora"
    tamanho: 400x300

    texto("Calculadora ULX")
        posicao: topo
        alinhamento: centro

    entrada(a)
        posicao: centro
        rotulo: "Número 1"

    entrada(b)
        posicao: centro
        rotulo: "Número 2"

    botao("Somar")
        posicao: centro
        acao: somar()
}
```

### Como Usar

1. Crie um arquivo `.ulv`
2. Abra no ULX Studio
3. Arraste componentes ou escreva código
4. Prévia em tempo real
5. Compile para binário

### Arquitetura

```
.ulv (Visual) → ULV Parser → ULX Code → CLX Compiler → Binário
```

O ULV compila para ULX, então todo código ULV é ULX válido.
