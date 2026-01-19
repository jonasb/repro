#!/usr/bin/env python3
"""
Create a minimal PDF that triggers the KeyError: 'bbox' bug in pypdf 6.6.0.

The bug occurs in pypdf/_font.py:56 when a font's FontDescriptor is missing
the /FontBBox key. This script creates a minimal PDF with such a font.
"""

import pikepdf
from pikepdf import Dictionary, Name, Array, Stream

def create_minimal_pdf():
    pdf = pikepdf.new()

    # Create FontDescriptor WITHOUT /FontBBox (this triggers the bug)
    font_descriptor = pdf.make_indirect(Dictionary({
        "/Type": Name.FontDescriptor,
        "/FontName": Name("/TestFont"),
        "/Flags": 32,
        "/ItalicAngle": 0,
        "/Ascent": 800,
        "/Descent": -200,
        "/CapHeight": 700,
        "/StemV": 80,
        # /FontBBox is intentionally omitted to trigger the bug
    }))

    # Create a simple Type1 font that references the descriptor
    font = pdf.make_indirect(Dictionary({
        "/Type": Name.Font,
        "/Subtype": Name.Type1,
        "/BaseFont": Name("/TestFont"),
        "/FontDescriptor": font_descriptor,
        "/FirstChar": 32,
        "/LastChar": 126,
        "/Widths": Array([500] * 95),  # Simple widths for ASCII range
    }))

    # Create minimal content stream that references the font
    content = b"BT /F1 12 Tf (Test) Tj ET"

    # Add a blank page and then modify it
    pdf.add_blank_page(page_size=(612, 792))
    page = pdf.pages[0]

    # Add font resources to the page
    page["/Resources"] = Dictionary({
        "/Font": Dictionary({
            "/F1": font
        })
    })

    # Add content stream
    page["/Contents"] = pdf.make_indirect(Stream(pdf, content))

    # Save the minimal PDF
    pdf.save("minimal.pdf")
    print("Created minimal.pdf")

if __name__ == "__main__":
    create_minimal_pdf()
