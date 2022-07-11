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
import subprocess
import time
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import logging


def measure_bandwidth(seconds):
    switch_dl_1 = int(
        subprocess.run(['snmpget', '-v', '1', '-c', 'public', '-Oqv', 'switch-610', 'IF-MIB::ifHCInOctets.1'],
                       capture_output=True, text=True).stdout)
    t1 = time.perf_counter()
    switch_up_1 = int(
        subprocess.run(['snmpget', '-v', '1', '-c', 'public', '-Oqv', 'switch-610', 'IF-MIB::ifHCOutOctets.1'],
                       capture_output=True, text=True).stdout)
    t2 = time.perf_counter()
    time.sleep(seconds)

    switch_dl_2 = int(
        subprocess.run(['snmpget', '-v', '1', '-c', 'public', '-Oqv', 'switch-610', 'IF-MIB::ifHCInOctets.1'],
                       capture_output=True, text=True).stdout)
    t4 = time.perf_counter()
    switch_up_2 = int(
        subprocess.run(['snmpget', '-v', '1', '-c', 'public', '-Oqv', 'switch-610', 'IF-MIB::ifHCOutOctets.1'],
                       capture_output=True, text=True).stdout)
    t5 = time.perf_counter()

    download_time = t4 - t1
    upload_time = t5 - t2

    # in Mbps
    return \
        switch_dl_2 - switch_dl_1, download_time, switch_up_2 - switch_up_1, upload_time


test_start = subprocess.run(['date'], capture_output=True, text=True).stdout
measurement_seconds = 3.0

logging.getLogger('WDM').disabled = True

options = Options()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                          options=options)

switch_dl_octets_before_trined, switch_dl_time_before_trined, \
    switch_up_octets_before_trined, switch_up_time_before_trined = measure_bandwidth(measurement_seconds)

driver.get("http://trined.speedtestcustom.com/")

WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button__wrapper"))).click()
WebDriverWait(driver, 300).until(EC.url_matches("http://trined.speedtestcustom.com/result/"))

download_speed = driver.find_element(By.CLASS_NAME, "result-tile-download").find_element(By.CLASS_NAME, "number").text
upload_speed = driver.find_element(By.CLASS_NAME, "result-tile-upload").find_element(By.CLASS_NAME, "number").text

trined_url = driver.current_url
trined_download = repr(round(float(download_speed)))
trined_upload = repr(round(float(upload_speed)))

switch_dl_octets_before_single, switch_dl_time_before_single, \
    switch_up_octets_before_single, switch_up_time_before_single = measure_bandwidth(measurement_seconds)

driver.get("https://www.speedtest.net/")

WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, ".test-modes-wrapper > .toggle > .test-mode-icon > .svg-icon"))).click()
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-start-test.test-mode-single"))).click()
WebDriverWait(driver, 300).until(EC.url_matches("https://www.speedtest.net/result/"))

download_speed = driver.find_element(By.CLASS_NAME, "result-item-download").find_element(By.CLASS_NAME, "number").text
upload_speed = driver.find_element(By.CLASS_NAME, "result-item-upload").find_element(By.CLASS_NAME, "number").text

single_url = driver.current_url
single_download = repr(round(float(download_speed)))
single_upload = repr(round(float(upload_speed)))

switch_dl_octets_before_multi,switch_dl_time_before_multi, \
    switch_up_octets_before_multi, switch_up_time_before_multi = measure_bandwidth(measurement_seconds)

driver.get("https://www.speedtest.net/")
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-start-test.test-mode-multi"))).click()
WebDriverWait(driver, 300).until(EC.url_matches("https://www.speedtest.net/result/"))

download_speed = driver.find_element(By.CLASS_NAME, "result-item-download").find_element(By.CLASS_NAME, "number").text
upload_speed = driver.find_element(By.CLASS_NAME, "result-item-upload").find_element(By.CLASS_NAME, "number").text

multi_url = driver.current_url
multi_download = repr(round(float(download_speed)))
multi_upload = repr(round(float(upload_speed)))

switch_dl_octets_after, switch_dl_time_after, \
    switch_up_octets_after, switch_up_time_after = measure_bandwidth(measurement_seconds)

print("Date Start, "
      "Date Finish, "
      "Trined URL, Single URL, Multi URL, "
      "Trined Down, Trined Up, "
      "Single Down, Single Up, "
      "Multi Down, Multi Up, "
      "Switch Octets Down (Before Trined), Switch Octets Down Time (Before Trined), "
      "Switch Octets Up (Before Trined), Switch Octets Up Time (Before Trined), "
      "Switch Octets Down (Before Single), Switch Octets Down Time (Before Single), "
      "Switch Octets Up (Before Single), Switch Octets Up Time (Before Single), "
      "Switch Octets Down (Before Multi), Switch Octets Down Time (Before Multi), "
      "Switch Octets Up (Before Multi), Switch Octets Up Time (Before Multi), "
      "Switch Octets Down (After Multi), Switch Octets Down Time (After Multi), "
      "Switch Octets Up (After Multi), Switch Octets Up Time (After Multi)")

print(test_start.replace("\n", "") + ', ' +
      subprocess.run(['date'], capture_output=True, text=True).stdout.replace("\n", "") + ', ' +
      trined_url + ', ' + single_url + ', ' + multi_url + ', ' +
      trined_download + ', ' + trined_upload + ', ' +
      single_download + ', ' + single_upload + ', ' +
      multi_download + ', ' + multi_upload + ', ' +
      repr(switch_dl_octets_before_trined) + ', ' + repr(switch_dl_time_before_trined) + ', ' +
      repr(switch_up_octets_before_trined) + ', ' + repr(switch_up_time_before_trined) + ', ' +
      repr(switch_dl_octets_before_single) + ', ' + repr(switch_dl_time_before_single) + ', ' +
      repr(switch_up_octets_before_single) + ', ' + repr(switch_up_time_before_single) + ', ' +
      repr(switch_dl_octets_before_multi) + ', ' + repr(switch_dl_time_before_multi) + ', ' +
      repr(switch_up_octets_before_multi) + ', ' + repr(switch_up_time_before_multi) + ', ' +
      repr(switch_dl_octets_after) + ', ' + repr(switch_dl_time_after) + ', ' +
      repr(switch_up_octets_after) + ', ' + repr(switch_up_time_after)
      )

driver.close()
