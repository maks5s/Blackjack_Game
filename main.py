import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = [{"rank": "A", "value": 11},
                 {"rank": "2", "value": 2},
                 {"rank": "3", "value": 3},
                 {"rank": "4", "value": 4},
                 {"rank": "5", "value": 5},
                 {"rank": "6", "value": 6},
                 {"rank": "7", "value": 7},
                 {"rank": "8", "value": 8},
                 {"rank": "9", "value": 9},
                 {"rank": "10", "value": 10},
                 {"rank": "J", "value": 10},
                 {"rank": "Q", "value": 10},
                 {"rank": "K", "value": 10},]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []

        for _ in range(number):
            cards_dealt.append(self.cards.pop())

        return cards_dealt


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value

            if card.rank["rank"] == "A":
                has_ace = True

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.value == 21

    def display_cards(self, show_dealer_cards=False):
        print(f'''{"Dealer`s" if self.dealer else "Your`s"} hand:''')

        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_dealer_cards and not self.is_blackjack():
                print("Hidden card")
            else:
                print(card)

        if not self.dealer:
            print(f"Value: {self.get_value()}")
        print("\n")


class Game:
    def play(self):
        game_number = 0
        games_to_play = 0

        while games_to_play <= 0:
            try:
                game_number = int(input("How many games do u wanna play? "))
            except:
                print("Please enter a correct number")

        while game_number <= games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for _ in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print("\n")
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)

            player_hand.display_cards()
            dealer_hand.display_cards()
