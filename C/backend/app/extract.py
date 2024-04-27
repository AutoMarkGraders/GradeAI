import google.generativeai as genai
from pathlib import Path
import hashlib

import os
from dotenv import load_dotenv
load_dotenv() # Load from .env file

from pdf2image import convert_from_path
from fastapi import UploadFile
import re

# Set up the model
genai.configure(api_key=os.getenv('GEMINI_API'))
generation_config = {"temperature": 1,"top_p": 0.95,"top_k": 0,"max_output_tokens": 12000,}
safety_settings = [
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",generation_config=generation_config,safety_settings=safety_settings)

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1]]

data_set = [
  "Display the text in input image.",
]


def extractText(file_path: str):
  answers = []
  
  # Convert the PDF to of PIL Image objects
  images = convert_from_path(file_path) #requires system's PATH setup, something else on ubuntu
  # Save each image to the current directory and extract text
  for i, image in enumerate(images):
    image_path = os.path.join(os.getcwd(), f"{i + 1}.png")
    image.save(image_path, "PNG")

    prompt_parts = [
      "input: ",
      *upload_if_needed(image_path),
      "output: ",
    ]
    data_set.extend(prompt_parts)

    response = model.generate_content(data_set) #OCR
    
    cleaned_text = re.sub(' +', ' ', response.text)  # Replace multiple spaces with one
    cleaned_text = re.sub('\n+', '\n', cleaned_text) # Replace multiple \n with one
    cleaned_text = re.sub('[*#①②]', '', cleaned_text) # Replace special characters
    #print(cleaned_text)

    answers.append(cleaned_text)

    # Delete the image file
    os.remove(image_path)

  for uploaded_file in uploaded_files:
    genai.delete_file(name=uploaded_file.name)

  return answers

#extractText("test.pdf")