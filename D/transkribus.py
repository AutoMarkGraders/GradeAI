from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

driver.get("https://transkribus.ai/")
driver.maximize_window()

upload = driver.find_element(By.CSS_SELECTOR,'.dropzone__input')
upload.send_keys("C:/DR/Documents/drpy/easyocr/0.jpg")

driver.find_element(By.CSS_SELECTOR,'.dropzone').click()

output = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.result__line')))

output = driver.find_elements(By.CSS_SELECTOR,'.result__line')
for line in output:
    print(line.get_attribute('innerHTML').strip())
    