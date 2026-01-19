#!/usr/bin/env python3
"""
Analyze fonts in a PDF and show FontDescriptor details.

This script helps identify fonts missing /FontBBox in their FontDescriptor,
which triggers the KeyError: 'bbox' bug in pypdf 6.6.0.
"""

import sys
import pikepdf


def analyze_pdf_fonts(pdf_path: str) -> None:
    """Analyze and print font information from a PDF."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {pdf_path}")
    print(f"{'='*60}")

    try:
        pdf = pikepdf.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    for page_num, page in enumerate(pdf.pages, start=1):
        print(f"\nPage {page_num}:")
        print("-" * 40)

        resources = page.get("/Resources")
        if not resources:
            print("  No resources found")
            continue

        fonts = resources.get("/Font")
        if not fonts:
            print("  No fonts found")
            continue

        for font_name, font_ref in fonts.items():
            print(f"\n  Font: {font_name}")

            # Dereference if it's an indirect object
            font = font_ref
            if isinstance(font_ref, pikepdf.Object):
                try:
                    font = pdf.get_object(font_ref.objgen) if hasattr(font_ref, 'objgen') else font_ref
                except:
                    pass

            # Get basic font info
            subtype = font.get("/Subtype", "Unknown")
            base_font = font.get("/BaseFont", "N/A")
            print(f"    Subtype: {subtype}")
            print(f"    BaseFont: {base_font}")

            # Check FontDescriptor
            font_descriptor = font.get("/FontDescriptor")
            if font_descriptor is None:
                print("    FontDescriptor: NONE")
                continue

            print("    FontDescriptor:")

            # Dereference FontDescriptor if needed
            if isinstance(font_descriptor, pikepdf.Object):
                try:
                    font_descriptor = pdf.get_object(font_descriptor.objgen) if hasattr(font_descriptor, 'objgen') else font_descriptor
                except:
                    pass

            # List all keys in FontDescriptor
            keys = list(font_descriptor.keys())
            print(f"      Keys: {', '.join(str(k) for k in sorted(keys))}")

            # Check specifically for FontBBox
            if "/FontBBox" in font_descriptor:
                bbox = font_descriptor["/FontBBox"]
                print(f"      FontBBox: {list(bbox)}")
            else:
                print("      FontBBox: MISSING  <-- This causes pypdf 6.6.0 bug!")

    pdf.close()


def main():
    if len(sys.argv) > 1:
        # Analyze specified PDF(s)
        for pdf_path in sys.argv[1:]:
            analyze_pdf_fonts(pdf_path)
    else:
        # Default: analyze both PDFs
        analyze_pdf_fonts("original.pdf")
        analyze_pdf_fonts("minimal.pdf")


if __name__ == "__main__":
    main()
