# 게임 부스터 설정 글 전용 이미지 2장(히어로·본문 인포그래픽)을 PIL로 그린다. 외부 크레딧 0.
# 사용: py automation/_gen_booster_imgs.py
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "assets", "posts")
FONT = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_R = r"C:\Windows\Fonts\malgun.ttf"
BG, BG2, ACC, TXT, MUTE = (11, 14, 20), (20, 25, 34), (62, 245, 139), (236, 240, 244), (150, 160, 175)


def f(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_R, size)


def glow_bg(w, h):
    img = Image.new("RGB", (w, h), BG)
    glow = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(glow)
    d.ellipse((w * 0.55, -h * 0.4, w * 1.3, h * 0.7), fill=(20, 70, 45))
    d.ellipse((-w * 0.3, h * 0.5, w * 0.35, h * 1.4), fill=(16, 40, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.blend(img, glow, 0.9)
    # 격자 라인
    d = ImageDraw.Draw(img)
    for x in range(0, w, 80):
        d.line((x, 0, x, h), fill=(255, 255, 255, 6), width=1)
    for y in range(0, h, 80):
        d.line((0, y, w, y), fill=(255, 255, 255, 6), width=1)
    return img


def phone(d, x, y, w, h):
    d.rounded_rectangle((x, y, x + w, y + h), radius=44, fill=(28, 34, 46), outline=(70, 80, 96), width=4)
    d.rounded_rectangle((x + 14, y + 14, x + w - 14, y + h - 14), radius=34, fill=(14, 18, 26))
    d.rounded_rectangle((x + w // 2 - 40, y + 26, x + w // 2 + 40, y + 38), radius=6, fill=(50, 56, 70))
    # 화면 안 게이지 4개
    gx, gy = x + 46, y + 120
    for i, (label, pct) in enumerate([("성능", 0.85), ("FPS", 0.65), ("해상도", 0.5), ("부스터", 0.9)]):
        yy = gy + i * 92
        d.text((gx, yy), label, font=f(26), fill=MUTE)
        d.rounded_rectangle((gx, yy + 40, x + w - 46, yy + 56), radius=8, fill=(40, 46, 60))
        d.rounded_rectangle((gx, yy + 40, gx + int((w - 92) * pct), yy + 56), radius=8, fill=ACC)


def hero():
    w, h = 1600, 900
    img = glow_bg(w, h)
    d = ImageDraw.Draw(img)
    phone(d, 1080, 110, 360, 700)
    d.text((110, 200), "갤럭시", font=f(56), fill=ACC)
    d.text((110, 270), "게임 부스터 설정", font=f(112), fill=TXT)
    d.text((110, 420), "성능 · FPS · 해상도 · 프레임 부스터", font=f(46), fill=MUTE)
    d.text((110, 490), "뭘 골라야 안 끊기고 안 뜨거울까", font=f(46), fill=MUTE)
    d.rounded_rectangle((110, 600, 560, 664), radius=32, fill=(24, 60, 42), outline=ACC, width=2)
    d.text((140, 612), "One UI 7 · 8.5 기준 총정리", font=f(30), fill=ACC)
    img.save(os.path.join(OUT, "galaxy-game-booster-settings.webp"), "WEBP", quality=88)


def infographic():
    w, h = 1600, 1000
    img = glow_bg(w, h)
    d = ImageDraw.Draw(img)
    d.text((80, 60), "게임 부스터 개별 게임 맞춤 설정 4가지 — 뭘 고르면 되나", font=f(50), fill=TXT)
    d.text((80, 130), "위로 갈수록 프레임↑ 발열·배터리↑  |  아래로 갈수록 발열↓ 배터리↑", font=f(28, False), fill=MUTE)
    cards = [
        ("① 게임 성능 수준", "성능 / 표준 / 배터리 절약", "고사양 게임·충전 중 → 성능\n외출·발열 심할 때 → 표준"),
        ("② FPS(초당 프레임)", "기기 주사율 범위에서 단계 선택", "액션·슈팅 → 최대\n캐주얼·수집형 → 60이면 충분"),
        ("③ 화면 해상도", "100%보다 한 단계 낮추기", "커뮤니티 권장 75% 안팎\n프레임 안정·발열 완화"),
        ("④ 프레임 부스터", "켜기 → 체감 안 되면 끄기", "게임마다 효과 다름\n끊김·잔상 느껴지면 끄기"),
    ]
    cw, ch, gap = 700, 330, 40
    for i, (t, v, note) in enumerate(cards):
        x = 80 + (i % 2) * (cw + gap)
        y = 200 + (i // 2) * (ch + gap)
        d.rounded_rectangle((x, y, x + cw, y + ch), radius=24, fill=BG2, outline=(50, 60, 76), width=2)
        d.rounded_rectangle((x, y, x + 10, y + ch), radius=5, fill=ACC)
        d.text((x + 36, y + 28), t, font=f(38), fill=ACC)
        d.text((x + 36, y + 90), v, font=f(30), fill=TXT)
        d.multiline_text((x + 36, y + 150), note, font=f(28, False), fill=MUTE, spacing=14)
    d.text((80, 940), "정리: 게임월드7 · 삼성전자서비스 공식 안내(One UI 7)와 커뮤니티 실측 정리를 대조", font=f(22, False), fill=(110, 120, 135))
    img.save(os.path.join(OUT, "galaxy-game-booster-settings-4items.webp"), "WEBP", quality=88)


hero()
infographic()
print("saved:", os.listdir(OUT).count("galaxy-game-booster-settings.webp"), os.listdir(OUT).count("galaxy-game-booster-settings-4items.webp"))
