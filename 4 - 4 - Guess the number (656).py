# Guess the number program
# Made by Ciprian Olariu (Romania)

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

# initialize global variables used in your code

num_range = 100
num_guesses = 7
secret_num = 0

# define event handlers for control panel

def init():
    global num_guesses
    global secret_num
    if num_range == 100:
        num_guesses = 7
        secret_num = random.randrange(0, 100)
        print "New game. Range is from 0 to 100"
        print "Number of remaining guesses is 7"
        print ""
    else:
        num_guesses = 10
        secret_num = random.randrange(0, 1000)
        print "New game. Range is from 0 to 1000"
        print "Number of remaining guesses is 10"
        print ""

def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    global num_guesses
    global secret_num
    num_range = 100
    num_guesses = 7
    secret_num = random.randrange(0, 100)
    print "New game. Range is from 0 to 100"
    print "Number of remaining guesses is 7"
    print ""

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    global num_guesses
    global secret_num
    num_range = 1000
    num_guesses = 10
    secret_num = random.randrange(0, 1000)
    print "New game. Range is from 0 to 1000"
    print "Number of remaining guesses is 10"
    print ""
    
def get_input(guess):
    # main game logic goes here
    print "Guess was ",guess
    global num_guesses
    num_guesses = num_guesses - 1
    print "Number of remaining guesses is ",num_guesses
    if secret_num == int(guess):
        print "Correct!"
        print ""
        init()
        return None
    if num_guesses == 0:
        print "You have lost! The secret number was ",secret_num
        print ""
        init()
        return None
    if secret_num < int(guess):
        print "Lower!"
        print ""
    else:
        print "Higher!"
        print ""
    
# create frame

f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements

f.add_button("Range is [0,100)", range100, 200)
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Enter a guess", get_input, 200)

# start frame

f.start()
init()