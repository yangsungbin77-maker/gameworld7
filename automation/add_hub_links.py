#!/usr/bin/env python3
# 스위치 주제 묶음(허브+위성) 내부링크 블록을 관련 글마다 넣는다. 이미 있으면 갱신만.
# 왜: 스위치 글 5편이 서로 띄엄띄엄 링크돼 있어 구글이 "묶음"으로 못 봤다(2026-09-15 점검).
#     허브(스위치 게임 추천 2026, 구글 8.9위)를 중심으로 전부 상호 링크해 권위를 모은다.
# 사용: py automation/add_hub_links.py
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "src", "content", "blog")

HUB = "switch-game-recommendations-2026"
CLUSTER = [
    ("switch-game-recommendations-2026", "닌텐도 스위치 게임 추천 2026 (허브)"),
    ("switch2-game-recommendations", "스위치 2 게임 추천 — 독점작·에디션"),
    ("switch-rpg-game-recommendations", "스위치 RPG 게임 추천 12선"),
    ("switch-2player-games", "스위치 2인 게임 추천 12선"),
    ("switch-co-op-games", "스위치 협동(코옵) 게임 추천 12선"),
    ("console-game-recommendations", "콘솔 게임 추천 2026 — PS5·스위치 2·엑스박스"),
]
START = "<!-- hub:switch start -->"
END = "<!-- hub:switch end -->"


def block(current):
    items = []
    for slug, label in CLUSTER:
        if slug == current:
            continue
        items.append(f"<li><a href=\"/{slug}/\">{label}</a></li>")
    return (
        f"{START}\n"
        f"<div class=\"cg-box cg-tip\"><span class=\"cg-title\">🎮 닌텐도 스위치 가이드 모음</span>"
        f"<ul>{''.join(items)}</ul></div>\n"
        f"{END}"
    )


def apply(slug):
    path = os.path.join(BLOG, slug + ".md")
    src = io.open(path, encoding="utf-8").read()
    new_block = block(slug)
    if START in src and END in src:
        src2 = re.sub(re.escape(START) + r".*?" + re.escape(END), new_block, src, flags=re.S)
        state = "갱신"
    else:
        # 본문 끝 '관련 키워드' 구분선 바로 앞에 삽입
        marker = "\n---\n\n**관련 키워드**"
        if marker in src:
            src2 = src.replace(marker, "\n" + new_block + "\n" + marker, 1)
        else:
            src2 = src.rstrip("\n") + "\n\n" + new_block + "\n"
        state = "삽입"
    if src2 != src:
        io.open(path, "w", encoding="utf-8", newline="\n").write(src2)
    print(f"{state}: {slug}")


for slug, _ in CLUSTER:
    apply(slug)
