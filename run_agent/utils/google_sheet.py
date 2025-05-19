from run_agent.client.sheet_client import init_google_sheet

def load_google_sheet():
    sheet = init_google_sheet()
    return sheet.get_all_records()