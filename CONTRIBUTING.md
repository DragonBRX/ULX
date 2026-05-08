# Contribuindo para ULX

Obrigado pelo interesse em contribuir com o projeto ULX!

## Como Contribuir

### Reportando Bugs

1. Verifique se o bug já não foi reportado
2. Abra uma issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Versão do ULX
   - Sistema operacional

### Sugerindo Melhorias

1. Abra uma issue com o prefixo `[Feature]`
2. Descreva a melhoria e seu uso
3. Explique por seria útil

### Pull Requests

1. Fork o repositório
2. Crie uma branch: `git checkout -b minha-feature`
3. Faça as alterações
4. Execute os testes: `python -m pytest tests/ -v`
5. Commit: `git commit -am 'Adiciona nova feature'`
6. Push: `git push origin minha-feature`
7. Abra um Pull Request

## Padrões de Código

- Use 4 espaços para indentação
- Siga PEP 8 para código Python
- Documente funções e classes
- Adicione testes para novas funcionalidades

## Desenvolvimento

### Estrutura do Projeto

```
ULX/
├── ulx_core/          # Módulo core (lexer, parser, interpreter)
├── clx_compiler/      # Compilador ULX
├── ulq_intelligence/  # Interface para IAs
├── uld_distribution/  # Sistema de build
├── nfx_format/        # Formato NFX
├── npx_classifier/    # Classificador NPX
├── tests/             # Testes unitários
├── examples/          # Exemplos ULX
└── docs/              # Documentação
```

### Executando Testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Teste específico
python -m pytest tests/test_lexer.py -v
python -m pytest tests/test_parser.py -v
python -m pytest tests/test_interpreter.py -v
```

### Usando o REPL

```bash
python -m ulx_core.repl
```

## Licença

Contribuições são licenciadas sob MIT License.
