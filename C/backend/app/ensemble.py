#not currently in use

from PyPDF2 import PdfReader
from PIL import Image
import io

def extract_images(pdf_path):
    images = []
    with open(pdf_path, "rb") as f:
        pdf = PdfReader(pdf_path)
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            try:
                xObject = page['/Resources']['/XObject'].get_object()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                        data = xObject[obj].get_data()
                        mode = "RGB" if xObject[obj]['/ColorSpace'] == '/DeviceRGB' else "P"

                        if xObject[obj]['/Filter'] == '/FlateDecode':
                            img = Image.frombytes(mode, size, data)
                            images.append(img)
                        else:
                            img = Image.open(io.BytesIO(data))
                            images.append(img)
            except KeyError:
                continue
    return images

def combine_images(images, output_path):
    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)
    combined_img = Image.new("RGB", (max_width, total_height))
    y_offset = 0
    for img in images:
        combined_img.paste(img, (0, y_offset))
        y_offset += img.height
    combined_img.save(output_path)

if __name__ == "__main__":
    pdf_path = "trial.pdf"
    output_path = "test.jpg"

    images = extract_images(pdf_path)
    combine_images(images, output_path)
