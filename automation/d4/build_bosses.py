"""research/bosses.json → src/data/d4-bosses.json(페이지용) + public/data/d4/drops.json(플래너용: 아이템 → 보스)

실행: py automation/d4/build_bosses.py
- 한글 이름이 비어 있으면 플래너 데이터(public/data/d4/*.json)의 고유템 한·영 짝으로 채운다.
- 보스·아이템 id가 겹치면 하나로 합친다.
"""
import io, json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(HERE, 'research', 'bosses.json')
OUT_PAGE = os.path.join(ROOT, 'src', 'data', 'd4-bosses.json')
OUT_DROPS = os.path.join(ROOT, 'public', 'data', 'd4', 'drops.json')
CLASSES = {'all', 'barbarian', 'druid', 'necromancer', 'rogue', 'sorcerer', 'spiritborn', 'paladin', 'warlock'}


def clean(v):
    if v is None:
        return None
    v = str(v).strip()
    return v or None


def key(s):
    return re.sub(r"[^a-z0-9]+", '', (s or '').lower().replace('’', "'"))


# 플래너 데이터에서 영문 → 한글 고유템 이름 사전
EN2KO = {}
for p in glob.glob(os.path.join(ROOT, 'public', 'data', 'd4', '*.json')):
    if os.path.basename(p) in ('drops.json',):
        continue
    d = json.load(io.open(p, encoding='utf-8'))
    for u in (d.get('uniques') or []) + (d.get('generic_uniques') or []):
        if u.get('en') and u.get('ko'):
            EN2KO.setdefault(key(u['en']), u['ko'])

src = json.load(io.open(SRC, encoding='utf-8-sig'))


def norm_cls(c):
    c = (c or 'all').lower().strip()
    return c if c in CLASSES else 'all'


def item(d):
    en = clean(d.get('en')) or ''
    ko = clean(d.get('ko')) or EN2KO.get(key(en))
    out = {'en': en, 'ko': ko, 'slot_ko': clean(d.get('slot_ko')) or '', 'class': norm_cls(d.get('class')), 'mythic': bool(d.get('mythic'))}
    if d.get('confirmed') is False:
        out['unsure'] = clean(d.get('note_ko')) or '가이드마다 출처가 달라 확인 중'
    if d.get('equip_classes'):
        out['equip'] = [c for c in d['equip_classes'] if c in CLASSES]
    return out


GROUP = {'grigoire': 'initiate', 'beast_in_the_ice': 'initiate', 'varshan': 'initiate', 'lord_zir': 'initiate', 'urivar': 'initiate',
         'duriel': 'greater', 'andariel': 'greater', 'harbinger_of_hatred': 'greater', 'butcher': 'greater',
         'belial': 'top', 'mephisto': 'top', 'astaroth': 'other', 'bartuc': 'other', 'prime_evils_s15': 'season'}


bosses, seen = [], set()
filled = missing = 0
for b in src.get('bosses', []):
    bid = re.sub(r'[^a-z0-9-]+', '-', (b.get('id') or b.get('en') or '').lower()).strip('-')
    if not bid or bid in seen:
        continue
    seen.add(bid)
    drops, dk = [], set()
    for d in b.get('drops') or []:
        it = item(d)
        if not it['en'] and not it['ko']:
            continue
        k = key(it['en']) or it['ko']
        if k in dk:
            continue
        dk.add(k)
        if not clean(d.get('ko')) and it['ko']:
            filled += 1
        if not it['ko']:
            missing += 1
        drops.append(it)
    # 정렬: 신화 → 공용 → 직업 순, 같은 그룹은 한글 이름순
    order = ['all', 'barbarian', 'druid', 'necromancer', 'rogue', 'sorcerer', 'spiritborn', 'paladin', 'warlock']
    drops.sort(key=lambda x: (not x['mythic'], order.index(x['class']), x['ko'] or x['en']))
    m = b.get('material') or {}
    t = b.get('trophy') or {}
    bosses.append({
        'id': bid, 'en': clean(b.get('en')) or bid, 'ko': clean(b.get('ko')),
        'location_ko': clean(b.get('location_ko')) or '',
        'material': {'en': clean(m.get('en')), 'ko': clean(m.get('ko')), 'per_summon': m.get('per_summon') if isinstance(m.get('per_summon'), int) else None, 'how_ko': clean(m.get('how_ko')) or ''} if m else None,
        'trophy': {'ko': clean(t.get('ko')), 'en': clean(t.get('en'))} if (t and (t.get('ko') or t.get('en'))) else None,
        'group': GROUP.get(bid.replace('-', '_'), 'season' if b.get('seasonal') else 'other'),
        'tiers_ko': clean(b.get('tiers_ko')) or '', 'seasonal': bool(b.get('seasonal')), 'drops': drops,
    })

mythics, extra_rules = [], []
for m in src.get('mythics') or []:
    if not clean(m.get('ko')) and not clean(m.get('slot_ko')):  # 아이템이 아니라 설명 줄 → 규칙으로
        if clean(m.get('from_ko')): extra_rules.append(m['from_ko'].strip())
        continue
    it = item(m)
    it['from_ko'] = clean(m.get('from_ko')) or ''
    mythics.append(it)
# 대부분 같은 설명이면 표 위에 한 번만 쓰고, 칸에는 짧게
from collections import Counter
common = Counter(m['from_ko'] for m in mythics).most_common(1)
mythic_note = common[0][0] if common and common[0][1] >= 3 else ''
for m in mythics:
    if mythic_note and m['from_ko'] == mythic_note:
        m['from_ko'] = '고행 무작위 드랍 · 대장장이 보관함'

page = {'updated': src.get('updated') or '2026-10', 'season': src.get('season') or 15, 'patch': src.get('patch') or '', 'rules_ko': [r for r in (src.get('rules_ko') or []) if clean(r)] + extra_rules, 'bosses': bosses, 'mythics': mythics, 'mythic_note_ko': mythic_note}
os.makedirs(os.path.dirname(OUT_PAGE), exist_ok=True)
io.open(OUT_PAGE, 'w', encoding='utf-8').write(json.dumps(page, ensure_ascii=False, indent=1))

# 플래너용: 아이템 이름(한글·영문) → 보스 한글 이름 목록
drops = {}
for b in bosses:
    for d in b['drops']:
        for name in {d['ko'], d['en']} - {None, ''}:
            drops.setdefault(name, [])
            bn = b['ko'] or b['en']
            if bn not in drops[name]:
                drops[name].append(bn)
for m in mythics:
    for name in {m['ko'], m['en']} - {None, ''}:
        drops.setdefault(name, [])
        if m['from_ko'] and m['from_ko'] not in drops[name]:
            drops[name].append(m['from_ko'])
io.open(OUT_DROPS, 'w', encoding='utf-8').write(json.dumps(drops, ensure_ascii=False, separators=(',', ':')))

print(f"보스 {len(bosses)} · 드랍 {sum(len(b['drops']) for b in bosses)} · 신화 {len(mythics)} · 한글 보충 {filled} · 한글 없음 {missing}")
for b in bosses:
    print(f"  {b['ko'] or b['en']}: {len(b['drops'])}개 · 재료 {(b['material'] or {}).get('ko')}")
