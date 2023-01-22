import time

import numpy
import tensorflow
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1400,2100")
    chrome_options.add_argument("disable-gpu")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.headless = True
    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return myDriver


def makePrediction(driver: webdriver.Chrome, stock_code: str) -> str:
    wait = WebDriverWait(driver, 30)
    driver.get("https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Tarihsel-Fiyat-Bilgileri.aspx")

    chosenStockBar = driver.find_element(By.XPATH,
                                         "//span[@aria-labelledby='select2-ctl00_ctl58_g_0d19e9f2_2afd_4e5a_9a92_57c4ab45c57a_ctl00_ddlHisseSec-container']")
    wait.until(expected_conditions.element_to_be_clickable(chosenStockBar))
    ActionChains(driver).pause(1).click(chosenStockBar).perform()

    searchBar = driver.find_element(By.XPATH, "//input[@class='select2-search__field']")
    wait.until(expected_conditions.element_to_be_clickable(searchBar))
    ActionChains(driver).click(searchBar).send_keys(stock_code).send_keys(Keys.ENTER).pause(1).perform()

    selectedStockBar = driver.find_element(By.XPATH, "(//span[@class='selection'])[2]")
    if not selectedStockBar.text.lower().__contains__(stock_code):
        return "There is no stock with given stock code: " + stock_code

    priceType = driver.find_element(By.XPATH, "//span[@aria-labelledby='select2-ddlFiyatSec-container']")
    wait.until(expected_conditions.element_to_be_clickable(priceType))
    priceType.click()

    unchangedPriceType = driver.find_element(By.XPATH, "(//li[@role='treeitem'])[2]")
    wait.until(expected_conditions.element_to_be_clickable(unchangedPriceType))
    unchangedPriceType.click()

    getStockDataButton = driver.find_element(By.XPATH, "//a[@id='btnGetHisseTekil']")
    wait.until(expected_conditions.element_to_be_clickable(getStockDataButton))
    getStockDataButton.click()

    data = numpy.ndarray((1, 30, 12))
    numberOfRows = len(driver.find_elements(By.XPATH, "//td[@class='sorting_1']"))
    time.sleep(2)
    dataFields = driver.find_elements(By.XPATH, "//td[@class='text-right']")
    wait.until(expected_conditions.element_to_be_clickable(dataFields[-1]))
    print(len(dataFields) / 12)
    for i in range(30):
        for j in range(12):
            if dataFields[(numberOfRows - 30 + i) * 12 + j].text == "":
                data[0][i][j] = 0
            else:
                data[0][i][j] = float(
                    dataFields[(numberOfRows - 30 + i) * 12 + j].text.replace(".", "").replace(",", "."))

    loaded_model = tensorflow.keras.models.load_model("./model2.h5")
    return str(loaded_model.predict(data)[0][29][1])
