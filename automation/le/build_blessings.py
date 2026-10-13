"""research/blessings.json + builds_*.json(빌드별 축복) → src/data/le-blessings.json

실행: py automation/le/build_blessings.py   (build_le.py 다음에 실행 — 빌드 목록을 le-builds.json에서 읽음)
"""
import io, json, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
src = json.load(io.open(os.path.join(HERE, 'research', 'blessings.json'), encoding='utf-8-sig'))
builds = json.load(io.open(os.path.join(ROOT, 'src', 'data', 'le-builds.json'), encoding='utf-8'))['builds']


def clean(v):
    if v is None:
        return None
    v = str(v).strip()
    return v or None


def fix(t):
    """공식 번역문에 남은 자리표시자({0})와 겹친 공백 정리"""
    t = re.sub(r'\s*\{\d+\}', '', clean(t) or '')
    return re.sub(r'\s{2,}', ' ', t).strip()


def base(en):
    """'Grand Survival of Might' → 'survival of might'"""
    return re.sub(r'[^a-z0-9]+', ' ', re.sub(r'^grand\s+', '', (en or '').strip(), flags=re.I).lower()).strip()


timelines, by_name = [], {}
for t in src.get('timelines') or []:
    tid = re.sub(r'[^a-z0-9]+', '-', (clean(t.get('id')) or t.get('en') or '').lower()).strip('-')
    bl = []
    for b in t.get('blessings') or []:
        en = clean(b.get('en'))
        if not en:
            continue
        item = {'id': re.sub(r'[^a-z0-9]+', '-', base(en)).strip('-'), 'en': en, 'ko': clean(b.get('ko')), 'grand_ko': clean(b.get('grand_ko')),
                'stat': fix(b.get('stat_ko')), 'stat_grand': fix(b.get('stat_grand_ko')), 'cat': clean(b.get('cat')) or '기타', 'tl': tid, 'builds': []}
        bl.append(item)
        by_name[base(en)] = item
    timelines.append({'id': tid, 'en': clean(t.get('en')) or tid, 'ko': clean(t.get('ko')), 'boss_en': clean(t.get('boss_en')), 'boss_ko': clean(t.get('boss_ko')),
                      'level': t.get('level') if isinstance(t.get('level'), (int, float)) else None, 'blessings': bl})

# 빌드별 추천: 앞서 조사한 builds_*.json의 blessings + blessings.json의 build_blessings
picks = {}
for f in glob.glob(os.path.join(HERE, 'research', 'builds_*.json')):
    for b in json.load(io.open(f, encoding='utf-8-sig')).get('builds') or []:
        if b.get('blessings'):
            picks[re.sub(r'[^a-z0-9]+', '-', (b.get('id') or '').lower()).strip('-')] = b['blessings']
for k, v in (src.get('build_blessings') or {}).items():
    if v:
        picks.setdefault(k, v)

unmatched = []
out_builds = []
for b in builds:
    raw = picks.get(b['id']) or []
    plist = []
    for p in raw:
        en = clean(p.get('en')) or ''
        hit = by_name.get(base(en))
        if not hit:
            unmatched.append(f"{b['id']}: {en}")
        else:
            if b['id'] not in hit['builds']:
                hit['builds'].append(b['id'])
        plist.append({'ref': hit['id'] if hit else None, 'en': en, 'ko': clean(p.get('ko')), 'grand': en.lower().startswith('grand'), 'note': clean(p.get('note_ko'))})
    out_builds.append({'id': b['id'], 'en': b['en'], 'ko': b['ko'], 'cls': b['cls'], 'mastery': b['mastery'], 'picks': plist})

out = {'updated': src.get('updated') or '2026-10', 'season': src.get('season') or 5, 'patch': src.get('patch') or '1.5.x',
       'rules': [r for r in (clean(x) for x in (src.get('rules_ko') or [])) if r and 'JSON' not in r and 'pool' not in r], 'timelines': timelines, 'builds': out_builds}
io.open(os.path.join(ROOT, 'src', 'data', 'le-blessings.json'), 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
nb = sum(len(t['blessings']) for t in timelines)
print(f"타임라인 {len(timelines)} · 축복 {nb} · 한글 없음 {sum(1 for t in timelines for x in t['blessings'] if not x['ko'])} · 추천 있는 빌드 {sum(1 for b in out_builds if b['picks'])}/{len(out_builds)}")
if unmatched:
    print('  ⚠ 목록에서 못 찾은 추천 축복:', unmatched[:12])
