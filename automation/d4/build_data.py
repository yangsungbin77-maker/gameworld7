"""조사 JSON(scratchpad/d4/*.json) → gameworld7/public/data/d4/<id>.json + meta.json"""
import json, re, sys, io, os
SRC = os.path.join(os.path.dirname(__file__), 'research')
OUT = r'C:\Users\use\gameworld7\public\data\d4'
os.makedirs(OUT, exist_ok=True)
WEAPONS = {'barbarian': ['양손 둔기', '양손 베기 무기', '쌍수 무기 (주)', '쌍수 무기 (보조)'], 'druid': ['주 무기', '보조 무기'], 'necromancer': ['주 무기', '보조 무기'],
           'rogue': ['근접 무기 1', '근접 무기 2', '원거리 무기'], 'sorcerer': ['주 무기', '보조 무기'], 'spiritborn': ['양손 무기'], 'paladin': ['주 무기', '보조 무기 · 방패'], 'warlock': ['주 무기', '보조 무기']}
MECH_MAX = {'barbarian': 1, 'druid': 5, 'necromancer': 3, 'rogue': 1, 'sorcerer': 2, 'spiritborn': 2, 'paladin': 1, 'warlock': 1}
ORDER = [('barbarian', '⚔️'), ('druid', '🐺'), ('necromancer', '💀'), ('rogue', '🗡️'), ('sorcerer', '🔥'), ('spiritborn', '🦅'), ('paladin', '🛡️'), ('warlock', '😈')]

def slug(s):
    s = re.sub(r"[’'`]", '', (s or '').lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def upslot(u):
    node = (u.get('node') or '').lower()
    if node == 'form': return 'form'
    if node == 'variant': return 'major'
    if node == 'side_upgrade': return 'minor1' if (u.get('pair') or 'A') == 'A' else 'minor2'
    v = str(u.get('slot') or u.get('branch') or '').lower()
    m = {'main': 'major', 'major': 'major', '3': 'major', 'side_1': 'minor1', 'minor1': 'minor1', '1': 'minor1', 'side_2': 'minor2', 'minor2': 'minor2', '2': 'minor2'}
    if v in m: return m[v]
    return None  # 없으면 아래에서 순서로 정한다

def clean(v):
    if v is None: return None
    v = str(v).strip()
    return v or None

def load(name):
    p = os.path.join(SRC, name + '.json')
    if not os.path.exists(p): return None
    with io.open(p, encoding='utf-8-sig') as f: return json.load(f)

report = []
classes = []
for cid, emoji in ORDER:
    d = load(cid)
    if not d:
        report.append(f'{cid}: 없음'); continue
    cats, seen = [], set()
    for c in d.get('categories', []):
        skills = []
        for s in c.get('skills', []):
            en = clean(s.get('en'))
            if not en: continue
            sid = slug(en)
            if sid in seen: sid = slug(c.get('en', '')) + '-' + sid
            seen.add(sid)
            t = (s.get('type') or 'active').lower().replace(' ', '_')
            if t not in ('active', 'passive', 'key_passive', 'ultimate'): t = 'passive' if 'passive' in t else 'active'
            mx = s.get('max_rank')
            try: mx = int(mx)
            except Exception: mx = 1 if t in ('key_passive',) else 5
            mx = max(1, min(mx, 15))
            ups, nenh = [], 0
            for u in (s.get('upgrades') or []):
                if not (clean(u.get('en')) or clean(u.get('ko'))): continue
                sl = upslot(u)
                if sl is None:  # 갈래 표시가 없으면: 보조(enhancement)는 앞 2개=①, 다음 2개=②, 변형(choice)=주 갈래
                    if 'enh' in (u.get('kind') or '').lower(): sl = 'minor1' if nenh < 2 else 'minor2'; nenh += 1
                    else: sl = 'major'
                ups.append({'ko': clean(u.get('ko')), 'en': clean(u.get('en')) or '', 'slot': sl})
            skills.append({'id': sid, 'ko': clean(s.get('ko')), 'en': en, 'type': t, 'max': mx, 'up': ups})
        if skills: cats.append({'ko': clean(c.get('ko')), 'en': clean(c.get('en')) or '', 'skills': skills})
    mech = d.get('mechanic') or None
    if mech:
        mech = {'ko': clean(mech.get('ko')), 'en': clean(mech.get('en')) or '', 'options': [{'ko': clean(o.get('ko')) or ((('한손 ' if (o.get('en') or '').startswith('One-Handed') else '') + o['weapon_ko']) if clean(o.get('weapon_ko')) else None), 'en': clean(o.get('en')) or clean(o.get('ko')) or '', 'desc_ko': clean(o.get('desc_ko')) or ''} for o in (mech.get('options') or []) if clean(o.get('en')) or clean(o.get('ko'))]}
    if mech: mech['max'] = MECH_MAX[cid]
    uniq = [{'ko': clean(u.get('ko')), 'en': clean(u.get('en')) or '', 'slot_ko': clean(u.get('slot_ko')) or ''} for u in d.get('uniques', []) if clean(u.get('en')) or clean(u.get('ko'))]
    weapons = WEAPONS[cid]
    out = {'id': cid, 'ko': clean(d.get('ko')) or cid, 'en': clean(d.get('en')) or cid, 'note': '기술마다 최대 15등급. 부가 업그레이드 두 줄에서 1개씩, 기술 변화형 3개 중 1개를 고릅니다' + (', 형상을 먼저 골라야 변화형이 열립니다' if cid == 'druid' else '') + '. 업그레이드 1개는 연결 노드 포함 2포인트입니다.', 'cats': cats, 'mech': mech, 'uniques': uniq, 'weapons': weapons}
    with io.open(os.path.join(OUT, cid + '.json'), 'w', encoding='utf-8') as f: json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    n = sum(len(c['skills']) for c in cats); nko = sum(1 for c in cats for s in c['skills'] if s['ko'])
    nup = sum(len(s['up']) for c in cats for s in c['skills']); nupko = sum(1 for c in cats for s in c['skills'] for u in s['up'] if u['ko'])
    report.append(f"{cid}: 스킬 {n}(한글 {nko}) 업그레이드 {nup}(한글 {nupko}) 고유능력 {len(mech['options']) if mech else 0} 고유템 {len(uniq)} 무기 {weapons}")
    classes.append({'id': cid, 'ko': out['ko'], 'emoji': emoji})

g = load('globals') or {}
gear = g.get('gear_slots_ko') or ['투구', '가슴 방어구', '장갑', '바지', '장화', '목걸이', '반지 1', '반지 2']
gear = [x for x in gear if not re.search(r'무기|weapon', x, re.I)]
meta = {'classes': classes, 'skill_points': g.get('skill_points') if isinstance(g.get('skill_points'), int) else 83,
        'gear': gear,
        'generic_uniques': [{'ko': clean(u.get('ko')), 'en': clean(u.get('en')) or ''} for u in (g.get('generic_uniques') or []) + (g.get('mythic_uniques') or []) if clean(u.get('en')) or clean(u.get('ko'))],
        'paragon_boards': (g.get('paragon') or {}).get('boards') if isinstance((g.get('paragon') or {}).get('boards'), int) else 5,
        'updated': '2026-10'}
with io.open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8') as f: json.dump(meta, f, ensure_ascii=False, separators=(',', ':'))
print('\n'.join(report)); print('meta:', {k: (v if k != 'generic_uniques' else len(v)) for k, v in meta.items() if k != 'classes'}, 'classes', len(classes))
