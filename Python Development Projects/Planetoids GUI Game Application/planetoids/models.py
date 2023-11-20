"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

# Aileen Huang(aeh245) and Jessica Andrews(jaa375)
# 12/8/22
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180
# END REMOVE

class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute x: x position of the bullet
    #Invariant: x is an int where 0<=x<=800
    #
    #Attribute y: y position of the bullet
    #Invariant: y is an int where 0<=y<=700
    #
    #Attribute width: width of the bullet
    #Invariant: width is int >=0
    #
    #Attribute height: height of the bullet
    #Invariant: height is an int >=0
    #
    #Attribute _velocity: velocity of the ship
    #Invariant: _velocity is a Vector2 Object
    #
    #Attribute fillcolor: color of the bullet
    #Invariant fillcolor is a valid color
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBulletVelocity(self):
        """
        Returns velocity of bullet
        """
        return self._velocity
    def getBulletFacing(self):
        """
        Returns facing of bullet
        """
        return self._facing
    
    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self,x,y,facing,width,height,color,velocity):
        """
        Initializes a Bullet Object

        Each bullet can fire at a velocity at a position that depends on
        the facing and/or position of the ship. 
        This function will be called in wave.py to satisfy this.
        
        Parameter x: x position of ship object
        Precondition: x is a float or int
        
        Parameter x: y position of ship object
        Precondition: y is a float or int

        Parameter facing: facing of ship
        Precondition: facing is a Vector2 Object

        Parameter width: width of bullet object
        Precondition: width is a float or int

        Parameter height: height of bullet object
        Precondition: height is a float or int

        Parameter color: color of bullet
        Precondition: color is a string with a valid color

        Parameter velocity: speed of bullet
        Precondition: speed is an int or float
        """
        assert isinstance(facing, Vector2), repr(facing) + 'is not a Vector2 Object'
        assert isinstance(velocity, int) or type(velocity)==float, repr(velocity) + 'is not an int or float'
        super().__init__(x=x, y=y,width=width,height=height,fillcolor=color)
        # Take the facing vector (which is a unit vector),
        #  multiply it by SHIP_RADIUS, and 
        # add this vector to the ship position (which is the center of the ship).
        position=Vector2(x=x,y=y)
        m=facing.__mul__(SHIP_RADIUS) 
        newfacing=m.__add__(position)
        self.x=newfacing.x
        self.y=newfacing.y
        self._velocity=facing.__mul__(velocity)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def updatev(self):
            """
            Updates position

            We add velocity to our position.
            """
            self.x = self.x + self._velocity.x
            self.y = self.y + self._velocity.y

    def isOutRange(self):
            """
            Returns True if object goes offscreen (top, bottom, right, or left)
            """
            x=self.x
            if(x <-DEAD_ZONE):
                    return True
                    #crosses the right threshold
            if(x>GAME_WIDTH+DEAD_ZONE):
                    return True
                        
            y=self.y
            if(y<-DEAD_ZONE):
                    return True
                    #crosses the top threshold
            if(y>GAME_HEIGHT+DEAD_ZONE):
                    return True
            return False


class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vecotr (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute x: x position of the ship
    #Invariant: x is an int where 0<=x<=800
    #
    #Attribute y: y position of the ship
    #Invariant: y is an int where 0<=y<=700
    #
    #Attribute angle: orientation of the ship
    #Invariant: angle is an int 0<=_angle<=360
    #
    #Attribute width: width of the ship
    #Invariant: width is int >=0
    #
    #Attribute height: height of the ship
    #Invariant: height is an int >=0
    #
    #Attribute _velocity: velocity of the ship
    #Invariant: _velocity is a Vector2 Object
    #
    #Attribute _facing: facing of the ship
    #Invariant: _facing is a Vector2 Object
    #
    #Attribute source: source image of ship
    #Invariant: source is a valid image file
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getShipVelocity(self):
        """
        Returns velocity of the ship
        """
        return self._velocity
    def getShipFacing(self):
        """
        Returns facing of the ship
        """
        return self._facing
    
    def getShipX(self):
        """
        Returns x position of ship
        """
        return self.x
    
    def getShipY(self):
        """
        Returns y position of ship
        """
        return self.y
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, angle, width = 2*SHIP_RADIUS, height =2*SHIP_RADIUS, source=SHIP_IMAGE):
        """
        Initializes the ship object

        The width, height, and source of the ship are automatically set (optional arguments).
        We need to define the ship position (x and y) and angle.

        Parameter x: the x position of the ship object
        Precondition: x is an int >=0

        Parameter y: the y position of the ship object
        Precondition: y is an int >=0

        Parameter angle: the initial angle of the ship object
        Precondition: angle is an int 0<=angle<=360

        Parameter width: width of ship
        Precondition: width is an int>=0

        Parameter height: height of ship
        Precondition: height is an int>=0

        Parameter source: source image of ship
        Precondition: source is a valid image file
        """
        assert type(x)==int, repr(x) +'is not an int'
        assert x>=0, repr(x) + 'is not greater than or equal to 0'
        assert type(y)==int, repr(y) + 'is not a int'
        assert y>=0, repr(y)+'is not greater than or equal to 0'
        assert type(angle)==int, repr(angle) + 'is not an int'
        assert 0<=angle<=360 , repr(angle) + 'is not between 0 and 360'
        super().__init__(x=x, y=y, angle = angle, width=width,height=height,source=source)
        self._velocity = Vector2(0,0)
        ang = degToRad(angle)
        self._facing=Vector2(math.cos(ang), math.sin(ang))

        

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)

    def turn(self, change):
        """
        Updates the angle and facing of the ship when turning

        Parameter change: number of degrees the ship turns by
        Precondition: change is an int or float
        """  
        assert type(change)==int or type(change)==float, repr(change)+'is not an int or float'
        self.angle = self.angle + change
        ang= degToRad(self.angle)
        self._facing = Vector2(math.cos(ang), math.sin(ang))

    def changev(self):
            """
            Updates the velocity 

            We change our velocity according to the impulse.
            """
            impulse = self._facing.__mul__(SHIP_IMPULSE)
            self._velocity= self._velocity.__add__(impulse)
            if self._velocity.length() > SHIP_MAX_SPEED:
                if not self._velocity.length()== 0.0:
                    normal = self._velocity.normalize()
                else:
                    normal = self._velocity
                self._velocity = normal.__mul__(SHIP_MAX_SPEED)

    def updatev(self):
            """
            Updates position

            We add our velocity to position.
            """
            self.x = self.x + self._velocity.x
            self.y = self.y + self._velocity.y
            
    def wraphori(self):
            """
            Wraps our object horizontally
            """
            x=self.x
            if(x <-DEAD_ZONE):
                    self.x =self.x+GAME_WIDTH+2*DEAD_ZONE
                #crosses the right threshold
            if(x>GAME_WIDTH+DEAD_ZONE):
                    self.x=self.x-GAME_WIDTH+2*DEAD_ZONE
            
    def wrapverti(self):
            """
            Wraps our object vertically
            """
            y=self.y
            if(y<-DEAD_ZONE):
                    self.y=self.y+GAME_HEIGHT+2*DEAD_ZONE
                #crosses the top threshold
            if(y>GAME_HEIGHT+DEAD_ZONE):
                    self.y=self.y-GAME_WIDTH+2*DEAD_ZONE 


class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute x: x position of the asteroid
    #Invariant: x is an int where 0<=x<=800
    #
    #Attribute y: y position of the asteroid
    #Invariant: y is an int where 0<=y<=700
    #
    #Attribute width: width of the asteroid
    #Invariant: width is int >=0
    #
    #Attribute height: height of the asteroid
    #Invariant: height is an int >=0
    #
    #Attribute _velocity: velocity of the asteroid
    #Invariant: _velocity is a Vector2 Object
    #
    #Attribute _size: size of the ship
    #Invariant: _size is a str
    #
    #Attribute source: source image of asteroid
    #Invariant: source is a valid image file
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAsteroidVelocity(self):
        """
        Returns velocity of asteroid
        """
        return self._velocity
    def getAsteroidsize(self):
        """
        Returns size of asteroid
        """
        return self._size
    
    
    # INITIALIZER TO CREATE A NEW ASTEROID

    def __init__(self,size,x,y,dv):
        """
        Initializes an Asteroid object

        Our asteroid velocity, source, and size depends on
        the size sent according to the json string from wave.py.
        This function is called in wave.py to satisfy this.

        Parameter x: the x position of the ship object
        Precondition: x is an int or float >=0

        Parameter y: the y position of the ship object
        Precondition: y is an int or float >=0

        Parameter size: the size of the asteroid
        Precondition: size is a str of either 'small' , 'medium' or 'large'

        Parameter dv: direction vector of asteroid
        Precondition: dv is a Vector2 Object
        """
        assert type(x)==int or type(x)==float , repr(x) +'is not an int or float'
        assert type(y)==int or type(y)==float, repr(y) + 'is not a int or float'
        assert y>=0, repr(y)+'is not greater than or equal to 0'
        assert size == 'small' or size=='medium' or size=='large', repr(size) + 'is not a valid size'
        assert isinstance(dv, Vector2), repr(dv)+'is not a Vector2 Object'
        
        if not dv.length()==0.0:
            if size == 'small':
                super().__init__(x=x, y=y, width=SMALL_RADIUS*2,height=SMALL_RADIUS*2,source=SMALL_IMAGE)
                self._size=SMALL_ASTEROID
                self._velocity=dv.normalize().__mul__(SMALL_SPEED)
            if size == 'medium':
                super().__init__(x=x, y=y, width=MEDIUM_RADIUS*2,height=MEDIUM_RADIUS*2,source=MEDIUM_IMAGE)
                self._size=MEDIUM_ASTEROID
                self._velocity=dv.normalize().__mul__(MEDIUM_SPEED)
            if size == 'large':
                super().__init__(x=x, y=y, width=LARGE_RADIUS*2,height=LARGE_RADIUS*2,source=LARGE_IMAGE)
                self._size=LARGE_ASTEROID
                self._velocity=dv.normalize().__mul__(LARGE_SPEED)
        else:
            if size == 'small':
                super().__init__(x=x, y=y, width=SMALL_RADIUS*2,height=SMALL_RADIUS*2,source=SMALL_IMAGE)
                self._size=SMALL_ASTEROID
                self._velocity=dv
            if size == 'medium':
                super().__init__(x=x, y=y, width=MEDIUM_RADIUS*2,height=MEDIUM_RADIUS*2,source=MEDIUM_IMAGE)
                self._size=MEDIUM_ASTEROID
                self._velocity=dv
            if size == 'large':
                super().__init__(x=x, y=y, width=LARGE_RADIUS*2,height=LARGE_RADIUS*2,source=LARGE_IMAGE)
                self._size=LARGE_ASTEROID
                self._velocity=dv
        
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def updatev(self):
            """
            updates position
            """
            self.x = self.x + self._velocity.x
            self.y = self.y + self._velocity.y

    def wraphori(self):
        """
        Wraps our object horizontally 
        """
        x=self.x
        if(x <-DEAD_ZONE):
                self.x =self.x+GAME_WIDTH+2*DEAD_ZONE
            #crosses the right threshold
        if(x>GAME_WIDTH+DEAD_ZONE):
                self.x=self.x-GAME_WIDTH+2*DEAD_ZONE
        
    def wrapverti(self):
        """
        Wraps our object vertically 
        """
        y=self.y
        if(y<-DEAD_ZONE):
                self.y=self.y+GAME_HEIGHT+2*DEAD_ZONE
            #crosses the top threshold
        if(y>GAME_HEIGHT+DEAD_ZONE):
                self.y=self.y-GAME_WIDTH+2*DEAD_ZONE 

    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
