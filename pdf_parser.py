import json
import re
from pathlib import Path
from PyPDF2 import PdfReader
from models import ExtractedData, ContentBlock


class PDFParser:
    def __init__(self):
        self.text = ""
        self.pages = []

    def parse_pdf(self, file_path: str) -> tuple[str, list]:
        pdf_path = Path(file_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        reader = PdfReader(file_path)
        full_text = ""
        pages = []

        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            pages.append({
                'page': page_num,
                'text': text
            })
            full_text += f"\n--- PAGE {page_num} ---\n{text}\n"

        self.text = full_text
        self.pages = pages
        return full_text, pages

    def split_into_blocks(self, text: str) -> List[ContentBlock]:
        blocks = []

        lines = text.split('\n')
        current_title = None
        current_content = []

        for line in lines:
            stripped = line.strip()

            if self._is_section_title(stripped):
                if current_content:
                    blocks.append(ContentBlock(
                        title=current_title,
                        content='\n'.join(current_content).strip()
                    ))
                current_title = stripped
                current_content = []
            else:
                if stripped or current_content:
                    current_content.append(line)

        if current_content:
            blocks.append(ContentBlock(
                title=current_title,
                content='\n'.join(current_content).strip()
            ))

        return blocks

    def _is_section_title(self, line: str) -> bool:
        if not line or len(line) < 3 or len(line) > 150:
            return False

        word_count = len(line.split())
        if word_count > 15:
            return False

        if re.match(r'^--- PAGE \d+ ---$', line):
            return False

        uppercase_ratio = sum(1 for c in line if c.isupper()) / len(line)

        return uppercase_ratio > 0.6

    def extract_data(self, file_path: str) -> ExtractedData:
        text, pages = self.parse_pdf(file_path)

        blocks = self.split_into_blocks(text)

        result = ExtractedData(
            full_text=text,
            blocks=blocks,
            metadata={
                'total_pages': len(pages),
                'total_blocks': len(blocks),
                'pdf_file': Path(file_path).name
            }
        )

        return result

    def save_to_json(self, data: ExtractedData, output_path: str) -> None:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data.model_dump(), f, ensure_ascii=False, indent=2)
