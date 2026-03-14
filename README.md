# Ordem Paranormal Parser

Parser de PDF para extrair informações do livro de regras de Ordem Paranormal RPG em formato JSON.

## Funcionalidades

- Extração de criaturas com atributos, ataques e habilidades
- Extração de rituais com círculo, execução, alcance e descrição
- Suporte para extração seletiva (criaturas, rituais ou tudo)
- Exportação para JSON estruturado

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Extrair tudo (criaturas e rituais)

```bash
python main.py caminho/para/livro-regras.pdf
```

### Extrair apenas criaturas

```bash
python main.py caminho/para/livro-regras.pdf creatures
```

### Extrair apenas rituais

```bash
python main.py caminho/para/livro-regras.pdf rituals
```

## Estrutura do JSON

### Criaturas

```json
{
  "creatures": [
    {
      "name": "Nome da Criatura",
      "category": "Categoria",
      "vd": 5,
      "hp": "100",
      "attacks": [
        {
          "name": "Ataque",
          "damage": "2d6+3",
          "description": "Descrição do ataque"
        }
      ],
      "abilities": [
        {
          "name": "Habilidade",
          "description": "Descrição da habilidade"
        }
      ],
      "raw_text": "Texto original extraído"
    }
  ]
}
```

### Rituais

```json
{
  "rituals": [
    {
      "name": "Nome do Ritual",
      "circle": 2,
      "execution": "padrão",
      "range": "pessoal",
      "target": "você",
      "duration": "cena",
      "description": "Descrição do ritual",
      "raw_text": "Texto original extraído"
    }
  ]
}
```

## Estrutura do Projeto

```
.
├── main.py              # Ponto de entrada CLI
├── models.py            # Definições Pydantic
├── pdf_parser.py        # Parser principal de PDF
├── creature_parser.py   # Parser específico para criaturas
├── ritual_parser.py     # Parser específico para rituais
├── requirements.txt     # Dependências Python
└── output/              # Arquivos JSON gerados
```

## Desenvolvimento

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar

```bash
python main.py caminho/para/arquivo.pdf
```

## Expansão Futura

O projeto está estruturado para facilmente adicionar novos tipos de extração:

- Habilidades de classes
- Itens e equipamentos
- Poderes paranormais
- Tabelas de referência

Para adicionar um novo tipo, crie um parser em seguindo o padrão dos existentes.
