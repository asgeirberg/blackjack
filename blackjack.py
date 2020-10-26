#!/usr/bin/env python3
# -*- coding: utf8 -*-

import random
import os
import time

class Card():

    suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
    ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
    value = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven" : 7, "Eight": 8, "Nine": 9, "Ten":10, "Jack":10, "Queen":10, "King":10, "Ace":10}

    def __init__(self, suit = "Joker", rank = None):
        if suit in Card.suits:
            self.suit = suit
        else:
            self.suit = "Joker" #Joker is the default card if things go wrong.
        if rank in Card.ranks:
            self.rank = rank
        else: 
            self.rank = None #Joker is considered a rankless suit.
        if rank in Card.value:
            self.value = Card.value[rank]
        else: 
            self.value = None
    
    def __str__(self):
        if self.rank != None:
            return self.rank + " of " + self.suit
        else: 
            return "Joker"
        #Here below are some equality operations on cards defined. Just uses the value.
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __ge__(self, other):
        return self.value >= other.value

class Deck():

    def __init__(self):
        ''' loops over every suit and every rank and adds one card to the deck. '''

        cards = []

        for suit in Card.suits:
            for rank in Card.ranks:
                new_card = Card(suit, rank)
                cards.append(new_card)

        self.cards = cards
        self.number_of_cards = self.__len__() 

    def __str__(self):
        ''' formats the string representation of the deck'''

        card_string = ""

        for card in self.cards[1:]: #skip the first card so we can format the string.
            card_string = card_string + ", " + str(card)

        card_string = str(self.cards[0]) + card_string  #add the first card without comma.

        return card_string
    
    def __len__(self):
        ''' returns the number of cards in the deck'''
        return len(self.cards)
    
    def shuffle(self, number = 1):
        ''' shuffles the deck. Has the option of shuffling more than once by taking in a number.
        Doesn't really do anything, just for effect.''' 

        for _ in range(number):
            random.shuffle(self.cards)

        return None
    
    def deal_one(self):
        ''' returns one card and removes it from the deck. 
        If there are no more cards, it returns None'''

        if len(self.cards) != 0:
            return self.cards.pop()
        else:
            return None

    def get_cards(self, cards):

        self.cards.extend(cards)


    def cut(self, number = 1):
        ''' "cuts" the deck by picking a random number somewhere in the middle and
        separating the deck into two lists and put one in front of the other. By passing a number to
        the function, this can be done many times. Strictly speaking not necessary, but nice for effect'''

        for _ in range(number):

            place_to_cut = random.randint(20, 35)
            first_half = self.cards[:place_to_cut]
            second_half = self.cards[place_to_cut:]

            self.cards = second_half + first_half

        return None

class Player():

    def __init__(self, name, amount = 1000):

        self.name = name
        self.hand = []
        self.number_of_cards = self.__len__()

        self.amount = amount

    def __len__(self):
        return len(self.hand)

    def __str__(self):
        ''' formats the string representation of the player's hand'''
        card_string = ""
            
        for card in self.hand[1:]: #skip the first card so we can format the string.
            card_string = card_string + ", " + str(card)

        card_string = str(self.hand[0]) + card_string  #add the first card without comma.

        return card_string
    
    def subtract_bet(self, amount):
        self.amount = self.amount - amount
    
    def add_money(self, amount):
        self.amount = self.amount + amount

    def give_one(self):
        ''' gives one card at the beginning of the hand'''
        return self.hand.pop(0)
    
    def give_cards(self):
        ''' gives every card the player has away. Returns a list of cards and sets hand to an empty list'''
        temp = self.hand
        self.hand = []

        print("Returning cards to deck...")
        return temp

    def add_cards(self, new_cards):
        ''' takes in a single card object or a list of card objects and adds them to the hand'''

        if type(new_cards) == type([]):
            self.hand.extend(new_cards)
        else:
            self.hand.append(new_cards)
        
def print_table(amount, dealer_hand, hidden_card = True):
    
    if hidden_card == True:
        dealer_hand = dealer_hand[1:] #take the hidden card off and make string out of it

    card_string = ""

    for card in dealer_hand[1:]: #skip the first card so we can format the string.
        card_string = card_string + ", " + str(card)

    card_string = str(dealer_hand[0]) + card_string  #add the first card without comma.

    print("The table is:")
    if hidden_card == True:
        print("Dealer has: " + str(card_string) + " and one card face down.")
    else: 
        print("Dealer has: " + str(card_string) + ".")
    print("{} has: ".format(player.name) + str(player) + ".")
    print("")
    print("There are $" + str(amount) + " in play.")

def ask_input(prompt, options):

    if type(options) == type(1):

        answer = 0

        while answer > options or type(answer) != type(int) or answer == 0:
            answer = input(prompt)

            try: 
                answer = int(answer)
                
            except: 
                print("The bet has to be a number. Try again")
                answer = 0
                continue

            if answer > options:
                print("Invalid amount. Try again.")
                continue

            elif answer == 0:
                print("Bet cannot be $0. Try again.")
            else:
                break

    if type(options) == type([]):

        answer = ""

        while answer not in options:
            answer = input(prompt) # for some reason, assignment to answer doesn't work, so this is hack to fix the issue.

            if answer not in options: 
                print("Only " + str(options) + " are allowed. Try again.")

    return answer

def evaluate_hand(hand, natural = False):
    
    number_of_aces = 0
    value = 0

    for card in hand:
        if card.rank == "Ace":
            number_of_aces += 1
    
    for card in hand:
        value += card.value

    if value > 21 and number_of_aces > 0:
        value = value - 10 + 1 #if the player is bust and has an ace, it counts as 1, not 10, so we subtract 10 and add 1.

    if value == 20 and len(hand) == 2 and (number_of_aces == 1 or number_of_aces == 2):
        if natural == True:
            return "Natural" #if one 10 card and one ace, then player wins if dealer doesn't also get natural.
        else:
            return 21

    return value

def clear_screen():
    os.system('clear')

def print_welcome_screen():
    
    clear_screen()

    print("Welcome to Blackjack!")
    print("\n")

def count_aces(hand):

    number_of_aces = 0

    for card in hand:
        if card.rank == 'Ace':
            number_of_aces += 1
    
    return number_of_aces

START_CARDS = 2 # number of cards in the beginning
round_number = 1 #counter for rounds
game_on = True

print_welcome_screen()

name = input("Enter player name: ")

#Create the deck, the dealer and the player. 
deck = Deck()
player = Player(name = name, amount=1000) #Player starts with 1000 dollars
dealer = Player(name = "Dealer")

#game starts here

while 1==1:
    
    if len(deck) < 52:
        print("Missing cards from deck...")

    if len(deck) > 52: 
        print("Too many cards in deck...")
        print(len(deck))

    print("\nStarting Round " + str(round_number) + "\n")

    print("Shuffling deck...")
    time.sleep(0.5)
    deck.shuffle(5) #shuffle the deck 5 times

    print("Cutting deck...\n")
    time.sleep(0.5)
    deck.cut(3) # cut the deck 3 times

    print("You have $" + str(player.amount) + " left.")
    amount_in_play = ask_input("How much do you want to bet?:", player.amount)
    player.subtract_bet(amount_in_play)

    print("Dealing cards...\n")
    time.sleep(0.5)

    for _ in range(START_CARDS):
        player.add_cards(deck.deal_one())
        dealer.add_cards(deck.deal_one())

    print_table(amount_in_play, dealer.hand)

    while game_on == True:

        if evaluate_hand(player.hand, natural = True) == "Natural" and evaluate_hand(dealer.hand, natural = True) != "Natural":
            print("Blackjack. You won!")
            player.add_money(amount_in_play * 2) #doubles the money the player gets back
            amount_in_play = 0

            break

        elif evaluate_hand(player.hand, natural = True) == "Natural" and evaluate_hand(dealer.hand, natural = True) == "Natural":
            print("Dealer also has Blackjack: " + str(dealer.hand[1]) + " and "  + str(dealer.hand[0]) + ".  Nobody wins!")
            amount_in_play = 0
            player.add_money(amount_in_play) #Player gets money back 

            break

        answer = ask_input("Do you want to Hit or Stand (h/s)?", ["h", "s", "q"])

        if answer == "h":
            player.add_cards(deck.deal_one())
            print_table(amount_in_play, dealer.hand)
            
            if evaluate_hand(player.hand) > 21:
                print("You are bust!")
                amount_in_play = 0
                break

        elif answer == "s":
            while evaluate_hand(dealer.hand) < 17:
                    print("Giving a new card to the dealer...")
                    time.sleep(0.5)
                    dealer.add_cards(deck.deal_one())   

            if evaluate_hand(dealer.hand) > 21:

                print_table(amount_in_play, dealer.hand, hidden_card = False)
                time.sleep(0.5)
                print("Dealer is bust. You win!")
                player.add_money(amount_in_play*2) #doubles the money the player gets back
                amount_in_play = 0

                break
            
            if evaluate_hand(player.hand) > evaluate_hand(dealer.hand):

                print_table(amount_in_play, dealer.hand, hidden_card = False)
                time.sleep(0.5)
                print("You win!")
                player.add_money(amount_in_play*2) #doubles the money the player gets back
                amount_in_play = 0

                break
            
            elif evaluate_hand(player.hand) < evaluate_hand(dealer.hand):

                print_table(amount_in_play, dealer.hand, hidden_card = False)
                time.sleep(0.5)
                print("You lose!")
                amount_in_play = 0
                
                break

            else: 
                print_table(amount_in_play, dealer.hand, hidden_card = False)
                print("Hands are equal! Nobody wins.")

                time.sleep(0.5)
                player.add_money(amount_in_play) #player gets money back
                amount_in_play = 0
            
                break

    print("You have $" + str(player.amount) + " left.")

    if player.amount <= 0:
        print("You are bankrupt. Sorry!")
        break
    else:
        answer = ask_input("Do you want to play another round? (y/n)\n", ["y", "n", "q"])

        if answer == "n" or answer == "q":
            break
        elif answer == "y":
            round_number += 1

            print("I am here")
            print(dealer.hand)
            deck.get_cards(dealer.give_cards())
            print(dealer.hand)
            print(player.hand)
            deck.get_cards(player.give_cards())   
            print(player.hand)










