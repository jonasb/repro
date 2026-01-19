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

## Files

- `repro.py` - Minimal reproduction script
- `requirements.txt` - Dependencies (pypdf==6.6.0)
- `original.pdf` - PDF that triggers the bug (not included)
