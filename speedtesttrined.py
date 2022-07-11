# pip3 install selenium webdriver-manager
#
# if KeyError: 'chromium' => apt install chromium
#
# if KeyError: 'chromium' on Windows,
# \Python\Lib\site-packages\browsers\windows.py
# =>
# WINDOWS_REGISTRY_BROWSER_NAMES
# =>
# Add "Chromium": "chromium"
#
# if cannot access libraries => find /usr/lib/python3/dist-packages/ -type d -exec chmod o+x {} +
# if cannot access libraries => find /usr/lib/python3/dist-packages/ -type f -exec chmod o+r {} +

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import logging

logging.getLogger('WDM').disabled = True

options = Options()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                          options=options)

driver.get("http://trined.speedtestcustom.com/")

WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button__wrapper"))).click()
WebDriverWait(driver, 300).until(EC.url_matches("http://trined.speedtestcustom.com/result/"))

download_speed = driver.find_element(By.CLASS_NAME, "result-tile-download").find_element(By.CLASS_NAME, "number").text
upload_speed = driver.find_element(By.CLASS_NAME, "result-tile-upload").find_element(By.CLASS_NAME, "number").text

trined_url = driver.current_url
trined_download = repr(round(float(download_speed)))
trined_upload = repr(round(float(upload_speed)))

driver.get("https://www.speedtest.net/")

WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".test-modes-wrapper > .toggle > .test-mode-icon > .svg-icon"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-start-test.test-mode-single"))).click()
WebDriverWait(driver, 300).until(EC.url_matches("https://www.speedtest.net/result/"))

download_speed = driver.find_element(By.CLASS_NAME, "result-item-download").find_element(By.CLASS_NAME, "number").text
upload_speed = driver.find_element(By.CLASS_NAME, "result-item-upload").find_element(By.CLASS_NAME, "number").text

single_url = driver.current_url
single_download = repr(round(float(download_speed)))
single_upload = repr(round(float(upload_speed)))

driver.get("https://www.speedtest.net/")
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-start-test.test-mode-multi"))).click()
WebDriverWait(driver, 300).until(EC.url_matches("https://www.speedtest.net/result/"))

download_speed = driver.find_element(By.CLASS_NAME, "result-item-download").find_element(By.CLASS_NAME, "number").text
upload_speed = driver.find_element(By.CLASS_NAME, "result-item-upload").find_element(By.CLASS_NAME, "number").text

multi_url = driver.current_url
multi_download = repr(round(float(download_speed)))
multi_upload = repr(round(float(upload_speed)))

print(trined_url + ', ' + single_url + ', ' + multi_url + ', ' +
      trined_download + ', ' + trined_upload + ', ' +
      single_download + ', ' + single_upload + ', ' +
      multi_download + ', ' + multi_upload)

driver.close()
