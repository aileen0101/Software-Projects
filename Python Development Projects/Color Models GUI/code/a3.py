""" 
Functions for Assignment A3

This file contains the functions for the assignment. 
You should replace the stubs
with your own implementations.

Aileen Huang (aeh245) and Jessica Andrews (jaa375)
10/3/22
"""
import introcs
import math


def complement_rgb(rgb):
    """
    Returns the complement of color rgb.
    
    Parameter rgb: the color to complement
    Precondition: rgb is an RGB object
    """
    # THIS IS WRONG.  FIX IT

    #print(introcs.RGB(rgb.red, rgb.green, rgb.blue))
    #print(rgb.red)
    #print(rgb.green)
    #print(rgb.blue)
    rgb.red = 255 - rgb.red
    rgb.green = 255 - rgb.green
    rgb.blue = 255 - rgb.blue
    #print(rgb.red, 'rgb:red: complement of red')
    #print(rgb.green, 'rgb.green: complement of green')
    #print(rgb.blue, 'rgb.blue: complement of blue')

    return rgb


def str5(value):
    """
    Returns value as a string, but expanded or 
    rounded to be exactly 5 characters.
    
    The decimal point counts as one of the five characters.
   
    Examples:
        str5(1.3546)  is  '1.355'.
        str5(21.9954) is  '22.00'.
        str5(21.994)  is  '21.99'.
        str5(130.59)  is  '130.6'.
        str5(130.54)  is  '130.5'.
        str5(1)       is  '1.000'.
    
    Parameter value: the number to conver to a 5 character string.
    Precondition: value is a number (int or float), 0 <= value <= 360.
    """
    # Remember that the rounding takes place at
    # # a different place depending 
    # on how big value is. Look at the
    #  examples in the specification.

    #round to 5 characters
    #find how many characters before the decimal 
    #round to a certain place after the 
    # decimal - there's a round function 
     
    #print(type(value))

    if 0 <= value < 0.0005:
        return '0.000'

    float_convert = float(value) 
    #print('float_convert: value converted 
    # to float is', float_convert)
    value_str = str(float_convert)
    #print('value_str: float_convert 
    # converted to a string:' ,value_str)
    #print('checking the type for value_str', type(value_str))
    
    decimal_index = value_str.find('.') #find index number of decimal
    before_decimal = value_str[:decimal_index] #find 
    #digits before decimal
    #print (before_decimal, "before_decimal:
    # spliced string of digits before decimal")
    numberofdigits_before = len(before_decimal) #count number of
    # digits before decimal
    #print (numberofdigits_before, 'numberofdigits_before: 
    # number of digits before decimal')
    
    decimalplace_round = 5 - numberofdigits_before - 1
    roundednumber_str = str(round(float_convert, decimalplace_round))
    #print('roundednumber_str: full string of 
    # rounded number',roundednumber_str)
    
    if len(roundednumber_str) < 5 and value > 0:
            zeros_to_add = 5 - len(roundednumber_str)
            zero_added_string = roundednumber_str + '0'*zeros_to_add
            #print ('zero_added_string: full string 
            # with "0"s added',zero_added_string)
            return zero_added_string
    else:
            return roundednumber_str


def str5_cmyk(cmyk):
    """
    Returns the string representation of cmyk in the form "(C, M, Y, K)".
    
    In the output, each of C, M, Y, and K should be exactly 5 characters long.
    Hence the output of this function is not the same as str(cmyk)
    
    Example: if str(cmyk) is 
    
          '(0.0,31.3725490196,31.3725490196,0.0)'
    
    then str5_cmyk(cmyk) is '(0.000, 31.37, 31.37, 0.000)'. 
    Note the spaces after the
    commas. These must be there.
    
    Parameter cmyk: the color to convert to a string
    Precondition: cmyk is an CMYK object.
    """
  
    cyan=(cmyk.cyan)
    magenta=(cmyk.magenta)
    yellow=(cmyk.yellow)
    black=(cmyk.black)
    cmyk="("+str5(cyan)+", "+str5(magenta)+", "+str5(yellow)+", "+str5(black)+")"
    #print("Testing", cmyk_format)
    return cmyk


def str5_hsv(hsv):
    """
    Returns the string representation of hsv in the form "(H, S, V)".
    
    In the output, each of H, S, and V should be exactly 5 characters long.
    Hence the output of this function is not the same as str(hsv)
    
    Example: if str(hsv) is 
    
          '(0.0,0.313725490196,1.0)'
    
    then str5_hsv(hsv) is '(0.000, 0.314, 1.000)'. Note the spaces after the
    commas. These must be there.
    
    Parameter hsv: the color to convert to a string
    Precondition: hsv is an HSV object.
    """
    #list into a string and returns the string
    hue = str5(hsv.hue)
    saturation = str5(hsv.saturation)
    value = str5(hsv.value)
    hsv_text = "("+hue+", "+saturation+", "+value+")"
    #print("Testing", hsv_text)
    return hsv_text

    pass


def rgb_to_cmyk(rgb):
    """
    Returns a CMYK object equivalent to rgb, with the most black possible.
    
    Formulae from https://www.rapidtables.com/convert/color/rgb-to-cmyk.html
    
    Parameter rgb: the color to convert to a CMYK object
    Precondition: rgb is an RGB object
    """
    # The RGB numbers are in the range 0..255.
    # Change them to the range 0..1 by dividing them by 255.0.
    
    r=rgb.red/255.0
    g=rgb.green/255.0
    b=rgb.blue/255.0
    k=1-max(r,g,b)
    if(k==1):
        c=0
        m=0
        y=0
    else:
        c=(1-r-k)/(1-k)
        m=(1-g-k)/(1-k)
        y=(1-b-k)/(1-k)
    cyan=c*100
    magenta=m*100
    yellow=y*100
    black=k*100
    converted_cmyk=introcs.CMYK(cyan,magenta,yellow,black)
    #print('Testing',converted_cmyk)
    return converted_cmyk

    pass


def cmyk_to_rgb(cmyk):
    """
    Returns an RGB object equivalent to cmyk
    
    Formulae from https://www.rapidtables.com/convert/color/cmyk-to-rgb.html
   
    Parameter cmyk: the color to convert to a RGB object
    Precondition: cmyk is an CMYK object.
    """
    # The CMYK numbers are in the range 0.0..100.0. 
    # Deal with them the same way as the RGB numbers in rgb_to_cmyk()
    

    cyan = (cmyk.cyan)/100.0
    #print(cyan, "what cyan converted looks like")
    magenta = (cmyk.magenta) /100.0
    yellow = (cmyk.yellow) /100.0
    black = (cmyk.black) /100.0

    red = (1-cyan)*(1-black) 
    #print(red, "what red looks like from formula, unconverted")
    green = (1-magenta)*(1-black) 
    blue = (1-yellow)*(1-black) 

    red = red * 255
    green = green * 255
    blue = blue * 255

    red_final = int((round(red, 0)))
    green_final = int((round(green, 0)))
    blue_final = int((round(blue, 0)))

    rgb = introcs.RGB(red_final, green_final, blue_final)
    
    return rgb

    pass


def rgb_to_hsv(rgb):
    """
    Return an HSV object equivalent to rgb
    
    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV
   
    Parameter hsv: the color to convert to a HSV object
    Precondition: rgb is an RGB object
    """
    # The RGB numbers are in the range 0..255.
    # Change them to range 0..1 by dividing them by 255.0.

    # Change them to range 0..1 by dividing them by 255.0.
    r=(rgb.red/255.0)
    g=(rgb.green/255.0)
    b=(rgb.blue/255.0)
    max_value=max(r,g,b)
    min_value=min(r,g,b)

    if(max_value==min_value):
        h=0.0
        #print(h)
    elif(max_value==r and g>=b):
        h=(60.0*(g-b))/(max_value-min_value)
        #print(h)
    elif(max_value==r and g<b):
        h=((60.0*(g-b))/(max_value-min_value))+360.0
        #print(h)
    elif(max_value==g):
        h=((60.0*(b-r))/(max_value-min_value))+120.0
        #print(h)
    elif(max_value==b):
        h=((60.0*(r-g))/(max_value-min_value))+240.0
        #print(h)

    if(max_value==0):
        s=0.0
    else:    
        s=1-(min_value/max_value)
  
    v=max_value
    
    converted_hsv=introcs.HSV(h,s,v)
    return converted_hsv

    pass


def hsv_to_rgb(hsv):
    """
    Returns an RGB object equivalent to hsv
    
    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV
    
    Parameter hsv: the color to convert to a RGB object
    Precondition: hsv is an HSV object.
    """

    h=hsv.hue
    s=hsv.saturation
    v=hsv.value

    hi=math.floor(h/60.0)
    f=h/60.0-hi
    p=v*(1.0-s)
    q=v*(1.0-f*s)
    t=v*(1.0-(1.0-f)*s)

    if(hi==0.0 or hi ==5.0):
        r=v
    elif(hi==1.0):
        r=q
    elif(hi==2.0 or hi==3.0):
        r=p
    elif(hi==4.0):
        r=t
    
    if(hi==0.0):
        g=t
    elif(hi==1.0 or hi==2.0):
        g=v
    elif(hi==3.0):
        g=q
    elif(hi==4.0 or hi==5.0):
        g=p

    if(hi==0.0 or hi==1.0):
        b=p
    elif(hi==2.0):
        b=t
    elif(hi==3.0 or hi==4.0):
        b=v
    elif(hi==5.0):
        b=q

    red=round(r*255.0)
    green=round(g*255.0)
    blue=round(b*255.0)
    converted_rgb=introcs.RGB(red,green,blue)
    return converted_rgb

    pass


def contrast_value(value,contrast):
    """
    Returns value adjusted to the "sawtooth curve" 
    for the given contrast
    
    At contrast = 0, the curve is the normal 
    line y = x, so value is unaffected.
    If contrast < 0, values are pulled closer together, 
    with all values collapsing
    to 0.5 when contrast = -1.  If contrast > 0, 
    values are pulled farther apart, 
    with all values becoming 0 or 1 when contrast = 1.
    
    Parameter value: the value to adjust
    Precondition: value is a float in 0..1
    
    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """

    x = value
    c = contrast
    
    if -1 <= c < 1:
        if x < 0.25 + 0.25*c:
            y = ((1-c)/(1+c))*x
        elif x > 0.75 - 0.25*c:
            y = ((1-c)/(1+c))*(x-((3-c)/4))+((3+c)/4)
        else:
            y = ((1+c)/(1-c))*(x-((1+c)/4))+ ((1-c)/4)
    
    elif c == 1:
        if x >= 0.5:
            y=1
        else:
            y=0

    return y

    pass


def contrast_rgb(rgb,contrast):
    """
    Applies the given contrast to the RGB object rgb
    
    This function is a PROCEDURE.  It modifies rgb 
    and has no return value.  It should
    apply contrast_value to the red, blue, and green values.
    
    Parameter rgb: the color to adjust
    Precondition: rgb is an RGB object
    
    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """
    #Converting values to scale of 0-1

    
    red=rgb.red/255.0
    green=rgb.green/255.0
    blue=rgb.blue/255.0
    
    #contrasting value
    r= contrast_value(red,contrast)
    g=contrast_value(green,contrast)
    b=contrast_value(blue,contrast)

    
    #converting value back to 255 scale
    rgb.red=int(round(r*255.0))
    rgb.green=int(round(g*255.0))
    rgb.blue=int(round(b*255.0))

    pass