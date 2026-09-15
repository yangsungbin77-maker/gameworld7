// 발행 후 "밖에 뿌릴 글" 자동 생성 — Threads·X·핀터레스트용 짧은 소개문을 automation/share/<slug>.md 에 쓴다.
// 왜: 구글은 밖에서 링크가 들어오는 글을 먼저 읽는다. 우리는 발행만 하고 뿌리지 않아 색인·유입이 0이었다(2026-09-15).
//     계정 API 연결 전까지는 이 파일을 열어 복사·붙여넣기로 올린다. 나중에 토큰이 생기면 여기서 바로 게시하도록 확장.
// 사용: node automation/share_text.mjs <slug>
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const slug = process.argv[2];
if (!slug) { console.error('사용법: node automation/share_text.mjs <slug>'); process.exit(2); }
const md = readFileSync(join(root, 'src', 'content', 'blog', `${slug}.md`), 'utf8');
const fm = Object.fromEntries([...md.matchAll(/^(\w+):\s*'?(.*?)'?\s*$/gm)].map((m) => [m[1], m[2]]));
const url = `https://gameworld7.com/${slug}/`;
const title = fm.title || slug;
const desc = fm.description || '';

// 본문에서 "숫자가 들어간 문장" 2개를 훅으로 뽑는다(사람들은 구체 숫자에 멈춘다).
const body = md.replace(/^---[\s\S]*?---/, '').replace(/<[^>]+>/g, ' ').replace(/[#*_>|`]/g, ' ');
const sents = body.split(/(?<=[.!?다요죠])\s+/).map((s) => s.trim()).filter((s) => s.length > 20 && s.length < 110);
const hooks = sents.filter((s) => /\d/.test(s)).slice(0, 2);
const tags = (md.match(/#[^\s#]+/g) || []).slice(0, 5).join(' ');

const out = `# 공유용 문구 — ${title}
URL: ${url}

## Threads / X (짧게, 훅 1개 + 링크)
${hooks[0] || desc}
👉 ${url}
${tags}

## Threads / X (질문형)
${title.split(' — ')[0]}, 뭐부터 봐야 할지 막막하셨죠?
${hooks[1] || desc}
정리해 뒀어요 → ${url}

## 핀터레스트 (제목 + 설명)
제목: ${title.slice(0, 90)}
설명: ${desc}
링크: ${url}

## 네이버 카페·커뮤니티 (답글용 한 줄)
${desc} 자세한 건 여기 정리해 뒀습니다. ${url}
`;
const dir = join(__dirname, 'share');
if (!existsSync(dir)) mkdirSync(dir);
writeFileSync(join(dir, `${slug}.md`), out);
console.log(`✔ 공유 문구 생성 → automation/share/${slug}.md`);
