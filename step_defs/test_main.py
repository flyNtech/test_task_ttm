# test_main.py

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pytest_bdd import scenarios, given, when, then, parsers
from step_defs.conftest import browser, elements_data, loaded_page_xpath, logger


scenarios('../feature/test_case.feature')
global rating_out


def get_status(browser):
    try:
        browser.execute(Command.STATUS)
        return True
    finally:
        return False


def check_captcha(browser, logger):
    first_iteration = True
    while 'market.yandex.ru/showcaptcha' in browser.current_url:
        logger.warning('Требуется решение капчи...')
        # Иногда достаточно нажатие кнопки для решения капчи
        if first_iteration:
            browser.find_element("class name", "CheckboxCaptcha-Anchor").click()
            logger.info('Капча была автоматически решена!')
            first_iteration = False
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(('xpath', loaded_page_xpath)))
        # Но бывает усложненная с вводом слов с картинки
        else:
            try:
                logger.warning('Необходим ручной ввод капчи...')
                WebDriverWait(browser, 60).until(EC.presence_of_element_located(('xpath', loaded_page_xpath)))
                logger.info('Капча была решена вручную!')
            except TimeoutException:
                logger.error('Время на решение капчи вышло!')
                raise Exception('Время на решение капчи вышло!')


@given(parsers.parse('the browser is open and maximized'))
def browser(browser, logger):
    browser.maximize_window()
    logger.info('Браузер открыт на весь экран')


@when(parsers.parse('the user navigates to the "{url}" page'))
def navigate_to_url(browser, url, logger):
    browser.get(f'https://{url}')
    logger.info(f'Переходим на {url} ...')
    check_captcha(browser, logger)


@then(parsers.parse('the page should load successfully'))
def page_should_be_loaded(browser, logger):
    assert browser.find_element('xpath', loaded_page_xpath)
    logger.info('Страница была загружена!')


@when(parsers.parse('the user clicks on "{catalog}" and select "{smartphones}" subcategory'))
def clicks_on_catalog(browser, elements_data, catalog, smartphones, logger):
    browser.find_element('id', elements_data[catalog]).click()
    logger.info('Кликаем на "Каталог" и ждем прогрузки...')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(('xpath', elements_data[smartphones])))
    browser.find_element('xpath', elements_data[smartphones]).click()
    logger.info('Кликаем на "Смартфоны и ждем прогрузки..."')
    check_captcha(browser, logger)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(('xpath', loaded_page_xpath)))


@then(parsers.parse('the "{smartphones_page}" should be displayed'))
def page_should_be_smartphones(browser, smartphones_page, elements_data, logger):
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(('id', 'searchFilters')))
    assert elements_data[smartphones_page] in browser.current_url
    logger.info('Страница "Смартфоны" прогружена!')


@when(parsers.parse('the user sets "{max_price}" to "{price}" Rubles and "{screen_size}" from "{size}" inches'))
def sets_price_size(browser, elements_data, max_price, price, screen_size, size, logger):
    logger.info('Заполняем формы с ценой и размером экрана...')
    browser.find_element('css selector', elements_data[max_price]).send_keys(price)
    browser.find_element('css selector', elements_data[screen_size]).send_keys(size)


@then(parsers.parse('the search parameters should be updated'), logger)
def check_search_parameters(browser, elements_data, max_price, price, screen_size, size, logger):
    assert browser.find_element('css selector', elements_data[max_price]).get_attribute("value") == price
    assert browser.find_element('css selector', elements_data[screen_size]).get_attribute("value") == size
    logger.info('Заполнили формы с ценой и размером экрана!')

@when(parsers.parse('the user selects at least 5 {brands} from the list'))
def select_brands(browser, elements_data, brands, logger):
    logger.info('Сейчас кликаем на бренды в фильтрах...')
    for brands in browser.find_elements('xpath', elements_data[brands]):
        brands.click()


@then(parsers.parse('at least {min_count:d} {brands} are selected in the search parameters'))
def check_brands_count(browser, min_count, brands, elements_data, logger):
    count_brands = 0
    for brand in browser.find_elements('xpath', f'{elements_data[brands]}/span/span/span'):
        count_brands += int(brand.value_of_css_property('opacity'))
    try:
        assert count_brands >= min_count
    except AssertionError:
        logger.error(f'Количество ({count_brands}) не соответствует мин. значению: {min_count}')
        raise Exception(f'Количество ({count_brands}) не соответствует мин. значению: {min_count}')
    logger.info(f'Количество соответствует мин. значению: {min_count}')
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located(('xpath', f'//*[@data-auto="filter-found-visible-tooltip"]')))


@when(parsers.parse('the user counts the number of smartphones on one page'))
def count_smartphones(browser, logger):
    logger.info('Результаты поиска обновились, крутим до конца страницы...')
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


@then(parsers.parse('the count in {search_result} should be more than {number:d}'))
def check_count_smartphones(browser, search_result, number, elements_data, logger):
    logger.info('Считаем количество телефонов...')
    count_smartphones = len(browser.find_elements('xpath', elements_data[search_result]))
    try:
        assert count_smartphones > number
    except AssertionError:
        logger.error(f'Смартфоны не найдены!')
        raise Exception(f'Смартфоны не найдены!')
    logger.info(f'Насчитали: {count_smartphones}')


@when(parsers.parse('the user is at the {end_of_page}'))
def scroll_to_end_page(browser, elements_data, end_of_page, logger):
    assert browser.execute_script(
        "return window.scrollY + window.innerHeight >= document.documentElement.scrollHeight*0.87;")
    logger.info(f'Находимся снизу страницы')

@then(parsers.parse('the user should remember the last smartphone in {search_result}'))
def remember_last_phone(browser, search_result, elements_data, logger):
    count_smartphones = len(browser.find_elements('xpath', elements_data[search_result]))
    try:
        logger.info(f'Ищем последний из списка...')
        last_smartphone_name = browser.find_elements('xpath', f'{elements_data[search_result]}')[count_smartphones-1].text
    except NoSuchElementException:
        logger.error('Телефон не найден!')
        raise Exception('Телефон не найден!')
    elements_data["Remembered smartphone"] = last_smartphone_name
    logger.info(f'Запомнили смартфон: {last_smartphone_name}')


@when(parsers.parse('the user changes the {sorting} to a different one ({sorting_xpath})'))
def change_sorting(browser, sorting, sorting_xpath, elements_data, logger):
    logger.info(f'Ищем сортировку {elements_data[sorting]}...')
    for button_sort in browser.find_elements('xpath', elements_data[sorting_xpath]):
        if elements_data[sorting] in button_sort.text:
            logger.info(f'Кликаем на "{elements_data[sorting]}"...')
            button_sort.click()
            try:
                WebDriverWait(browser, 10).until(EC.staleness_of((browser.find_element('xpath', f'//*[@data-auto="snippet-title-header"]'))))
            except TimeoutException:
                logger.error('Результаты поиска не были обновлены!')
                raise Exception('Результаты поиска не были обновлены!')


@then(parsers.parse('the search results should be updated accordingly'))
def check_change_sorting(browser, elements_data, logger):
    for button_sort in browser.find_elements('xpath', elements_data['Price, Rating, Discount']):
        if button_sort.text == elements_data['Sorting option']:
            assert button_sort.get_attribute('aria-pressed') == 'true'
            logger.info(f'Сортировка "{elements_data["Sorting option"]}" успешно выставлена!')


@when(parsers.parse('the user looking for the {smartphone_name} in {search_result} and click on it'))
def search_remembered_phone(browser, smartphone_name, search_result, elements_data, logger):
    logger.info(f'Опять крутим вниз страницы для прогрузки...')
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        browser.find_element('xpath', f'//*[contains(text(), "{elements_data[smartphone_name]}")]').click()
        logger.info('Телефон был успешно обнаружен!')
    except NoSuchElementException:
        logger.error('Телефон после изменения сортировки найден не был!')
        raise Exception("Телефон после изменения сортировки найден не был!")


@then(parsers.parse('the user should see the page and {rating} of the selected smartphone'))
def remembered_phone_page(browser, rating, elements_data, logger):
    logger.info('Переключаем драйвер на окно смартфона...')
    browser.switch_to.window(browser.window_handles[-1])
    check_captcha(browser, logger)
    try:
        assert elements_data['Remembered smartphone'] in browser.title
    except AssertionError:
        logger.error('Ошибка загрузки страницы смартфона!')
        raise Exception('Ошибка загрузки страницы смартфона!')
    logger.info(f'Страница была успешно открыта. Подргужаем и ищем рейтинг...')
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    rating_out = browser.find_element("css selector", elements_data[rating]).text
    while rating_out == '':
        rating_out = browser.find_element("css selector", elements_data[rating]).text
    logger.info(f'Телефон: {elements_data["Remembered smartphone"]}\nРейтинг: {rating_out}')


@when(parsers.parse('the user closes the browser'))
def close_browser(browser, logger):
    logger.info('Закрываем браузер...')
    browser.quit()


@then(parsers.parse('the browser should close successfully'))
def check_browser_status(browser, logger):
    logger.info('Браузер был успешно закрыт!')
    assert not get_status(browser)
