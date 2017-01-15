from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from decimal import Decimal
import pytest
import time
import allure
import csv

testparams = []
with open('test_data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        testparams.append(row)


@pytest.fixture
def chromium_instance():
    """
    Fixture. Start chromedriver.
    :return:
    """
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get("http://www.sberbank.ru/ru/quotes/converter")
    browser.implicitly_wait(20)
    try:
        assert "Сбербанк" in browser.title
        return browser
    except exceptions.NoSuchElementException:
        print("Site is unreachable")


@allure.testcase("Check_converting")
@pytest.mark.parametrize(testparams[0][0], testparams[0][1:])
def test_variable_sum(chromium_instance, sum_to_convert):
    """
    Test different variables to convert from RUR to USD and check result.
    :param chromium_instance:
    :param sum_to_convert:
    :return:
    """
    browser = chromium_instance
    browser.implicitly_wait(10)
    sum_of_money = browser.find_element_by_xpath("//div/form/input")
    sum_of_money.clear()
    time.sleep(2)
    sum_of_money.send_keys(sum_to_convert)
    time.sleep(1)
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH,
                                                                 "//div[7]/button[contains(., 'Показать')]")))
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH,
                                                                 "//h4/span[1]")))
    result = browser.find_element_by_xpath("//h4/span[1]").text
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH,
                                                                 "//td[4]/span")))
    price = browser.find_element_by_xpath("//td[4]/span").text
    sum_to_convert = sum_to_convert.replace(',', '.').replace(' ', '')
    price = price.replace(',', '.').replace(' ', '')
    result = result.replace(',', '.').replace(' ', '')
    try:
        assert (round(Decimal(sum_to_convert) / Decimal(price), 2) == Decimal(result))
    finally:
        browser.quit()


@allure.testcase("Same_currencies")
@pytest.mark.parametrize(testparams[1][0], testparams[1][1:])
def test_convert_rur_to_rur(chromium_instance, currency):
    """
    Test converting same currencies (for example: RUR to RUR).
    :param chromium_instance:
    :param currency:
    :return:
    """
    browser = chromium_instance
    browser.find_element_by_xpath("//div[3]/div[2]/div/header/em").click()
    browser.find_element_by_xpath("//div[3]/div[2]/div/div/span[contains(., " + currency + ")]").click()
    browser.find_element_by_xpath("//div[4]/div[2]/div/header/em").click()
    browser.find_element_by_xpath("//div[4]/div[2]/div/div/span[contains(., " + currency + ")]").click()
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    first_currency = browser.find_element_by_xpath("//div[3]/div[2]/div/header/strong").text
    second_currency = browser.find_element_by_xpath("//div[4]/div[2]/div/header/strong").text
    try:
        assert first_currency != second_currency
    finally:
        browser.quit()


@allure.testcase("Old dates")
@pytest.mark.parametrize(testparams[2][0], testparams[2][1:])
@pytest.mark.parametrize(testparams[3][0], testparams[3][1:])
@pytest.mark.parametrize(testparams[4][0], testparams[4][1:])
def test_early_date(chromium_instance, year, month, day):
    """
    Test converting with different dates.
    :param chromium_instance:
    :param year:
    :param month:
    :param day:
    :return:
    """
    browser = chromium_instance
    browser.find_element_by_xpath("//div[6]/label[2]/p").click()
    WebDriverWait(browser, 10).until(
        lambda x: browser.find_element_by_xpath("//*[@id='ui-datepicker-div']"))
    browser.find_element_by_xpath("//div[6]/div[2]/span").click()
    WebDriverWait(browser, 10).until(
        lambda x: browser.find_element_by_xpath("//div/div/select/option[contains(text(), " + year + ")]"))
    browser.find_element_by_xpath(
        "//div/div/select/option[contains(text(), " + year + ")]").click()
    for i in range(int(month) - 1):
        browser.find_element_by_xpath(
            "//*[@id='ui-datepicker-div']/div[1]/a[2]").click()
    browser.find_element_by_xpath(
        "//div[@id='ui-datepicker-div']//a[@class='ui-state-default'][text()='"+ day + "']").click()
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH,
                                                                 "//dl/span[contains(., 'Выбрать')]")))
    browser.find_element_by_xpath("//dl/span[contains(., 'Выбрать')]").click()
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH,
                                                                 "//div[7]/button[contains(., 'Показать')]")))
    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    time.sleep(1)
    try:
        result = browser.find_element_by_xpath("//h4/span[1]").text.replace(',', '.')
        assert Decimal(result) != 0
    finally:
        browser.quit()
