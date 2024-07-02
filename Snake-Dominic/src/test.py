import unittest
from unittest.mock import patch
from minimax import alphabeta

class TestAlphaBeta(unittest.TestCase):
    def setUp(self):
        self.state = {"my_snake": {"head": {"x": 0, "y": 0}, "body": [{"x": 0, "y": 0}], "health": 100},
                      "board": {"width": 3, "height": 3, "food": [], "snakes": []},
                      "turn": 0}

    @patch('minimax.is_terminal', return_value=True)
    @patch('minimax.evaluate', return_value=10)
    def test_alphabeta_terminal_state(self, mock_evaluate, mock_is_terminal):
        score = alphabeta(self.state, 1, -float('inf'), float('inf'), True)
        self.assertEqual(score, 10)

    @patch('minimax.is_terminal', side_effect=[False, True, True])
    @patch('minimax.get_next', return_value=[{"dummy_state_1": None}, {"dummy_state_2": None}])
    @patch('minimax.evaluate', side_effect=[5, 7])
    def test_alphabeta_non_terminal_maximizing(self, mock_evaluate, mock_get_next, mock_is_terminal):
        score = alphabeta(self.state, 1, -float('inf'), float('inf'), True)
        self.assertEqual(score, 7)

    @patch('minimax.is_terminal', side_effect=[False, True, True])
    @patch('minimax.get_next', return_value=[{"dummy_state_1": None}, {"dummy_state_2": None}])
    @patch('minimax.evaluate', side_effect=[5, 3])
    def test_alphabeta_non_terminal_minimizing(self, mock_evaluate, mock_get_next, mock_is_terminal):
        score = alphabeta(self.state, 1, -float('inf'), float('inf'), False)
        self.assertEqual(score, 3)

    # Additional tests for pruning can be added here following a similar pattern

if __name__ == '__main__':
    unittest.main()