"""
Steganography methods for the imager application.

This module provides all of the test processing operations (encode, decode) 
that are called by the application. Note that this class is a subclass of Filter. 
This allows us to layer this functionality on top of the Instagram-filters, 
providing this functionality in one application.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Aileen Huang (aeh245) and Jessica Andrews (jaa375)
11/15/22
"""
import a6filter


class Encoder(a6filter.Filter):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of Filter.  That means it inherits all of the 
    methods and attributes of that class too. We do that separate the 
    steganography methods from the image filter methods, making the code
    easier to read.
    
    Both the `encode` and `decode` methods should work with the most recent
    image in the edit history.
    """
    
    def encode(self, text):
        """
        Returns True if it could hide the text; False otherwise.
        
        This method attemps to hide the given message text in the current 
        image. This method first converts the text to a byte list using the 
        encode() method in string to use UTF-8 representation:
            
            blist = list(text.encode('utf-8'))
        
        This allows the encode method to support all text, including emoji.
        
        If the text UTF-8 encoding requires more than 999999 bytes or the 
        picture does  not have enough pixels to store these bytes this method
        returns False without storing the message. However, if the number of
        bytes is both less than 1000000 and less than (# pixels - 10), then 
        the encoding should succeed.  So this method uses no more than 10
        pixels to store additional encoding information.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns True...)
        # The last paragraph (If the text UTF-8 encoding...)
        # The precondition (text is a string)

        assert type(text)==str
        blist = list(text.encode('utf-8')) #convert text to byte
        current  = self.getCurrent()
        start="*"
        end="#"
        text.insert(0,start)
        text.append(end)
        if(len(blist)>1000000 or len(blist)>len(current._data-10)):
            return False
        else:
            for pos in range(len(blist)):  #rotate through pixels ?
                pixel = blist[pos]   
                blist._encode_pixel(self,pos,pixel)  #i dont even know, is this encoding all the pixels? how do i get text back from encoded bytes?
            return True
          


        pass    # Implement me

        
    
    def decode(self):
        """
        Returns the secret message (a string) stored in the current image. 
        
        The message should be decoded as a list of bytes. Assuming that a list
        blist has only bytes (ints in 0.255), you can turn it into a string
        using UTF-8 with the decode method:
            
            text = bytes(blist).decode('utf-8')
        
        If no message is detected, or if there is an error in decoding the
        message, this method returns None
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns the secret...)
        # The last paragraph (If no message is detected...)
        pass    # Implement me
    
    # HELPER METHODS
    def _decode_pixel(self, pos):
        """
        Return: the number n hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as 
        the last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        # This is helper. You do not have to use it. You are allowed to change it.
        # There are no restrictions on how you can change it.
        rgb = self.getCurrent()[pos]
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10
    
    def _encode_pixel(self,pos,k):
        """
        
        
        Modifies the pixel with the byte k hidden in it.
        
        This function assumes that k is a valid byte, and pos is a valid pixel.
        
        Parameter pos: a pixel position, k:the byte to encode
        Precondition: pos is an int with  0 <= p < image length (as a 1d list), k is a valid byte
        """
        current = self.getCurrent()
        rgb = current.__getitem__(pos) #get pixel 
        print(rgb, 'rgb')
        #access ones place of each attribute
        red = str(rgb.red)
        green = str(rgb.green)
        blue = str(rgb.blue)
        k_str = str(k)

        if len(k_str) ==3: #if k is a 3-digit number
            k_100 = k//100 #100s place
            k_10 = (k-(k//100 * 100))//10 #10s place
            k_1 = k-( k//100 * 100) -  ( (k-( k//100 * 100))//10)* 10 #ones place
            if len(red) == 3:
                first = red[:1]
                red = first + str(k_100)
            if len(red) == 2:
                first = red[0]
                red = first + str(k_100)
            if len(red) ==1:
                red =  str(k_100)
            if len(green) == 3:
                first = green[:1]
                green = first + str(k_10)
            if len(green) == 2:
                green = green + str(k_10)
            if len(green) ==1:
                green = str(k_10)
            if len(blue) == 3:
                first = blue[:1]
                blue = first + str(k_1)
            if len(blue) == 2:
                blue = blue + str(k_1)
            if len(green) ==1:
                blue = str(k_10)

        if len(k_str)==2: #if k is a 2-digit number
            k_10 = (k-(k//100 * 100))//10 #10s place
            k_1 = k-( k//100 * 100) -  ( (k-( k//100 * 100))//10)* 10 #ones place

            if len(red) == 3:
                first = red[:1]
                red = first + str(k_10)
            if len(red) == 2:
                first = red[0]
                red = first + str(k_10)
            if len(red) ==1:
                red =  str(k_10)
            if len(green) == 3:
                first = green[:1]
                green = first + str(k_1)
            if len(green) == 2:
                green = green + str(k_1)
            

        if len(k_str) ==1:
            k_1 = k
            if len(red) == 3:
                first = red[:1]
                red = first + str(k_1)
            if len(red) == 2:
                first = red[0]
                red = first + str(k_1)
            if len(red) ==1:
                red =  str(k_1)
            
    
        red = int(red)
        green = int(green)
        blue = int(blue)

        rgb.red = red
        rgb.green = green
        rgb.blue = blue
        