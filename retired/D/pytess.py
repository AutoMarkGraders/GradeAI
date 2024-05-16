# Import the necessary libraries
import pytesseract as tess
from pdf2image import convert_from_path
from PIL import Image

# Convert the PDF file to images
pages = convert_from_path('test.pdf', 500)

# Set the path to the Tesseract executable
tess.pytesseract.tesseract_cmd = r'C:\Users\danie\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Loop through each page of the PDF
for num, page in enumerate(pages):
    page.save(str(num) + ".jpg", 'JPEG') # Save the page as a JPEG image with a filename based on the page number
    img = Image.open(str(num) + ".jpg") # Open the JPEG image using the PIL Image class
    text = tess.image_to_string(img) # Use pytesseract to extract text from the image

    print(text) # Print the extracted text
    print("**end of page**") # Print a message to indicate the end of the page