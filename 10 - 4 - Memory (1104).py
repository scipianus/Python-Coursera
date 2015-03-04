# Implementation of card game - Memory
# Made by Ciprian Olariu (Romania)

import simplegui
import random

cards = []
exposed = []
state = 0
moves = 0
last1 = 0
last2 = 0

# helper function to initialize globals
def init():
    global state, cards, exposed, moves, last1, last2
    cards = []
    exposed = []
    for x in range(8):
        cards.append(x)
        cards.append(x)
        exposed.append(False)
        exposed.append(False)
    state = 0
    moves = 0
    last1 = 0
    last2 = 0
    random.shuffle(cards)
     
# define event handlers
def mouseclick(pos):
    global state, moves, last1, last2
    x = pos[0] // 50
    if exposed[x]==False:
        exposed[x] = True
        if state==0:
            state = 1
            last1 = x
        elif state==1:
            state = 2
            last2 = x
            moves = moves + 1
        else:
            state = 1
            if cards[last1]!=cards[last2]:
                exposed[last1] = False
                exposed[last2] = False
            last1 = x
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    l.set_text("Moves = "+str(moves))
    for i in range(16):
        if exposed[i]==True:
            canvas.draw_text(str(cards[i]),(8+50*i,70),50,"White")
        else:
            canvas.draw_line((50*i+25,0),(50*i+25,99),50,"Green")
        


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()