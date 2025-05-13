import os
import pickle
from embedding_client import get_embedding_response
from google_sheet import load_google_sheet

TEMP_DIR = "temp"


def load_or_build_embedding_cache():
    os.makedirs(TEMP_DIR, exist_ok=True)
    sheet_data = load_google_sheet()

    all_data = []
    all_embeddings = []

    for idx, row in enumerate(sheet_data):
        question = row.get("問題", "")
        answer = row.get("回覆有誤（正確回答）", "")
        cache_file = os.path.join(TEMP_DIR, f"{idx}.pkl")
        if not question:
            print(f"⚠️ 跳過空白問題（Row {idx + 1}）")
            continue

        if os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                cached = pickle.load(f)
        else:
            # 新資料 → 建立 embedding
            print(f"🔄 新增快取：Row {idx + 1} | 問題：{question[:15]}...")
            response = get_embedding_response([question])
            embedding = response.data[0].embedding
            cached = {"question": question, "answer": answer, "embedding": embedding}
            with open(cache_file, "wb") as f:
                pickle.dump(cached, f)

        all_data.append(cached)
        all_embeddings.append(cached["embedding"])

    return all_data, all_embeddings


if __name__ == "__main__":
    # 測試嵌入快取
    all_data, all_embeddings = load_or_build_embedding_cache()
    print(f"總共 {len(all_data)} 筆資料")
    print(f"第一筆資料：{all_data[0]['question']}")
    print(f"第一筆資料的嵌入：{all_embeddings[0][:10]}")
