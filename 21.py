#!/usr/bin/env python3

import sys
import argparse
from game import Game
from pyfiglet import Figlet
from colorama import Style, Fore
from os import name, system


def print_welcome():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    f = Figlet(font='alligator', width=120)
    print(Style.BRIGHT + Fore.GREEN +
          '\n' + '-' * 55 + '\n')
    print(f'{f.renderText("        2  1")}')
    print('\n' + '-' * 55 + '\n' + Style.RESET_ALL)


def main():
    # Check for command-line arguments
    parser = argparse.ArgumentParser(
        description='Play a game of blackjack.')
    parser.add_argument('-d', '--decks', nargs='?', default=-1, type=int,
                        choices=range(1,9), metavar='1-8', help='Set number of decks')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Run in debug mode')
    parser.add_argument('--test', action='store_true',
                        help='Jump straight to current test')
    args = parser.parse_args(sys.argv[1:])

    print_welcome()

    # Set number of decks
    try:
        # Check if the user passed a valid number of decks via command line, and use it if so
        if args.decks in range(1, 9):
            num_decks = args.decks
        else:
            num_decks = input(
                'Enter 1-8 for number of decks (default 1):')
            num_decks = int(num_decks[0])
            # If the user gave invalid input or no input, use the default
            if num_decks not in range(1, 5):
                num_decks = 1
    # Either the user pressed enter for the default, or they can't even be trusted to type in an integer
    except Exception:
        num_decks = 1

    game = Game(num_decks, args.debug)
    game.play()


if __name__ == '__main__':
    main()
