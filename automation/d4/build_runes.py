"""research/runes.json → src/data/d4-runes.json(페이지용) + public/data/d4/runewords.json(플래너용: 이름 → 룬 조합)

실행: py automation/d4/build_runes.py
"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
src = json.load(io.open(os.path.join(HERE, 'research', 'runes.json'), encoding='utf-8-sig'))
CLASSES = {'all', 'barbarian', 'druid', 'necromancer', 'rogue', 'sorcerer', 'spiritborn', 'paladin', 'warlock'}


def clean(v):
    if v is None:
        return None
    v = str(v).strip()
    return v or None


runes = []
for r in src.get('runes') or []:
    if not (clean(r.get('en')) or clean(r.get('ko'))):
        continue
    runes.append({'en': clean(r.get('en')) or clean(r.get('ko')), 'ko': clean(r.get('ko')), 'tier': clean(r.get('tier')) if not isinstance(r.get('tier'), (int, float)) else str(r.get('tier')),
                  'order': r.get('order') if isinstance(r.get('order'), (int, float)) else None,
                  'effect_ko': clean(r.get('effect_ko')), 'drop_ko': clean(r.get('drop_ko')), 'upgrade_ko': clean(r.get('upgrade_ko'))})
runes.sort(key=lambda r: (r['order'] is None, r['order'] or 0))
TIER_NOTE = None
for r in runes:  # 표에 맞게 짧게: 등급 설명·[의식/기원] 머리말·반복 문구 정리
    t = r['tier'] or ''
    if t.startswith('시즌 15 신규'):
        TIER_NOTE = TIER_NOTE or t
        r['tier'] = '시즌 15 신규'
    m = re.match(r'\[(의식의 룬|기원의 룬)\]\s*', r['effect_ko'] or '')
    r['kind'] = m.group(1) if m else None
    if m:
        r['effect_ko'] = r['effect_ko'][m.end():]
    if r['drop_ko']:
        r['drop_ko'] = re.sub(r'^(시즌 15 신규 룬|증오의 그릇부터 있던 기존 룬)\.\s*', '', r['drop_ko'])
known = {r['en'].lower() for r in runes}

items, seen = [], set()
for it in src.get('items') or []:
    en = clean(it.get('en'))
    if not en:
        continue
    iid = re.sub(r'[^a-z0-9]+', '-', (clean(it.get('id')) or en).lower()).strip('-')
    if iid in seen:
        continue
    seen.add(iid)
    rr = [{'en': clean(x.get('en')) or clean(x.get('ko')), 'ko': clean(x.get('ko'))} for x in (it.get('runes') or []) if clean(x.get('en')) or clean(x.get('ko'))]
    unsure = None
    if it.get('confirmed') is False:
        unsure = clean(it.get('note_ko')) or '자료마다 내용이 달라 확인 중'
    raw = it.get('class') or 'all'
    cl = [c.lower() for c in (raw if isinstance(raw, list) else [raw]) if isinstance(c, str) and c.lower() in CLASSES]
    cls = 'all' if (not cl or 'all' in cl) else ','.join(cl)
    items.append({'id': iid, 'en': en, 'ko': clean(it.get('ko')), 'kind_ko': clean(it.get('kind_ko')), 'runes': rr,
                  'bases_ko': [b for b in (clean(x) for x in (it.get('bases_ko') or [])) if b],
                  'sockets': it.get('sockets') if isinstance(it.get('sockets'), int) else None,
                  'level_req': it.get('level_req') if isinstance(it.get('level_req'), int) else None,
                  'class': cls, 'stats_ko': [s for s in (clean(x) for x in (it.get('stats_ko') or [])) if s],
                  'seasonal': bool(it.get('seasonal')), 'unsure': unsure})
    for x in rr:
        if x['en'].lower() not in known:
            print('  ⚠ 룬 목록에 없는 룬:', x['en'], '←', en)

page = {'updated': src.get('updated') or '2026-10', 'season': src.get('season') or 15, 'patch': src.get('patch') or '',
        'how_ko': [h for h in (clean(x) for x in (src.get('how_ko') or [])) if h], 'rules_ko': [h for h in (clean(x) for x in (src.get('rules_ko') or [])) if h] + ([f'룬 등급: {TIER_NOTE}'] if TIER_NOTE else []),
        'runes': runes, 'items': items,
        'materials': [{'en': clean(m.get('en')) or '', 'ko': clean(m.get('ko')), 'how_ko': clean(m.get('how_ko')) or ''} for m in (src.get('materials') or []) if clean(m.get('en')) or clean(m.get('ko'))]}
os.makedirs(os.path.join(ROOT, 'src', 'data'), exist_ok=True)
io.open(os.path.join(ROOT, 'src', 'data', 'd4-runes.json'), 'w', encoding='utf-8').write(json.dumps(page, ensure_ascii=False, indent=1))

planner = {}
for it in items:
    recipe = ' + '.join(x['ko'] or x['en'] for x in it['runes'])
    for name in {it['ko'], it['en']} - {None, ''}:
        planner[name] = recipe
io.open(os.path.join(ROOT, 'public', 'data', 'd4', 'runewords.json'), 'w', encoding='utf-8').write(json.dumps(planner, ensure_ascii=False, separators=(',', ':')))
print(f"룬 {len(runes)} · 아이템 {len(items)} · 확인 중 {sum(1 for i in items if i['unsure'])} · 옵션 없는 아이템 {sum(1 for i in items if not i['stats_ko'])}")
