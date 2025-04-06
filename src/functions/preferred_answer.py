from rapidfuzz import fuzz
from src.clients.sheet_client import init_google_sheet

def load_google_sheet():
    sheet = init_google_sheet()
    data = sheet.get_all_records()
    return data


def get_preferred_answer(query, google_sheet=load_google_sheet(), threshold=40):
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


if __name__ == "__main__":
    # 測試模糊匹配
    test_query = "申請復學的居留簽證的時候需要的復學證明可以什麼時候拿到?"
    matched_answer = get_preferred_answer(test_query)
    print("\n對於查詢：", test_query)
    print("匹配到的預設回答：", matched_answer)
