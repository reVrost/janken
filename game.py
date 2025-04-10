import random
from typing import Optional

MOVES = ['rock', 'paper', 'scissors']

class Player:
    def __init__(self, name: str, mover):
        self.name = name
        self.score = 0
        self.mover = mover

    def make_move(self) -> str:
        return self.mover.make_move(self)

class HumanMover:
    def make_move(self, player: Player) -> str:
        while True:
            choice = input(f"{player.name}, enter your move (rock/paper/scissors): ").strip().lower()
            if choice in MOVES:
                return choice
            print("Invalid choice. Please enter rock, paper, or scissors.")

class ComputerMover:
    def make_move(self, _: Player) -> str:
        return random.choice(MOVES)

class Game:
    WINNING_PAIRS = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }

    def __init__(self, player1: Player, player2: Player, rounds: int):
        self.players = (player1, player2)
        self.rounds = rounds

    def determine_winner(self, move1: str, move2: str) -> Optional[Player]:
        if move1 == move2:
            return None
        if self.WINNING_PAIRS[move1] == move2:
            return self.players[0]
        return self.players[1]

    def play_round(self):
        move1 = self.players[0].make_move()
        move2 = self.players[1].make_move()
        print(f"\n{self.players[0].name} played {move1}")
        print(f"{self.players[1].name} played {move2}")

        winner = self.determine_winner(move1, move2)
        if winner:
            winner.score += 1
            print(f"{winner.name} wins this round!")
        else:
            # Noone gets any point for a draw
            print("It's a draw!")

    def play_game(self):
        print(f"\nStarting Paper Scissors Rock - Best of {self.rounds} rounds!")

        for round_num in range(1, self.rounds + 1):
            print(f"\nRound {round_num}:")
            self.play_round()

        print("\n------------------------")
        print("\nGame over! Final scores:")
        for player in self.players:
            print(f"{player.name}: {player.score}")


def main():
    print("Welcome to Janken! (Scissors Paper Rock)")
    player_name = input("Enter your name: ").strip() or "Player"
    rounds = int(input("How many rounds would you like to play? "))

    human = Player(player_name, HumanMover())
    computer = Player("Computer", ComputerMover())

    game = Game(human, computer, rounds)
    game.play_game()

if __name__ == "__main__":
    main()
