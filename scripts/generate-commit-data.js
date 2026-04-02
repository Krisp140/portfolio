import { execSync } from 'child_process';
import { writeFileSync } from 'fs';

const extMap = {
  '.svelte': 'Svelte', '.js': 'JavaScript', '.ts': 'TypeScript',
  '.css': 'CSS', '.html': 'HTML', '.json': 'JSON', '.py': 'Python',
  '.yml': 'YAML', '.yaml': 'YAML', '.md': 'Markdown', '.csv': 'CSV',
};

const log = execSync('git log --pretty=format:"COMMIT:%H,%aI" --numstat', { encoding: 'utf-8' });

const rows = [];
let commit = null;
let date = null;

for (const line of log.split('\n')) {
  if (line.startsWith('COMMIT:')) {
    const parts = line.slice(7).split(',', 2);
    commit = parts[0].slice(0, 7);
    date = parts[1];
  } else if (line.trim() && commit) {
    const [added, removed, file] = line.split('\t');
    if (added === '-' || removed === '-') continue;
    const ext = '.' + file.split('.').pop();
    const lang = extMap[ext] || 'Other';
    const total = Number(added) + Number(removed);
    if (total > 0) {
      rows.push(`${commit},${date},${file},${lang},${total}`);
    }
  }
}

writeFileSync('static/commit_data.csv', 'commit,date,file,language,lines\n' + rows.join('\n') + '\n');
console.log(`Generated static/commit_data.csv (${rows.length} rows)`);
