import random
import sys
import time
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []

        for suit in suits:#for each suit, cycle through each 'rank', or card, and create all 52 cards
            for rank in ranks:
                created_card = Card(suit,rank)
                #create each card object
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)#shuffle all the cards, happens in place - needs to be called
    
    def deal_one(self):#deals one card, removes it from the list
        return self.all_cards.pop()

class Player:

    def __init__(self,name,bank=100):

        self.name = name
        self.all_cards= []
        self.bank = bank
        self.cardvalue = 0

    def add_card(self,new_card):

        self.all_cards.append(new_card)

    def __str__(self):
        return f'Player {self.name} has ${self.bank} remaining.'

class Dealer:

    def __init__(self,name='Dealer'):

        self.name = name
        self.all_cards= []
        self.cardvalue = 0
    
    def add_card(self,new_card):

        self.all_cards.append(new_card)

    def __str__(self):
        return f'{self.name} has {len(self.all_cards)} cards.'

def game_choice_no_money():
    choice = "default"
    global player

    while choice not in ['Yes', 'No']:
        choice = input('Do you want to play again? (Yes or No)')
        if choice not in ['Yes', 'No']:
            print('Sorry I do not understand, please choose Yes or No')
    if choice == 'Yes':
        player.bank = 100
        return True
    else:
        sys.exit(0)

def game_choice():
    choice = "default"
    global player
    time.sleep(1)
    if player.bank <= 0:
        print('You are out of money!')
        game_choice_no_money()
        return  
    print(f"Your bank balance is ${player.bank}")
    while choice not in ['Yes', 'No', 'yes', 'no']:
        choice = input('Do you want to play another hand? (Yes or No)')
        if choice not in ['Yes', 'yes', 'No', 'no']:
            print('Sorry I do not understand, please choose Yes or No')
    if choice == 'Yes' or choice == 'yes':
        return True
    else:
        print(f"You have left the table with ${player.bank} remaining, thank you for playing!")
        time.sleep(1)
        print('Exiting the game in 5 seconds')
        time.sleep(5)
        sys.exit(0)

def deal_cards():
    global new_deck
    new_deck = Deck()
    new_deck.shuffle()
    player.all_cards = [new_deck.all_cards[0], new_deck.all_cards[2]]
    dealer.all_cards = [new_deck.all_cards[1], new_deck.all_cards[3]]


def check_player_score():
    global player_turn
    global player_score
    player_score = 0
    for card in range(0,len(player.all_cards)):
        player_score += player.all_cards[card].value
    
    num_of_aces = 0
    for card in range(0,len(player.all_cards)):
        if player.all_cards[card].rank == 'Ace':
            num_of_aces += 1

    acceptable_num = [player_score, player_score-10, player_score-20, player_score-30, player_score-40]

    for total in acceptable_num:
        count = 0
        if total > 23:
            count += 1
        if count == len(acceptable_num):
            print('You have bust!')
            player_turn = False
            player.bank -= bet
            game_choice() 


    if num_of_aces > 0:
        choice = 'default'
        within_range = False
        acceptable_num = acceptable_num[:len(acceptable_num)-4+num_of_aces]
        while choice.isdigit() == False or within_range == False:
            choice = input(f'You have {num_of_aces} Ace(s). Your score can be any of {acceptable_num}. Please select:')
            if choice.isdigit() == False:
                print('Sorry that is not an acceptable number')
            if choice.isdigit() == True:
                if int(choice) > 21:
                    print('That score is in excess of 21, please choose again')
                    within_range = False
                elif int(choice) in acceptable_num:
                    within_range = True
                    player_score = int(choice)

    if player_score > 21:
        print('You have bust!')
        player_turn = False
        player.bank -= bet
        game_choice()        

    

def check_dealer_score():
    global dealer_turn
    global player_score
    dealer_score = 0
    dealer_turn = False
    for card in range(0, len(dealer.all_cards)):
        dealer_score += dealer.all_cards[card].value
    
    num_of_aces = 0

    for card in range(0, len(dealer.all_cards)):
        if dealer.all_cards[card].rank == 'Ace':
            num_of_aces += 1
    
    if dealer_score > 21 and num_of_aces == 1:
        dealer_score -= 10
    
    if dealer_score > 21 and num_of_aces == 2:
        dealer_score -= 10
        if dealer_score > 21:
            dealer_score -= 10
    
    if dealer_score > 21 and num_of_aces == 3:
        dealer_score -= 10
        if dealer_score > 21:
            dealer_score -= 10
            if dealer_score > 21:
                dealer_score -= 30
    
    if dealer_score > 21 and num_of_aces == 4:
        dealer_score -= 10
        if dealer_score > 21:
            dealer_score -= 10
            if dealer_score > 21:
                dealer_score -= 30
                if dealer_score > 21:
                    dealer_score - 40  
    
    if dealer_score > 21:
        time.sleep(1)
        print(f'The dealer has bust with a score of {dealer_score}')
        player.bank += bet
    elif dealer_score > player_score:
        time.sleep(1)
        player.bank -= bet
        print(f"The dealer wins with a score of {dealer_score} to {player_score}")
    elif dealer_score == player_score:
        time.sleep(1)
        print(f'The hand is tied with a score of {dealer_score}')
    else:
        time.sleep(1)
        player.bank += bet
        print(f'Congratulations, you have won the hand with a score of {player_score} to {dealer_score}')
    game_choice()

def check_dealer_aces():
    global dealer
    num_of_aces = 0
    for card in range(0, len(dealer.all_cards)):
        if dealer.all_cards[card].rank == 'Ace':
            num_of_aces += 1
    
    if dealer.cardvalue > 21 and num_of_aces == 1:
        dealer.cardvalue -= 10
        return dealer.cardvalue    
    elif dealer.cardvalue > 21 and num_of_aces == 2:
        dealer.cardvalue -= 10
        if dealer.cardvalue > 21:
            dealer.cardvalue -= 10
        return dealer.cardvalue 
    elif dealer.cardvalue > 21 and num_of_aces == 3:
        dealer.cardvalue -= 10
        if dealer.cardvalue > 21:
            dealer.cardvalue -= 10
            if dealer.cardvalue > 21:
                dealer.cardvalue -= 30
        return dealer.cardvalue     
    elif dealer.cardvalue > 21 and num_of_aces == 4:
        dealer.cardvalue -= 10
        if dealer.cardvalue > 21:
            dealer.cardvalue -= 10
            if dealer.cardvalue > 21:
                dealer.cardvalue -= 30
                if dealer.cardvalue > 21:
                    dealer.cardvalue - 40  
        return dealer.cardvalue 


        





player = Player(input('Please enter your name: '))
print(f'Welcome to The Mac Shack Casino Offshoot, {player.name}')
time.sleep(1)
print('The Game is Blackjack!')
time.sleep(1)
dealer = Dealer()

game_on = True

while game_on:

    if player.bank <= 0:
        print('You are out of money!')
        game_choice_no_money()
    
    bet = 'Default'
    within_range = False
    while type(bet) != int or within_range == False:
        bet = input(f'You have ${player.bank} remaining. Please enter your bet: ')
        if bet.isdigit() == False:
            print('Sorry, that is not a whole number')
        if bet.isdigit() == True:
            bet = int(bet)
            if bet <= player.bank:
                print(f"Your bet is ${bet}")
                bet = int(bet)
                within_range = True
            else:
                print(f'Please bet an amount less than your balance (${player.bank})')


    
    deal_cards()
    player.cardvalue = player.all_cards[0].value + player.all_cards[1].value
    print(f'{player.name}, your cards are the {player.all_cards[0].rank} of {player.all_cards[0].suit} and the {player.all_cards[1].rank} of {player.all_cards[1].suit}')
    time.sleep(1)
    if player.cardvalue == 21 and len(player.all_cards) == 2:
        print('You have won blackjack!')
        player.bank += bet*2
        game_choice()
    else:
        num_of_aces = 0
        for card in range (0,len(player.all_cards)):
            if player.all_cards[card].rank == 'Ace':
                num_of_aces += 1
        if num_of_aces > 0:
            print(f'Your total hand is worth {player.cardvalue}. You have {num_of_aces} aces, which can be worth 11 or 1')
        else:
            print(f'Your total hand is worth {player.cardvalue}')
            time.sleep(1)
            print(f"The dealer's first card is the {dealer.all_cards[0].rank} of {dealer.all_cards[0].suit}")
            time.sleep(1)

    check_player_score()

    card_count = 3 #the index of the last card drawn
    player_turn = True
    dealer_turn = False
    while player_turn:
        choice = 'default'
        print(f'{player.name}, your current score is {player_score}')
        while choice not in ['stick', 'hit', 'Stick', 'Hit']:
            choice = input(f'{player.name}, do you want to stick or hit?')
            if choice not in ['stick', 'hit', 'Stick', 'Hit']:
                print("Sorry I didn't understand your request, please choose stick or hit")
        if choice == 'stick' or choice == 'Stick':
            player_turn = False
            dealer_turn = True
        else:
            player.all_cards.append(new_deck.all_cards[card_count+1])
            card_count += 1
            print(f"Your next card is the {player.all_cards[-1].rank} of {player.all_cards[-1].suit}")
            time.sleep(1)
            check_player_score()
    
    while dealer_turn:
        dealer.cardvalue = dealer.all_cards[0].value + dealer.all_cards[1].value
        print(f"The dealer's second card is the {dealer.all_cards[1].rank} of {dealer.all_cards[1].suit}")
        time.sleep(1)
        num_of_aces = 0
        check_dealer_aces()
        
        if dealer.cardvalue >= 17:
            check_dealer_score()
        while dealer.cardvalue < 17:
            dealer.all_cards.append(new_deck.all_cards[card_count+1])
            dealer.cardvalue += dealer.all_cards[-1].value
            check_dealer_aces()
            card_count += 1
            print(f"The dealer's next card is {dealer.all_cards[-1].rank} of {dealer.all_cards[-1].suit}")
            time.sleep(1)
            if dealer.cardvalue >=17:                
                check_dealer_score()


                    
    

        

    


    


    
    
