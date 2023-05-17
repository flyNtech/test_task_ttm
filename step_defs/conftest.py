import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import logging
import os
from datetime import datetime

loaded_page_xpath = '/html/body/div[2]/header'
if not os.path.exists('logs'):
    os.makedirs('logs')
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver


@pytest.fixture(scope="session")
def elements_data():
    return {
        "Catalog": "catalogPopupButton",
        "Smartphones": '//*[@id="catalogPopup"]/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/ul/li[1]',
        "Smartphones page": "market.yandex.ru/catalog--smartfony",
        "Max price parameter": '[id^="range-filter-field-glprice_"][id$="_max"]',
        "Screen Size parameter": '[id^="range-filter-field-14805766_"][id$="_min"]',
        "Brands": '//*[@id="searchFilters"]/div/div[3]/div/div/div/div/div[4]/div/fieldset/div/div/div/div/div/div/label',
        "Search result": '//*[@data-auto="snippet-title-header"]',
        "End of the page": "return window.scrollY + window.innerHeight >= document.documentElement.scrollHeight*0.87;",
        "Sorting option": 'по рейтингу',
        "Price, Rating, Discount": '//*[@id="serpTop"]/div/div/div[1]/div/div/noindex/div/button',
        "Rating": '[data-auto="rating-badge-value"]'
    }

@pytest.fixture(scope="session")
def logger(request):

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(f"logs/{current_datetime}.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger