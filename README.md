# pypdf 6.6.0 Bug Reproduction

Reproduces `KeyError: 'bbox'` when extracting text from certain PDFs in pypdf 6.6.0.

## Bug Summary

Text extraction fails with `KeyError: 'bbox'` in pypdf 6.6.0, but works in 6.5.0. The error occurs in `_font.py:58` during font descriptor parsing when a font resource dictionary lacks a `bbox` key.

## Error Trace

```
File "venv/lib/python3.14/site-packages/pypdf/_font.py", line 58, in _parse_font_descriptor
    bbox_tuple = tuple(map(float, font_kwargs["bbox"]))
KeyError: 'bbox'
```

## Reproduction Steps

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python repro.py
```

## Version Comparison

```bash
# Works
pip install pypdf==6.5.0
python repro.py

# Fails with KeyError: 'bbox'
pip install pypdf==6.6.0
python repro.py
```

## Bug Details

The root cause is in pypdf's font descriptor parsing (`_font.py:56-58`):

1. When a font has a `FontDescriptor`, pypdf checks for `/FontBBox` and conditionally assigns it to `font_kwargs["bbox"]`
2. However, the code unconditionally accesses `font_kwargs["bbox"]` afterward, assuming it exists
3. If the FontDescriptor is missing the `/FontBBox` key (which is technically optional per PDF spec), pypdf raises `KeyError: 'bbox'`

The minimal reproduction creates a PDF with a Type1 font whose FontDescriptor intentionally omits `/FontBBox`.

## Font Analysis

Use `analyze_fonts.py` to inspect font structures and identify fonts missing `/FontBBox`:

```bash
./venv/bin/python analyze_fonts.py original.pdf
./venv/bin/python analyze_fonts.py minimal.pdf
```

### original.pdf (Page 1 excerpt)

```
============================================================
Analyzing: original.pdf
============================================================

Page 1:
----------------------------------------

  Font: /F5
    Subtype: /Type0
    BaseFont: /AAAAAA+UncutSans-Bd
    FontDescriptor: NONE

  Font: /F7
    Subtype: /Type3
    BaseFont: N/A
    FontDescriptor:
      Keys: /CapHeight, /Flags, /FontFamily, /FontName, /FontStretch, /FontWeight, /ItalicAngle, /StemV, /Type, /XHeight
      FontBBox: MISSING  <-- This causes pypdf 6.6.0 bug!
```

The original PDF has multiple Type3 fonts across pages 1-4, all missing `/FontBBox` in their FontDescriptor.

### minimal.pdf

```
============================================================
Analyzing: minimal.pdf
============================================================

Page 1:
----------------------------------------

  Font: /F1
    Subtype: /Type1
    BaseFont: /TestFont
    FontDescriptor:
      Keys: /Ascent, /CapHeight, /Descent, /Flags, /FontName, /ItalicAngle, /StemV, /Type
      FontBBox: MISSING  <-- This causes pypdf 6.6.0 bug!
```

The minimal reproduction creates a Type1 font with the same condition: a FontDescriptor that omits `/FontBBox`.

## Files

- `repro.py` - Minimal reproduction script
- `requirements.txt` - Dependencies (pypdf==6.6.0, pikepdf for PDF creation)
- `minimal.pdf` - Minimal PDF that triggers the bug
- `create_minimal.py` - Script to generate minimal.pdf using pikepdf
- `analyze_fonts.py` - Script to analyze font structures in PDFs
