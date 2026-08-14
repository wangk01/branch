"""生成应用图标（.png 与 .ico）。运行：python scripts/make_icon.py"""
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 256


def make_icon(color="#ff6b9d") -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    body = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    d.ellipse((40, 70, 216, 220), fill=body)
    belly = (255, 214, 224, 255)
    d.ellipse((100, 150, 180, 215), fill=belly)
    for ex in (110, 160):
        d.ellipse((ex - 14, 115, ex + 14, 143), fill=(0, 0, 0, 255))
    d.arc((100, 150, 156, 180), 0, 180, fill=(0, 0, 0, 255), width=8)
    return img


def main():
    out = Path(__file__).resolve().parent.parent / "assets" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    img = make_icon()
    img.save(out / "pet.png")
    img.save(out / "pet.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"已生成: {out / 'pet.png'} 与 {out / 'pet.ico'}")


if __name__ == "__main__":
    main()
