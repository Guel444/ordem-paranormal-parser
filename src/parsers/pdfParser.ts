import * as fs from 'fs';
import * as pdfParse from 'pdf-parse';
import { ExtractedData } from '../types/creature';
import { CreatureParser } from './creatureParser';
import { RitualParser } from './ritualParser';

export class PDFParser {
  async parsePDF(filePath: string): Promise<string> {
    const dataBuffer = fs.readFileSync(filePath);
    const data = await pdfParse(dataBuffer);
    return data.text;
  }

  async extractData(filePath: string, type: 'creatures' | 'rituals' | 'all' = 'all'): Promise<ExtractedData> {
    const pdfText = await this.parsePDF(filePath);
    const result: ExtractedData = {};

    if (type === 'creatures' || type === 'all') {
      result.creatures = CreatureParser.parseCreatures(pdfText);
    }

    if (type === 'rituals' || type === 'all') {
      result.rituals = RitualParser.parseRituals(pdfText);
    }

    return result;
  }

  async saveToJSON(data: ExtractedData, outputPath: string): Promise<void> {
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), 'utf-8');
  }
}
