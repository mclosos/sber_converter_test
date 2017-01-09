import test_cases

# test_case_1
test_cases.test_variable_sum("1,50")
test_cases.test_variable_sum("100,00")
test_cases.test_variable_sum("99999999999,00")

# test_case_2
for i in range(1,7):
    test_cases.test_convert_rur_to_rur(str(i))

# test_case_3
test_cases.test_early_date("22.02.2002 15:35")
test_cases.test_early_date("01.01.2002 00:00")
test_cases.test_early_date("31.12.2007 23:59")
test_cases.test_early_date("29.02.2008 08:59")
test_cases.test_early_date("29.02.2009 08:59")
test_cases.test_early_date("03.01.2015 08:59")