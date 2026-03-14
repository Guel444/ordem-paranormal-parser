import { Creature } from '../types/creature';
import { TextProcessor } from '../utils/textProcessor';

export class CreatureParser {
  static parseCreatures(pdfText: string): Creature[] {
    const creatures: Creature[] = [];

    const sections = TextProcessor.extractSections(
      pdfText,
      /^[A-ZÀÁÃÂÉÊÍÓÔÕÚÇ\s]+$/m
    );

    for (const section of sections) {
      try {
        const creature = this.parseCreatureSection(section);
        if (creature && creature.name) {
          creatures.push(creature);
        }
      } catch (error) {
        console.error('Error parsing creature section:', error);
      }
    }

    return creatures;
  }

  private static parseCreatureSection(text: string): Creature | null {
    const lines = text.split('\n').filter(line => line.trim());

    if (lines.length === 0) return null;

    const creature: Creature = {
      name: lines[0].trim(),
      rawText: text
    };

    const fullText = lines.join(' ');

    const vdMatch = fullText.match(/VD[:\s]+(\d+)/i);
    if (vdMatch) {
      creature.vd = parseInt(vdMatch[1], 10);
    }

    const hpMatch = fullText.match(/PV[:\s]+(\d+d?\d*[\+\-]?\d*)/i);
    if (hpMatch) {
      creature.hp = hpMatch[1];
    }

    const categoryMatch = fullText.match(/Criatura[:\s]+([^.]+)/i);
    if (categoryMatch) {
      creature.category = categoryMatch[1].trim();
    }

    creature.attacks = this.extractAttacks(fullText);
    creature.abilities = this.extractAbilities(fullText);

    return creature;
  }

  private static extractAttacks(text: string): Array<{name: string; type?: string; damage?: string; description?: string}> {
    const attacks: Array<{name: string; type?: string; damage?: string; description?: string}> = [];

    const attackPatterns = [
      /(?:Ataque|Golpe|Investida)[:\s]+([^.]+)/gi,
      /(\d+d\d+[\+\-]?\d*)\s+(?:de\s+)?dano/gi
    ];

    for (const pattern of attackPatterns) {
      let match;
      while ((match = pattern.exec(text)) !== null) {
        if (match[1]) {
          attacks.push({
            name: match[1].trim(),
            description: match[0]
          });
        }
      }
    }

    return attacks.length > 0 ? attacks : undefined;
  }

  private static extractAbilities(text: string): Array<{name: string; description: string}> {
    const abilities: Array<{name: string; description: string}> = [];

    const abilityPattern = /(?:Habilidade|Trait|Poder)[:\s]+([^.]+)/gi;
    let match;

    while ((match = abilityPattern.exec(text)) !== null) {
      if (match[1]) {
        abilities.push({
          name: match[1].trim().split(':')[0],
          description: match[1].trim()
        });
      }
    }

    return abilities.length > 0 ? abilities : undefined;
  }
}
