# -*- coding: utf-8 -*-
"""추억의 PC방 고전게임 글 이미지 2장 fal flux-pro → webp. 상표·실제 게임화면 없음."""
import os, sys, urllib.request, io
sys.path.insert(0, r"C:/Users/use/클로드 코드/TheLastDay-troy")
import fal_lib
from PIL import Image

OUT = r"C:/Users/use/gameworld7/src/assets/posts"
os.makedirs(OUT, exist_ok=True)

JOBS = [
    ("retro-pc-cafe-games.webp",
     "Cinematic nostalgic photo of an early-2000s Korean internet cafe (PC bang) at night, long rows of old CRT and early flat monitors glowing blue and green in the dark, empty gaming chairs, atmospheric haze, warm retro nostalgia mood, no text, no words, no letters, no logos, no game screenshots"),
    ("retro-pc-cafe-games-genres.webp",
     "Retro pixel-art style collage background evoking 2000s online gaming, abstract arcade shapes, joystick and keyboard silhouettes, race-car and fantasy-sword and bomb icons in flat pixel art, nostalgic neon color blocks, no text, no words, no letters, no logos, no real game characters"),
]

for fname, prompt in JOBS:
    r = fal_lib.run("fal-ai/flux-pro/v1.1",
                    {"prompt": prompt, "image_size": "landscape_16_9", "num_images": 1,
                     "safety_tolerance": "5"}, poll=3, maxwait=180)
    raw = urllib.request.urlopen(r["images"][0]["url"], timeout=120).read()
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    p = os.path.join(OUT, fname)
    img.save(p, "WEBP", quality=88, method=6)
    print("saved", p, img.size)
