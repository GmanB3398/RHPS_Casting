import os.path
import logging
import csv
from typing import Dict

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleConnector:
    def __init__(self, credentials_path="credentials.json"):
        """
        Initializes the GoogleDriveService with the service account credentials.

        :param credentials_path: Path to the service account JSON credentials file.
        """
        self.credentials_path = credentials_path
        self.scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
        ]
        self.authenticate()

    def authenticate(self, cache=True):
        """
        Authenticates the service account and initializes the Google Drive API client.
        """
        try:
            creds = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", self.scopes)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                if cache:
                    with open("token.json", "w") as token:
                        token.write(creds.to_json())

            self.drive_service = build("drive", "v3", credentials=creds)
            self.sheets_service = build("sheets", "v4", credentials=creds)

            logging.info("Authenticated successfully!")
        except Exception as e:
            logging.error(f"Failed to authenticate: {e}")

    def download_sheet_as_csv(self, spreadsheet_id, output_directory) -> Dict:
        """
        Exports each sheet in a Google Spreadsheet to a separate CSV file.

        :param spreadsheet_id: The ID of the Google Spreadsheet.
        :param output_directory: The directory where the CSV files will be saved.

        :returns Dictionary of sheet titles and file names
        """
        if not self.sheets_service:
            print("Service is not initialized. Please authenticate first.")
            return

        try:
            # Get spreadsheet metadata to retrieve sheet names and IDs
            sheet_metadata = (
                self.sheets_service.spreadsheets()
                .get(spreadsheetId=spreadsheet_id)
                .execute()
            )
            sheets = sheet_metadata.get("sheets", [])

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            for sheet in sheets:
                sheet_title = sheet["properties"]["title"]
                # sheet_id = sheet["properties"]["sheetId"]

                # Read data from the sheet
                result = (
                    self.sheets_service.spreadsheets()
                    .values()
                    .get(spreadsheetId=spreadsheet_id, range=sheet_title)
                    .execute()
                )

                rows = result.get("values", [])
                output_file = os.path.join(output_directory, f"{sheet_title}.csv")

                # Write data to CSV file
                with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

                logging.info(f"Exported sheet '{sheet_title}' to {output_file}")

        except Exception as e:
            logging.error(f"Failed to export sheets: {e}")

    def upload_casts_from_df(
        self, df: pd.DataFrame, spreadsheet_id, sheet_name="outfile"
    ):
        """
        Uploads

        :param df: dataframe of
        :param spreadsheet_id: The ID of the Google Spreadsheet.
        :param output_directory: The directory where the CSV files will be saved.

        :returns Dictionary of sheet titles and file names
        """
        if not self.sheets_service:
            print("Service is not initialized. Please authenticate first.")
            return

        try:
            # Step 1: Check if the sheet already exists and delete
            sheet_metadata = (
                self.sheets_service.spreadsheets()
                .get(spreadsheetId=spreadsheet_id)
                .execute()
            )
            sheets = sheet_metadata.get("sheets", [])
            existing_sheet_id = None

            for sheet in sheets:
                if sheet["properties"]["title"] == sheet_name:
                    existing_sheet_id = sheet["properties"]["sheetId"]
                    break
            if existing_sheet_id:
                batch_update_request_body = {
                    "requests": [{"deleteSheet": {"sheetId": existing_sheet_id}}]
                }
                self.sheets_service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id, body=batch_update_request_body
                ).execute()
                logging.debug(f"Deleted existing sheet '{sheet_name}'.")

            # Step 2: Create a new sheet in the spreadsheet
            batch_update_request_body = {
                "requests": [{"addSheet": {"properties": {"title": sheet_name}}}]
            }
            response = (
                self.sheets_service.spreadsheets()
                .batchUpdate(
                    spreadsheetId=spreadsheet_id, body=batch_update_request_body
                )
                .execute()
            )
            logging.debug(f"Sheet '{sheet_name}' created successfully: {response}")

            # Step 3: Read the dataframe file and prepare data
            values = [df.columns.tolist()] + df.values.tolist()

            # Step 4: Write data to the new sheet
            data_range = f"{sheet_name}!A1"  # Start writing from the first cell
            body = {"values": values}
            response = (
                self.sheets_service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=data_range,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )
            logging.debug(f"Dataframe uploaded to sheet '{sheet_name}' successfully.")
            return response
        except Exception as e:
            logging.error(f"Failed to upload CSV: {e}")
