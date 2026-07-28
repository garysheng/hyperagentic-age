#!/usr/bin/env -S uv run --with pillow --script
"""
Blueprint plate for the setting `the-room` (book: the-room-it-was-made-in).

DETERMINISTIC GRAPHICS RENDER IN CODE, NOT AN IMAGE MODEL (global non-negotiable).
This fixes the room's geometry so `wide` and `night` stay the same place: window wall,
desk-cluster positions, whiteboard and shelf locations, and the camera's fixed spot at
the near end. It argues nothing, which is what makes it safe to pass alongside a state.

Output: blueprint.png (1536x1024)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1536, 1024
PAPER = (243, 240, 232)
INK = (38, 42, 50)
FAINT = (150, 155, 165)
WARM = (176, 139, 62)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(size, bold=False):
    for p in ("/System/Library/Fonts/Supplemental/Courier New Bold.ttf" if bold
              else "/System/Library/Fonts/Supplemental/Courier New.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


F_TITLE, F_HEAD, F_BODY, F_DIM = font(30, True), font(19, True), font(15), font(13)

d.rectangle([28, 28, W - 28, H - 28], outline=INK, width=2)
d.line([(28, 92), (W - 28, 92)], fill=INK, width=2)
d.text((48, 60), "THE ROOM", font=F_TITLE, fill=INK, anchor="lm")
d.text((W - 48, 52), "setting / geometry seed plate", font=F_BODY, fill=INK, anchor="rm")
d.text((W - 48, 74), "book: the-room-it-was-made-in   universe: hyperagentic-age",
       font=F_DIM, fill=FAINT, anchor="rm")

# ---------------------------------------------------------------- plan
d.text((48, 122), "PLAN  (camera fixed at the near end, looking down the length)",
       font=F_HEAD, fill=INK, anchor="lm")

L, R_, T, B = 150, 1180, 190, 690          # room walls
d.rectangle([L, T, R_, B], outline=INK, width=3)

# window wall (top), drawn as a broken line with mullions
for x in range(L + 60, R_ - 60, 96):
    d.line([(x, T), (x + 66, T)], fill=PAPER, width=7)
    d.line([(x, T - 5), (x, T + 5)], fill=INK, width=2)
    d.line([(x + 66, T - 5), (x + 66, T + 5)], fill=INK, width=2)
d.text((L + 40, T - 26), "WINDOW WALL  (daylight in `wide`; dark + reflecting in `night`)",
       font=F_DIM, fill=FAINT, anchor="lm")

# desk clusters: irregular, deliberately not a grid
clusters = [(250, 300, 190, 90), (500, 270, 210, 95), (800, 305, 175, 88),
            (300, 500, 200, 92), (620, 520, 195, 85), (900, 480, 185, 95)]
for i, (x, y, w, h) in enumerate(clusters, 1):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.line([(x + w // 2, y), (x + w // 2, y + h)], fill=FAINT, width=1)
    d.text((x + w // 2, y + h // 2), f"C{i}", font=F_DIM, fill=FAINT, anchor="mm")
d.text((250, 660), "desk clusters are IRREGULAR and mismatched, never a grid",
       font=F_DIM, fill=FAINT, anchor="lm")

# whiteboard + shelf + taped printouts on the far/right walls
d.line([(R_, 250), (R_, 380)], fill=INK, width=8)
d.text((R_ - 14, 315), "WHITEBOARD", font=F_DIM, fill=INK, anchor="rm")
d.line([(R_, 430), (R_, 540)], fill=INK, width=8)
d.text((R_ - 14, 485), "BOOK SHELF", font=F_DIM, fill=INK, anchor="rm")
d.line([(L, 300), (L, 470)], fill=INK, width=6)
d.text((L + 14, 385), "TAPED PRINTOUTS", font=F_DIM, fill=INK, anchor="lm")

# camera
cx, cy = 120, (T + B) // 2
d.polygon([(cx - 34, cy), (cx, cy - 26), (cx, cy + 26)], outline=INK, width=2)
d.text((cx - 6, cy + 52), "CAMERA", font=F_DIM, fill=INK, anchor="mm")
d.text((cx - 6, cy + 70), "eye height, INSIDE", font=F_DIM, fill=FAINT, anchor="mm")
d.line([(cx, cy), (R_ - 20, cy)], fill=FAINT, width=1)

# ---------------------------------------------------------------- notes
d.line([(28, 740), (W - 28, 740)], fill=INK, width=1)
d.text((48, 772), "BOTH STATES SHARE THIS GEOMETRY. Only the LIGHT and the time change.",
       font=F_HEAD, fill=INK, anchor="lm")
notes = [
    "`wide`   daylight through the window wall; room mid-work; evidence of people everywhere.",
    "`night`  overheads off, two or three desk-lamp pools, screens brightest, windows dark and reflecting.",
    "NEVER: soaring ceiling, atrium, glass conference boxes, rows of identical monitors, branding, slogans, neon.",
    "ALWAYS: lived-in and a little untidy. A jacket over a chair back. A half-drunk mug. Whatever light the room has.",
]
for i, n in enumerate(notes):
    d.text((48, 812 + i * 26), n, font=F_BODY, fill=INK if i > 1 else FAINT, anchor="lm")
d.line([(40, 806), (40, 806 + len(notes) * 26)], fill=WARM, width=3)

img.save(__file__.rsplit("/", 1)[0] + "/blueprint.png")
print("wrote blueprint.png", img.size)
