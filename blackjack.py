import functions
from decks import deck, default_card_values
from functions import hit, stay, calculate_hand_value, get_balance, check_equal_cards
import random


#8 decks of cards
deck_list = []
for suit, ranks in deck.items():
    for rank in ranks:
        card_value = next((card['points'] for card in default_card_values if card['value'] == rank['value']), None)
        if card_value is not None:
            deck_list.append(f"{rank['value']} of {suit} (Value: {card_value})")
live_deck = deck_list * 8


#Before beginning a game, greet the player and ask for their name
user_name = input("Please enter your name:")
print(f"Hello and welcome {user_name}. Good luck in your game of blackjack!")


#create a empty dictionary to hold each player's hand and wallet amounts
players = {
    "John": {
        "hand": [],
        "wallet": 100
    },
    "Ivan": {
        "hand": [],
        "wallet": 100
    },
    user_name: {
        "hand": [],
        "wallet": 100
    },
    "Dealer": {
        "hand": [],
        "wallet": 0
    }
}



play_again = True #allow the game to run in a loop
while play_again:


    #random shuffle
    random.shuffle(live_deck)


    #take starting bets
    your_balance = functions.get_balance(players, user_name)
    print(f"Your wallet: {players[user_name]['wallet']}")

    
    bet_amount = int(input("place your bet: "))
    if bet_amount > your_balance:
        print(f"The bet amount is higher than your balance. Please bet a lower amount")
        continue
    else:
        players[user_name]["wallet"] -= bet_amount #deduct from user's wallet
        print(f"Your wallet: {players[user_name]['wallet']}")



    #deal 2 cards to each player & 1 to the dealer
    num_players = 4  #number of players including the dealer
    hand_size = 2  #number of initial cards for each player


    #get a separate list of player names
    player_names = list(players.keys())



    #deal initial cards to each player
    for i, player in enumerate(player_names):
        if player == "Dealer":
            players[player]['hand'].extend(live_deck[:1]) #deal 1 card to the dealer
        else:
            players[player]['hand'].extend(live_deck[:hand_size])  #deal 2 cards to the other players
        del live_deck[:hand_size]  #remove the dealt cards from the deck


    #Introduce John's turn
    print("We'll start with John")
    #get the dealer's face card (card at position 0)
    dealer_face_card = players["Dealer"]["hand"][0]
    dealer_face_card_value = int(dealer_face_card.split(" (Value: ")[-1].replace(")", ""))

    #show dealer's face card and John's starting hand
    for player, hand_wallet in players.items():
        if player == "Dealer":
            print(f"{player}: {hand_wallet['hand']}")
        else:
            pass
    hand_value_1 = functions.calculate_hand_value(players["John"]["hand"])
    print(f"John: {players['John']['hand']}")
    print(f"Total: {hand_value_1}")


    #check the conditions and call the appropriate functions for John
    if dealer_face_card_value in [4, 5, 6] and functions.calculate_hand_value(players["John"]["hand"]) >= 12:
        functions.stay()
        print("stay")
    else:
        while functions.calculate_hand_value(players["John"]["hand"]) <= 15: #continue hitting until John has > 15
            hit(players["John"]["hand"], live_deck)
            new_card = players["John"]["hand"][-1] #get the last card added to the hand
            hand_value = functions.calculate_hand_value(players["John"]["hand"])
            print(f"New Card: {new_card}")
            print(f"John: {players['John']['hand']}")
            print(f"Total: {hand_value}")
            if hand_value == 21:
                print("NICE!")
            elif hand_value > 21:
                print("BUST!")
            if hand_value > 15:
                break


    hand_value = functions.calculate_hand_value(players["John"]["hand"])
    if hand_value in [16, 17, 18, 19, 20]:
        print("Stay")
    elif hand_value == 21 and len(players["John"]["hand"]) == 2:
        print("BLACKJACK!")
    else:
        print(f"John total: {hand_value}")


    #Introduce Ivan's turn
    print("Ivan will take his turn")
    #get the dealer's face card (card at position 0)
    dealer_face_card = players["Dealer"]["hand"][0]
    dealer_face_card_value = int(dealer_face_card.split(" (Value: ")[-1].replace(")", ""))

    #show dealer's face card and Ivan's starting hand
    for player, hand_wallet in players.items():
        if player == "Dealer":
            print(f"{player}: {hand_wallet['hand']}")
        else:
            pass
    hand_value_1 = functions.calculate_hand_value(players["Ivan"]["hand"])
    print(f"Ivan: {players['Ivan']['hand']}")
    print(f"Total: {hand_value_1}")


    #check the conditions and call the appropriate functions for Ivan
    if dealer_face_card_value in [4, 5, 6] and functions.calculate_hand_value(players["Ivan"]["hand"]) >= 12:
        functions.stay()
    else:
        while functions.calculate_hand_value(players["Ivan"]["hand"]) <= 15: #continue hitting until Ivan has > 15
            hit(players["Ivan"]["hand"], live_deck)
            new_card = players["Ivan"]["hand"][-1] #get the last card added to the hand
            hand_value = functions.calculate_hand_value(players["Ivan"]["hand"])
            print(f"New Card: {new_card}")
            print(f"Ivan: {players['Ivan']['hand']}")
            print(f"Total: {hand_value}")
            if hand_value == 21:
                print("NICE!")
            elif hand_value > 21:
                print("BUST!")
            if hand_value > 15:
                break


    hand_value = functions.calculate_hand_value(players["Ivan"]["hand"])
    if hand_value in [16, 17, 18, 19, 20]:
        print("Stay")
    elif hand_value == 21 and len(players["Ivan"]["hand"]) == 2:
        print("BLACKJACK!")
    else:
        print(f"Ivan total: {hand_value}")


    #Call the player in to take their turn
    print(f"Okay, {user_name}! Now you'll play")
    #show dealer's face card and John's starting hand
    for player, hand_wallet in players.items():
        if player == "Dealer":
            print(f"{player}: {hand_wallet['hand']}")
        else:
            pass
    hand_value_1 = functions.calculate_hand_value(players[user_name]["hand"])
    print(f"You have: {players[user_name]['hand']}")
    print(f"Your total: {hand_value_1}")


    player_name = user_name
    player_hand = players[player_name]["hand"]
    cards_equal = functions.check_equal_cards(player_hand)
    if cards_equal:
        user_response = input("You have two cards the same. Would you like to split? yes/no: ")
        if user_response.lower() == "yes":

            #take a second bet
            players[user_name]["wallet"] -= bet_amount
            print(f"Your new wallet amount: {players[user_name]['wallet']}")
            
            #create two separate hands
            new_hand_1 = [player_hand[0]]
            new_hand_2 = [player_hand[1]]

            #append second card to each new hand
            new_card_1 = functions.hit(new_hand_1, live_deck)
            new_card_2 = functions.hit(new_hand_2, live_deck)

            #Update the player's holding with the new hands
            players[player_name]["hand"] = new_hand_1
            players[player_name + "_split"] = {
                "hand": new_hand_2,
                "wallet": players[player_name]["wallet"]
            }

            print("Your cards have been split into two hands.")
            print("Hand 1:", new_hand_1)
            print("Hand 2:", new_hand_2)

            new_hand_1_value = functions.calculate_hand_value(new_hand_1)
            new_hand_2_value = functions.calculate_hand_value(new_hand_2)

            #play first hand
            print("Let's play Hand 1:", new_hand_1)
            print(f"Hand 1 total: {new_hand_1_value}")
            while functions.calculate_hand_value(new_hand_1) < 21:
                a = (input("Would you like to hit or stay?"))
                if a == "stay":
                    functions.stay()
                    break
                
                if a == "hit":
                    functions.hit(new_hand_1, live_deck)
                    new_card = new_hand_1[-1] #get the last card added to the hand
                    hand_value = functions.calculate_hand_value(new_hand_1)
                    print(f"New Card: {new_card}")
                    print(f"You have: {new_hand_1}")
                    print(f"New total: {hand_value}")
                    if hand_value == 21:
                        print("NICE!")
                    elif hand_value > 21:
                        print("BUST!")
                        break

            hand_value = functions.calculate_hand_value(new_hand_1)
            if hand_value == 21 and len(new_hand_1) == 2:
                print("BLACKJACK!")
            else:
                print(f"Hand 1: {hand_value}")

            #play second hand
            print("Let's play Hand 2:", new_hand_2)
            print(f"Hand 2 total: {new_hand_2_value}")
            while functions.calculate_hand_value(new_hand_2) < 21:
                a = (input("Would you like to hit or stay?"))
                if a == "stay":
                    functions.stay()
                    break
                
                if a == "hit":
                    functions.hit(new_hand_2, live_deck)
                    new_card = new_hand_2[-1] #get the last card added to the hand
                    hand_value = functions.calculate_hand_value(new_hand_2)
                    print(f"New Card: {new_card}")
                    print(f"You have: {new_hand_2}")
                    print(f"New total: {hand_value}")
                    if hand_value == 21:
                        print("NICE!")
                    elif hand_value > 21:
                        print("BUST!")
                        break

            hand_value = functions.calculate_hand_value(new_hand_2)
            if hand_value == 21 and len(new_hand_2) == 2:
                print("BLACKJACK!")
            else:
                print(f"Hand 2: {hand_value}")

        else:
            print("Continuing with the current hand.")
    else:
        while functions.calculate_hand_value(players[user_name]["hand"]) < 21:
            a = (input("Would you like to hit or stay?"))
            if a == "stay":
                functions.stay()
                break
            
            if a == "hit":
                functions.hit(players[user_name]["hand"], live_deck)
                new_card = players[user_name]["hand"][-1] #get the last card added to the hand
                hand_value = functions.calculate_hand_value(players[user_name]["hand"])
                print(f"New Card: {new_card}")
                print(f"You have: {players[user_name]['hand']}")
                print(f"New total: {hand_value}")
                if hand_value == 21:
                    print("NICE!")
                elif hand_value > 21:
                    print("BUST!")
                    break

        hand_value = functions.calculate_hand_value(players[user_name]["hand"])
        if hand_value == 21 and len(players[user_name]["hand"]) == 2:
            print("BLACKJACK!")
        else:
            print(f"You: {hand_value}")


        #Introduce the dealer to end the round
        print("And finally, the Dealer")
        print(f"Dealer: {players['Dealer']['hand']}")
        #give dealer a second card
        functions.hit(players["Dealer"]["hand"], live_deck)
        new_card = players["Dealer"]["hand"][-1] #get the last card added to the hand
        hand_value = functions.calculate_hand_value(players["Dealer"]["hand"])
        print(f"second_card: {new_card}")
        print(f"Dealer: {players['Dealer']['hand']}")
        print(f"Total: {hand_value}")


        if functions.calculate_hand_value(players["Dealer"]["hand"]) in [17, 18 ,19 ,20]:
            print(f"Dealer has {hand_value}")
            functions.stay()
        elif functions.calculate_hand_value(players["Dealer"]["hand"]) == 21:
            print("Oh no, dealer has Blackjack")


        while functions.calculate_hand_value(players["Dealer"]["hand"]) <= 16: #continue hitting until Dealer holds >16 or busts
            functions.hit(players["Dealer"]["hand"], live_deck)
            new_card = players["Dealer"]["hand"][-1] #get the last card added to the hand
            hand_value = functions.calculate_hand_value(players["Dealer"]["hand"])
            print(f"New card: {new_card}")
            print(f"Dealer: {players['Dealer']['hand']}")
            print(f"Total: {hand_value}")

            if hand_value == 21:
                print("Oh no, Dealer has 21")
            elif hand_value in [17, 18, 19, 20]:
                print(f"Dealer has: {hand_value}")
                functions.stay()
                pass
            else:
                print("Dealer bust")

            

    print("So, who are the winners & losers?")

    #determine winners, losers, blackjack, bust and push hands in a list
    winners = []
    losers = []
    push = []
    blackjack = []

    player_hand = players[player_name]["hand"]

    if len(players) > 4:
        dealer_hand_value = functions.calculate_hand_value(players["Dealer"]["hand"])
        john_hand_value = functions.calculate_hand_value(players["John"]["hand"])
        ivan_hand_value = functions.calculate_hand_value(players["Ivan"]["hand"])    
        new_hand_1_value = functions.calculate_hand_value(player_hand)
        new_hand_2_value = functions.calculate_hand_value(players[user_name + "_split"]["hand"])


        # check dealer's hand
        if dealer_hand_value > 21:
            print("Dealer has busted!")
            if new_hand_1_value <= 21 and new_hand_2_value <= 21:
                players[user_name]["wallet"] += bet_amount * 4
            elif new_hand_1_value <= 21 or new_hand_2_value > 21:
                players[user_name]["wallet"] += bet_amount * 2
            else:
                losers.append(user_name)             

        else:
            if john_hand_value <= 21:
                if john_hand_value == 21 and len(players["John"]["hand"]) == 2:  # Blackjack condition
                    blackjack.append("John")
                elif john_hand_value > dealer_hand_value:
                    winners.append("John")
                elif john_hand_value == dealer_hand_value:
                    push.append("John")
                else:
                    losers.append("John")
            elif john_hand_value > 21:
                losers.append("John")

            if ivan_hand_value <= 21:
                if ivan_hand_value == 21 and len(players["Ivan"]["hand"]) == 2:  # Blackjack condition
                    blackjack.append("Ivan")
                elif ivan_hand_value > dealer_hand_value:
                    winners.append("Ivan")
                elif ivan_hand_value == dealer_hand_value:
                    push.append("Ivan")
                else:
                    losers.append("Ivan")
            elif ivan_hand_value > 21:
                losers.append("Ivan")

            if new_hand_1_value <= 21:
                if new_hand_1_value == 21 and len(new_hand_1) == 2:  # Blackjack condition
                    blackjack.append(user_name)
                    players[user_name]["wallet"] += bet_amount * 2.5 #pay 3/2 for blackjack
                elif new_hand_1_value > dealer_hand_value:
                    winners.append(user_name)
                    players[user_name]["wallet"] += bet_amount * 2 #pay evens for winning hand
                elif new_hand_1_value == dealer_hand_value:
                    push.append(user_name)
                    players[user_name]["wallet"] += bet_amount #return stake to wallet
                else:
                    losers.append(user_name)
            elif new_hand_1_value > 21:
                losers.append(user_name)
                
            if new_hand_2_value <= 21:
                if new_hand_2_value == 21 and len(new_hand_2) == 2:  # Blackjack condition
                    blackjack.append(user_name)
                    players[user_name]["wallet"] += bet_amount * 2.5 #pay 3/2 for blackjack
                elif new_hand_2_value > dealer_hand_value:
                    winners.append(user_name)
                    players[user_name]["wallet"] += bet_amount * 2 #pay evens for winning hand
                elif new_hand_2_value == dealer_hand_value:
                    push.append(user_name)
                    players[user_name]["wallet"] += bet_amount #return stake to wallet
                else:
                    losers.append(user_name)
            elif new_hand_2_value > 21:
                losers.append(user_name)

        if user_name in blackjack and "Dealer" not in blackjack:
            print(f"{user_name} wins! Congratulations! Blackjack pays 3/2")

    else:
        dealer_hand_value = functions.calculate_hand_value(players["Dealer"]["hand"])
        john_hand_value = functions.calculate_hand_value(players["John"]["hand"])
        ivan_hand_value = functions.calculate_hand_value(players["Ivan"]["hand"])
        you_hand_value = functions.calculate_hand_value(players[user_name]["hand"])

        # check dealer's hand
        if dealer_hand_value > 21:
            print("Dealer has busted!")
            for player in players:
                if player != "Dealer" and functions.calculate_hand_value(players[player]["hand"]) <= 21:
                    winners.append(player)
                    if player != "Dealer" and functions.calculate_hand_value(players[player]["hand"]) <= 20:
                        players[player]["wallet"] += bet_amount * 2
                    elif player != "Dealer" and functions.calculate_hand_value(players[player]["hand"]) == 21 and len(players[user_name]["hand"]) == 2:
                        players[player]["wallet"] += bet_amount * 2.5 #pay 3/2 for blackjack
                        blackjack.append(player)
                    elif player != "dealer" and functions.calculate_hand_value(players[player]["hand"]) == 21 and len(players[user_name]["hand"]) > 2:
                        players[player]["wallet"] += bet_amount * 2 #pay evens for non-blackjack 21                                                                                     
                else:
                    if player != "Dealer":
                        losers.append(player)
        else:
            if john_hand_value <= 21:
                if john_hand_value == 21 and len(players["John"]["hand"]) == 2:  # Blackjack condition
                    blackjack.append("John")
                elif john_hand_value > dealer_hand_value:
                    winners.append("John")
                elif john_hand_value == dealer_hand_value:
                    push.append("John")
                else:
                    losers.append("John")
            elif john_hand_value > 21:
                losers.append("John")

            if ivan_hand_value <= 21:
                if ivan_hand_value == 21 and len(players["Ivan"]["hand"]) == 2:  # Blackjack condition
                    blackjack.append("Ivan")
                elif ivan_hand_value > dealer_hand_value:
                    winners.append("Ivan")
                elif ivan_hand_value == dealer_hand_value:
                    push.append("Ivan")
                else:
                    losers.append("Ivan")
            elif ivan_hand_value > 21:
                losers.append("Ivan")

            if you_hand_value <= 21:
                if you_hand_value == 21 and len(players[user_name]["hand"]) == 2:  # Blackjack condition
                    blackjack.append(user_name)
                    players[user_name]["wallet"] += bet_amount * 2.5 #pay 3/2 for blackjack
                elif you_hand_value > dealer_hand_value:
                    winners.append(user_name)
                    players[user_name]["wallet"] += bet_amount *2 #pay evens for winning hand
                elif you_hand_value == dealer_hand_value:
                    push.append(user_name)
                    players[user_name]["wallet"] += bet_amount #return stake to wallet
                else:
                    losers.append(user_name)
            elif you_hand_value > 21:
                losers.append(user_name)

        # Print player blackjacks
        if "John" in blackjack and "Dealer" not in blackjack:
            print("John wins! Blackjack pays 3/2")
        if "Ivan" in blackjack and "Dealer" not in blackjack:
            print("Ivan wins! Blackjack pays 3/2")
        if user_name in blackjack and "Dealer" not in blackjack:
            print(f"{user_name} wins! Congratulations! Blackjack pays 3/2")

    if winners:
        print("Winners:")
        for winner in winners:
            print(winner)

    if losers:
        print("Losers:")
        for loser in losers:
            print(loser)

    if push:
        print("Push:")
        for p in push:
            print(p)

    print(f"{user_name}'s wallet balance: {players[user_name]['wallet']}")


    #clear stored hands
    for player in players.values():
        player['hand'] = []


    choice = input("Do you want to play another hand? (yes/no): ") #ask if the player wants to continue
    if choice.lower() == "no":
        play_again = False