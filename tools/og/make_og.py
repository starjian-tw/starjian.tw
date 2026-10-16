"""產生每篇文章的分享預覽圖（1200×630 PNG），存到 static/images/og/<檔名>.png，
並在文章前置資料補一行 images。字型用思源黑體（Noto Sans TC）靜態檔，以 --font-dir 指定。

用法：python tools/og/make_og.py --font-dir <有 NotoSansTC-Bold.ttf 與 NotoSansTC-Regular.ttf 的資料夾> [文章.md ...]
不指定文章就處理 content/posts/ 底下全部（_index.md 除外）。前置資料已經有 images 的文章只重畫圖，不改文章。
"""
import argparse
import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
W, H = 1200, 630
MARGIN = 80
GREEN, PAPER, GOLD = "#1f4a3f", "#f5efe3", "#c9a961"
NO_LINE_START = set("，。、：；？！」』）〉》…—")
NO_LINE_END = set("「『（〈《")


def wrap(text, font, width):
    lines, cur = [], ""
    for ch in text:
        if not cur or font.getlength(cur + ch) <= width:
            cur += ch
        elif ch in NO_LINE_START:
            cur += ch  # 標點不放行首，留在上一行
        elif cur[-1] in NO_LINE_END:
            lines.append(cur[:-1])  # 開括號不放行尾，帶到下一行
            cur = cur[-1] + ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def front_matter(md_text):
    m = re.match(r"---\n(.*?)\n---\n", md_text, re.S)
    if not m:
        raise SystemExit("找不到前置資料")
    return m


def draw_card(title, out, font_dir):
    bold = font_dir / "NotoSansTC-Bold.ttf"
    regular = font_dir / "NotoSansTC-Regular.ttf"
    img = Image.new("RGB", (W, H), GREEN)
    d = ImageDraw.Draw(img)
    d.text((MARGIN, 64), "星鑑", font=ImageFont.truetype(str(bold), 40), fill=PAPER)
    d.text((MARGIN + 100, 74), "有據可鑑的紫微斗數", font=ImageFont.truetype(str(regular), 28), fill=GOLD)
    for size in (68, 60, 54):
        font = ImageFont.truetype(str(bold), size)
        lines = wrap(title, font, W - MARGIN * 2)
        if len(lines) <= 3:
            break
    y = 190
    for line in lines:
        d.text((MARGIN, y), line, font=font, fill=PAPER)
        y += round(size * 1.32)
    d.text((MARGIN, H - 64 - 28), "starjian.tw", font=ImageFont.truetype(str(regular), 28), fill=GOLD)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font-dir", required=True, type=pathlib.Path)
    ap.add_argument("posts", nargs="*", type=pathlib.Path)
    args = ap.parse_args()
    posts = args.posts or sorted(p for p in (ROOT / "content" / "posts").glob("*.md") if p.name != "_index.md")
    for post in posts:
        newline = "\r\n" if b"\r\n" in post.read_bytes() else "\n"
        text = post.read_text(encoding="utf-8")
        fm = front_matter(text)
        title = re.search(r'^title:\s*"(.*)"\s*$', fm.group(1), re.M).group(1)
        rel = f"/images/og/{post.stem}.png"
        draw_card(title, ROOT / "static" / rel.lstrip("/"), args.font_dir)
        if not re.search(r"^images:", fm.group(1), re.M):
            head = fm.group(1)
            line = f'images: ["{rel}"]'
            head = re.sub(r"^(description:.*)$", lambda m: m.group(1) + "\n" + line, head, count=1, flags=re.M) \
                if re.search(r"^description:", head, re.M) else head + "\n" + line
            post.write_text(text.replace(fm.group(1), head, 1), encoding="utf-8", newline=newline)
        print(post.name, "→", rel)


if __name__ == "__main__":
    main()
