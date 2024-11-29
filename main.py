import argparse
import logging

from src.classes.google_connector import GoogleConnector

from src.classes.cast_generator import CastGenerator

parser = argparse.ArgumentParser()
parser.add_argument(
    "--member_list", "-l", nargs="+", help="List of members to cast.", required=True
)
parser.add_argument(
    "--spreadsheet_id", "-id", help="Spreadsheet ID for Google Drive.", required=True
)
parser.add_argument(
    "--verbose", "-v", action="store_true", help="Display all Debug Messages. Local Upload of Files."
)
parser.add_argument(
   "--new_sheet_name", "-n", help="Name of sheet to add", default= "casts"
)

gc = GoogleConnector()

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    gc.download_sheet_as_csv(spreadsheet_id=args.spreadsheet_id, output_directory='data/')
    available_members = list(args.member_list)
    df = CastGenerator(available_members=available_members).get_all_casts(1000)
    gc.upload_casts_from_df(spreadsheet_id=args.spreadsheet_id, sheet_name=args.new_sheet_name, df=df)
    
