import random
import uuid
from enum import Enum
from pprint import pprint
from typing import List, Dict, Any, Optional

import attr

"""
This is a pseudo-random game of non-interactive blackjack.

The player must choose a number at which to stay,
and then see their win percentage
after their virtual player runs out of funds.

As we are not limited by the physical constraints of a deck of cards,
we have an infinitely self-shuffling random card generator
in the Card class itself.

The only limitation on our randomness is the limit of computers
themselves in being able to produce truly "random" numbers,
but I think this will suffice for our purposes :)

The purpose of this specific code is pedagogical,
intending to serve as a non-trivial example of an object oriented program
for learning programmers.

Also, this project serves as a reminder of why gambling is bad for you.
"""


class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    SPADES = 3
    CLUBS = 4


class Value(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10
    ACE = 11


class Strength(Enum):
    """ Hands with ACEs are soft,
    and we must allow handle such soft hands optimally
    on behalf of the player.
    """
    SOFT = 1
    HARD = 2


def random_element(xs: List[Any]) -> Any:
    return xs[random.randint(0, len(xs) - 1)]


@attr.s
class Card:
    value: Value = attr.ib(factory=lambda: random_element([v for v in Value]))
    suit: Suit = attr.ib(factory=lambda: random_element([s for s in Suit]))


@attr.s
class Hand:
    cards: List[Card] = attr.ib(factory=list)

    def get_value(self) -> int:
        return sum([c.value.value for c in self.cards])
        # TODO: optimally handle "Soft" hands (where Aces are present)
        # if self.get_strength() == Strength.HARD:
        #     return sum([c.value.value for c in self.cards])
        # else:
        #     number_of_aces = len([c for c in self.cards
        #                           if c.value == Value.ACE])
        #     non_ace_value = sum([c.value.value for c in self.cards
        #                          if not c.value == Value.ACE])
        #     want to get the closest value to 21, but not go over if possible
        # pass

    def get_strength(self) -> Strength:
        return Strength.SOFT \
            if Value.ACE in [c.value for c in self.cards] \
            else Strength.HARD


@attr.s
class Player:
    hand: Hand = attr.ib(factory=Hand)
    money: int = attr.ib(default=200)
    pending_bet: int = attr.ib(default=0)
    hit_threshold: int = attr.ib(default=15)
    rounds_survived: int = attr.ib(default=0)
    player_id: uuid.UUID = attr.ib(factory=uuid.uuid4)
    wins: int = attr.ib(default=0)
    loses: int = attr.ib(default=0)

    def place_bet(self, bet: int) -> None:
        self.pending_bet = bet

    def hit(self) -> None:
        self.hand.cards.append(Card())

    def is_active(self) -> bool:
        return self.money > 0

    def is_bust(self) -> bool:
        return self.hand.get_value() > 21

    def should_hit(self) -> bool:
        return self.hand.get_value() < self.hit_threshold

    def should_stay(self) -> bool:
        return not self.should_hit()

    def __increment_rounds_survived__(self) -> None:
        if self.is_active():
            self.rounds_survived += 1

    def handle_result(self, dealer_score: int) -> None:
        self.__increment_rounds_survived__()
        if self.is_bust():
            self.money -= self.pending_bet
            self.loses += 1
        elif self.hand.get_value() > dealer_score:
            self.money += self.pending_bet
            self.wins += 1
        else:
            self.money -= self.pending_bet
            self.loses += 1
        self.pending_bet = 0
        self.hand = Hand()

    def get_stats(self) -> Dict:
        return {'player_id': str(self.player_id),
                'hit_threshold': self.hit_threshold,
                'rounds_survived': self.rounds_survived,
                'wins': self.wins,
                'loses': self.loses}


@attr.s
class Dealer(Player):
    hit_threshold = attr.ib(default=17)

    def deal(self, players: List[Player]) -> None:
        for player in players + [self]:
            for i in range(2):
                player.hit()

    def show(self) -> Optional[Card]:
        if len(self.hand.cards) >= 2:
            return self.hand.cards[1]
        else:
            return None


@attr.s
class Game:
    players: List[Player] = attr.ib(factory=list)
    ante: int = attr.ib(default=10)
    dealer: Dealer = attr.ib(factory=Dealer)
    game_num: int = attr.ib(default=1)

    def has_active_players(self) -> bool:
        return len([p for p in self.players if p.is_active()]) > 0

    def players_bet(self) -> None:
        for player in self.players:
            player.place_bet(self.ante)

    def setup_game(self):
        self.dealer.deal(self.players)

    @staticmethod
    def player_play(player: Player) -> None:
        done = not player.is_active()
        while not done:
            pprint(player)
            if player.should_hit():
                player.hit()
            if player.is_bust() or player.should_stay():
                done = True

    def players_play(self) -> None:
        for player in self.players:
            self.player_play(player)

    def finish_round(self) -> None:
        for player in self.players + [self.dealer]:
            if player.is_active():
                player.handle_result(self.dealer.hand.get_value())

    def play_round(self) -> None:
        print('Game Number: ' + str(self.game_num))
        self.players_bet()
        self.setup_game()
        self.players_play()
        self.player_play(self.dealer)
        self.finish_round()
        self.game_num += 1

    def play(self) -> Dict:
        while self.has_active_players():
            self.play_round()
        print('\n')
        print('=============================================')
        print('==============    GAME OVER    ==============')
        print('=============================================')
        print('End Game Summary:')
        end_game_summary = \
            {'total_number_of_games': self.game_num,
             'player_stats': sorted([p.get_stats() for p in self.players],
                                    key=lambda x: x['wins'])}
        pprint(end_game_summary)
        return end_game_summary


if __name__ == '__main__':
    Game(players=[Player(hit_threshold=i, money=1000) for i in range(22)],
         ante=1).play()
