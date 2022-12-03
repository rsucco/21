from os import name, system
from re import I

from colorama import Fore, Back, Style, init

from card import Card
from deck import Deck
from message import Message


class Game:
    def __init__(self, num_decks=1, debug=False):
        # Initialize colorama to enable styled terminal output on Windows
        init()
        self.num_decks = num_decks
        self.debug = debug
        self.messages = [Message()]
        self.deck = Deck(num_decks)
        self.cash = 100.0
        self.bet = 0
        self.split_bet = 0
        self.dealer_hand = []
        self.player_hand = []
        self.split_hand = []
        

    # Clear the screen with the appropriate terminal command for the system
    def clear(self):
        # Don't clear the screen in debug mode. This helps with debugging because it enables scrollback to see snapshots of game state change
        if not self.debug:
            if name == 'nt':
                system('cls')
            else:
                system('clear')

    # Can be used directly or passed as a callback to player objects so they can write to the UI
    def set_message(self, *messages, **kwargs):
        # If the replace_line argument is passed, use it
        try:
            if kwargs['replace_line']:
                replace_line = kwargs['replace_line']
            else:
                replace_line = -1
        # If the kwarg wasn't included, make it -1 to ignore
        except Exception:
            replace_line = -1
        messages_list = list(Message(message) for message in messages)
        if replace_line > -1:
            while len(self.messages) <= replace_line:
                self.messages.append(Message(''))
            self.messages[replace_line] = messages_list[0]
        else:
            self.messages = messages_list
        self.draw_game()

    # Renders a list of Message objects inside in a nice little box
    def render_ui_messages(self, messages, render_strs=[''] * 9, width=80, margin_left=10):
        render_strs = [render_str + ' ' * margin_left for render_str in render_strs]
        render_strs[0] += '╓' + '─' * width + '╖'
        for i, message in enumerate(messages, start=1):
            render_strs[i] += '║ ' + message.ljust(width) + ' ║'
        for i in range(len(messages) + 1, 8):
            render_strs[i] += '║' + ' ' * width + '║'
        render_strs[8] += '╙' + '─' * width + '╜'
        return render_strs

    def render_ui_table(self, show_dealer, render_strs=[''] * 12, margin_left = 10):
        start = Style.RESET_ALL + Back.GREEN + Fore.WHITE
        end = Style.RESET_ALL
        render_strs = [render_str + " " * margin_left for render_str in render_strs]
        render_strs[0] += f'{start}                                                                     {end}'
        if show_dealer:
            dealer_hand = Message("".join(str(card) for card in self.dealer_hand) + Back.GREEN).center(68)
            render_strs[1] += f'{start} {dealer_hand}{start}{end}'
        else:
            render_strs[1] += f'{start}                                 {self.dealer_hand[0]} *{start}                                {end}'
        render_strs[2] += f'{start}        ╒═══════════════════════════════════════════════════╕        {end}'
        render_strs[3] += f'{start}        │              {Style.BRIGHT}{Fore.YELLOW}DEALER MUST HIT SOFT 17{start}              │        {end}'
        render_strs[4] += f'{start}        │  {Style.BRIGHT}{Fore.RED}BLACKJACK PAYS 3 TO 2     INSURANCE PAYS 2 TO 1{start}  │        {end}'
        render_strs[5] += f'{start}        ╘═══════════════════════════════════════════════════╛        {end}'
        render_strs[6] += f'{start}                                                                     {end}'
        render_strs[7] += f'{start}        ╭─────────────────╮               ╭─────────────────╮        {end}'
        hand = Message(''.join(str(card) for card in self.player_hand) + Back.GREEN).ljust(19)
        split_hand = Message(''.join(str(card) for card in self.split_hand) + Back.GREEN).ljust(19)
        render_strs[8] += f'{start}        │{hand}│               │{split_hand}│        {end}'
        render_strs[9] += f'{start}        ╰─────────────────╯               ╰─────────────────╯        {end}'
        render_strs[10] += f'{start}                                                                     {end}'

        return render_strs

    def draw_game(self, show_dealer = False):
        self.clear()
        # Helper method to print out a list of strings
        def render(render_strs):
            for render_str in render_strs:
                print(render_str)
        show_dealer = True
        render_strs = self.render_ui_table(show_dealer)
        render(render_strs)
        

        print('Dealer hand:', str(self.dealer_hand[0]), '*')
        print('Your hand:  ', ''.join(str(card) for card in self.player_hand))

    # Core game loop
    def play(self):
        # Play until out of money. Probably a life lesson there.
        while self.cash > 0:
            # Start a new shoe by creating a deck, shuffling it, 
            self.deck = Deck(self.num_decks)
            self.deck.shuffle()
            marker_position = int(len(self.deck) * 0.25)
            # Play hands until the marker is reached, then shuffle after that hand
            while len(self.deck) > marker_position:
                self.split_hand = []
                self.player_hand, self.dealer_hand = self.deck.deal_hands()
                self.draw_game()
                input()
                
