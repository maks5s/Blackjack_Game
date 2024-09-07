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
        suits = ["Hearts ♥", "Diamonds ♦", "Clubs ♣", "Spades ♠"]
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
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []

        for _ in range(number):
            if len(self.cards) > 0:
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
        ace_count = 0

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value

            if card.rank["rank"] == "A":
                ace_count += 1

        if ace_count > 0 and self.value > 21:
            self.value -= 10
            ace_count -= 1

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display_cards(self, show_dealer_cards=False):
        print(f'''{"Dealer`s" if self.dealer else "Your`s"} hand:''')

        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_dealer_cards and not self.is_blackjack():
                print("Hidden card")
            else:
                print(card)

        if not self.dealer:
            print(f"Value: {self.get_value()}")
        print()


class Game:
    def play(self):
        game_number = 0
        games_to_play = 0

        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except:
                print("Please enter a correct number: ")

        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for _ in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)

            player_hand.display_cards()
            dealer_hand.display_cards()

            if self.check_winner(player_hand, dealer_hand):
                continue

            choice = ""

            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("Choose 'Hit' or 'Stand' ('H' or 'S'): ").lower()
                print()

                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please choose correct option ('Hit' / 'H' or 'Stand' / 'S'): ").lower()
                    print()

                if choice in ["h", "hit"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display_cards()

            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display_cards(show_dealer_cards=True)

            if self.check_winner(player_hand, dealer_hand):
                continue

            print("Final Results:")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, game_over=True)

        print("\nThanks for playing!")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You have more than 21. You lost!")
                return True

            elif dealer_hand.get_value() > 21:
                print("Dealer has more than 21. You win!")
                return True

            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("You and Dealer both have a Blackjack. Tie!")
                return True

            elif player_hand.is_blackjack():
                print("You have a Blackjack! You win!")
                return True

            elif dealer_hand.is_blackjack():
                print("Dealer has a Blackjack! You lost!")
                return True

        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("Your`s hand value is higher than Dealer`s. You win!")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("Your`s hand value is equal to Dealer`s. Tie!")
            else:
                print("Your`s hand value is lower than Dealer`s. You lost!")

            return True

        return False


game = Game()
game.play()
