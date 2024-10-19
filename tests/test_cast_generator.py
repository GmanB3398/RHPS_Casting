from unittest import TestCase

from src.classes.cast_generator import CastGenerator

import pandas as pd


class TestGetPreferenceForCast(TestCase):

    def setUp(self):
        csv_path = "tests/fixtures/preferences.csv"
        self.data = pd.read_csv(csv_path)

        self.cast = {
            "cast_id": 0,
            "Riff": "Shawn",
            "Brad": "Taylor",
            "Janet": "Cameron",
            "Columbia": "Reese",
            "Eddie": "Avery",
            "Magenta": "Dakota",
            "Frank": "Skyler",
            "Crim": "Logan",
            "Trixie": "Avery",
            "Rocky": "Alex",
            "Scott": "Avery",
            "Crew": ["Jamie", "Parker"],
        }

        self.obj = CastGenerator(available_members=list(self.cast.values()))
        self.obj.preferences = self.data.set_index("member")

    def test_valid_cast_with_actors(self):
        # Test when cast has valid actors with corresponding preferences
        expected_cast = self.cast
        expected_cast["preference_score"] = 10

        result = self.obj.get_preference_for_cast(self.cast)
        assert result == expected_cast

    def test_cast_with_missing_actors(self):
        # Test when a role has no actor assigned (i.e., empty string for the actor)
        missing_role_cast = self.cast.copy()
        missing_role_cast["Crim"] = ""

        expected_cast = missing_role_cast
        expected_cast["preference_score"] = 9

        result = self.obj.get_preference_for_cast(missing_role_cast)
        assert result == expected_cast

    def test_cast_with_invalid_actor_role(self):
        # Test when the actor-role combination is not in the preferences DataFrame
        invalid_role_cast = self.cast.copy()
        invalid_role_cast["Crim"] = "Jackson"

        expected_cast = invalid_role_cast
        expected_cast["preference_score"] = 9

        result = self.obj.get_preference_for_cast(invalid_role_cast)
        assert result == expected_cast
