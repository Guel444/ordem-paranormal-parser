import sys
from pathlib import Path
from pdf_parser import PDFParser
from creature_parser import CreatureParser
from ritual_parser import RitualParser


def main():
    args = sys.argv[1:]

    if not args:
        print("Uso: python main.py <caminho-do-pdf> [tipo]")
        print("")
        print("Argumentos:")
        print("  <caminho-do-pdf>  Caminho para o arquivo PDF")
        print("  [tipo]            Tipo de extração: all, creatures, rituals (padrão: all)")
        print("")
        print("Exemplos:")
        print("  python main.py livro-regras.pdf")
        print("  python main.py livro-regras.pdf all")
        print("  python main.py livro-regras.pdf creatures")
        print("  python main.py livro-regras.pdf rituals")
        sys.exit(1)

    pdf_path = args[0]
    extraction_type = args[1] if len(args) > 1 else "all"

    if extraction_type not in ["creatures", "rituals", "all"]:
        print("Tipo inválido. Use: creatures, rituals, ou all")
        sys.exit(1)

    if not Path(pdf_path).exists():
        print(f"Erro: Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    print(f"Processando: {pdf_path}")
    print(f"Tipo de extração: {extraction_type}")
    print("")

    parser = PDFParser()

    try:
        data = parser.extract_data(pdf_path)

        output_data = {
            'metadata': data.metadata,
            'full_text': data.full_text
        }

        if extraction_type in ["creatures", "all"]:
            creature_parser = CreatureParser()
            blocks_for_creatures = [
                {'title': block.title, 'content': block.content}
                for block in data.blocks
            ]
            creatures = creature_parser.extract_creatures(blocks_for_creatures)
            output_data['creatures'] = creatures
            print(f"Criaturas encontradas: {len(creatures)}")

        if extraction_type in ["rituals", "all"]:
            ritual_parser = RitualParser()
            blocks_for_rituals = [
                {'title': block.title, 'content': block.content}
                for block in data.blocks
            ]
            rituals = ritual_parser.extract_rituals(blocks_for_rituals)
            output_data['rituals'] = rituals
            print(f"Rituais encontrados: {len(rituals)}")

        pdf_name = Path(pdf_path).stem
        output_file = Path("output") / f"{pdf_name}_{extraction_type}.json"

        import json
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print("")
        print(f"Arquivo salvo em: {output_file}")

    except Exception as e:
        print(f"Erro ao processar PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
