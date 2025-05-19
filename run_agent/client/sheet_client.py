import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

def init_google_sheet():
    key_file = os.getenv("GOOGLE_SHEET_KEY_FILE")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id).sheet1
    return sheet


if __name__ == "__main__":
    sheet = init_google_sheet()
    print(sheet.get_all_records())