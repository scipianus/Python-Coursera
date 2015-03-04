# RiceRocks (Asteroids)
# Made by Ciprian Olariu (Romania)

import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.vector = angle_to_vector(self.angle)
        
    def draw(self,canvas):
        if self.thrust == True:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[0] %= width
        self.pos[1] += self.vel[1]
        self.pos[1] %= height
        self.angle += self.angle_vel
        self.vector = angle_to_vector(self.angle)
        self.vel[0] *= 0.95
        self.vel[1] *= 0.95
        if self.thrust == True:
            self.vel[0] += self.vector[0] * 0.5
            self.vel[1] += self.vector[1] * 0.5
    
    def turn_left(self):
        self.angle_vel -= 0.1
        
    def turn_right(self):
        self.angle_vel += 0.1
        
    def set_thrust(self, value):
        self.thrust = value
        if value == True:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def shoot(self):
        global missile_group, started
        if started:
            pos = [0,0]
            pos[0] = self.pos[0] + self.radius * self.vector[0]
            pos[1] = self.pos[1] + self.radius * self.vector[1]
            vel = [0,0]
            vel[0] = self.vel[0] + self.vector[0] * 5
            vel[1] = self.vel[1] + self.vector[1] * 5
            a_missile = Sprite([pos[0], pos[1]], [vel[0], vel[1]], 0, 0, missile_image, missile_info, missile_sound)
            missile_group.add(a_missile)
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + self.age*self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[0] %= width
        self.pos[1] += self.vel[1]
        self.pos[1] %= height
        self.angle += self.angle_vel
        self.age += 1
        if self.age < self.lifespan:
            return True
        else:
            return False
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def collide(self,other_object):
        if dist(self.pos,other_object.get_position()) <= self.radius + other_object.get_radius():
            return True
        else:
            return False
        
            
def draw(canvas):
    global time, my_ship, rock_group, missile_group, started, lives, score, explosion_group
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    score += group_group_collide(missile_group,rock_group)
    lives -= group_collide(rock_group,my_ship)
    process_sprite_group(explosion_group,canvas)
    
    # update lives 
    if lives <= 0:
        lives = 0
        started = False
        missile_group = set([])
        rock_group = set([])
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [width/2, height/2], 
                          splash_info.get_size())

def keydown(key):
    global my_ship
    if key==simplegui.KEY_MAP['left']:
        my_ship.turn_left()
    if key==simplegui.KEY_MAP['right']:
        my_ship.turn_right()
    if key==simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    if key==simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup(key):
    global my_ship
    if key==simplegui.KEY_MAP['left']:
        my_ship.turn_right()
    if key==simplegui.KEY_MAP['right']:
        my_ship.turn_left()
    if key==simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started, my_ship
    if len(rock_group)<12 and started:
        what = random.randint(0,1)
        pos = [0,0]
        if what==0:
            pos[0] = random.random()*50+50
        else:
            pos[0] = random.random()*50+700
        pos[1] = random.random()*400+100
        vel = [0,0]
        vel[0] = random.random()*4.0-2.0
        vel[1] = random.random()*4.0-2.0
        angle_vel = random.random()*0.4-0.2
        a_rock = Sprite([pos[0], pos[1]], [vel[0], vel[1]], 0, angle_vel, asteroid_image, asteroid_info)
        if a_rock.collide(my_ship)==False:
            rock_group.add(a_rock)

def process_sprite_group(S,canvas):
    removed = set([])
    for x in S:
        x.draw(canvas)
        if x.update() == False:
            removed.add(x)
    S.difference_update(removed)
        
def group_collide(group,other_object):
    global explosion_group
    nr = 0
    removed = set([])
    for x in group:
        if x.collide(other_object):
            nr += 1
            removed.add(x)
            an_explosion = Sprite(x.get_position(),[0,0],0,0,explosion_image,explosion_info,explosion_sound)
            explosion_group.add(an_explosion)
    group.difference_update(removed)
    return nr

def group_group_collide(group1,group2):
    nr = 0
    removed = set([])
    for x in group1:
        if group_collide(group2,x):
            nr += 1
            removed.add(x)
    group1.difference_update(removed)
    return nr 
        
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)

# initialize ship and sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()