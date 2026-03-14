import re
from typing import List, Optional
from models import Ritual


class RitualParser:
    def parse_rituals(self, text: str) -> List[Ritual]:
        rituals = []
        lines = text.split("\n")

        ritual_start_indices = []
        for i, line in enumerate(lines):
            if self._is_ritual_title(line):
                ritual_start_indices.append(i)

        for idx, start in enumerate(ritual_start_indices):
            end = ritual_start_indices[idx + 1] if idx + 1 < len(ritual_start_indices) else len(lines)
            section = "\n".join(lines[start:end])

            ritual = self._parse_ritual_section(section)
            if ritual:
                rituals.append(ritual)

        return rituals

    def _is_ritual_title(self, line: str) -> bool:
        line = line.strip()
        if not line:
            return False

        if re.match(r"^[A-ZÀÁÃÂÉÊÍÓÔÕÚÇ\s\-']+$", line):
            return len(line) > 3 and len(line) < 100

        return False

    def _parse_ritual_section(self, text: str) -> Optional[Ritual]:
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if not lines:
            return None

        full_text = " ".join(lines)

        circle_match = re.search(r"(?:Círculo|Circle)[:\s]+(\d+)", full_text, re.IGNORECASE)
        if not circle_match:
            return None

        ritual = Ritual(
            name=lines[0],
            circle=int(circle_match.group(1)),
            execution="",
            range="",
            target="",
            duration="",
            description="",
            raw_text=text
        )

        execution_match = re.search(r"(?:Execução|Execution)[:\s]+([^.]+)", full_text, re.IGNORECASE)
        if execution_match:
            ritual.execution = execution_match.group(1).strip()

        range_match = re.search(r"(?:Alcance|Range)[:\s]+([^.]+)", full_text, re.IGNORECASE)
        if range_match:
            ritual.range = range_match.group(1).strip()

        target_match = re.search(r"(?:Alvo|Target)[:\s]+([^.]+)", full_text, re.IGNORECASE)
        if target_match:
            ritual.target = target_match.group(1).strip()

        duration_match = re.search(r"(?:Duração|Duration)[:\s]+([^.]+)", full_text, re.IGNORECASE)
        if duration_match:
            ritual.duration = duration_match.group(1).strip()

        resistance_match = re.search(r"(?:Resistência|Resistance)[:\s]+([^.]+)", full_text, re.IGNORECASE)
        if resistance_match:
            ritual.resistance = resistance_match.group(1).strip()

        desc_lines = lines[1:]
        ritual.description = " ".join(desc_lines).strip()

        return ritual
