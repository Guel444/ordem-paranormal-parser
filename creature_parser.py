import re
from typing import List, Dict, Any, Optional


class CreatureParser:
    CREATURE_KEYWORDS = [
        'VD', 'PV', 'PE', 'Defesa', 'Ataque', 'Dano',
        'Resistência', 'Imunidade', 'Vulnerabilidade',
        'Habilidade', 'Perícia', 'Tamanho', 'Deslocamento'
    ]

    def extract_creatures(self, blocks: List) -> List[Dict[str, Any]]:
        creatures = []

        for block in blocks:
            title = block.get('title', '').strip()
            content = block.get('content', '').strip()

            if not title or not content:
                continue

            if self._is_creature_block(title, content):
                creature_data = self._parse_creature_block(title, content)
                if creature_data:
                    creatures.append(creature_data)

        return creatures

    def _is_creature_block(self, title: str, content: str) -> bool:
        if not title:
            return False

        title_lower = title.lower()

        excluded_titles = [
            'livro de regras', 'sumário', 'índice', 'registro de atualizações',
            'capítulo', 'prefácio', 'introdução', 'créditos', 'agradecimentos',
            'tabela', 'figura', 'anexo'
        ]

        for excluded in excluded_titles:
            if excluded in title_lower:
                return False

        creature_indicators = any(keyword in content for keyword in self.CREATURE_KEYWORDS)

        return creature_indicators

    def _parse_creature_block(self, title: str, content: str) -> Optional[Dict[str, Any]]:
        creature = {
            'name': title.strip(),
            'raw_content': content,
            'extracted_fields': {}
        }

        extracted = {}

        vd_match = re.search(r'VD[:\s]+(\d+)', content, re.IGNORECASE)
        if vd_match:
            extracted['vd'] = int(vd_match.group(1))

        pv_match = re.search(r'PV[:\s]+([0-9d\+\-\s]+)', content, re.IGNORECASE)
        if pv_match:
            extracted['pv'] = pv_match.group(1).strip()

        pe_match = re.search(r'PE[:\s]+(\d+)', content, re.IGNORECASE)
        if pe_match:
            extracted['pe'] = int(pe_match.group(1))

        defesa_match = re.search(r'Defesa[:\s]+(\d+)', content, re.IGNORECASE)
        if defesa_match:
            extracted['defesa'] = int(defesa_match.group(1))

        tamanho_match = re.search(r'Tamanho[:\s]+([^\n]+)', content, re.IGNORECASE)
        if tamanho_match:
            extracted['tamanho'] = tamanho_match.group(1).strip()

        deslocamento_match = re.search(r'Deslocamento[:\s]+([^\n]+)', content, re.IGNORECASE)
        if deslocamento_match:
            extracted['deslocamento'] = deslocamento_match.group(1).strip()

        resistencias = re.findall(r'Resistência[:\s]+([^\n]+)', content, re.IGNORECASE)
        if resistencias:
            extracted['resistencias'] = [r.strip() for r in resistencias]

        imunidades = re.findall(r'Imunidade[:\s]+([^\n]+)', content, re.IGNORECASE)
        if imunidades:
            extracted['imunidades'] = [i.strip() for i in imunidades]

        vulnerabilidades = re.findall(r'Vulnerabilidade[:\s]+([^\n]+)', content, re.IGNORECASE)
        if vulnerabilidades:
            extracted['vulnerabilidades'] = [v.strip() for v in vulnerabilidades]

        creature['extracted_fields'] = extracted

        return creature
