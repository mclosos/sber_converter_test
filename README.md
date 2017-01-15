# sber_converter_test
<b>Packets</b>:
<pre>
pytest==2.9.0
pytest-allure-adaptor==1.7.6
selenium==3.0.2
</pre>

<b>Test target URL:</b> http://www.sberbank.ru/ru/quotes/converter

Webdriver is specified in fixture:
<pre>
browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
</pre>

<b>Test data:</b>
<pre>
test_data.csv 
</pre>
as rows like
<pre>
({parameter_name},{value1},...{valueN})
</pre>

<b>How_To_Start:</b>
<pre>
python -m pytest --alluredir reports/
</pre>

_Result_: xml allure report
