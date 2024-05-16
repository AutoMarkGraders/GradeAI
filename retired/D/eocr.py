# Import the necessary libraries
import easyocr
from pdf2image import convert_from_path

# Convert the PDF file to images
pages = convert_from_path('test.pdf', 500)

# Create an easyocr reader object
reader = easyocr.Reader(['en'], gpu=True)

# Loop through each page of the PDF
for num, page in enumerate(pages):
    # Save the page as a JPEG image
    page.save(str(num) + ".jpg", 'JPEG')
    
    # Extract text from the image using easyocr
    result = reader.readtext(str(num) + ".jpg")

    # Print the extracted text
    for (bbox, text, prob) in result:
        print(text)
    print("**end of page**")