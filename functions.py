import decks
from decks import deck, default_card_values


#define functions "hit" and "stay"
def hit(hand, live_deck):
    #take the first card from the deck and add it to the player's hand
    card = live_deck[0]
    hand.append(card)
    live_deck.pop(0)


def stay():
    print("stay")
    pass


def get_balance(players, player_name):
    if player_name in players:
        return players[player_name]["wallet"]
    else:
        print(f"Player '{player_name}' not found.")
        return None


#determine if split is possible
def check_equal_cards(hand):
    card1 = hand[0][0]
    card2 = hand[1][0]
    if card1 == card2:
        return True
    else:
        return False


#define total hand value
def calculate_hand_value(hand):
    total_value = 0
    num_aces = 0
    
    for card in hand:
        rank = card.split()[0]  # Extract the rank from the card string
        card_value = next((card['points'] for card in default_card_values if card['value'] == rank), None)
        
        if rank == "Ace":  # Handle Aces separately
            num_aces += 1
        else:
            total_value += card_value
            
    # Handle the value of Aces
    for _ in range(num_aces):
        if total_value + 11 <= 21:
            total_value += 11
        else:
            total_value += 1
        
    return total_value



#place bets
def take_bet(players, user_name):
    bet_amount = int(input("place your bet: "))
    players[user_name]["wallet"] -= bet_amount #deduct from user's wallet
    print(f"Your wallet: {players[user_name]['wallet']}")


