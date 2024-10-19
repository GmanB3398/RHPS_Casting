import argparse
import logging

from src.classes.cast_generator import CastGenerator

parser = argparse.ArgumentParser()
parser.add_argument(
    "--member_list", "-l", nargs="+", help="List of members to cast.", required=True
)
parser.add_argument(
    "--verbose", "-v", action="store_true", help="Display all Debug Messages."
)

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    available_members = list(args.member_list)
    df = CastGenerator(available_members=available_members).get_all_casts()
    df.to_csv("outfile.csv", index=False)
