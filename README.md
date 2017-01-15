# sber_converter_test

_Test target URL:_ http://www.sberbank.ru/ru/quotes/converter

Webdriver specified in fixture:
<pre>
browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
</pre>

_Test data:_
<pre>
test_data.csv 
</pre>
as rows like
<pre>
({parameter_name},{value1},...{valueN})
</pre>

_How_To_Start:_
<pre>
python -m pytest --alluredir reports/
</pre>

_Result_: xml allure report
