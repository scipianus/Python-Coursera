# Rock-paper-scissors-lizard-Spock program
# Made by Ciprian Olariu (Romania)


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

import random

def number_to_name(number):
    # convert number to a name using if/elif/else
    if number==0:
        return "rock"
    elif number==1:
        return "Spock"
    elif number==2:
        return "paper"
    elif number==3:
        return "lizard"
    else:
        return "scissors"

    
def name_to_number(name):
    # convert name to number using if/elif/else
    if name=="rock":
        return 0
    elif name=="Spock":
        return 1
    elif name=="paper":
        return 2
    elif name=="lizard":
        return 3
    else:
        return 4


def rpsls(name): 
    # convert name to player_number using name_to_number
    player_number=name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number=random.randrange(0,5)
    # compute difference of player_number and comp_number modulo five
    difference=(player_number-comp_number)%5
    # use if/elif/else to determine winner
    # convert comp_number to name using number_to_name
    # print results
    print ""
    print "Player chooses",name
    print "Computer chooses",number_to_name(comp_number)
    if difference==0:
        print "Player and computer tie!"
    elif difference<=2:
        print "Player wins!"
    else:
        print "Computer wins!"

    
# testing
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")


