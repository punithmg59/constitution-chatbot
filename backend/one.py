from pypdf import PdfReader

reader = PdfReader("constitution1.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

with open("constitution_raw.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Extraction done")