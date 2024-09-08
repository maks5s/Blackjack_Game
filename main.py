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

        card_value = self.get_value()

        if self.dealer and not show_dealer_cards and not self.is_blackjack() and len(self.cards):
            # Subtracting the value of the first dealer`s card which is hidden
            # because of show_dealer_cards variable
            card_value -= int(self.cards[0].rank["value"])

        print(f"Value: {card_value} \n")


class Game:
    def __init__(self):
        self.money = 50000
        self.bet = 0

    def play(self):
        print("Welcome to the Blackjack\n")

        game_number = 0

        while self.money > 0:
            print(f"Your budget is: {self.money}\n")

            is_playing = input("Enter 'Yes' or 'Y' to start a new game:").lower()

            if is_playing not in ['yes', 'y']:
                break

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
            print(f"Game #{game_number}")
            print("*" * 30)

            print(f"\nYour budget is: {self.money}\n")

            self.bet = 0

            while self.bet <= 0 or self.bet > self.money:
                try:
                    self.bet = int(input("Enter your bet: "))
                    if self.bet <= 0:
                        raise Exception("\nBet must be more than 0!\n")
                    if self.bet > self.money:
                        raise Exception(f"\nBet must be lower than your budget ({self.money})!\n")

                except ValueError:
                    print("\nPlease enter a correct number!\n")

                except Exception as e:
                    print(e)

            self.money -= self.bet

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

        if self.money == 0:
            print("You lost all your budget!😥")

        print("\nThanks for playing!")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You have more than 21. You lost!\n")
                return True

            elif dealer_hand.get_value() > 21:
                print("Dealer has more than 21. You win!\n")
                self.win_bet()
                return True

            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("You and Dealer both have a Blackjack. Tie!\n")
                self.tie_bet()
                return True

            elif player_hand.is_blackjack():
                print("You have a Blackjack! You win!\n")
                self.win_bet()
                return True

            elif dealer_hand.is_blackjack():
                print("Dealer has a Blackjack! You lost!\n")
                return True

        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("Your`s hand value is higher than Dealer`s. You win!\n")
                self.win_bet()
            elif player_hand.get_value() == dealer_hand.get_value():
                print("Your`s hand value is equal to Dealer`s. Tie!\n")
                self.tie_bet()
            else:
                print("Your`s hand value is lower than Dealer`s. You lost!\n")

            return True

        return False

    def win_bet(self):
        self.money += self.bet * 2

    def tie_bet(self):
        self.money += self.bet


game = Game()
game.play()
