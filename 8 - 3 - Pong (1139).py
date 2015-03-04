# Implementation of classic arcade game Pong
# Made by Ciprian Olariu (Romania)

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [300, 200]
ball_vel = [0, 0]
score1 = 0
score2 = 0
paddle1_pos = 160
paddle2_pos = 160
paddle1_vel = 0
paddle2_vel = 0
right = True

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init():
    global ball_pos, ball_vel
    ball_pos[0] = 300
    ball_pos[1] = 200
    if right == True:
        ball_vel[0] = random.randrange(120, 180) / 60
        ball_vel[1] = -random.randrange(60, 180) / 60
    else:
        ball_vel[0] = -random.randrange(120, 180) / 60
        ball_vel[1] = -random.randrange(60, 180) / 60

def paddle_init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    paddle1_pos = 160
    paddle2_pos = 160
    paddle1_vel = 0
    paddle2_vel = 0
    
# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel 
    global score1, score2 
    ball_init()
    paddle_init()
    score1 = 0
    score2 = 0

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, right
 
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >=0 and paddle1_pos + paddle1_vel <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >=0 and paddle2_pos + paddle2_vel <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line([2, paddle1_pos],[2, paddle1_pos+PAD_HEIGHT-1], PAD_WIDTH, "White") 
    c.draw_line([598, paddle2_pos],[598, paddle2_pos+PAD_HEIGHT-1], PAD_WIDTH, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            score2 += 1
            right = True
            ball_init()
            paddle_init()
    if ball_pos[0] + BALL_RADIUS >= WIDTH-PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            score1 += 1
            right = False
            ball_init()
            paddle_init()
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1]
    # draw ball and scores
    c.draw_circle(ball_pos,BALL_RADIUS,1,"White","White")
    c.draw_text(str(score1),[180,130],80,"Blue")
    c.draw_text(str(score2),[362,130],80,"Red")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -2.5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 2.5
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -2.5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 2.5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)


# start frame
init()
frame.start()

