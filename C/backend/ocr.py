import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext('level2.png')

for (bbox, text, prob) in result:
    print(text)