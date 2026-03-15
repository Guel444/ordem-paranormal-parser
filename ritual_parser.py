import re
from typing import List, Dict, Any, Optional


class RitualParser:
    RITUAL_KEYWORDS = [
        'Círculo', 'Execução', 'Alcance', 'Alvo', 'Duração',
        'Resistência', 'Efeito', 'Ritual', 'Conjuração'
    ]

    def extract_rituals(self, blocks: List) -> List[Dict[str, Any]]:
        rituals = []

        for block in blocks:
            title = block.get('title', '').strip()
            content = block.get('content', '').strip()

            if not title or not content:
                continue

            if self._is_ritual_block(title, content):
                ritual_data = self._parse_ritual_block(title, content)
                if ritual_data:
                    rituals.append(ritual_data)

        return rituals

    def _is_ritual_block(self, title: str, content: str) -> bool:
        if not title:
            return False

        title_lower = title.lower()

        excluded_titles = [
            'livro de regras', 'sumário', 'índice', 'registro de atualizações',
            'capítulo', 'prefácio', 'introdução', 'créditos', 'agradecimentos',
            'tabela', 'figura', 'anexo', 'criatura', 'monstro', 'entidade'
        ]

        for excluded in excluded_titles:
            if excluded in title_lower:
                return False

        ritual_indicators = any(keyword in content for keyword in self.RITUAL_KEYWORDS)

        return ritual_indicators

    def _parse_ritual_block(self, title: str, content: str) -> Optional[Dict[str, Any]]:
        ritual = {
            'name': title.strip(),
            'raw_content': content,
            'extracted_fields': {}
        }

        extracted = {}

        circulo_match = re.search(r'Círculo[:\s]+(\d+)', content, re.IGNORECASE)
        if circulo_match:
            extracted['circulo'] = int(circulo_match.group(1))
        else:
            return None

        execucao_match = re.search(r'Execução[:\s]+([^\n]+)', content, re.IGNORECASE)
        if execucao_match:
            extracted['execucao'] = execucao_match.group(1).strip()

        alcance_match = re.search(r'Alcance[:\s]+([^\n]+)', content, re.IGNORECASE)
        if alcance_match:
            extracted['alcance'] = alcance_match.group(1).strip()

        alvo_match = re.search(r'Alvo[:\s]+([^\n]+)', content, re.IGNORECASE)
        if alvo_match:
            extracted['alvo'] = alvo_match.group(1).strip()

        duracao_match = re.search(r'Duração[:\s]+([^\n]+)', content, re.IGNORECASE)
        if duracao_match:
            extracted['duracao'] = duracao_match.group(1).strip()

        resistencia_match = re.search(r'Resistência[:\s]+([^\n]+)', content, re.IGNORECASE)
        if resistencia_match:
            extracted['resistencia'] = resistencia_match.group(1).strip()

        efeito_match = re.search(r'Efeito[:\s]+([^\n]+)', content, re.IGNORECASE)
        if efeito_match:
            extracted['efeito'] = efeito_match.group(1).strip()

        ritual['extracted_fields'] = extracted

        return ritual
