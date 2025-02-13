import unittest

import pandas as pd

from src.classes.cast_generator import CastGenerator


class TestCastGeneratorWithFixtures(unittest.TestCase):

    def setUp(self):
        # Load CSV fixtures
        self.roles = pd.read_csv("tests/fixtures/roles.csv")
        self.preferences = pd.read_csv("tests/fixtures/preferences.csv")
        self.available_members = [
            "Alex",
            "Dakota",
            "Avery",
            "Skyler",
            "Jamie",
            "Shawn",
            "Parker",
            "Reese",
            "Taylor",
            "Cameron",
            "Logan",
        ]

        # Mock the CastGenerator initialization
        self.cast_generator = CastGenerator(self.available_members, self.roles, self.preferences)

        # Recreate roles_long for testing
        roles_sub = self.roles[self.roles.member.isin(self.available_members)]
        roles_long = pd.melt(roles_sub, id_vars=["member"], var_name="role")
        self.roles_long = roles_long.loc[roles_long.value == 1]

    def test_roles_long_format(self):
        # Ensure roles_long is correctly generated
        pd.testing.assert_frame_equal(
            self.cast_generator.roles_long.reset_index(drop=True),
            self.roles_long.reset_index(drop=True),
        )

    def test_eligible_members(self):
        # Validate eligible_members method
        eligible_for_frank = self.cast_generator.eligible_members("Frank")
        roles = self.roles[self.roles.member.isin(self.available_members)]
        expected_eligible = roles.loc[roles["Frank"] == 1, "member"].tolist()
        self.assertListEqual(eligible_for_frank, expected_eligible)

    def test_assign_Sceddie(self):
        # Test assign_Sceddie method for Eddie
        self.cast_generator.assign_Sceddie("Eddie")
        self.assertGreater(len(self.cast_generator.full_casts), 0)
        for cast in self.cast_generator.full_casts:
            self.assertIn("Eddie", cast)

    def test_assign_standard_role(self):
        # Test assign_standard_role method for Frank
        self.cast_generator.assign_standard_role("Frank")
        self.assertGreater(len(self.cast_generator.full_casts), 0)
        for cast in self.cast_generator.full_casts:
            self.assertIn("Frank", cast)

    def test_get_preferences_for_casts(self):
        # Validate preference scores for casts
        self.cast_generator.full_casts = [{"Frank": "Alex", "Janet": "Taylor", "Brad": "Jordan"}]
        self.cast_generator.get_preferences_for_casts()

        for cast in self.cast_generator.full_casts:
            self.assertIn("preference_score", cast)
            self.assertIsInstance(cast["preference_score"], float)

    def test_get_all_casts(self):
        # Full integration test for get_all_casts
        all_casts = self.cast_generator.get_all_casts()
        self.assertIsInstance(all_casts, pd.DataFrame)
        self.assertGreater(len(all_casts), 0)
        self.assertIn("preference_score", all_casts.columns)

    def test_get_all_casts_failure(self):
        # Full integration test for get_all_casts with not enough people
        available_members = ["Alex", "Taylor", "Parker", "Rowan", "Quinn", "Cameron"]
        cast_generator = CastGenerator(available_members, self.roles, self.preferences)
        all_casts = cast_generator.get_all_casts()
        self.assertIsNone(all_casts)
