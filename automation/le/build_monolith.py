"""research/monolith.json (+ le-blessings.json) → src/data/le-monolith.json

실행: py automation/le/build_monolith.py   (build_blessings.py 다음)
- 시간선마다 축복 페이지의 같은 시간선 id(bless_tl)를 붙여, 진행 체크표에서 빌드별 추천 축복을 보여 줄 수 있게 한다.
"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
src = json.load(io.open(os.path.join(HERE, 'research', 'monolith.json'), encoding='utf-8-sig'))
bless = json.load(io.open(os.path.join(ROOT, 'src', 'data', 'le-blessings.json'), encoding='utf-8'))


def clean(v):
    if v is None:
        return None
    v = str(v).strip()
    return v or None


def norm(s):
    return re.sub(r'[^a-z0-9가-힣]+', '', (s or '').lower())


def strs(x):
    return [s for s in (clean(v) for v in (x or [])) if s]


btl = {}
for t in bless['timelines']:
    for k in (t['id'], t['en'], t['ko']):
        if k:
            btl[norm(k)] = t['id']

tls = []
for t in src.get('timelines') or []:
    tid = re.sub(r'[^a-z0-9]+', '-', (clean(t.get('id')) or t.get('en') or '').lower()).strip('-')
    bt = btl.get(norm(t.get('id'))) or btl.get(norm(t.get('en'))) or btl.get(norm(t.get('ko')))
    tls.append({'id': tid, 'en': clean(t.get('en')) or tid, 'ko': clean(t.get('ko')), 'level': t.get('level') if isinstance(t.get('level'), (int, float)) else None,
                'boss_en': clean(t.get('boss_en')), 'boss_ko': clean(t.get('boss_ko')), 'requires': [re.sub(r'[^a-z0-9]+', '-', r.lower()).strip('-') for r in (t.get('requires') or []) if isinstance(r, str)],
                'stat': (t.get('blessing_type') or '') == 'stat', 'notes': clean(t.get('notes_ko')) or '',
                'know': (2 if '지식 2개' in (t.get('notes_ko') or '') else 1) if (t.get('level') or 0) < 90 else 0, 'gate': 5 if (t.get('level') or 0) >= 90 else 0, 'drops': strs(t.get('drops_ko')), 'bless_tl': bt})
tls.sort(key=lambda t: (t['level'] or 999, t['en']))

c = src.get('corruption') or {}
out = {
    'updated': src.get('updated') or '2026-10', 'season': src.get('season') or 5, 'patch': src.get('patch') or '1.5.x',
    'terms': [{'en': clean(x.get('en')) or '', 'ko': clean(x.get('ko')), 'community': clean(x.get('community_ko'))} for x in (src.get('terms') or []) if clean(x.get('en'))],
    'unlock': strs(src.get('unlock_ko')), 'loop': strs(src.get('loop_ko')), 'empowered': strs(src.get('empowered_ko')),
    'timelines': tls,
    'corruption': {'increase': strs(c.get('increase_ko')), 'effects': strs(c.get('effects_ko')), 'defense': strs(c.get('defense_ko')),
                   'milestones': [{'at': m.get('at'), 'ko': clean(m.get('ko')) or ''} for m in (c.get('milestones') or []) if clean(m.get('ko'))]},
    'encounters': [{'id': re.sub(r'[^a-z0-9]+', '-', (clean(e.get('id')) or e.get('en') or '').lower()).strip('-'), 'en': clean(e.get('en')) or '', 'ko': clean(e.get('ko')),
                    'unlock': clean(e.get('unlock_ko')) or '', 'why': clean(e.get('why_ko')) or '', 'drops': strs(e.get('drops_ko'))} for e in (src.get('encounters') or []) if clean(e.get('en'))],
    'alts': strs(src.get('alts_ko')), 'season5': strs(src.get('season5_ko')),
    'roadmap': [{'step': clean(r.get('step')) or '', 'ko': clean(r.get('ko')) or '', 'level': clean(r.get('level')) if not isinstance(r.get('level'), (int, float)) else str(r.get('level')), 'check': clean(r.get('check_ko')) or ''} for r in (src.get('roadmap') or []) if clean(r.get('ko'))],
    'sources': [s for s in (src.get('sources') or []) if isinstance(s, str) and s.startswith('http')][:10],
}
io.open(os.path.join(ROOT, 'src', 'data', 'le-monolith.json'), 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
print(f"시간선 {len(tls)} (축복 연결 {sum(1 for t in tls if t['bless_tl'])}) · 조우 {len(out['encounters'])} · 로드맵 {len(out['roadmap'])} · 타락 단계 {len(out['corruption']['milestones'])}")
for t in tls:
    print(f"  {t['level']} {t['ko'] or t['en']} ← {t['requires']} 보스 {t['boss_ko']} 축복연결 {t['bless_tl']}")
