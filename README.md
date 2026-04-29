# ULX - Linguagem de Programação Universal

**ULX** é uma linguagem de programação revolucionária, fácil, rápida e universal. Desenvolvida para todos - iniciantes, programadores experientes, e até IAs.

## Características Principais

- **Fácil para Todos**: Sintaxe simples em português, legível e intuitiva
- **Ultra-Rápida**: Compila para binários nativos otimizados
- **Universal**: Funciona em Windows, Linux, MacOS
- **Visual**: Prévia visual em tempo real do seu código
- **Cross-Platform**: Um código, qualquer sistema operacional
- **Stdlib Completa**: Biblioteca padrão vasta para qualquer tarefa

## Instalação Rápida

### Linux / Ubuntu

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

### MacOS

```bash
git clone https://github.com/DragonBRX/ULX.git
cd ULX
chmod +x install.sh
sudo ./install.sh
```

## Primeiro Programa

```ulx
escreva("Olá, Mundo!")
```

## Sintaxe Básica

```ulx
// Variáveis
nome = "Maria"
idade = 25
ativo = verdadeiro

// Condições
se (idade >= 18) {
    escreva("Maior de idade")
}

// Loops
para (i = 1; i <= 10; i = i + 1) {
    escreva(i)
}

// Funções
funcao saudar(nome) {
    retorna "Olá, " + nome
}

escreva(saudar("Mundo"))
```

## Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `ulx-compile <arquivo.ulx>` | Compila para binário |
| `ulx-run <app.ulx>` | Executa aplicativo |
| `ulx-visual` | Editor visual com prévia |
| `ulx-pack <binario>` | Empacota aplicativo |
| `ulx-init <projeto>` | Cria novo projeto |

## Performance

ULX gera binários nativos extremamente otimizados:

- Compilação com GCC/Clang
- Otimização -O3 nativa
- Suporte SIMD (AVX2/AVX-512)
- Binários estáticos (sem dependências)
- Link-Time Optimization (LTO)

## Roadmap

- [x] Compilador CLX
- [x] Runtime ULX
- [x] Bibliotecas padrão
- [ ] Editor Visual completo
- [ ] Debugger integrado
- [ ] Gerenciador de pacotes
- [ ] Suporte a banco de dados
- [ ] Bindings para C/C++/Python

## Documentação

Veja `docs/guia.md` para guia completo.

## Licença

MIT License - Use, modifique, distribua livremente.

## Autor

DragonBRX - https://github.com/DragonBRX
