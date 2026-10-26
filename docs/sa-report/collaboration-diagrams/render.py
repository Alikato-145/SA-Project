"""Render detailed UML communication diagrams from the sequence source."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "sequence-diagrams" / "README.md"
OUTPUT = ROOT / "collaboration-diagrams" / "figures"
FONT = "/System/Library/Fonts/Supplemental/Tahoma.ttf"
WIDTH = 3000
ORANGE = "#f4a34a"
PALE = "#fff8ec"
DARK = "#283746"
MUTED = "#687783"


def face(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
         width: int) -> list[str]:
    lines = [""]
    for char in text:
        candidate = lines[-1] + char
        if lines[-1] and draw.textlength(candidate, font=font) > width:
            split = lines[-1].rfind(" ")
            if split > len(lines[-1]) // 3:
                rest = lines[-1][split + 1:] + char
                lines[-1] = lines[-1][:split].rstrip()
                lines.append(rest.lstrip())
            else:
                lines.append(char)
        else:
            lines[-1] = candidate
    return lines


def arrow(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int,
          *, dashed: bool = False, color: str = DARK) -> None:
    direction = 1 if x2 > x1 else -1
    distance = abs(x2 - x1)
    if dashed:
        for offset in range(0, distance, 24):
            start = x1 + direction * offset
            end = x1 + direction * min(offset + 13, distance)
            draw.line((start, y, end, y), fill=color, width=4)
    else:
        draw.line((x1, y, x2, y), fill=color, width=4)
    draw.polygon((x2, y, x2 - direction * 19, y - 10,
                  x2 - direction * 19, y + 10), fill=color)


def participant(draw: ImageDraw.ImageDraw, x: int, y: int, name: str,
                *, actor: bool = False, database: bool = False) -> None:
    if actor:
        draw.rounded_rectangle((x - 128, y - 100, x + 128, y + 115),
                               radius=10, fill=ORANGE, outline=DARK, width=4)
        draw.ellipse((x - 29, y - 70, x + 29, y - 12), outline=DARK, width=5)
        draw.line((x, y - 12, x, y + 60), fill=DARK, width=5)
        draw.line((x - 42, y + 13, x + 42, y + 13), fill=DARK, width=5)
        draw.line((x, y + 60, x - 34, y + 92), fill=DARK, width=5)
        draw.line((x, y + 60, x + 34, y + 92), fill=DARK, width=5)
    else:
        if database:
            draw.rectangle((x - 208, y - 75, x + 212, y + 95),
                           fill=PALE, outline=DARK, width=4)
            draw.rectangle((x - 195, y - 86, x + 225, y + 84),
                           fill=PALE, outline=DARK, width=4)
        draw.rounded_rectangle((x - 225, y - 98, x + 195, y + 72),
                               radius=8, fill=ORANGE, outline=DARK, width=4)
    label_font = face(42 if len(name) <= 16 else 35)
    if len(name) > 22 and name.endswith(("Controller", "Service")):
        prefix, suffix = re.match(r"(.+?)(Controller|Service)$", name).groups()
        lines = [prefix, suffix]
        label_font = face(35)
    else:
        lines = wrap(draw, name, label_font, 405 if not actor else 245)
    y0 = y + (128 if actor else -28) - (len(lines) - 1) * 25
    for i, line in enumerate(lines):
        draw.text((x, y0 + i * 50), line, anchor="mm", font=label_font,
                  fill=DARK)


def parse_block(source: str) -> tuple[list[str], list[tuple[int, str, str, str, str]]]:
    lanes = re.findall(r"^\s*(?:actor|participant)\s+(\w+)\s+as\s+.+$", source, re.M)
    messages = []
    for sender, kind, receiver, number, label in re.findall(
        r"^\s*(\w+)(-->>|->>)(\w+):\s*(\d+)\s+(.+)$", source, re.M
    ):
        messages.append((int(number), sender, kind, receiver, label))
    assert len(lanes) >= 5 and messages
    assert [m[0] for m in messages] == list(range(1, len(messages) + 1))
    assert all(a in lanes and b in lanes for _, a, _, b, _ in messages)
    return lanes, messages


def render(number: str, title: str, source: str) -> Path:
    lanes, messages = parse_block(source)
    width = max(WIDTH, 420 + (len(lanes) - 1) * 645)
    groups: list[list[tuple[int, str, str, str, str]]] = [[] for _ in range(len(lanes) - 1)]
    for msg in messages:
        _, sender, _, receiver, _ = msg
        a, b = lanes.index(sender), lanes.index(receiver)
        group = min(a, b) if a != b else min(a, len(lanes) - 2)
        groups[group].append(msg)

    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    text_font = face(61)
    midpoint = (len(messages) + 1) // 2
    entries: list[list[tuple[tuple[int, str, str, str, str], list[str], int]]] = []
    heights = []
    for column in (messages[:midpoint], messages[midpoint:]):
        prepared = []
        for msg in column:
            lines = wrap(measure, msg[4], text_font, 1240)
            entry_height = 110 + len(lines) * 74
            prepared.append((msg, lines, entry_height))
        entries.append(prepared)
        heights.append(sum(item[2] for item in prepared))

    title_font = face(76)
    title_lines = wrap(measure, f"UC{number[:2]}  {title}", title_font, width - 100)
    header_height = 120 + 88 * len(title_lines)
    network_y = header_height + 230
    list_y = network_y + 340
    height = list_y + max(heights) + 110
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    for i, line in enumerate(title_lines):
        draw.text((60, 45 + i * 88), line, font=title_font, fill=DARK)

    xs = [210 + 645 * i for i in range(len(lanes))]
    for i, name in enumerate(lanes):
        participant(draw, xs[i], network_y, name, actor=i == 0, database=name == "DatabaseInstance")

    for group_index in range(len(lanes) - 1):
        x1, x2 = xs[group_index], xs[group_index + 1]
        draw.line((x1 + 225, network_y, x2 - 225, network_y),
                  fill=DARK, width=5)
        forward = [str(n) for n, sender, _, receiver, _ in groups[group_index]
                   if sender == lanes[group_index] and receiver == lanes[group_index + 1]]
        backward = [str(n) for n, sender, _, receiver, _ in groups[group_index]
                    if sender == lanes[group_index + 1] and receiver == lanes[group_index]]
        if forward:
            arrow(draw, x1 + 260, x2 - 255, network_y - 48)
            draw.text(((x1 + x2) // 2, network_y - 116), ", ".join(forward),
                      anchor="mm", font=face(42), fill=DARK)
        if backward:
            arrow(draw, x2 - 255, x1 + 260, network_y + 50,
                  dashed=True, color=MUTED)
            draw.text(((x1 + x2) // 2, network_y + 105), ", ".join(backward),
                      anchor="mm", font=face(42), fill=MUTED)

    for n, sender, kind, receiver, label in messages:
        a, b = lanes.index(sender), lanes.index(receiver)
        if abs(a - b) <= 1:
            continue
        y = network_y - 190 - (n % 3) * 38
        draw.line([(xs[a], network_y - 100), (xs[a], y), (xs[b], y), (xs[b], network_y - 100)], fill=MUTED, width=3)
        draw.polygon([(xs[b]-12, network_y-118), (xs[b]+12, network_y-118), (xs[b], network_y-100)], fill=MUTED)
        draw.text(((xs[a]+xs[b])//2, y-20), str(n), anchor="mm", font=face(38), fill=DARK)

    for i, name in enumerate(lanes[1:-1], 1):
        numbers = [str(n) for n, sender, _, receiver, _ in messages
                   if sender == receiver == name]
        if not numbers:
            continue
        x, y = xs[i] + 125, network_y + 118
        draw.arc((x, y, x + 80, y + 70), 260, 100, fill=DARK, width=5)
        draw.text((x + 100, y + 32), ", ".join(numbers), anchor="lm",
                  font=face(40), fill=DARK)

    col_x = [55, 1545]
    for column_index, prepared in enumerate(entries):
        x = col_x[column_index]
        heading = "ข้อความลำดับ 1–" + str(midpoint) if column_index == 0 else f"ข้อความลำดับ {midpoint + 1}–{len(messages)}"
        draw.text((x, list_y - 90), heading, font=face(56), fill=DARK)
        y = list_y + 10
        for msg, lines, entry_height in prepared:
            number_, sender, kind, receiver, _ = msg
            draw.rounded_rectangle((x, y, x + 105, y + 86), radius=12,
                                   fill=PALE, outline=ORANGE, width=4)
            draw.text((x + 52, y + 43), str(number_), anchor="mm",
                      font=face(53), fill=DARK)
            if sender == receiver:
                route = f"{sender} ตรวจภายใน"
            elif kind == "-->>":
                route = f"{sender} ตอบกลับ {receiver}"
            else:
                route = f"{sender} ส่งถึง {receiver}"
            route_lines = wrap(draw, route, face(44), 1260)
            for j, part in enumerate(route_lines[:2]):
                draw.text((x + 120, y + 5 + j * 46), part,
                          font=face(44), fill=MUTED)
            for j, part in enumerate(lines):
                draw.text((x + 120, y + 96 + j * 74), part,
                          font=text_font, fill=DARK)
            y += entry_height
            draw.line((x, y - 12, x + 1390, y - 12), fill="#dedede", width=2)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / f"collab-{number.lower()}.png"
    canvas.save(path, optimize=True, dpi=(300, 300))
    return path


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    blocks = re.findall(
        r"~~~mermaid\n(.*?)\n~~~\n\n!\[SEQ-(\d{2}[ab]?) ([^]]+)\]\(figures/seq-\2\.png\)",
        text, re.S,
    )
    assert len(blocks) == 23, len(blocks)
    for source, number, title in blocks:
        render(number, title, source)
    print(f"Rendered {len(blocks)} collaboration diagrams from the sequence source.")


if __name__ == "__main__":
    main()
