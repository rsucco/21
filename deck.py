from card import Card
import random


class Deck:
    def __init__(self, num_decks=1):
        # Create a super-deck composed of as many decks as requested
        self.cards = []
        for num_rank in range(1, 14):
            for suit in ['c', 's', 'h', 'd']:
                card = Card(num_rank, suit)
                for i in range(num_decks):
                    self.cards.append(card)

    def __len__(self):
        return len(self.cards)

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal the player and dealer hands
    def deal_hands(self):
        hands = [self.cards[:4:2], self.cards[1:4:2]]
        self.cards = self.cards[4:]
        return hands

    # Take a card from the top of a pile (pop from the stack)
    def draw_card(self):
        return self.cards.pop(0)
