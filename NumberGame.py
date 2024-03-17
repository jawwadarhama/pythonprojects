from __future__ import annotations
import random

class NumberGame:
    """A number game for two players.

    A count starts at 0. On a player's turn, they add to the count an amount
    between a set minimum and a set maximum. The player who brings the count
    to a set goal amount is the winner.

    The game can have multiple rounds.

    === Attributes ===
    goal:
        The amount to reach in order to win the game.
    min_step:
        The minimum legal move.
    max_step:
        The maximum legal move.
    current:
        The current value of the game count.
    players:
        The two players.
    turn:
        The turn the game is on, beginning with turn 0.
        If turn is even number, it is players[0]'s turn.
        If turn is any odd number, it is player[1]'s turn.

    === Representation invariants ==
    - self.turn >= 0
    - 0 <= self.current <= self.goal
    - 0 < self.min_step <= self.max_step <= self.goal
    """
    goal: int
    min_step: int
    max_step: int
    current: int
    players: tuple[Player, Player]
    turn: int

    def __init__(self, goal: int, min_step: int, max_step: int,
                 players: tuple[Player, Player]) -> None:
        """Initialize this NumberGame.

        Preconditions:
            0 < min_step <= max_step <= goal
        """
        self.goal = goal
        self.min_step = min_step
        self.max_step = max_step
        self.current = 0
        self.players = players
        self.turn = 0

    def play(self) -> str:
        """Play one round of this NumberGame. Return the name of the winner.

        A "round" is one full run of the game, from when the count starts
        at 0 until the goal is reached.
        """
        while self.current < self.goal:
            self.play_one_turn()
        # The player whose turn would be next (if the game weren't over) is
        # the loser. The one who went one turn before that is the winner.
        winner = self.whose_turn(self.turn - 1)
        return winner.name

    def whose_turn(self, turn: int) -> Player:
        """Return the Player whose turn it is on the given turn number.
        """
        if turn % 2 == 0:
            return self.players[0]
        else:
            return self.players[1]

    def play_one_turn(self) -> None:
        """Play a single turn in this NumberGame.

        Determine whose move it is, get their move, and update the current
        total as well as the number of the turn we are on.
        Print the move and the new total.
        """
        next_player = self.whose_turn(self.turn)
        amount = next_player.move(
            self.current,
            self.min_step,
            self.max_step,
            self.goal
        )
        self.current += amount
        self.turn += 1

        print(f'{next_player.name} moves {amount}.')
        print(f'Total is now {self.current}.')


class Player:
    """
    Player of the game <NumberGame>
    """
    def __init__(self, name):
        self.name = name

    def move(self, current: int, min_step: int, max_step: int, goal: int):
        raise NotImplementedError


class RandomPlayer(Player):

    def move(self, current: int, min_step: int, max_step: int, goal: int)->int:
        return random.randint(min_step,max_step)


class UserPlayer(Player):

    def move(self, current: int, min_step: int, max_step: int, goal: int)->int:
        while True:
            move = int(input(f'Input your move between {min_step} and'
                             f' {max_step}:'))
            if min_step <= move <= max_step:
                return move
            else:
                print("Invalid move. Try Again!")


class StrategicPlayer(Player):

    def move(self, current: int, min_step: int, max_step: int, goal: int)->int:
        remaining = goal - current
        if remaining >= max_step:
            return max_step
        elif remaining < min_step:
            return min_step
        else:
            return remaining % (max_step + 1)


def make_player(generic_name: str) -> Player:
    """Return a new Player based on user input.

    Allow the user to choose a player name and player type.
    <generic_name> is a placeholder used to identify which player is being made.
    """
    name = input(f'Enter a name {generic_name}: ')
    player_type = input(f'Select player type for {generic_name}'
                        f'(random/user/strategic): ').lower()
    if player_type == 'random':
        return RandomPlayer(name)
    elif player_type == 'user':
        return UserPlayer(name)
    elif player_type == 'strategic':
        return StrategicPlayer(name)
    else:
        print('Invalid player type. Choosing RandomPlayer by default.')
        return RandomPlayer()

def main() -> None:
    """Play multiple rounds of a NumberGame based on user input settings.
    """
    goal = int(input('Enter goal amount: '))
    minimum = int(input('Enter minimum move: '))
    maximum = int(input('Enter maximum move: '))
    p1 = make_player('p1')
    p2 = make_player('p2')
    while True:
        g = NumberGame(goal, minimum, maximum, (p1, p2))
        winner = g.play()
        print(f'And {winner} is the winner!!!')
        print(p1)
        print(p2)
        again = input('Again? (y/n) ')
        if again != 'y':
            return print("Thanks for playing!")


if __name__ == '__main__':
    main()
