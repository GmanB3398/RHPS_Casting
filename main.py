import argparse
import logging

import pandas as pd

from src.classes.cast_generator import CastGenerator

parser = argparse.ArgumentParser()

parser.add_argument("--verbose", "-v", action="store_true", help="Display all Debug Messages.")


args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    roles = pd.read_csv("data/roles.csv")
    preferences = pd.read_csv("data/preferences.csv")
    available_members = preferences["member"].to_list()
    df = CastGenerator(
        available_members=available_members, roles=roles, preferences=preferences
    ).get_all_casts()
    df.to_csv("outfile.csv", index=False)
