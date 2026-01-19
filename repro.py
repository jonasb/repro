from pypdf import PdfReader

reader = PdfReader("minimal.pdf")
for page in reader.pages:
    text = page.extract_text(extraction_mode="plain")
    print(text[:200] if text else "No text")
