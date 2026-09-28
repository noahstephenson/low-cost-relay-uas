"""Render Figure 3 from its editable Mermaid source."""

from pathlib import Path
import shutil
import subprocess

import pymupdf
from PIL import Image, ImageChops

FIGS = Path(__file__).resolve().parent / "figs"
SOURCE = FIGS / "architecture_assessment_workflow.mmd"
BASENAME = FIGS / "architecture_assessment_workflow"


def crop_pdf_to_diagram(path: Path) -> None:
    """Remove Mermaid CLI's square PDF page margin, preserving vector content."""
    with pymupdf.open(path) as document:
        page = document[0]
        pixmap = page.get_pixmap(alpha=False)
        rendered = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        background = Image.new("RGB", rendered.size, "white")
        bounds = ImageChops.difference(rendered, background).getbbox()
        if bounds is None:
            raise RuntimeError("Mermaid rendered an empty PDF")
        x0, y0, x1, y1 = bounds
        page.set_cropbox(pymupdf.Rect(x0 - 6, y0 - 6, x1 + 6, y1 + 6) & page.rect)
        cropped = path.with_name(path.stem + "-cropped.pdf")
        document.save(cropped, garbage=4, deflate=True)
    cropped.replace(path)


def main() -> None:
    npx = shutil.which("npx")
    if npx is None:
        raise SystemExit("Node.js npx is required to render the Mermaid workflow")
    version = subprocess.run(
        [npx, "--no-install", "@mermaid-js/mermaid-cli", "--version"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if version != "12.0.0":
        raise SystemExit(f"Mermaid CLI 12.0.0 is required; found {version}")
    for extension in ("pdf", "png"):
        subprocess.run(
            [npx, "--no-install", "@mermaid-js/mermaid-cli",
             "-i", str(SOURCE), "-o", str(BASENAME.with_suffix(f".{extension}")),
             "-b", "white", "--size", "1200", "-s", "2"],
            check=True,
        )
    crop_pdf_to_diagram(BASENAME.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
