import { Ritual } from '../types/creature';
import { TextProcessor } from '../utils/textProcessor';

export class RitualParser {
  static parseRituals(pdfText: string): Ritual[] {
    const rituals: Ritual[] = [];

    const sections = TextProcessor.extractSections(
      pdfText,
      /^[A-ZÀÁÃÂÉÊÍÓÔÕÚÇ\s]+$/m
    );

    for (const section of sections) {
      try {
        const ritual = this.parseRitualSection(section);
        if (ritual && ritual.name) {
          rituals.push(ritual);
        }
      } catch (error) {
        console.error('Error parsing ritual section:', error);
      }
    }

    return rituals;
  }

  private static parseRitualSection(text: string): Ritual | null {
    const lines = text.split('\n').filter(line => line.trim());

    if (lines.length === 0) return null;

    const fullText = lines.join(' ');

    const circleMatch = fullText.match(/(?:Círculo|Circle)[:\s]+(\d+)/i);
    if (!circleMatch) return null;

    const ritual: Ritual = {
      name: lines[0].trim(),
      circle: parseInt(circleMatch[1], 10),
      execution: '',
      range: '',
      target: '',
      duration: '',
      description: '',
      rawText: text
    };

    const executionMatch = fullText.match(/(?:Execução|Execution)[:\s]+([^.]+)/i);
    if (executionMatch) {
      ritual.execution = executionMatch[1].trim();
    }

    const rangeMatch = fullText.match(/(?:Alcance|Range)[:\s]+([^.]+)/i);
    if (rangeMatch) {
      ritual.range = rangeMatch[1].trim();
    }

    const targetMatch = fullText.match(/(?:Alvo|Target)[:\s]+([^.]+)/i);
    if (targetMatch) {
      ritual.target = targetMatch[1].trim();
    }

    const durationMatch = fullText.match(/(?:Duração|Duration)[:\s]+([^.]+)/i);
    if (durationMatch) {
      ritual.duration = durationMatch[1].trim();
    }

    const resistanceMatch = fullText.match(/(?:Resistência|Resistance)[:\s]+([^.]+)/i);
    if (resistanceMatch) {
      ritual.resistance = resistanceMatch[1].trim();
    }

    const descLines = lines.slice(1);
    ritual.description = descLines.join(' ').trim();

    return ritual;
  }
}
