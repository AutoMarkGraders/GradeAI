from pdfminer.high_level import extract_pages, extract_text

text = extract_text('lvl1.pdf')
print(text)