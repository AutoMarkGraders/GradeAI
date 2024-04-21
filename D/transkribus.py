from pdf2image import convert_from_path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import os                                       #for path, remove method

if not os.path.exists('temp'): 
    os.mkdir('temp')
if not os.path.exists('final'): 
    os.mkdir('final')

doc = str("Alan_Joseph.pdf")                       #input pdf

#move pdf to temp

absolute_path = os.path.dirname(__file__)
relative_path = "temp//"
full_path = os.path.join(absolute_path, relative_path)

options = Options()                                         #selenium options
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

pages = convert_from_path('./temp/'+ doc, 500)

f = open("./final/" + doc[:-4] + 'ocr.txt','w',encoding='utf-8')

for num, page in enumerate(pages):
    page.save("./temp/" + str(num) + ".jpg", 'JPEG')
    driver.get("https://transkribus.ai/")
    #driver.maximize_window()

    wait = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.select__head-arrow')))  #select english language
    driver.find_element(By.CSS_SELECTOR,'.select__head-arrow').click()
    driver.find_element(By.XPATH, '//div[@class="select__item" and contains(., "English")]').click()

    upload = driver.find_element(By.CSS_SELECTOR,'.dropzone__input')
    upload.send_keys(full_path + str(num) + ".jpg")

    driver.find_element(By.CSS_SELECTOR,'.dropzone').click()

    wait = WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.result__line')))

    output = driver.find_elements(By.CSS_SELECTOR,'.result__line')
    for line in output:
        print(line.get_attribute('innerHTML').strip())
        f.write(line.get_attribute('innerHTML').strip() + "\n")
    print("***end of page***\n")
    f.write("\n")

f.close()
for num, page in enumerate(pages):
    os.remove("./temp/"+ str(num) + ".jpg")