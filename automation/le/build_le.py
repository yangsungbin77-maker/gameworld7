"""research/builds_*.json → src/data/le-builds.json

실행: py automation/le/build_le.py
- 빌드 3개 파일을 합치고, 옵션 한글 이름이 비어 있으면 builds_3.json의 affix_ko 사전으로 채운다.
- 티어(파밍·보스·엔드게임)는 사이트 글(last-epoch-season5-build-tier)과 같은 맥스롤 10/9 갱신본 기준으로 붙인다.
"""
import io, json, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

CLASSES = [
    ('primalist', '원시술사', [('beastmaster', '야수 조련사'), ('shaman', '주술사'), ('druid', '드루이드')]),
    ('mage', '마법사', [('sorcerer', '원소술사'), ('spellblade', '주문검사'), ('runemaster', '룬 마스터')]),
    ('sentinel', '파수꾼', [('voidknight', '공허기사'), ('forgeguard', '대장간지기'), ('paladin', '성기사')]),
    ('acolyte', '수행사제', [('necromancer', '강령술사'), ('lich', '리치'), ('warlock', '워록')]),
    ('rogue', '도적', [('bladedancer', '검무가'), ('marksman', '명사수'), ('falconer', '매사냥꾼')]),
]
# 맥스롤 시즌5 티어표(2026-10-09 갱신) — 파밍/보스/엔드게임. 사이트 티어 글과 같은 값.
TIERS = {
    'flay mana lich': 'SSS', 'rip blood lich': 'SSS', 'stygian coal lich': 'SSS', 'shield throw time rot void knight': 'SSS',
    'erasing strike void knight': 'SSS', 'ballista (zhp) falconer': 'SSS', 'ballista falconer': 'SSS', 'shadow cascade bladedancer': 'SSS',
    'static orb sorcerer': 'SSS', 'flame reave spellblade': 'SSS',
    'tornado shaman': 'SAS', 'warpath void knight': 'SAS', 'harvest flay lich': 'SAA', 'bladestorm bladedancer': 'SAA',
    'shadow rend bladedancer': 'SAA', 'shuriken marksman': 'SAA',
    'blood spectre necromancer': 'BSS', 'skeleton necromancer': 'BSS', 'storm crows beastmaster': 'BSS', 'shatter strike spellblade': 'BSA',
    'profane veil warlock': 'BSB', 'lightning blast runemaster': 'ASS', 'rive void knight': 'ASA', 'radiant lance paladin': 'AAA',
    'shatter totem werebear druid': 'AAA', 'multistrike forge guard': 'B-B',
}


def clean(v):
    if v is None:
        return None
    v = str(v).strip()
    return v or None


def key(s):
    return re.sub(r'[^a-z0-9]+', ' ', (s or '').lower()).strip()


files = sorted(glob.glob(os.path.join(HERE, 'research', 'builds_*.json')))
raw = [json.load(io.open(f, encoding='utf-8-sig')) for f in files]
AFFIX_KO = {}
common = []
for r in raw:
    for k, v in (r.get('affix_ko') or {}).items():
        if clean(v):
            AFFIX_KO[key(k)] = clean(v)
    common += [c for c in (r.get('common_ko') or []) if clean(c)]

masteries = {m: (c, mk) for c, _, ms in CLASSES for m, mk in ms}
filled = missing = 0


def affix(a):
    global filled, missing
    en = clean(a.get('en')) or ''
    ko = clean(a.get('ko'))
    if not ko:
        ko = AFFIX_KO.get(key(en)) or AFFIX_KO.get(key(re.sub(r'^\+?%?\s*(increased\s+)?', '', en, flags=re.I)))
        if ko:
            filled += 1
    if not ko:
        missing += 1
    cat = clean(a.get('cat')) or '유틸'
    if cat not in ('공격', '방어', '유틸'):
        cat = '유틸'
    try:
        prio = max(1, min(3, int(a.get('prio') or 2)))
    except Exception:
        prio = 2
    return {'en': en, 'ko': ko, 'cat': cat, 'prio': prio, 'slots': [s for s in (clean(x) for x in (a.get('slots_ko') or [])) if s]}


def stage(s):
    if not s or not (s.get('affixes') or []):
        return None
    items = [affix(a) for a in s['affixes'] if clean(a.get('en')) or clean(a.get('ko'))]
    items.sort(key=lambda x: x['prio'])
    return {'affixes': items, 'notes': clean(s.get('notes_ko')) or ''}


builds, seen = [], set()
for r in raw:
    for b in r.get('builds') or []:
        m = (b.get('mastery') or '').lower().replace(' ', '').replace('_', '')
        if m not in masteries:
            print('  ⚠ 알 수 없는 마스터리:', b.get('mastery'), b.get('en'))
            continue
        bid = re.sub(r'[^a-z0-9]+', '-', (clean(b.get('id')) or b.get('en') or '').lower()).strip('-')
        if bid in seen:
            continue
        seen.add(bid)
        st = b.get('stages') or {}
        t = {key(k): v for k, v in TIERS.items()}.get(key(b.get('en')))
        builds.append({
            'id': bid, 'en': clean(b.get('en')) or bid, 'ko': clean(b.get('ko')), 'cls': masteries[m][0], 'mastery': m,
            'skills': [{'en': clean(s.get('en')) or '', 'ko': clean(s.get('ko'))} for s in (b.get('skills') or []) if clean(s.get('en'))],
            'damage': clean(b.get('damage_ko')) or '',
            'tier': {'farm': t[0], 'boss': t[1], 'end': t[2]} if t else None,
            'stages': {k: stage(st.get(k)) for k in ('leveling', 'endgame', 'high_corruption')},
            'defense': [d for d in (clean(x) for x in (b.get('defense_ko') or [])) if d],
            'idols': [{'en': clean(i.get('en')) or '', 'ko': clean(i.get('ko')) or AFFIX_KO.get(key(i.get('en')))} for i in (b.get('idols') or []) if clean(i.get('en')) or clean(i.get('ko'))],
            'uniques': [{'en': clean(u.get('en')) or '', 'ko': clean(u.get('ko')), 'slot': clean(u.get('slot_ko')) or '', 'core': (u.get('role') or '') == 'build-enabling'} for u in (b.get('uniques') or []) if clean(u.get('en'))],
            'exalted': [e for e in (clean(x) for x in (b.get('exalted_ko') or [])) if e],
            'sources': [s for s in (b.get('sources') or []) if isinstance(s, str) and s.startswith('http')][:4],
            'updated': clean(b.get('guide_updated')) or '',
            'note': clean(b.get('confidence_ko')) or '',
            'low': '낮음' in (b.get('confidence_ko') or ''),
        })

order = {m: i for i, (m, _) in enumerate([(m, 0) for _, _, ms in CLASSES for m, _ in ms])}
builds.sort(key=lambda b: (order[b['mastery']], ''.join((b['tier'] or {'f': 'Z'}).values())))

out = {'updated': '2026-10', 'season': 5, 'patch': (raw[0].get('patch') if raw else '1.5.x'),
       'classes': [{'id': c, 'ko': ck, 'masteries': [{'id': m, 'ko': mk} for m, mk in ms]} for c, ck, ms in CLASSES],
       'common': common, 'builds': builds}
os.makedirs(os.path.join(ROOT, 'src', 'data'), exist_ok=True)
io.open(os.path.join(ROOT, 'src', 'data', 'le-builds.json'), 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
print(f"파일 {len(files)} · 빌드 {len(builds)} · 옵션 한글 보충 {filled} · 한글 없음 {missing}")
for b in builds:
    s = b['stages']
    print(f"  {b['mastery']:12} {b['en']:36} 티어 {''.join((b['tier'] or {}).values()) or '-':4} 레벨링 {len((s['leveling'] or {}).get('affixes', []))} 엔드 {len((s['endgame'] or {}).get('affixes', []))} 고부패 {'O' if s['high_corruption'] else '-'}")
