from colorama import Fore, Back, Style
from message import Message


class Card:
    SPADES = Fore.LIGHTYELLOW_EX + '[s]pades ♠' + Style.RESET_ALL
    HEARTS = Fore.RED + '[h]earts ♥' + Style.RESET_ALL
    CLUBS = Fore.GREEN + '[c]lubs ♣' + Style.RESET_ALL
    DIAMONDS = Style.BRIGHT + Fore.BLUE + '[d]iamonds ♦' + Style.RESET_ALL

    def __init__(self, num_rank=0, suit='0'):
        self.num_rank = num_rank
        self.suit = suit
        # Give the correct rank to ace, jack, queen, and king
        if num_rank == 1:
            self.rank = 'A'
        elif num_rank == 10:
            self.rank = 'T'
        elif num_rank == 11:
            self.rank = 'J'
        elif num_rank == 12:
            self.rank = 'Q'
        elif num_rank == 13:
            self.rank = 'K'
        else:
            self.rank = str(num_rank)

    # String representation should be snazzy, and str should only be used for terminal UI stuff
    def __str__(self):
        # Spades yellow, hearts red, clubs green, diamonds blue
        card_str = Back.BLACK
        if self.suit == 's':
            card_str += Fore.LIGHTYELLOW_EX + self.rank + '♠' + Style.RESET_ALL
        elif self.suit == 'h':
            card_str += Fore.RED + self.rank + '♥' + Style.RESET_ALL
        elif self.suit == 'c':
            card_str += Fore.GREEN + self.rank + '♣' + Style.RESET_ALL
        elif self.suit == 'd':
            card_str += Style.BRIGHT + Fore.BLUE + self.rank + '♦' + Style.RESET_ALL
        else:
            card_str += str(self.rank)
        return card_str

    def render_card(self, render_strs=None):
        if render_strs is None:
            render_strs = [''] * 5
        render_strs[0] = '┌───┐'
        render_strs[1] = '│   │'
        render_strs[2] = '│' + Message(str(self)) + '│'
        render_strs[3] = '│   │'
        render_strs[4] = '└───┘'

    # Equality is determined by rank and suit
    def __eq__(self, other):
        return (self.rank == other.rank and self.suit == other.suit) or (self.rank == other.rank and self.suit == '0')

    # Less than is determined by rank
    def __lt__(self, other):
        return self.num_rank < other.num_rank

    # Rank and suit are enough to make the object unique
    def __hash__(self):
        return hash((self.rank, self.suit))

    def __copy__(self):
        return Card(self.num_rank, self.suit)

    def get_suit(self):
        # Spades yellow, hearts red, clubs green, diamonds blue
        card_str = ''
        if self.suit == 's':
            card_str = Fore.LIGHTYELLOW_EX + '♠' + Style.RESET_ALL
        elif self.suit == 'h':
            card_str = Fore.RED + '♥' + Style.RESET_ALL
        elif self.suit == 'c':
            card_str = Fore.GREEN + '♣' + Style.RESET_ALL
        elif self.suit == 'd':
            card_str = Style.BRIGHT + Fore.BLUE + '♦' + Style.RESET_ALL
        else:
            card_str = Style.BRIGHT + str(self.rank) + Style.RESET_ALL
        return card_str

    def plays_on(self, other_card):
        if self.rank == '8' or self.suit == other_card.suit or self.rank == other_card.rank:
            return True
        else:
            return False
