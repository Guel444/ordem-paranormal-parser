import json
from pathlib import Path
from PyPDF2 import PdfReader
from models import ExtractedData


class PDFParser:
    def __init__(self):
        self.text = ""

    def parse_pdf(self, file_path: str) -> str:
        pdf_path = Path(file_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        self.text = text
        return text

    def extract_data(self, file_path: str, extraction_type: str = "all") -> ExtractedData:
        self.parse_pdf(file_path)

        from creature_parser import CreatureParser
        from ritual_parser import RitualParser

        result = ExtractedData()

        if extraction_type in ["creatures", "all"]:
            parser = CreatureParser()
            result.creatures = parser.parse_creatures(self.text)

        if extraction_type in ["rituals", "all"]:
            parser = RitualParser()
            result.rituals = parser.parse_rituals(self.text)

        return result

    def save_to_json(self, data: ExtractedData, output_path: str) -> None:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data.model_dump(exclude_none=True), f, ensure_ascii=False, indent=2)
