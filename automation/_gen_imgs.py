# -*- coding: utf-8 -*-
"""콘솔 게임 추천 글 이미지 2장 fal.ai(flux-pro)로 생성 → webp 저장."""
import os, sys, urllib.request
sys.path.insert(0, r"C:/Users/use/클로드 코드/TheLastDay-troy")
import fal_lib
from PIL import Image
import io

OUT = r"C:/Users/use/gameworld7/src/assets/posts"
os.makedirs(OUT, exist_ok=True)

JOBS = [
    ("console-game-recommendations.webp",
     "Cinematic photorealistic modern living room gaming setup at dusk, a large 4K TV glowing on a wooden media console, three next-gen home game consoles with their controllers arranged neatly below it, cozy ambient lighting with a subtle dark neon green accent glow, shallow depth of field, premium tech magazine cover look, no text, no words, no letters, no logos"),
    ("console-game-recommendations-platforms.webp",
     "Cinematic studio product photography, three modern home game consoles standing side by side with their gamepad controllers on a matte dark surface, dramatic rim lighting with a subtle dark neon green accent, clean comparison layout, high detail, photorealistic, no text, no words, no letters, no logos"),
]

for fname, prompt in JOBS:
    r = fal_lib.run("fal-ai/flux-pro/v1.1",
                    {"prompt": prompt, "image_size": "landscape_16_9", "num_images": 1,
                     "safety_tolerance": "5"},
                    poll=3, maxwait=180)
    url = r["images"][0]["url"]
    raw = urllib.request.urlopen(url, timeout=120).read()
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    path = os.path.join(OUT, fname)
    img.save(path, "WEBP", quality=88, method=6)
    print("saved", path, img.size)
