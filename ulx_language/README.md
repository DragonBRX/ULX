# ULX - Universal Linux
## Linguagem de Programação Universal

**ULX** é uma linguagem de programação revolucionária escrita em português, fácil de aprender e extremamente rápida.

### Características

- **Sintaxe em Português**: Comandos como `escreva`, `se`, `enquanto`, `funcao`
- **Ultra-Rápida**: Compila para binários nativos otimizados
- **Universal**: Funciona em qualquer sistema
- **Fácil**: Perfeita para iniciantes e profissionais

### Hello World

```ulx
escreva("Olá, Mundo!")
```

### Exemplo Completo

```ulx
// Calculadora simples
funcao soma(a, b) {
    retorna a + b
}

funcao subtracao(a, b) {
    retorna a - b
}

escreva("Calculadora ULX")
escreva("================")

a = 10
b = 5

escreva(a, " + ", b, " = ", soma(a, b))
escreva(a, " - ", b, " = ", subtracao(a, b))
```

### Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `escreva()` | Imprime texto na tela |
| `leia()` | Lê entrada do usuário |
| `se / senao` | Condicional |
| `enquanto` | Loop enquanto |
| `para` | Loop for |
| `funcao` | Define função |

### Como Compilar

```bash
ulx-compile programa.ulx -o app
./app
```

### Como Executar

```bash
ulx-run app.ulx
```

### Documentação

Veja `docs/ulx_syntax.md` para referência completa da sintaxe.
