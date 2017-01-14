from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from decimal import Decimal
import pytest


@pytest.fixture
def chromium_instance():
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get("http://www.sberbank.ru/ru/quotes/converter")
    assert "Сбербанк" in browser.title
    return browser


@pytest.mark.parametrize("sum_to_convert", ["1,50", "100,00", "99999999999,00"])
def test_variable_sum(chromium_instance, sum_to_convert):
    # get firefox browser and open url
    browser = chromium_instance

    # wait a little.
    browser.implicitly_wait(10)
    # clear and fill the sum field, click the button for result
    sum_of_money = browser.find_element_by_xpath("//div/form/input")
    sum_of_money.clear()
    sum_of_money.send_keys(sum_to_convert)
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    browser.implicitly_wait(10)
    #
    result = browser.find_element_by_xpath("//h4/span[1]").text
    price = browser.find_element_by_xpath("//td[4]/span").text
    sum_to_convert = sum_to_convert.replace(',', '.').replace(' ', '')
    price = price.replace(',', '.').replace(' ', '')
    result = result.replace(',', '.').replace(' ', '')
    browser.quit()
    print(round(Decimal(sum_to_convert)/Decimal(price), 2), Decimal(result))
    try:
        assert (round(Decimal(sum_to_convert) / Decimal(price), 2) == Decimal(result))
    finally:
        browser.quit()


@pytest.mark.parametrize("currency", [i for i in range(1, 7)])
def test_convert_rur_to_rur(chromium_instance, currency):
    browser = chromium_instance
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//div[3]/div[2]/div/header/em").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//div[3]/div[2]/div/div/span[contains(., " + str(currency) + ")]").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//div[4]/div[2]/div/header/em").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//div[4]/div[2]/div/div/span[contains(., " + str(currency) + ")]").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    browser.implicitly_wait(10)
    first_currency = browser.find_element_by_xpath("//div[3]/div[2]/div/header/strong").text
    second_currency = browser.find_element_by_xpath("//div[4]/div[2]/div/header/strong").text
    browser.quit()
    print(first_currency, second_currency)
    try:
        assert first_currency != second_currency
    finally:
        browser.quit()


@pytest.mark.parametrize("year", ["2016", "2015", "2012", "2008", "2003", "2002"])
@pytest.mark.parametrize("month", ["11", "12", "2", "8", "6", "1"])
@pytest.mark.parametrize("day", ["10", "31", "29", "15", "25", "1"])
def test_early_date(chromium_instance, year, month, day):
    browser = chromium_instance
    browser.implicitly_wait(10)
    # open datepicker, select year, month and day
    browser.find_element_by_xpath("//div[6]/label[2]/p").click()
    WebDriverWait(browser, 10).until(lambda x: browser.find_element_by_xpath("//*[@id='ui-datepicker-div']"))
    browser.find_element_by_xpath("//div[6]/div[2]/span").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath(
        "//div/div/select/option[contains(text(), "+ year +")]").click()
    browser.implicitly_wait(10)
    for i in range(int(month) - 1):
        browser.find_element_by_xpath(
            "//*[@id='ui-datepicker-div']/div[1]/a[2]").click()
        browser.implicitly_wait(10)
    browser.find_element_by_xpath(
        "//div[@id='ui-datepicker-div']//a[@class='ui-state-default'][text()='"+ day + "']").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//dl/span[contains(., 'Выбрать')]").click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    browser.implicitly_wait(10)
    result = browser.find_element_by_xpath("//h4/span[1]").text.replace(',', '.')
    browser.quit()
    try:
        assert Decimal(result) != 0
    finally:
        browser.quit()


