"""
User interface for module currency

When run as a script, this module prompts the user for two currencies and 
an amount. It prints out the result of converting the first currency to 
the second.

Author: Jessica Andrews (jaa375), Aileen Huang (aeh245)
Date:   9/21/22
"""

import a1

#DESIRED OUTPUT:
#[user@machine]:a1 > python a1app.py 
#Enter original currency: USD
#Enter desired currency: CUP
#Enter original amount: 2.5
#You can exchange 2.5 USD for 64.375 CUP."""

lhs=(input("Enter original currency: ")).upper()
rhs=(input("Enter desired currency: ")).upper()
amt=float(input("Enter original amount: "))
exchangeamt = a1.exchange(lhs,rhs,amt)              
print("You can exchange "+str(amt),lhs,"for",str(exchangeamt),rhs+".")
