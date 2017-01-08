# -*- coding: utf-8 -*-

from selenium import webdriver
import time

#get firefox browser and open url
browser =  webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
browser.get("http://www.sberbank.ru/ru/quotes/converter")
assert "Сбербанк" in browser.title
sum_to_convert = "1.5"
#wait a little.
time.sleep(1.5)

sum_of_money = browser.find_element_by_xpath("//div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div/div/aside/div[1]/div[1]/div[2]/div/form/input")
sum_of_money.clear()
sum_of_money.send_keys(sum_to_convert)
time.sleep(1.5)


browser.find_element_by_xpath("//div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div/div/aside/div[1]/div[7]/button").click()
time.sleep(1.5)

new_sum = browser.find_element_by_xpath("//div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div/div/aside/div[1]/div[1]/div[2]/div/form/input").text
result = browser.find_element_by_xpath("//div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div/div/aside/div[2]/h4/span[1]").text
price = browser.find_element_by_xpath(".//*[@id='main']/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div[1]/div/div[1]/table/tbody/tr/td[4]/span").text
print(result)
print(price)
print(sum_to_convert)
print(round(float(sum_to_convert.replace(',','.'))/float(price.replace(',','.')), 2) == float(result.replace(',','.')))
assert (round(float(sum_to_convert.replace(',','.'))/float(price.replace(',','.')), 2) == float(result.replace(',','.')))

browser.quit()