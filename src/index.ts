import * as path from 'path';
import { PDFParser } from './parsers/pdfParser';

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Uso: ts-node src/index.ts <caminho-do-pdf> [tipo]');
    console.log('');
    console.log('Argumentos:');
    console.log('  <caminho-do-pdf>  Caminho para o arquivo PDF');
    console.log('  [tipo]            Tipo de extração: creatures, rituals, ou all (padrão: all)');
    console.log('');
    console.log('Exemplos:');
    console.log('  ts-node src/index.ts livro-regras.pdf');
    console.log('  ts-node src/index.ts livro-regras.pdf creatures');
    console.log('  ts-node src/index.ts livro-regras.pdf rituals');
    process.exit(1);
  }

  const pdfPath = args[0];
  const extractionType = (args[1] || 'all') as 'creatures' | 'rituals' | 'all';

  if (!['creatures', 'rituals', 'all'].includes(extractionType)) {
    console.error('Tipo inválido. Use: creatures, rituals, ou all');
    process.exit(1);
  }

  console.log(`Processando: ${pdfPath}`);
  console.log(`Tipo de extração: ${extractionType}`);
  console.log('');

  const parser = new PDFParser();

  try {
    const data = await parser.extractData(pdfPath, extractionType);

    const outputFileName = `${path.basename(pdfPath, '.pdf')}_${extractionType}.json`;
    const outputPath = path.join('output', outputFileName);

    await parser.saveToJSON(data, outputPath);

    console.log('Extração concluída!');
    console.log('');
    console.log('Resultados:');
    if (data.creatures) {
      console.log(`  - ${data.creatures.length} criaturas extraídas`);
    }
    if (data.rituals) {
      console.log(`  - ${data.rituals.length} rituais extraídos`);
    }
    console.log('');
    console.log(`Arquivo salvo em: ${outputPath}`);
  } catch (error) {
    console.error('Erro ao processar PDF:', error);
    process.exit(1);
  }
}

main();
