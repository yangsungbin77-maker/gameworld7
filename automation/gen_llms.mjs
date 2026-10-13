// llms.txt 자동 생성기 — 글 폴더(src/content/blog)를 읽어 public/llms.txt를 다시 쓴다.
// 왜: 손으로 관리하던 llms.txt가 글 24편 중 12편만 담고 제목도 옛것이었다(2026-09-15 점검).
//     AI 검색(ChatGPT·Perplexity 등)이 사이트를 훑을 때 보는 목차라, 발행 때마다 코드로 갱신한다.
// 사용: node automation/gen_llms.mjs   (finalize.mjs가 빌드 전에 자동 호출)
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const blogDir = join(root, 'src', 'content', 'blog');
const SITE = 'https://gameworld7.com';
const EXCLUDE = new Set(['welcome']); // 인사글은 목차에서 제외

function frontmatter(md) {
  const m = md.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const out = {};
  if (!m) return out;
  for (const line of m[1].split(/\r?\n/)) {
    const i = line.indexOf(':');
    if (i === -1) continue;
    const k = line.slice(0, i).trim();
    let v = line.slice(i + 1).trim();
    if ((v.startsWith("'") && v.endsWith("'")) || (v.startsWith('"') && v.endsWith('"'))) v = v.slice(1, -1);
    out[k] = v;
  }
  return out;
}

const posts = readdirSync(blogDir)
  .filter((f) => f.endsWith('.md') || f.endsWith('.mdx'))
  .map((f) => {
    const slug = f.replace(/\.mdx?$/, '');
    const fm = frontmatter(readFileSync(join(blogDir, f), 'utf8'));
    return { slug, title: fm.title || slug, description: fm.description || '', pubDate: new Date(fm.pubDate || 0), updatedDate: fm.updatedDate ? new Date(fm.updatedDate) : null };
  })
  .filter((p) => !EXCLUDE.has(p.slug))
  .sort((a, b) => (b.updatedDate || b.pubDate) - (a.updatedDate || a.pubDate));

// 주제 묶음(허브) — 같은 주제 글을 한 덩어리로 보여주면 AI가 "이 사이트는 이 주제 전문"으로 읽는다.
const CLUSTERS = [
  { name: '닌텐도 스위치 가이드', match: /^switch|^console-game/ },
  { name: '스팀·PC 게임', match: /^steam|^game-performance|^game-frame|^nvidia|^fps-settings|^retro-pc/ },
  { name: '모바일 게임', match: /^mobile/ },
  { name: '게임 추천·장르', match: /^rpg|^co-op|^game-genre|^apple-game/ },
  { name: '게임 상식·용어·기획', match: /^game-terms|^game-nickname|^game-design/ },
];

const fmtDate = (d) => d.toISOString().slice(0, 10);
const line = (p) => `- [${p.title}](${SITE}/${p.slug}/): ${p.description}${p.updatedDate ? ` (수정 ${fmtDate(p.updatedDate)})` : ''}`;

let out = `# 게임월드7

> 게임월드7은 게임 뉴스·공략·리뷰를 한국어로 정리하는 게임 블로그입니다. 닌텐도 스위치·스위치 2, 스팀·PC, 모바일 게임의 추천·설정·구매 가이드를 다루며, 운영자가 직접 자료를 찾아 확인한 내용만 씁니다. 가격·발매일처럼 잘 바뀌는 정보는 기준 시점을 본문에 밝힙니다.

## Key pages
- [홈](${SITE}/)
- [블로그 전체 목록](${SITE}/blog/)
- [운영자 소개 (Sungbin)](${SITE}/author/)
- [소개](${SITE}/about/)
- [문의](${SITE}/contact/)

## 게임 도구
- [디아블로4 빌드 플래너](${SITE}/d4-build-planner/): 디아블로4 시즌 15(증오의 군주 이후) 8개 직업 기술 트리를 한국어 공식 명칭으로 찍어 보는 무료 플래너. 기술 15등급·부가 업그레이드·기술 변화형·형상(드루이드), 기술 포인트 83 한도, 단축키 6칸, 장비·정복자 문양 메모, 링크 공유와 텍스트 복사를 지원합니다. 서버 저장 없이 브라우저에서 동작합니다.
- [디아블로4 보스 드랍 테이블](${SITE}/d4-boss-drops/): 디아블로4 시즌 15(패치 3.2.x) 소굴 우두머리 등 보스 14종의 고유 아이템 드랍 목록 260건과 상징적 신화 13종의 출처를 한국어 공식 명칭으로 정리한 표. 아이템 이름 검색·직업 거르기, 비축고 열쇠와 우두머리 전리품, 가이드끼리 출처가 다른 아이템은 '확인 중'으로 표시합니다.
- [디아블로4 룬워드 제작서](${SITE}/d4-runewords/): 디아블로4 시즌 15(패치 3.2.x) 호라드림의 함으로 만드는 룬워드 19종의 룬 조합·일반(흰색) 바탕 아이템·레벨·옵션과 룬 16종의 효과·드랍처·합성 사다리를 한국어 공식 명칭으로 정리. 가진 룬을 고르면 지금 제작 가능한 룬워드를 표시합니다.
- [라스트에폭 빌드별 중요 옵션](${SITE}/last-epoch-build-affixes/): 라스트에폭 시즌 5(패치 1.5.x) 빌드 27개(15개 마스터리 전부)의 장비 옵션 우선순위를 레벨링·엔드게임·최종 세팅 단계별로 정리. 직업→마스터리→빌드→단계를 고르면 꼭 챙길 옵션, 방어 목표, 우상 옵션, 핵심 고유템, 승격 목표를 보여 줍니다. 옵션 이름은 라스트 에포크 툴즈 한국어(게임 공식 번역) 기준, 맥스롤 빌드 가이드·플래너 기반.
- [라스트에폭 축복 정리·빌드별 추천](${SITE}/last-epoch-blessings/): 라스트에폭 시즌 5(1.5.2) 모노리스 시간선(타임라인) 10곳의 축복 112종(일반·상급 수치, 공식 한국어), 얻는 법·바꾸는(교체) 법·상급 축복 규칙, 빌드 27개의 추천 축복 5칸(맥스롤 플래너 엔드게임 기준). 빌드를 고르면 어느 시간선 보스에서 무엇을 골라야 하는지 표시합니다.
`;

const used = new Set();
for (const c of CLUSTERS) {
  const items = posts.filter((p) => c.match.test(p.slug));
  if (!items.length) continue;
  out += `\n## ${c.name}\n`;
  for (const p of items) { out += line(p) + '\n'; used.add(p.slug); }
}
const rest = posts.filter((p) => !used.has(p.slug));
if (rest.length) {
  out += `\n## 기타 글\n`;
  for (const p of rest) out += line(p) + '\n';
}
out += `\n## Optional\n- [RSS](${SITE}/rss.xml)\n- [사이트맵](${SITE}/sitemap-index.xml)\n`;

writeFileSync(join(root, 'public', 'llms.txt'), out);
console.log(`✔ llms.txt 갱신 — 글 ${posts.length}편, 묶음 ${CLUSTERS.length}개`);
