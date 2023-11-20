"""
Test script for module a1

When run as a script, this module invokes several procedures that 
test the various functions in the module a1.

Author: Jessica Andrews (jaa375), Aileen Huang (aeh245)
Date:   9/21/22
"""
import introcs
import a1


def testA():
    """
    Test procedure for Part A  <<I REARRANGED THESE
    """   
    #testing single space for before_space
    input='4.502 Euros'
    result1=a1.before_space(input)
    introcs.assert_equals("4.502",result1)
    #testing single space for after_space
    result2=a1.after_space(input)  
    introcs.assert_equals("Euros",result2)

    #testing integer input for before_space
    input='4 Euros '
    result1=a1.before_space(input)
    introcs.assert_equals("4",result1)
    #testing integer input for after_space
    result2=a1.after_space(input)
    introcs.assert_equals("Euros ",result2) 
     
    #testing space at beginning for before_space
    input=' 1.5Euros'
    result1=a1.before_space(input)
    introcs.assert_equals("",result1)
    #testing space at beginning for after_space
    result2=a1.after_space(input)
    introcs.assert_equals("1.5Euros",result2)

    #testing space for before_space
    input='1.5Euros '
    result1=a1.before_space(input)
    introcs.assert_equals("1.5Euros",result1)
    #testing space for after_space
    result2=a1.after_space(input)
    introcs.assert_equals("",result2)

    #testing space in the middle of word for before_space
    input='2.39Eur os'
    result1=a1.before_space(input)
    introcs.assert_equals("2.39Eur",result1)
    #testing space in the middle of word for before_space
    result2=a1.after_space(input)
    introcs.assert_equals("os",result2) 
    
    #testing no spaces
    #input='2.23Euros'
    #result1=a1.before_space(input)
    #result2=a1.after_space(input)
    #introcs.assert_equals("2.23",result1)
    #introcs.assert_equals("Euros",result2) 

    #testing spaces in between digits of a float for before_space
    input='2.2     3Euros'
    result1=a1.before_space(input)
    introcs.assert_equals("2.2",result1)
    #testing spaces in between digits of a float for after_space
    result2=a1.after_space(input)
    introcs.assert_equals("    3Euros",result2) 
    pass
    
   

def testB():
    """
    Test procedure for Part B
    """

     #testing empty string inside double quotes for first_inside_quotes
    input = '""'
    result1 = a1.first_inside_quotes(input)
    introcs.assert_equals('', result1)
    

    #tests word in quotes for first_inside_quotes
    input='  "word"'
    result2=a1.first_inside_quotes(input)
    introcs.assert_equals('word',result2)

    #tests word in quotes in word for first_inside_quotes
    input='  anoth"erword"s'
    result3=a1.first_inside_quotes(input)
    introcs.assert_equals("erword",result3)

    #testing words with spaces inside double quotes for first_inside_quotes
    input = ' "ok      more   words"  '
    result4 = a1.first_inside_quotes(input)
    introcs.assert_equals('ok      more   words', result4)

    #testing more than one pair of quotes for first_inside_quotes 
    input = ' "ok"some "words"  '
    result4 = a1.first_inside_quotes(input)
    introcs.assert_equals('ok', result4)

    #testing where all characters are inside double quotes for first_inside quotes
    input = '"fjelwdnlwen"'
    result5 = a1.first_inside_quotes(input)
    introcs.assert_equals('fjelwdnlwen', result5)

    #Testing example of correct input for lhs
    input= '{ "lhs":"2 Namibian Dollars", "rhs":"2 Lesotho Maloti", "err": "" }'
    result1=a1.get_lhs(input)
    introcs.assert_equals('2 Namibian Dollars',result1)
    #Testing example of correct input for rhs
    result2=a1.get_rhs(input)
    introcs.assert_equals('2 Lesotho Maloti', result2)
    #Testing example of correct input for has_error
    result3=a1.has_error(input)
    introcs.assert_equals(False, result3)  

    #Testing example of incorrect conversion for lhs
    input= '{ "lhs":"2 Namibian Dollars", "rhs":"1 Lesotho Maloti", "err": "" }'
    result1=a1.get_lhs(input)
    introcs.assert_equals('2 Namibian Dollars',result1)
    #Testing example of incorrect conversion for rhs
    result2=a1.get_rhs(input)
    introcs.assert_equals('1 Lesotho Maloti', result2)
    #Testing example of incorrect conversion for has_error
    result3=a1.has_error(input)
    introcs.assert_equals(False, result3) 

    #Testing when there is an error statement for lhs
    a = '{ "lhs" : "2 Namibian Dollars", "rhs" : "2 Lesotho Maloti",'
    b = ' "err" : "Currency amount is invalid." }'
    input= a + b
    result1=a1.get_lhs(input)
    introcs.assert_equals('2 Namibian Dollars',result1)
    #Testing when there is an error statement for lhs
    result2=a1.get_rhs(input)
    introcs.assert_equals('2 Lesotho Maloti', result2)
    #Testing when there is an error statement for has_error
    result3=a1.has_error(input)
    introcs.assert_equals(True, result3)
    pass
    

    

def testC():

    """
    Test procedure for Part C
    """
    # testing the example from assignment 1 for query_webite
    result1= a1.query_website('USD','CUP',2.5)
    a='{ "lhs" : "2.5 United States Dollars", "rhs" : '
    b='"64.375 Cuban Pesos", "err" : "" }'
    introcs.assert_equals(a+b,result1)

    #testing when entering a wrong currency type (USDD) for query_website
    result1=a1.query_website('USDD','CUP',3.0)
    a='{ "lhs" : "", "rhs" : "", "err" : '
    b='"Source currency code is invalid." }'
    introcs.assert_equals(a+b, result1)

    #testing when amt has more than two decimal places for query_website
    result1=a1.query_website('USD','EUR', 3.5555555)
    a='{ "lhs" : "3.5555555 United States Dollars", '
    b='"rhs" : "3.580792832939 Euros", "err" : "" }'
    introcs.assert_equals(a+b, result1) 
    
    #testing lower case for query_website
    result1=a1.query_website('usd','eur', 3.45)
    a='{ "lhs" : "", "rhs" : "", "err" : '
    b='"Source currency code is invalid." }'
    introcs.assert_equals(a+b, result1)

    #testing empty string for query_website
    result1 = a1.query_website("","",3.5)
    a='{ "lhs" : "", "rhs" : "", "err" : '
    b='"Source currency code is invalid." }'
    introcs.assert_equals(a+b, result1)
  
    pass




def testD():
    """
    Test procedure for Part D
    """
    #testing all uppercase 3-letter currency code for is_currency
    result1 = a1.is_currency('USD')
    introcs.assert_equals (True, result1)
    #testing all uppercase 4-letter currency code for is_currency
    result1=a1.is_currency('EURO')
    introcs.assert_equals (False, result1)  
    #testing all lowercase 3-letter currency code for is_currency
    result1= a1.is_currency('usd')
    introcs.assert_equals (False, result1)
    #Testing empty string for is_currency 
    result1 = a1.is_currency("")
    introcs.assert_equals (False, result1)


    #testing exchange function
    #testing correct conversion for exchange
    resulta=a1.exchange('USD','CUP',2.5)
    introcs.assert_floats_equal(64.375,resulta)
    #testing conversion to USD for exchange
    resulta=a1.exchange('CHF','USD',300.0)
    introcs.assert_floats_equal(306.15650108022,resulta)
    #testing conversion back for exchange
    resulta=a1.exchange('USD','CHF',306.15650108022)
    introcs.assert_floats_equal(300.0,resulta)
    
    pass


testA()
testB()
testC()
testD()
print('Module a1 passed all tests.')
