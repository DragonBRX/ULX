# Guia Completo ULX v3.0

## Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Sintaxe Básica](#sintaxe-básica)
4. [Variáveis e Tipos](#variáveis-e-tipos)
5. [Operadores](#operadores)
6. [Controle de Fluxo](#controle-de-fluxo)
7. [Funções](#funções)
8. [Entrada e Saída](#entrada-e-saída)
9. [Biblioteca Padrão](#biblioteca-padrão)
10. [Exemplos Práticos](#exemplos-práticos)

## Introdução

ULX é uma linguagem de programação universal, fácil e rápida. Projetada para:

- **Iniciantes**: Sintaxe simples em português
- **Profissionais**: Performance de código nativo
- **Universal**: Funciona em qualquer sistema

## Instalação

### Linux

```bash
git clone https://github.com/DragonBRX/ULX.git
cd ULX
chmod +x install.sh
sudo ./install.sh
```

### Windows

```powershell
git clone https://github.com/DragonBRX/ULX.git
cd ULX
.\install.ps1
```

## Sintaxe Básica

### Hello World

```ulx
escreva("Olá, Mundo!")
```

### Comentários

```ulx
// Comentário de linha única

/*
   Comentário
   de múltiplas
   linhas
*/
```

## Variáveis e Tipos

### Declaração

ULX usa tipagem dinâmica. Declare variáveis simplesmente atribuindo valores:

```ulx
// Números inteiros
idade = 25
ano = 2024
negativo = -10

// Números decimais
preco = 19.99
pi = 3.14159

// Textos (strings)
nome = "Maria"
sobrenome = 'Silva'

// Booleanos
ativo = verdadeiro
inativo = falso

// Nulo
vazio = nulo
```

### Arrays

```ulx
numeros = [1, 2, 3, 4, 5]
nomes = ["Ana", "Bruno", "Carla"]
misturado = [1, "dois", 3.0]
```

### Dicionários

```ulx
pessoa = {
    "nome": "João",
    "idade": 30,
    "cidade": "São Paulo"
}
```

## Operadores

### Aritméticos

```ulx
a = 10 + 5    // Adição: 15
b = 10 - 3    // Subtração: 7
c = 4 * 2     // Multiplicação: 8
d = 15 / 3    // Divisão: 5
e = 17 % 5    // Módulo: 2
f = 2 ^ 8     // Potência: 256
```

### Comparação

```ulx
x == y       // Igual
x != y       // Diferente
x > y        // Maior
x < y        // Menor
x >= y       // Maior ou igual
x <= y       // Menor ou igual
```

### Lógicos

```ulx
a && b       // E (AND)
a || b       // OU (OR)
!a           // NÃO (NOT)
```

### Atribuição Composta

```ulx
x = 10
x += 5       // x = 15
x -= 3       // x = 12
x *= 2       // x = 24
x /= 4       // x = 6
```

## Controle de Fluxo

### Se / Senão

```ulx
idade = 18

se (idade >= 18) {
    escreva("Maior de idade")
} senao {
    escreva("Menor de idade")
}

// Encadeado
se (nota >= 90) {
    escreva("A")
} senao se (nota >= 80) {
    escreva("B")
} senao se (nota >= 70) {
    escreva("C")
} senao {
    escreva("Reprovado")
}
```

### Enquanto (Loop)

```ulx
contador = 0

enquanto (contador < 5) {
    escreva(contador)
    contador += 1
}
```

### Para (Loop)

```ulx
// Contagem de 1 a 10
para (i = 1; i <= 10; i = i + 1) {
    escreva(i)
}

// Contagem regressiva
para (i = 10; i > 0; i = i - 1) {
    escreva(i)
}
```

### Break e Continue

```ulx
para (i = 0; i < 100; i = i + 1) {
    se (i == 5) {
        continua  // Pula para próxima iteração
    }
    se (i == 10) {
        pare      // Sai do loop
    }
    escreva(i)
}
```

## Funções

### Definição

```ulx
funcao soma(a, b) {
    retorna a + b
}

funcao saudar(nome) {
    retorna "Olá, " + nome + "!"
}

funcao eh_par(numero) {
    se (numero % 2 == 0) {
        retorna verdadeiro
    }
    retorna falso
}
```

### Chamada

```ulx
resultado = soma(10, 20)
escreva(resultado)  // 30

mensagem = saudar("Mundo")
escreva(mensagem)   // Olá, Mundo!

se (eh_par(4)) {
    escreva("É par")
}
```

## Entrada e Saída

### Saída (escreva)

```ulx
escreva("Olá, mundo!")
escreva("Valor:", 42)
escreva("Nome:", nome, "Idade:", idade)
escreva(1 + 2 + 3)
```

### Entrada (leia)

```ulx
escreva("Digite seu nome:")
nome = leia()
escreva("Olá,", nome)

escreva("Digite sua idade:")
idade = leia()
escreva("Você tem", idade, "anos")
```

## Biblioteca Padrão

### Funções Matemáticas

```ulx
x = sqrt(16)        // Raiz quadrada: 4
y = pow(2, 3)       // Potência: 8
z = abs(-5)         // Valor absoluto: 5
w = floor(3.7)      // Arredonda para baixo: 3
v = ceil(3.2)       // Arredonda para cima: 4
u = round(3.5)      // Arredonda: 4

// Trigonometria
s = sin(0)         // Seno: 0
c = cos(0)         // Cosseno: 1
t = tan(0)         // Tangente: 0

// Logaritmos
l = log(2.718)      // Log natural: ~1
l10 = log10(100)   // Log base 10: 2
```

### Funções de Texto

```ulx
texto = "  Hello World  "

tamanho(texto)              // Comprimento: 14
texto_maior = maiuscula(texto)  // "HELLO WORLD"
texto_menor = minuscula(texto)  // "hello world"
texto_limpo = trim(texto)       // "Hello World"

// Divisão e junção
partes = split("a,b,c", ",")  // ["a", "b", "c"]
junto = join(["a", "b"], "-")   // "a-b"

// Conversão
numero = inteiro("42")    // String para int: 42
texto = texto(42)        // Int para string: "42"
```

## Exemplos Práticos

### Calculadora

```ulx
escreva("Calculadora ULX")
escreva("================")

escreva("Digite o primeiro número:")
a = leia()

escreva("Digite o segundo número:")
b = leia()

escreva("Escolha a operação: + - * /")
op = leia()

se (op == "+") {
    resultado = a + b
} senao se (op == "-") {
    resultado = a - b
} senao se (op == "*") {
    resultado = a * b
} senao se (op == "/") {
    se (b != 0) {
        resultado = a / b
    } senao {
        escreva("Erro: Divisão por zero!")
    }
}

escreva("Resultado:", resultado)
```

### Tabuada

```ulx
escreva("Tabuada de Multiplicação")
escreva("=========================")

escreva("Digite um número:")
num = leia()

para (i = 1; i <= 10; i = i + 1) {
    resultado = num * i
    escreva(num, " x ", i, " = ", resultado)
}
```

### Lista de Tarefas

```ulx
escreva("Lista de Tarefas ULX")
escreva("====================")

tarefas = ["Aprender ULX", "Criar projeto", "Compilar app"]

escreva("")
escreva("Suas tarefas:")
para (i = 0; i < tamanho(tarefas); i = i + 1) {
    escreva(i + 1, ". ", tarefas[i])
}

escreva("")
escreva("Adicionar nova tarefa:")
nova = leia()

tarefas[2] = nova

escreva("")
escreva("Tarefas atualizadas:")
para (i = 0; i < tamanho(tarefas); i = i + 1) {
    escreva(i + 1, ". ", tarefas[i])
}
```

## Compilação

```bash
# Compilar
ulx-compile programa.ulx -o app

# Apenas gerar C
ulx-compile programa.ulx --c-only

# Executar
./app

# Empacotar
ulx-pack pack app -o programa.ulx --name "Meu App" --version "1.0"

# Executar pacote
ulx-run programa.ulx
```

## Criar Projeto

```bash
# Novo projeto
ulx-init meu_projeto -d "Meu primeiro app ULX"

# Entrar no projeto
cd meu_projeto

# Compilar e executar
make run
```

## Mais Informações

- Repositório: https://github.com/DragonBRX/ULX
- Documentação: https://github.com/DragonBRX/ULX/docs
