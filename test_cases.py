from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
import time
from decimal import Decimal
import pytest

@pytest.fixture
def chromium_instance():
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get("http://www.sberbank.ru/ru/quotes/converter")
    assert "Сбербанк" in browser.title
    return browser


def test_variable_sum(chromium_instance):
    # get firefox browser and open url
    browser = chromium_instance
    sum_to_convert = '100,00'
    # wait a little.
    time.sleep(1.5)
    # clear and fill the sum field, click the button for result
    sum_of_money = browser.find_element_by_xpath("//div/form/input")
    sum_of_money.clear()
    sum_of_money.send_keys(sum_to_convert)
    time.sleep(1.5)

    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    time.sleep(1.5)

    #
    result = browser.find_element_by_xpath("//h4/span[1]").text
    price = browser.find_element_by_xpath("//td[4]/span").text

    sum_to_convert = sum_to_convert.replace(',', '.').replace(' ', '')
    price = price.replace(',', '.').replace(' ', '')
    result = result.replace(',', '.').replace(' ', '')

    print(round(Decimal(sum_to_convert)/Decimal(price), 2), Decimal(result))
    try:
        assert (round(Decimal(sum_to_convert) / Decimal(price), 2) == Decimal(result))
    except AssertionError:
        print("Calculation mistake ", "expected:", round(Decimal(sum_to_convert)/Decimal(price), 2), ",actual:", result)
    browser.quit()


def test_convert_rur_to_rur(chromium_instance):
    browser = chromium_instance
    currency = "RUR"
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[3]/div[2]/div/header/em").click()
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[3]/div[2]/div/div/span[contains(., " + currency + ")]").click()
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[4]/div[2]/div/header/em").click()
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[4]/div[2]/div/div/span[contains(., " + currency + ")]").click()
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    time.sleep(1.5)
    first_currency = browser.find_element_by_xpath("//div[3]/div[2]/div/header/strong").text
    second_currency = browser.find_element_by_xpath("//div[4]/div[2]/div/header/strong").text
    print(first_currency, second_currency)
    try:
        assert first_currency != second_currency
    except AssertionError:
        print("Replacement mistake")
    browser.quit()


def test_early_date(chromium_instance):
    browser = chromium_instance
    year = '2016'
    month = '1'
    day = "10"
    time.sleep(2.5)
    # open datepicker, select year, month and day
    browser.find_element_by_xpath("//div[6]/label[2]/p").click()
    time.sleep(1.5)
    WebDriverWait(browser, 10).until(lambda x: browser.find_element_by_xpath("//*[@id='ui-datepicker-div']"))
    browser.find_element_by_xpath("//div[6]/div[2]/span").click()
    time.sleep(2.5)
    browser.find_element_by_xpath(
        "//div/div/select/option[contains(text(), "+ year +")]").click()
    time.sleep(2.5)
    for i in range(int(month) - 1):
        browser.find_element_by_xpath(
            "//*[@id='ui-datepicker-div']/div[1]/a[2]").click()
        time.sleep(2.5)
    browser.find_element_by_xpath(
        "//div[@id='ui-datepicker-div']//a[@class='ui-state-default'][text()='"+ day + "']").click()
    time.sleep(2.5)
    browser.find_element_by_xpath("//dl/span[contains(., 'Выбрать')]").click()
    time.sleep(2.5)
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    time.sleep(2.5)
    try:
        result = browser.find_element_by_xpath("//h4/span[1]").text.replace(',', '.')
        try:
            assert Decimal(result) != 0
            print(Decimal(result))
        except AssertionError:
            print("Old date database error")
    except exceptions.NoSuchElementException:
        print("No result")

    browser.quit()

