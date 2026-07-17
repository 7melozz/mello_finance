import unittest

from pydantic import ValidationError

from app.schemas.goal_schema import GoalCreate


class GoalSchemaTests(unittest.TestCase):
    def test_rejects_empty_title(self):
        with self.assertRaises(ValidationError):
            GoalCreate(user_id=1, title="   ", target_amount="100.00")

    def test_rejects_invalid_goal_type(self):
        with self.assertRaises(ValidationError):
            GoalCreate(user_id=1, title="Viagem", target_amount="100.00", goal_type="unknown")


if __name__ == "__main__":
    unittest.main()
