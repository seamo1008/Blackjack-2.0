#Blackjack database fundamentals



#define the deck

deck = {

    'Spades': ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],

    'Hearts': ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],

    'Clubs': ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],

    'Diamonds': ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

}



#define card values

default_card_values = {

    'Ace': 11,

    '2': 2,

    '3': 3,

    '4': 4,

    '5': 5,

    '6': 6,

    '7': 7,

    '8': 8,

    '9': 9,

    '10': 10,

    'Jack': 10,

    'Queen': 10,

    'King': 10

}



#4 decks of cards

deck_list = []



for suit, ranks in deck.items():

    for rank in ranks:

        card_value = default_card_values[rank]

        deck_list.append(f"{rank} of {suit} (Value: {card_value})")



live_deck = deck_list*4

print(live_deck)



#random shuffle

import random



random.shuffle(live_deck)

print(live_deck)



#define functions "hit" and "stay"

def hit(hand, live_deck):

    #take the first card from the deck and add it to the player's hand

    card = live_deck[0]

    hand.append(card)

    live_deck.pop(0)



def stay():

    print("Stay")#player chooses not to take a card, no action needed

    pass



#define total hand value

def calculate_hand_value(hand):

    total_value = 0

    num_aces = 0

    

    for card in hand:

        rank = card.split()[0] #extract the rank from the card string

        card_value = default_card_values[rank] #retrieve card value from the dictionary

        

        if rank == "Ace": #handle Aces separately

            num_aces += 1

        else:

            total_value += card_value

            

    #handle the value of Aces

    for _ in range(num_aces):

        if total_value + 11 <= 21:

            total_value += 11

        else:

            total_value += 1

        

    return total_value



#Before beginning a game, greet the player and ask for their name

user_name = input("Enter your name:")



#deal 2 cards to each player & 1 to the dealer

num_players = 4  #number of players including the dealer

hand_size = 2  #number of initial cards for each player



#create an empty dictionary to hold each player's hand

players = {

    "John": [],

    "You": [],

    "Ivan": [],

    "Dealer": []

}



#get a separate list of player names

player_names = list(players.keys())



#deal initial cards to each player

for i, player in enumerate(player_names):

    if player == "Dealer":

        players[player].extend(live_deck[:1]) #deal 1 card to the dealer

    else:

        players[player].extend(live_deck[:hand_size])  #deal 2 cards to the other players

    del live_deck[:hand_size]  #remove the dealt cards from the deck

    

#print the hands of each player

for player, hand in players.items():

    if player == "Dealer":

        print(f"{player}: {hand}")

    else:

        hand_value = calculate_hand_value(hand)

        print(f"Player {player}: {hand} (Total: {hand_value})")





#Base code for generating a hand

dealer_face_card = players["Dealer"][0] #get the dealer's face card (card at position 0)



#show dealer's face card and John's starting hand

for player, hand in players.items():

    if player == "Dealer":

        print(f"{player}: {hand}")

    else:

        pass

hand_value_1 = calculate_hand_value(players["Ivan"])

print(f"Ivan: {players['Ivan']}")

print(f"Total: {hand_value_1}")



#check the conditions and call the appropriate functions for a player

if dealer_face_card in ['4', '5', '6'] and calculate_hand_value(players["Ivan"]) >= 12:

    stay()

else:

    while calculate_hand_value(players["Ivan"]) <= 15: #continue hitting until John has > 15

        hit(players["Ivan"], live_deck)

        new_card = players["Ivan"][-1] #get the last card added to the hand

        hand_value = calculate_hand_value(players["Ivan"])

        print(f"New Card: {new_card}")

        print(f"Ivan: {players['Ivan']}")

        print(f"Total: {hand_value}")

        if hand_value == 21:

            print("NICE!")

        elif hand_value > 21:

            print("BUST!")

        if hand_value > 15:

            break



hand_value = calculate_hand_value(players["Ivan"])

if hand_value in [16, 17, 18, 19, 20]:

    print("Stay")

elif hand_value == 21:

    print("BLACKJACK!")

print(f"Ivan total: {calculate_hand_value(players['Ivan'])}")









# dealer automatically hits <=16, sticks >= 17, busts >21