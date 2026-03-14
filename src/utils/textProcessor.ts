export class TextProcessor {
  static cleanText(text: string): string {
    return text
      .replace(/\s+/g, ' ')
      .replace(/\n+/g, '\n')
      .trim();
  }

  static extractSections(text: string, startPattern: RegExp, endPattern?: RegExp): string[] {
    const sections: string[] = [];
    const lines = text.split('\n');
    let currentSection: string[] = [];
    let inSection = false;

    for (const line of lines) {
      if (startPattern.test(line)) {
        if (currentSection.length > 0) {
          sections.push(currentSection.join('\n'));
        }
        currentSection = [line];
        inSection = true;
      } else if (endPattern && endPattern.test(line) && inSection) {
        currentSection.push(line);
        sections.push(currentSection.join('\n'));
        currentSection = [];
        inSection = false;
      } else if (inSection) {
        currentSection.push(line);
      }
    }

    if (currentSection.length > 0) {
      sections.push(currentSection.join('\n'));
    }

    return sections;
  }

  static extractValue(text: string, pattern: RegExp): string | null {
    const match = text.match(pattern);
    return match ? match[1].trim() : null;
  }

  static extractNumber(text: string, pattern: RegExp): number | undefined {
    const value = this.extractValue(text, pattern);
    return value ? parseInt(value, 10) : undefined;
  }
}
