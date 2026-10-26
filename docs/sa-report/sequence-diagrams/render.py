"""Render every Mermaid sequence block in README.md to its linked PNG."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from build_report import draw_sequence


def main() -> None:
    source = (ROOT / "README.md").read_text(encoding="utf-8")
    blocks = re.findall(
        r"~~~mermaid\n(.*?)\n~~~\n\n!\[SEQ-(\d{2}[ab]?) ([^]]+)\]\(figures/seq-\2\.png\)",
        source, re.S,
    )
    assert len(blocks) == 23, f"expected 23 sequence blocks, found {len(blocks)}"
    for code, number, title in blocks:
        result = draw_sequence(f"UC{number}", title, code.splitlines(), ROOT / "figures")
        assert result and result.exists(), number
    print(f"Rendered {len(blocks)} sequence diagrams to {ROOT / 'figures'}")


if __name__ == "__main__":
    main()
