#!/usr/bin/env python3
"""Prepare a source document for translation.

Usage: python scripts/extract_source.py <source-file> <work-dir>

Writes into <work-dir>:
  <stem>.txt            extracted text (digital PDF / .docx), page by page
  <stem>_p<N>.png       page images (PDF pages, photos) — read these with vision
                        to catch stamps, seals, handwriting and layout.

Scanned PDFs have little or no text layer; their page images are the source of truth.
"""
import subprocess
import sys
from pathlib import Path

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".gif"}
DPI = 200


def from_pdf(src: Path, out: Path) -> None:
    import pymupdf as fitz

    doc = fitz.open(src)
    text_parts = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        text_parts.append(f"=== Page {i} ===\n{text or '[no text layer — scanned page, use image]'}\n")
        page.get_pixmap(dpi=DPI).save(out / f"{src.stem}_p{i}.png")
    (out / f"{src.stem}.txt").write_text("\n".join(text_parts), encoding="utf-8")
    print(f"{len(doc)} page(s): text + images written to {out}")


def from_docx(src: Path, out: Path) -> None:
    from docx import Document

    doc = Document(src)
    lines = []
    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            lines.append("".join(t.text or "" for t in child.iter() if t.tag.endswith("}t")))
        elif tag == "tbl":
            for row in child.iter():
                if row.tag.endswith("}tr"):
                    cells = []
                    for cell in row:
                        if cell.tag.endswith("}tc"):
                            cells.append(" ".join(t.text or "" for t in cell.iter() if t.tag.endswith("}t")).strip())
                    lines.append("| " + " | ".join(cells) + " |")
            lines.append("")
    (out / f"{src.stem}.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"Text written to {out / (src.stem + '.txt')} (embedded images/stamps are not extracted — check the original)")


def from_image(src: Path, out: Path) -> None:
    dest = out / f"{src.stem}_p1.png"
    if src.suffix.lower() == ".png":
        dest.write_bytes(src.read_bytes())
    else:
        import pymupdf as fitz

        fitz.Pixmap(str(src)).save(dest)
    print(f"Image written to {dest}")


def from_heic(src: Path, out: Path) -> None:
    dest = out / f"{src.stem}_p1.png"
    subprocess.run(["sips", "-s", "format", "png", str(src), "--out", str(dest)], check=True, capture_output=True)
    print(f"Image written to {dest}")


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    if ext == ".pdf":
        from_pdf(src, out)
    elif ext == ".docx":
        from_docx(src, out)
    elif ext == ".heic":
        from_heic(src, out)
    elif ext in IMAGE_EXT:
        from_image(src, out)
    else:
        sys.exit(f"Unsupported file type: {ext} (convert .doc to .docx first)")


if __name__ == "__main__":
    main()
