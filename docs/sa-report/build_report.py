"""Build the Haris SA Word report and sequence figures from the reviewed Markdown."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
SOURCE = ROOT / "README.md"
FIGURES = ROOT / "figures"
OUTPUT = ROOT / "Haris-SA-Report.docx"
FONT_PATH = "/System/Library/Fonts/Supplemental/Tahoma.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def short(value: str, limit: int = 48) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "…"


def draw_sequence(number: str, title: str, block: list[str]) -> Path | None:
    lanes: list[tuple[str, str]] = []
    messages: list[tuple[str, str, str, bool]] = []
    for raw in block:
        line = raw.strip()
        participant = re.match(r"(?:actor|participant)\s+(\w+)\s+as\s+(.+)", line)
        if participant:
            lanes.append((participant.group(1), participant.group(2)))
            continue
        message = re.match(r"(\w+)(-->>|->>)(\w+):\s*(.+)", line)
        if message:
            messages.append((message.group(1), message.group(3), message.group(4), message.group(2) == "-->>"))
    if len(lanes) < 2 or not messages:
        return None

    scale = 2
    width = max(1450, 360 * len(lanes))
    height = 180 + 125 * len(messages)
    canvas = Image.new("RGB", (width * scale, height * scale), "white")
    draw = ImageDraw.Draw(canvas)
    navy, blue, gray = "#17324d", "#dbeaf5", "#aebdca"
    draw.text((46 * scale, 25 * scale), f"{number} {title}", font=font(23 * scale), fill=navy)
    left, right = 125 * scale, (width - 125) * scale
    xpos = {key: left + i * (right - left) // (len(lanes) - 1) for i, (key, _) in enumerate(lanes)}
    top = 88 * scale
    for key, label in lanes:
        x = xpos[key]
        draw.rounded_rectangle((x - 125 * scale, top, x + 125 * scale, top + 48 * scale), radius=8 * scale, fill=blue, outline=navy, width=2 * scale)
        draw.text((x, top + 24 * scale), short(label, 23), anchor="mm", font=font(16 * scale), fill=navy)
        draw.line((x, top + 48 * scale, x, (height - 30) * scale), fill=gray, width=2 * scale)
    for i, (source, target, label, response) in enumerate(messages):
        if source not in xpos or target not in xpos:
            continue
        y = (177 + 125 * i) * scale
        a, b = xpos[source], xpos[target]
        color = "#597a91" if response else navy
        if a == b:
            draw.arc((a, y - 13 * scale, a + 56 * scale, y + 45 * scale), 270, 90, fill=color, width=3 * scale)
            draw.text((a + 75 * scale, y - 19 * scale), short(label, 44), font=font(15 * scale), fill=color)
        else:
            draw.line((a, y, b, y), fill=color, width=3 * scale)
            direction = 1 if b > a else -1
            draw.polygon([(b, y), (b - direction * 13 * scale, y - 6 * scale), (b - direction * 13 * scale, y + 6 * scale)], fill=color)
            midpoint = (a + b) // 2
            draw.text((midpoint, y - 21 * scale), short(label, 49), anchor="ms", font=font(15 * scale), fill=color, stroke_width=0)
    FIGURES.mkdir(exist_ok=True)
    path = FIGURES / f"sequence-{number.lower()}.png"
    canvas.save(path)
    return path


def add_inline(paragraph, value: str) -> None:
    # Preserve link targets without placing long URLs in the report body.
    pieces = re.split(r"(\[[^]]+\]\([^)]+\))", value)
    for piece in pieces:
        match = re.fullmatch(r"\[([^]]+)\]\(([^)]+)\)", piece)
        if match:
            label, target = match.groups()
            if target.startswith("http"):
                link = OxmlElement("w:hyperlink")
                link.set(qn("r:id"), paragraph.part.relate_to(target, RT.HYPERLINK, is_external=True))
                run_xml = OxmlElement("w:r")
                props = OxmlElement("w:rPr")
                color = OxmlElement("w:color")
                color.set(qn("w:val"), "1765A0")
                props.append(color)
                run_xml.append(props)
                text_xml = OxmlElement("w:t")
                text_xml.text = label
                run_xml.append(text_xml)
                link.append(run_xml)
                paragraph._p.append(link)
            else:
                paragraph.add_run(label)
            continue
        for subpiece in re.split(r"(`[^`]+`|\*\*[^*]+\*\*)", piece):
            add_piece(paragraph, subpiece)


def add_piece(paragraph, piece: str) -> None:
    if not piece:
        return
    run = paragraph.add_run(piece.strip("`*"))
    run.bold = piece.startswith("**")
    fonts = run._element.get_or_add_rPr().rFonts
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        run._element.get_or_add_rPr().insert(0, fonts)
    fonts.set(qn("w:cs"), "Tahoma")
    fonts.set(qn("w:eastAsia"), "Tahoma")
    if piece.startswith("`"):
        run.font.name = "Consolas"
        run.font.size = Pt(8)


def add_table(doc: Document, lines: list[str]) -> None:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    rows = [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row)]
    if not rows:
        return
    cols = max(map(len, rows))
    table = doc.add_table(rows=len(rows), cols=cols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    header_props = table.rows[0]._tr.get_or_add_trPr()
    header_props.append(OxmlElement("w:tblHeader"))
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            p = table.cell(i, j).paragraphs[0]
            add_inline(p, cell)
            for run in p.runs:
                run.font.size = Pt(8.5)
            if i == 0:
                for run in p.runs:
                    run.bold = True
        table.rows[i]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))


def build() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.2)
    styles = doc.styles
    for name in ["Normal", "Title", "Heading 1", "Heading 2", "Heading 3", "Heading 4"]:
        style = styles[name]
        style.font.name = "Tahoma"
        fonts = style._element.get_or_add_rPr().rFonts
        if fonts is None:
            fonts = OxmlElement("w:rFonts")
            style._element.get_or_add_rPr().insert(0, fonts)
        fonts.set(qn("w:cs"), "Tahoma")
        fonts.set(qn("w:eastAsia"), "Tahoma")
        style.font.size = Pt(10.5 if name == "Normal" else {"Title": 19, "Heading 1": 16, "Heading 2": 13, "Heading 3": 11, "Heading 4": 10}.get(name, 10))
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_after = Pt(5)
        if name.startswith("Heading"):
            style.paragraph_format.keep_with_next = True
    title_style = styles["Title"]
    title_ppr = title_style._element.get_or_add_pPr()
    border = title_ppr.find(qn("w:pBdr"))
    if border is not None:
        title_ppr.remove(border)
    styles["Normal"].paragraph_format.line_spacing = 1.25
    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(title, "รายงานการวิเคราะห์และออกแบบระบบจัดการพนักงานและเงินเดือนร้าน Haris")
    subtitle = doc.add_paragraph("เอกสารฉบับร่างเพื่อทบทวนความสอดคล้องของกระบวนการ Use Case และฐานข้อมูล")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].font.color.rgb = RGBColor(0, 0, 0)
    current_uc: tuple[str, str] | None = None
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            heading = line[level:].strip()
            if level == 2 and doc.paragraphs:
                doc.add_page_break()
            doc.add_heading(heading, min(level - 1, 4))
            match = re.match(r"3\.3\.\d+\s+(UC\d+)\s+(.+)", heading)
            if match:
                current_uc = (match.group(1), match.group(2))
            i += 1
            continue
        if line.startswith("|"):
            group = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                group.append(lines[i]); i += 1
            add_table(doc, group)
            continue
        image_match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", line)
        if image_match:
            image_path = ROOT / image_match.group(2)
            if image_path.exists():
                paragraph = doc.add_paragraph()
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.paragraph_format.keep_with_next = True
                paragraph.add_run().add_picture(str(image_path), width=Cm(15.5))
                doc.add_paragraph(image_match.group(1), style="Caption")
            i += 1
            continue
        if line.startswith("```mermaid"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i]); i += 1
            i += 1
            if block and block[0].strip() == "sequenceDiagram" and current_uc:
                image = draw_sequence(*current_uc, block)
                if image:
                    paragraph = doc.add_paragraph()
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    paragraph.paragraph_format.keep_with_next = True
                    paragraph.add_run().add_picture(str(image), width=Cm(15.5))
                    doc.add_paragraph(f"ภาพ Sequence Diagram {current_uc[0]}: {current_uc[1]}", style="Caption")
            else:
                p = doc.add_paragraph("แผนภาพเชิงแนวคิด: " + " / ".join(short(part.strip(), 70) for part in block if "-->" in part)[:450])
                p.style = "Caption"
            continue
        if line.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                p = doc.add_paragraph(lines[i])
                p.style = "No Spacing"
                for run in p.runs:
                    run.font.name = "Consolas"
                    run.font.size = Pt(8)
                i += 1
            i += 1
            continue
        if line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, line[2:])
            i += 1
            continue
        p = doc.add_paragraph()
        add_inline(p, line)
        i += 1
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Haris Payroll — รายงานการวิเคราะห์และออกแบบระบบ | หน้า ")
    page_field = OxmlElement("w:fldSimple")
    page_field.set(qn("w:instr"), "PAGE")
    footer._p.append(page_field)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
