"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

# Aileen Huang(aeh245) and Jessica Andrews(jaa375)
# 12/8/22
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) H
    # ERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    #
    # Attribute 
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getData(self):
        """
        Returns the wave json file
        """
        return self._data

    def getLives(self):
        """
        Returns the number of lives the player has left
        """
        return self._lives
    def getAst(self):
        """
        Returns the list of Asteroid objects in our game
        """
        return self._asteroids
    
    def getBullets(self):
        """
        Returns the list of Bullet objects in our game
        """
        return self._bullets
    

    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS

    def __init__(self, data, lives=3, ast_list = [], bullet_list=[]):
        """ 
        Initializes a Wave object
        
        We're creating our ship object and list of asteroids here. We'll also be
        setting our list of bullets here as well. Our game will start or continue
        (depending on how many lives we have left) at these asteroids, bullets, and 
        our Ship.

        Parameter data: The wave JSON dictionary file
        Precondition: data is a dictionary JSON file

        Parameter lives: The number of lives the ship has left
        We start off with 3 lives.
        Precondition: lives is an int >=0

        Parameter ast_list: The list of asteroids for our game
        Preconditon: ast_list is a list (empty or of Asteroid objects)

        Parameter bullet_list: The list of bullets for our game
        Precondition: bullet_list is a list(empty or of Bullet objects)
        """
        assert type(data) == dict, repr(data)+'is not a dictionary file'
        assert type(lives) == int and lives >=0, repr(lives) + 'is not an int >=0'
        assert type(bullet_list) == list, repr(bullet_list) + 'is not a list'
        if bullet_list != []:
            for n in range(len(bullet_list)):
                assert isinstance(bullet_list[n], Bullet), repr(bullet_list[n]) + 'is not a Bullet object'
        assert type(ast_list) == list, repr(ast_list) + 'is not a list'
        if ast_list !=[]:
            for n in range(len(ast_list)):
                assert isinstance(ast_list[n], Asteroid), repr(ast_list[n]) + 'is not an Asteroid object'
        self._data = data
        json = self._data
        json_ship = json["ship"]
        self._ship = Ship(x=json_ship["position"][0],y=json_ship["position"][1],angle=json_ship["angle"])
        self._lives = lives
        if ast_list != []:
            self._asteroids = ast_list
        else:
            asteroids_list = []
            json_asteroids=json["asteroids"]
            for n in range(len(json_asteroids)):
                dv=Vector2(x=json_asteroids[n]["direction"][0], y=json_asteroids[n]["direction"][1])
                if json_asteroids[n]["size"]=='small':
                    json_size='small'
                if json_asteroids[n]["size"]=='medium':
                    json_size='medium'
                if json_asteroids[n]["size"]=='large':
                    json_size='large'
                asteroid_obj = Asteroid(x=json_asteroids[n]['position'][0], y=json_asteroids[n]["position"][1], size=json_size,dv=dv)
                asteroids_list.append(asteroid_obj)
            self._asteroids = asteroids_list 
        self._firereate=0
        if bullet_list != []:
            self._bullets = bullet_list
        else:
            self._bullets=[]
             
        

    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, input, dt):
        """
        Animates the ship, asteroids, and bullets

        We call this function in app.py to animate our Wave
        objects. Our objects change their attributes
        according to user key presses and how objects interact with 
        each other (whether they collide or not). Objects can turn, 
        change velocity, move forward, or collide.

        Parameter dt: Time elasped since previous animation frame
        Precondition: dt is an int or float

        Parameter input: user input
        Precondition: input is a GInput object
        """
        assert type(dt)==int or type(dt)==float, repr(dt)+'is an int or float'
        assert isinstance(input, GInput), repr(input)+'is not a GInput Object'
        if not self._ship == None:
            if input.is_key_down('left'):
                change = SHIP_TURN_RATE
                self._ship.turn(change)
            if input.is_key_down('right'):
                change = -SHIP_TURN_RATE
                self._ship.turn(change)
            if input.is_key_down('up'):
                self._ship.changev()
                self._ship.updatev()
            else:
                self._ship.updatev()
            self._ship.wraphori()
            self._ship.wrapverti()
            for n in range(len(self._asteroids)):
                self._asteroids[n].updatev()
            for n in range(len(self._asteroids)):
                self._asteroids[n].updatev()
                self._asteroids[n].wraphori()
                self._asteroids[n].wrapverti()
            if input.is_key_down('spacebar'):  
                if(self._firereate>=BULLET_RATE):
                    self._firereate=0
                    bullet_obj=Bullet(self._ship.getShipX(),self._ship.getShipY(),self._ship.getShipFacing(),BULLET_RADIUS*2,BULLET_RADIUS*2,BULLET_COLOR,BULLET_SPEED)
                    self._bullets.append(bullet_obj)
                self._firereate=self._firereate+1
            for n in range(len(self._bullets)):
                self._bullets[n].updatev()
            i=0
            while(i<len(self._bullets)):
                if self._bullets[i].isOutRange():
                    del self._bullets[i]
                else:    
                    i+=1
            m_asteroids=[]
            speed = 0
            velocity = Vector2(0,0)
            facing = Vector2(0,0)
            for n in range(len(self._asteroids)):
                    if self.col_detect(self._asteroids[n], self._ship):
                        speed = speed + self._ship.getShipVelocity().length()
                        velocity = velocity.__add__(self._ship.getShipVelocity())
                        facing= facing.__add__(self._ship.getShipFacing())
                        m_asteroids.append(self._asteroids[n])
                        self._lives = self._lives -1
                        self._ship = None
            for m in range(len(m_asteroids)):
                self._asteroids.remove(m_asteroids[m])
                if speed ==0:
                    self.newasteroids(facing, m_asteroids[m])
                else:
                    self.newasteroids(velocity, m_asteroids[m])
            mark_asteroids=[]
            mark_bullets=[] #bullets collided
            for k in range((len(self._asteroids))): 
                for m in range(len(self._bullets)):
                    if self.col_detect(self._asteroids[k], self._bullets[m]):
                        mark_asteroids.append(self._asteroids[k])
                        mark_bullets.append(self._bullets[m])
            velocityb=Vector2(0,0)
            for k in range(len(mark_bullets)):
                velocityb = velocityb.__add__(mark_bullets[k].getBulletVelocity())
                self._bullets.remove(mark_bullets[k])
            for n in range(len(mark_asteroids)):            
                        self._asteroids.remove(mark_asteroids[n])
                        self.newasteroids(velocityb,mark_asteroids[n])

    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self, view):
        """
        Draws wave objects

        We call this function in app.py to display our 
        objects. We only draw objects that are not NoneType.
        We have an additional parameter view to 
        access Planetoids' view attribute. 

        Parameter view: game view for drawing our objects
        Precondition: view is an GView Object
        """
        assert isinstance(view, GView), repr(view) + 'is not a GView Object'
        if not self._ship == None:
            self._ship.draw(view)

        for n in range(len(self._asteroids)):
            self._asteroids[n].draw(view)

        for n in range(len(self._bullets)):
            self._bullets[n].draw(view)

            

    # RESET METHOD FOR CREATING A NEW LIFE

    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION

    def col_detect(self, obj1, obj2):
            """
            Detects whether obj 1 and obj2 collided:
            
            We want to find out whether an asteroid collided with 
            either a ship or bullet. When the distance between the radii
            of the two objects is less than the sum of their radii, the two
            objects are considered to have collided. 

            Parameter obj1: object to test for collision detection
            Precondition: An Asteroid or Bullet or Ship (could be None) object

            Parameter obj2: object to test for collision detection
            Precondition: An Asteroid or Bullet or Ship (could be None) object
            """
            #Ship could be registered as None briefly so None is included
            assert isinstance(obj1, Asteroid) or isinstance(obj1, Ship) or obj1 == None or isinstance(obj1, Bullet)
            assert isinstance(obj2, Asteroid) or isinstance(obj2, Ship) or obj2 == None or isinstance(obj2, Bullet)
            #radii of objects
            if not obj1 == None and not obj2 == None:
                r_obj1 = (obj1.width)/2
                r_obj2 = (obj2.width)/2
                #distance between objects
                #pythagorean theorem or use vectors
                distance_squared = (obj1.x-obj2.x)**2 + (obj1.y-obj2.y)**2
                distance = math.sqrt(distance_squared)
                if distance < (r_obj1 + r_obj2): #collision
                    return True
                else: #no collision
                    return False

        
    
    def newasteroids(self, col_objv, asteroid):
        """
        Creates new asteroids after collision

        If either a ship or bullet collides with a medium or large asteroid, 
        the asteroid breaks into 3 smaller ones (next size down, so medium 
        asteroids break up into smaller asteroids and
        large asteroids break up into medium asteroids). We send either the collision 
        velocity of bullet, the collision facing of a still ship, or collision velocity
        of a moving ship.

        Parameter col_objv: The velocity vector (or facing vector) of object 
        that collided with asteroid
        Precondition: A Vector2 Object

        Parameter asteroid: The asteroid of interest
        Precondition: an Asteroid object
        """
        assert isinstance(col_objv, Vector2), repr(col_objv) +'is not a Vector2 Object'
        assert isinstance(asteroid, Asteroid), repr(asteroid) + 'is not an Asteroid Object'
        if not col_objv.length() ==0.0:
            res_1 = col_objv.normalize()
            vx=res_1.x
            vy=res_1.y
            ang=degToRad(120)
            res_2=Vector2((vx*math.cos(ang))-(vy*math.sin(ang)), (vx*math.sin(ang))+vy*math.cos(ang))
            res_3=Vector2((vx*math.cos(2*ang))-(vy*math.sin(2*ang)), (vx*math.sin(2*ang))+vy*math.cos(2*ang))
            x= asteroid.x
            y=asteroid.y
            if asteroid._size == MEDIUM_ASTEROID:
                radius = SMALL_RADIUS
                pos_1 = res_1.__mul__(radius)
                pos_1.x = pos_1.x + x
                pos_1.y= pos_1.y+y
                ast_1 = Asteroid(x=pos_1.x, y=pos_1.y, dv=res_1, size='small')
                self._asteroids.append(ast_1)
                pos_2 = res_2.__mul__(radius)
                pos_2.x = pos_2.x + x
                pos_2.y= pos_2.y+y
                ast_2 = Asteroid(x=pos_2.x, y=pos_2.y, dv=res_2, size='small')
                self._asteroids.append(ast_2)
                pos_3 = res_3.__mul__(radius)
                pos_3.x = pos_3.x + x
                pos_3.y= pos_3.y+y
                ast_3 = Asteroid(x=pos_3.x, y=pos_3.y, dv=res_3, size='small')
                self._asteroids.append(ast_3)
            if asteroid._size== LARGE_ASTEROID:
                radius = MEDIUM_RADIUS
                pos_1 = res_1.__mul__(radius)
                pos_1.x = pos_1.x + x
                pos_1.y= pos_1.y+y
                ast_1 = Asteroid(x=pos_1.x, y=pos_1.y, dv=res_1, size='medium')
                self._asteroids.append(ast_1)
                pos_2 = res_2.__mul__(radius)
                pos_2.x = pos_2.x + x
                pos_2.y= pos_2.y+y
                ast_2 = Asteroid(x=pos_2.x, y=pos_2.y, dv=res_2, size='medium')
                self._asteroids.append(ast_2)
                pos_3 = res_3.__mul__(radius)
                pos_3.x = pos_3.x + x
                pos_3.y= pos_3.y+y
                ast_3 = Asteroid(x=pos_3.x, y=pos_3.y, dv=res_3, size='medium')
                self._asteroids.append(ast_3)
        
    def ship_active(self):
        """
        Returns True if our ship is None (inactive)
        """
        if(self._ship is None):
            return True
        else:
            return False
    
    def numAst(self):
        """
        Returns the number of asteroids we have left
        """
        return len(self._asteroids)