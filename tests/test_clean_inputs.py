import unittest

import pandas as pd

from src.classes.cast_generator import clean_inputs


class TestCleanInputsWithFixtures(unittest.TestCase):

    def setUp(self):
        self.input_df = pd.read_csv("tests/fixtures/roles.csv")

    def test_happy_path(self):
        # Ensure roles_long is correctly generated
        pd.testing.assert_frame_equal(
            self.input_df,
            clean_inputs(self.input_df),
        )

    def test_whitespace_additions(self):
        df = self.input_df.copy()
        df = df.rename(columns={"Frank": "Frank "})

        pd.testing.assert_frame_equal(
            self.input_df,
            clean_inputs(df),
        )

        df.loc[df["member"] == "Taylor", "member"] = "Taylor "

        pd.testing.assert_frame_equal(
            self.input_df,
            clean_inputs(df),
        )

    def test_known_switches(self):
        df = self.input_df.copy()
        df = df.rename(columns={"Riff": "Riff Raff", "Scott": "Dr. Scott "})

        pd.testing.assert_frame_equal(
            self.input_df,
            clean_inputs(df),
        )

    def test_unknown_switches(self):
        df = self.input_df.copy()
        df = df.rename(columns={"Frank": "Daddy"})

        self.assertEqual(clean_inputs(df), f"One or more roles missing: {["Frank"]}")

    def test_member_col_inference(self):
        df = self.input_df.copy()
        df = df.rename(columns={"member": "people"})
        pd.testing.assert_frame_equal(
            self.input_df,
            clean_inputs(df)[self.input_df.columns],
        )

        df["people2"] = df["people"]

        pd.testing.assert_frame_equal(
            self.input_df,
            clean_inputs(df)[self.input_df.columns],
        )
