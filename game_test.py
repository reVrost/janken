import unittest
from unittest.mock import patch
from io import StringIO
from game import Player, HumanMover, ComputerMover, Game, MOVES

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player("Test", HumanMover())
        self.assertEqual(player.name, "Test")
        self.assertEqual(player.score, 0)

    def test_make_move_with_human_mover(self):
        player = Player("Test", HumanMover())
        with patch('builtins.input', return_value='rock'):
            move = player.make_move()
            self.assertEqual(move, 'rock')

    def test_make_move_with_computer_mover(self):
        player = Player("Test", ComputerMover())
        move = player.make_move()
        self.assertIn(move, MOVES)

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Player1", HumanMover())
        self.player2 = Player("Player2", HumanMover())
        self.game = Game(self.player1, self.player2, 3)

    def test_determine_winner_rock_vs_scissors(self):
        winner = self.game.determine_winner('rock', 'scissors')
        self.assertEqual(winner, self.player1)

    def test_determine_winner_paper_vs_rock(self):
        winner = self.game.determine_winner('paper', 'rock')
        self.assertEqual(winner, self.player1)

    def test_determine_winner_scissors_vs_paper(self):
        winner = self.game.determine_winner('scissors', 'paper')
        self.assertEqual(winner, self.player1)

    def test_determine_winner_draw(self):
        winner = self.game.determine_winner('rock', 'rock')
        self.assertIsNone(winner)

    def test_determine_winner_losing_conditions(self):
        self.assertEqual(self.game.determine_winner('scissors', 'rock'), self.player2)
        self.assertEqual(self.game.determine_winner('rock', 'paper'), self.player2)
        self.assertEqual(self.game.determine_winner('paper', 'scissors'), self.player2)

class TestGamePlay(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Player1", ComputerMover())
        self.player2 = Player("Player2", ComputerMover())
        self.game = Game(self.player1, self.player2, 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_play_round(self, mock_stdout):
        with patch('game.random.choice', side_effect=['rock', 'scissors']):
            self.game.play_round()
            output = mock_stdout.getvalue()
            self.assertIn("Player1 played rock", output)
            self.assertIn("Player2 played scissors", output)
            self.assertIn("Player1 wins this round!", output)
            self.assertEqual(self.player1.score, 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game(self, mock_stdout):
        with patch('game.random.choice', side_effect=['paper', 'rock', 'scissors', 'paper']):
            game = Game(self.player1, self.player2, 2)
            game.play_game()
            output = mock_stdout.getvalue()
            self.assertIn("Starting Paper Scissors Rock", output)
            self.assertIn("Game over! Final scores", output)

class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=['TestPlayer', '3', 'rock', 'paper', 'scissors'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout, mock_input):
        from game import main
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Welcome to Janken!", output)
        self.assertIn("Game over! Final scores", output)

if __name__ == '__main__':
    unittest.main()
