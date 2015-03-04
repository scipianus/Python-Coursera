# Stopwatch : The Game
# Made by Ciprian Olariu (Romania)

# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
correct = 0
total = 0
works = True

# define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    t = t // 10
    A = t // 60
    t = t % 60
    C = t % 10
    B = t // 10
    return str(A) + ':' + str(B) + str(C) + '.' + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global works
    timer.start()
    works = True

def stop():
    global total, correct, works
    timer.stop()
    if works==True:
        total = total + 1
        if time%10==0:
            correct = correct + 1
    works = False
    
def reset():
    global time, total, correct, works
    timer.stop()
    works = False
    time = 0
    total = 0
    correct = 0

def draw(canvas):
    canvas.draw_text(format(time), [50,175], 60, "White")
    canvas.draw_text(str(correct)+'/'+str(total), [225,50], 20, "Red")
    
# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time = time + 1
    
# create frame
frame=simplegui.create_frame("Stopwatch",300,300)

# register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)
timer=simplegui.create_timer(100, tick)

# start timer and frame
frame.start()
timer.start()
