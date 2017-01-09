import test_cases
#test_case_1
test_cases.test_variable_sum("1,50")
test_cases.test_variable_sum("100,00")
test_cases.test_variable_sum("99999999999,00")

#test_case_2
for i in range(1,7):
    test_cases.test_convert_rur_to_rur(str(i))

