import sys
from pathlib import Path
from pdf_parser import PDFParser


def main():
    args = sys.argv[1:]

    if not args:
        print("Uso: python main.py <caminho-do-pdf> [tipo]")
        print("")
        print("Argumentos:")
        print("  <caminho-do-pdf>  Caminho para o arquivo PDF")
        print("  [tipo]            Tipo de extração: creatures, rituals, ou all (padrão: all)")
        print("")
        print("Exemplos:")
        print("  python main.py livro-regras.pdf")
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
        data = parser.extract_data(pdf_path, extraction_type)

        pdf_name = Path(pdf_path).stem
        output_file = Path("output") / f"{pdf_name}_{extraction_type}.json"

        parser.save_to_json(data, str(output_file))

        print("Extração concluída!")
        print("")
        print("Resultados:")

        if data.creatures:
            print(f"  - {len(data.creatures)} criatura(s) extraída(s)")

        if data.rituals:
            print(f"  - {len(data.rituals)} ritual(is) extraído(s)")

        print("")
        print(f"Arquivo salvo em: {output_file}")

    except Exception as e:
        print(f"Erro ao processar PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
