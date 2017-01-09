# -*- coding: utf-8 -*-

from selenium import webdriver
import time
from decimal import *

def test_variable_sum(sum_to_convert):
    #get firefox browser and open url
    browser =  webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get("http://www.sberbank.ru/ru/quotes/converter")
    assert "Сбербанк" in browser.title
    #wait a little.
    time.sleep(1.5)

    sum_of_money = browser.find_element_by_xpath("//div/form/input")
    sum_of_money.clear()
    sum_of_money.send_keys(sum_to_convert)
    time.sleep(1.5)

    browser.find_element_by_xpath("//div[7]/button[contains(., 'Показать')]").click()
    time.sleep(1.5)

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


def test_convert_rur_to_rur(currency):

    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get("http://www.sberbank.ru/ru/quotes/converter")
    assert "Сбербанк" in browser.title

    time.sleep(1.5)
    browser.find_element_by_xpath("//div[3]/div[2]/div/header/em").click()
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[1]/div[1]/div[3]/div[2]/div/div/span["+ currency +"]").click()
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[4]/div[2]/div/header/em").click()
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[4]/div[2]/div/div/span[" + currency + "]").click()
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
