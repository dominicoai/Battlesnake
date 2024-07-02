import unittest
from main import simulate_move, check_collision
class TestSimulateMove(unittest.TestCase):
    def setUp(self):
        self.base_state = {
            "my_snake": {
                "head": {"x": 5, "y": 5},
                "body": [{"x": 5, "y": 5}, {"x": 5, "y": 4}, {"x": 5, "y": 3}],
                "health": 100
            },
            "board": {
                "width": 11,
                "height": 11,
                "food": [],
                "snakes": []
            },
            "turn": 0
        }

    def test_move_up(self):
        expected_head = {"x": 5, "y": 6}
        result = simulate_move(self.base_state, "up")
        self.assertEqual(result["my_snake"]["head"], expected_head)

    def test_move_down(self):
        expected_head = {"x": 5, "y": 4}
        result = simulate_move(self.base_state, "down")
        self.assertEqual(result["my_snake"]["head"], expected_head)

    def test_move_left(self):
        expected_head = {"x": 4, "y": 5}
        result = simulate_move(self.base_state, "left")
        self.assertEqual(result["my_snake"]["head"], expected_head)

    def test_move_right(self):
        expected_head = {"x": 6, "y": 5}
        result = simulate_move(self.base_state, "right")
        self.assertEqual(result["my_snake"]["head"], expected_head)

    def test_wall_collision(self):
        # Move the snake to the edge of the board
        self.base_state["my_snake"]["head"] = {"x": 0, "y": 5}
        result = simulate_move(self.base_state, "left")
        self.assertTrue(check_collision(result))

    def test_body_collision(self):
        # Attempt to move back into its own body
        result = simulate_move(self.base_state, "down")
        self.assertTrue(check_collision(result))

    def test_no_collision(self):
        result = simulate_move(self.base_state, "up")
        self.assertFalse(check_collision(result))

if __name__ == '__main__':
    unittest.main()