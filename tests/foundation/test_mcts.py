import unittest

from vanguard.mcts import ActionCandidate, MCTSController, SearchState


class MCTSTests(unittest.TestCase):
    def test_selects_highest_value_action(self):
        controller = MCTSController(
            evaluator=lambda _state, action: {"a": 0.2, "b": 0.9, "c": 0.4}[action.action_id]
        )
        result = controller.select(
            SearchState("s1", "choose capability"),
            [ActionCandidate("a", "A"), ActionCandidate("b", "B"), ActionCandidate("c", "C")],
        )
        self.assertEqual(result.action.action_id, "b")
        self.assertEqual(result.value, 0.9)
        self.assertEqual(result.trace, ("s1", "b"))

    def test_empty_action_space(self):
        result = MCTSController().select(SearchState("s1", "none"), [])
        self.assertIsNone(result.action)
        self.assertEqual(result.visits, 0)


if __name__ == "__main__":
    unittest.main()
