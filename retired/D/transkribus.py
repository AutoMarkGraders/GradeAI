# Import necessary libraries
from pdf2image import convert_from_path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#for path, remove method
import os
#to get text from clipboard
import tkinter as tk


# Create temp and final directories
if not os.path.exists('temp'):
    os.mkdir('temp')
if not os.path.exists('final'): 
    os.mkdir('final')

#input pdf
doc = str("Alan_Joseph.pdf")


#move pdf to temp


# Define the path to the temporary directory
absolute_path = os.path.dirname(__file__)
relative_path = "temp//"
full_path = os.path.join(absolute_path, relative_path)

#selenium options
options = Options()
options.add_experimental_option("detach", True)
# Initialize Chrome driver with some options
driver = webdriver.Chrome(options=options)

# Convert the PDF file to a list of images
pages = convert_from_path('./temp/'+ doc, 500)

# Initialize output text file
f = open("./final/" + doc[:-4] + 'ocr.txt','w',encoding='utf-8')

# Loop through each page of the PDF
for num, page in enumerate(pages):
    # Save the page as a JPEG image in the temporary directory
    page.save("./temp/" + str(num) + ".jpg", 'JPEG')

    # Open the Transkribus website in the Chrome browser
    driver.get("https://transkribus.ai/")
    driver.maximize_window()

    # Wait for the language selection dropdown to be visible
    wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.select__head-arrow')))
    # Select English language
    driver.find_element(By.CSS_SELECTOR,'.select__head-arrow').click()
    driver.find_element(By.XPATH, '//div[@class="select__item" and contains(., "English")]').click()

    # Upload the image to Transkribus
    upload = driver.find_element(By.CSS_SELECTOR,'.dropzone__input')
    upload.send_keys(full_path + str(num) + ".jpg")
    driver.find_element(By.CSS_SELECTOR,'.dropzone').click()

    """wait = WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result__line')))
    output = driver.find_elements(By.CSS_SELECTOR,'.result__line')"""
    
    # Wait for the OCR result to be visible
    wait = WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result__copy-to-clipboard')))
    # Copy the OCR result to the clipboard
    driver.find_element(By.CSS_SELECTOR,'.result__copy-to-clipboard').send_keys(Keys.RETURN)

    # Get the text from the clipboard
    root = tk.Tk()
    root.withdraw()  # to hide the window
    tout = root.clipboard_get()
    output = tout.replace('Text Recognition powered by transkribus.ai', '')

    for line in output:
        print(line,end="")#.get_attribute('innerHTML').strip())
        f.write(line)#.get_attribute('innerHTML').strip() + "\n")
    print("***end of page***\n")
    f.write("\n")

f.close()
# Remove the temporary images
for num, page in enumerate(pages):
    os.remove("./temp/"+ str(num) + ".jpg")


#delete temp directory