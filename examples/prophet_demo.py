"""Prophet test: three painted poses -> cutout -> chalk outline -> parallax camera -> MP4.
Run: python examples/prophet_demo.py <poses_dir> <out.mp4>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PIL import Image
from oldbrain.cutout import cutout, pigment_mask, normalise_height
from oldbrain.outline import chalk_outline
from oldbrain.plate import clean_plate
from oldbrain.camera import Layer, Shot, push_in, shake, pull_back, contact_shadow
from oldbrain.assemble import shot_frames, whip, caption, write_mp4, SIZE

poses, out = Path(sys.argv[1]), sys.argv[2]
W, H = SIZE
src = {n: Image.open(poses / f"prophet-pose-{n}.png").convert("RGB") for n in ["preach", "shocked", "walk-side"]}
wall = clean_plate(src["preach"], pigment_mask(src["preach"])).resize(SIZE, Image.LANCZOS).convert("RGBA")
fig = {n: chalk_outline(normalise_height(cutout(im), 1150), W) for n, im in src.items()}

def scene(name, move, dur, vx=0.0, x=None):
    f = fig[name]; px = (W - f.width) // 2 if x is None else x; py = H - f.height - 330
    sh = contact_shadow(f)
    return Shot([Layer(wall, 0.0), Layer(sh, 0.15, (px - 40, py - 40), bob=0, vx=vx),
                 Layer(f, 0.9, (px, py), bob=6, vx=vx)], dur, move)

lines = [("THE SKY HAS CHOSEN ME.", scene("preach", push_in(0.12), 2.6)),
         ("...wait. Why is it getting BIGGER?", scene("shocked", shake(26), 1.8)),
         ("*leaves to 'prepare a sermon'*", scene("walk-side", pull_back(0.10), 2.4, vx=260, x=200))]
frames = []
for i, (text, shot) in enumerate(lines):
    fs = [caption(f, text) for f in shot_frames(shot)]
    if frames:
        frames.extend(whip(frames.pop(), fs[0], frames=8))
    frames.extend(fs)
write_mp4(frames, out)
print("frames", len(frames))
