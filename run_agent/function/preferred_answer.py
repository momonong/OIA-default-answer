import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from run_agent.function.embedding_cache import load_or_build_embedding_cache
from run_agent.client.embedding_client import get_embedding_response
from run_agent.function.answer_verify import verify_answer_match

def get_preferred_answer(query, threshold=0.7):
    """
    語意比對版本：根據 query 在 embedding 快取中找出最相近問題並回傳回答。
    :param query: 使用者輸入的問題文字
    :param threshold: 相似度門檻（0~1），預設為 0.6
    :return: 相似度足夠則返回 AI 回覆，否則 None
    """
    data, vectors = load_or_build_embedding_cache()
    vectors = np.array(vectors)

    # 對 query 建立 embedding
    response = get_embedding_response([query])
    query_vec = np.array(response.data[0].embedding).reshape(1, -1)

    # 計算語意相似度
    sims = cosine_similarity(query_vec, vectors)[0]
    best_idx = np.argmax(sims)
    best_score = sims[best_idx]
    best_question = data[best_idx]["question"]
    best_answer = data[best_idx]["answer"]

    print(f"🧠 最相近問題：{best_question}")
    print(f"📈 相似度：{best_score:.4f}")

    # 相似度門檻通過後 → 語意驗證
    if best_score >= threshold:
        matched = verify_answer_match(query, best_answer)
        print(f"🔍 驗證結果：{'✅ 有回到問題' if matched else '❌ 沒回到重點'}")
        if matched:
            return best_answer

    return None

if __name__ == "__main__":
    # 測試語意比對
    query = "復學證明什麼時候可以拿到？"
    answer = get_preferred_answer(query)
    print(f"查詢問題：{query}")
    print(f"推薦回答：{answer if answer else '查無匹配'}")