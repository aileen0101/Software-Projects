
"""
Module for currency exchange

This module provides several string parsing functions to implement a 
simple currency exchange routine using an online currency service. 
The primary function in this module is exchange.

Author: Jessica Andrews (jaa375), Aileen Huang (aeh245)
Date:   9/21/22
"""

def before_space(s):
   """Returns a copy of s up to, but not including, the 
   first space

   Find the location of the first space
   Store and return all characters from the beginning of the
   string to (not including) the first space

   Parameter s: the string to slice
   Precondition: s is a string with at least one space"""

  #start=3
   start = s.find(' ')
   beforespace = s[:start]
   #print (beforespace, "does it work")
   return beforespace

  
def after_space(s):
   """Returns a copy of s after the first space. 

   Find the location of the first space   
   Store and return all characters after the first space
   
   Parameter s: the string to slice
   Precondition: s is a string with at least one space"""
  
   start = s.find(' ')
   afterspace = s[start + 1:]
   return afterspace
  
def first_inside_quotes(s):
  """Returns the first substring of s between two (double) 
  quotes
  
  A quote character is one that is inside a string, not one that 
  delimits it.  We typically use single quotes (') to 
  delimit a 
  string if want to use a double quote character (") 
  inside of it.

  Find the location (represented by index number) of the first quote
  Store all characters following the first quote into the variable everything
  Find the location of the second quote within everything
  Return all characters from the beginning of the first quote (noninclusive)
  to the location of the second quote (noninclusive) 
  
  Examples:
  first_inside_quotes('A "B C" D') returns 'B C'
  first_inside_quotes('A "B C" D "E F" G') returns 'B C', 
  because it only picks the first such substring
  
  Parameter s: a string to search
  Precondition: s is a string containing at least two 
  double quotes"""
  """ first=s.index('"')
  last=s.index('"',first+1)
  word=s[first+1:last]"""
  
  start = s.index('"')
  everything = s[start + 1:]
  end = everything.index('"')
  return everything[:end]


def get_lhs(json):
  """Returns the lhs value in the response to a currency 
   query
  
  Given a JSON response to a currency query, this returns 
  the 
  string inside double quotes (") immediately following 
  the keyword
  "lhs". For example, if the JSON is
      
  '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros", 
  "err" : "" }'
  
  then this function returns '1 Bitcoin' (not '"1 
   Bitcoin"').  
  
  This function returns the empty string if the JSON 
  response
  contains an error message.

  Find the string inside the first set of double quotes after "lhs" 
  using first_inside_quotes: 
  Splice the json string to include the first set of double quotes 
  after lhs
  Use first_inside_quotes function on the spliced json string
  
  Parameter json: a json string to parse
  Precondition: json is the response to a currency 
  query"""

  lhs_index=json.index("lhs")#==3 or the index of first letter of lhs
  start = json.index('"',lhs_index+4) #the index of the first " after lhs
  lhstotheend = json[start:] #splice json from first "" to the end of the json string
  lhs_string = first_inside_quotes(lhstotheend) 
  return lhs_string.strip()

  #Alternative method
  
  #lhs_index=json.index("lhs") #==3  
  #start = json[lhs_index + 4:] #take everything after the "
  #end = start.index('"') #find the index of first double quote after lhs
  #return start[:end] #this should return "1 Bitcoin"
  #print("it worked")
  
  return lhs

  
def get_rhs(json):

  """Returns the rhs value in the response to a currency
  query
  Given a JSON response to a currency query, this returns
  the string inside double quotes (") immediately following
  the keyword "rhs". For example, if the JSON is

  '{ "lhs" : "1 Bitcoin", "rhs" : "19995.85429186 Euros",     "err" : "" }'

  then this function returns '19995.85429186 Euros' (not 
  '"38781.518240835 Euros"').  

  This function returns the empty string if the JSON 
  response contains an error message.

  Find the string inside the first set of double quotes after "rhs"
  with first_inside_quotes:
  Splice the json string to include the first set of double quotes
  after "rhs"
  Use first_inside_quotes on this spliced string

  Parameter json: a json string to parse
  Precondition: json is the response to a currency query
  """

   #input= '{ "lhs":"2 Namibian Dollars", "rhs":"2 Lesotho Maloti", "err": "" }' 
  rhs_index=json.index("rhs")#==index of first letter of rhs
  startrhs=rhs_index+4 #index of first space after rhs(i think)
  rhs=first_inside_quotes(json[startrhs:]) #the first thing inside quotes after "rhs"
  rhs=rhs.strip()

  return rhs

  
def has_error(json):
  """Returns True if the query has an error; False   
  otherwise.
  
  Given a JSON response to a currency query, this returns 
  True if there
  is an error message. For example, if the JSON is 
  
  '{ "lhs" : "", "rhs" : "", "err" : "Currency amount is 
  invalid." }'
  
  then the query is not valid, so this function returns 
  True (It 
  does NOT return the message 'Currency amount is 
  invalid.').

  Find index of "e" in "err" of json string.
  Find the first string in quotes using the first_inside_quotes 
  function starting in the index after "err"
  Use len function to count the number of characters in between the quotes after "err"
  Check if the len==0 and store result as a boolean variable
  Return the negated result from the boolean variable
  
  Parameter json: a json string to parse
  Precondition: json is the response to a currency 
  query"""

  check_err=json.index("err") # index of the e in err
  check_err=check_err+4
  check=first_inside_quotes(json[check_err:])
  #check = the first string in quotes starting after "err"
  #print("THIS IS INSIDE CHECK",check)
  is_it_there = (len(check)==0) #if the len=0, 
  #this will be True, if the len!=0, this will be false
  #string contains something = True there is error, return true
  #string empty = False there is no error, return false
  #print("DOES THIS WORK", is_it_there)

  return not is_it_there  #we need to invert it


def query_website(old, new, amt):
  """
  Returns a JSON string that is a response to a currency query.

  A currency query converts amt money in currency old to the 
  currency new. The response should be a string of the form    

  '{ "lhs":"<old-amt>", "rhs":"<new-amt>", "err":"" }'

  where the values old-amount and new-amount contain the value 
  and name for the old and new currencies. If the query is 
  invalid, both old-amount and new-amount will be empty, while 
  "err" will have an error message.

  We want to first create the website url. Then, query_website function
  will read and output the json string contents from the website. 

  Creating the website:
  Capitalize the parameters and store them into variables
  Make sure all variables to be concatenated to the website are stored as strings
  Concatenate the variables and the remaining characters from the website

  Getting the json string:
  Have the urlread function (from introcs module) read the json string from the 
  website
  Return the json string 
  
  

  Parameter old: the currency on hand
  Precondition: old is a string with no spaces or non-letters
      
  Parameter new: the currency to convert to
  Precondition: new is a string with no spaces or non-letters
      
  Parameter amt: amount of currency to convert
  Precondition: amt is a float"""
  
  
  oldurl = old
  newurl = new
  amtconvert = amt
  amturl = str(amtconvert)
  starturl= 'http://cs1110.cs.cornell.edu/2022fa/a1?old='
  combine = starturl+oldurl+'&new='+newurl+'&amt='+amturl


  import introcs
  finalurl= introcs.urlread(combine)
  #print(finalurl)
  return finalurl
  
def is_currency(code):
  """Returns: True if code is a valid (3 letter code for a) currency
  It returns False otherwise.  

  To check if the currency code works, we can create the website url 
  containing the currency code and check for an error specifically
  for currency code. 

  Use query_website to create the website url containing the currency code
  Have has_error read the resulting json string returned from query_website
  When has_error returns True if there is an error, we want
  is_currency to return False to show that there is an invalid currency code
  Return the negation of the returned boolean from has_error 


  
  Parameter code: the currency code to verify
  Precondition: code is a string with no spaces or non-letters."""

  
  json_currencycode_url = query_website(code, code, 3.02) 
  #print (json_currencycode_url, "does it work")
  return not has_error (json_currencycode_url)
  
  
  pass


def exchange(old, new, amt):

  """
  Returns the amount of currency received in the given exchange.
  
  In this exchange, the user is changing amt money in currency 
  old to the currency new. The value returned represents the 
  amount in currency new.
  
  The value returned has type float.
  
  Find the float of the converted currency from the json string:
  Use query_website to output the json string
  The new currency value is located after "rhs" of the json string
  Use get_rhs to retrieve the string in double quotes after "rhs"
  Splice the rhs string using before space to retrieve the number only
  Convert the number into a float and return the float

  Parameter old: the currency on hand
  Precondition: old is a string for a valid currency code
      
  Parameter new: the currency to convert to
  Precondition: new is a string for a valid currency code
      
  Parameter amt: amount of currency to convert
  Precondition: amt is a float
  """
  #o=old
  #n=new
  #a=float(amt)
  #website=query_website(o,n,a)
  #website_rhs=get_rhs(website)
  #exchange_number=(before_space(website_rhs)).strip()
  #exchange_number=float(exchange_number)
  #return exchange_number
  
  jsonstring_exchange = query_website(old,new,amt)
  #print(jsonstring_exchange, "DOES IT WORK")
  rhsvalue = get_rhs(jsonstring_exchange)
  #print(rhsvalue, "THIS HOPEFULLY WORKS")
  amtstring = before_space(rhsvalue)
  amtfloat = float(amtstring)
  #print(amtfloat, "IS IT WORKING")
  
  return amtfloat
  