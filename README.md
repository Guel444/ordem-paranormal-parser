# Ordem Paranormal Parser

Parser de PDF para extrair informações do livro de regras de Ordem Paranormal RPG em formato JSON.

## Funcionalidades

- Extração de criaturas com atributos, ataques e habilidades
- Extração de rituais com círculo, execução, alcance e descrição
- Suporte para extração seletiva (criaturas, rituais ou tudo)
- Exportação para JSON estruturado

## Instalação

```bash
npm install
```

## Uso

### Extrair tudo (criaturas e rituais)

```bash
npm start caminho/para/livro-regras.pdf
```

ou

```bash
ts-node src/index.ts caminho/para/livro-regras.pdf
```

### Extrair apenas criaturas

```bash
npm start caminho/para/livro-regras.pdf creatures
```

### Extrair apenas rituais

```bash
npm start caminho/para/livro-regras.pdf rituals
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
      "rawText": "Texto original extraído"
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
      "rawText": "Texto original extraído"
    }
  ]
}
```

## Estrutura do Projeto

```
src/
├── index.ts              # Ponto de entrada CLI
├── types/
│   └── creature.ts       # Definições TypeScript
├── parsers/
│   ├── pdfParser.ts      # Parser principal de PDF
│   ├── creatureParser.ts # Parser específico para criaturas
│   └── ritualParser.ts   # Parser específico para rituais
└── utils/
    └── textProcessor.ts  # Utilitários de processamento de texto
output/                    # Arquivos JSON gerados
```

## Desenvolvimento

### Compilar TypeScript

```bash
npm run build
```

### Executar em modo desenvolvimento

```bash
npm run dev caminho/para/arquivo.pdf
```

## Expansão Futura

O projeto está estruturado para facilmente adicionar novos tipos de extração:

- Habilidades de classes
- Itens e equipamentos
- Poderes paranormais
- Tabelas de referência

Para adicionar um novo tipo, crie um parser em `src/parsers/` seguindo o padrão dos existentes.
