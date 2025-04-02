from rapidfuzz import fuzz
from dotenv import load_dotenv
from src.clients.sheet_client import init_google_sheet

load_dotenv()

def load_google_sheet():
    sheet = init_google_sheet()
    data = sheet.get_all_records()
    return data

def get_preferred_answer(query, google_sheet, threshold=40):
    best_match = None
    best_score = 0
    for record in google_sheet:
        candidate = record.get("問題", "")
        score = fuzz.token_set_ratio(query, candidate)
        if score > best_score:
            best_score = score
            best_match = record
    if best_score >= threshold:
        return best_match.get("回覆有誤", None)
    return None
