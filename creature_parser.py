import re
from typing import List, Optional
from models import Creature, Attack, Ability


class CreatureParser:
    def parse_creatures(self, text: str) -> List[Creature]:
        creatures = []
        lines = text.split("\n")

        creature_start_indices = []
        for i, line in enumerate(lines):
            if self._is_creature_title(line):
                creature_start_indices.append(i)

        for idx, start in enumerate(creature_start_indices):
            end = creature_start_indices[idx + 1] if idx + 1 < len(creature_start_indices) else len(lines)
            section = "\n".join(lines[start:end])

            creature = self._parse_creature_section(section)
            if creature and creature.name:
                creatures.append(creature)

        return creatures

    def _is_creature_title(self, line: str) -> bool:
        line = line.strip()
        if not line:
            return False

        if re.match(r"^[A-ZÀÁÃÂÉÊÍÓÔÕÚÇ\s\-]+$", line):
            return len(line) > 3 and len(line) < 100

        return False

    def _parse_creature_section(self, text: str) -> Optional[Creature]:
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if not lines:
            return None

        creature = Creature(
            name=lines[0],
            raw_text=text
        )

        full_text = " ".join(lines)

        vd_match = re.search(r"VD[:\s]+(\d+)", full_text, re.IGNORECASE)
        if vd_match:
            creature.vd = int(vd_match.group(1))

        hp_match = re.search(r"PV[:\s]+(\d+d?\d*[\+\-]?\d*)", full_text, re.IGNORECASE)
        if hp_match:
            creature.hp = hp_match.group(1)

        category_match = re.search(r"Criatura[:\s]+([^.]+)", full_text, re.IGNORECASE)
        if category_match:
            creature.category = category_match.group(1).strip()

        creature.attacks = self._extract_attacks(full_text)
        creature.abilities = self._extract_abilities(full_text)

        return creature

    def _extract_attacks(self, text: str) -> Optional[List[Attack]]:
        attacks = []

        attack_patterns = [
            r"(?:Ataque|Golpe|Investida)[:\s]+([^.]+)",
            r"(\d+d\d+[\+\-]?\d*)\s+(?:de\s+)?dano"
        ]

        for pattern in attack_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.group(1):
                    attacks.append(Attack(
                        name=match.group(1).strip(),
                        description=match.group(0)
                    ))

        return attacks if attacks else None

    def _extract_abilities(self, text: str) -> Optional[List[Ability]]:
        abilities = []

        ability_pattern = r"(?:Habilidade|Trait|Poder)[:\s]+([^.]+)"
        matches = re.finditer(ability_pattern, text, re.IGNORECASE)

        for match in matches:
            if match.group(1):
                name_desc = match.group(1).strip()
                name = name_desc.split(":")[0] if ":" in name_desc else name_desc

                abilities.append(Ability(
                    name=name,
                    description=name_desc
                ))

        return abilities if abilities else None
