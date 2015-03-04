# Mini-project #6 - Blackjack
# Made by Ciprian Olariu (Romania)

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
first_game = True
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.L = []
        self.value = 0

    def __str__(self):
        s = ""
        for c in self.L:
            s = s + str(c) + " "
        return s

    def add_card(self, card):
        self.L.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        self.value = 0
        ace = False
        for c in self.L:
            self.value += VALUES[c.get_rank()]
            if c.get_rank() == 'A':
                ace = True
        if ace and self.value+10<=21:
            self.value += 10
        return self.value

    def busted(self):
        self.value = self.get_value()
        if self.value > 21:
            return True
        else:
            return False
    
    def draw(self, canvas, p):
        for c in self.L:
            c.draw(canvas,p)
            p[0] += 75
    
    def has_ace(self):
        value = 0
        ace = False
        for c in self.L:
            value += VALUES[c.get_rank()]
            if c.get_rank() == 'A':
                ace = True
        if ace and value+10<=21:
            return True
        return False
 
        
# define deck class
class Deck:
    def __init__(self):
        self.L = []
        for s in SUITS:
            for r in RANKS:
                self.L.append(Card(s,r))

    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.L)

    def deal_card(self):
        return self.L.pop()

player = Hand()
dealer = Hand()
deck = Deck()
    
#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score, first_game
    if in_play:
        score -= 1
        outcome = "You have lost"
    outcome = ""
    in_play = True
    first_game = False
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

def hit():
    global outcome, in_play, player, deck, score
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
    # if busted, assign an message to outcome, update in_play and score
    if in_play and player.busted():
        in_play = False
        score -= 1
        outcome = "Busted"
       
def stand():
    global outcome, in_play, player, dealer, deck, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value()<17:
            dealer.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
    if in_play:
        in_play = False
        if dealer.busted():
            score += 1
            outcome = "You have won"
        else:
            valp = player.get_value()
            vald = dealer.get_value()
            if valp>vald:
                score += 1
                outcome = "You have won"
            else:
                score -= 1
                outcome = "You have lost"

# draw handler    
def draw(canvas):
    global player, dealer, outcome
    canvas.draw_text("Blackjack",[310,70],40,"Black")
    canvas.draw_text(outcome,[330,370],40,"Black")
    canvas.draw_text("Dealer",[80,170],40,"Black")
    canvas.draw_text("You",[80,370],40,"Black")
    canvas.draw_text("Score : " + str(score),[480,570],40,"Black")
    player.draw(canvas,[80,400])
    if not first_game:
        if player.has_ace():
            canvas.draw_text(str(player.get_value()-10)+"("+str(player.get_value())+")",[180,370],40,"Black")
        else:
            canvas.draw_text(str(player.get_value()),[180,370],40,"Black")
    if in_play:
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,[116.5,248],CARD_BACK_SIZE)
        dealer.L[1].draw(canvas,[155,200])
        canvas.draw_text("Hit or Stand?",[330,370],40,"Black")
    else:    
        dealer.draw(canvas,[80,200])
        if not first_game:
            if dealer.has_ace():
                canvas.draw_text(str(dealer.get_value()-10)+"("+str(dealer.get_value())+")",[230,170],40,"Black")
            else:
                canvas.draw_text(str(dealer.get_value()),[230,170],40,"Black")
        canvas.draw_text("New deal?",[80,570],40,"Black")
        


# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()
