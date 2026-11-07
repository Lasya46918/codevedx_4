import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FAQ_FILE = Path(__file__).resolve().parent / "faq_data.json"

def load_faqs():
    with FAQ_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    return data

def get_answer(question, threshold=0.18):
    faqs = load_faqs()
    if not faqs:
        return {"answer": "No FAQs are available yet.", "intent": "unknown", "score": 0.0}
    documents = [
        " ".join([x.get("question", ""), x.get("keywords", ""), x.get("intent", "").replace("_", " ")])
        for x in faqs
    ]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents + [question])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    idx = int(scores.argmax())
    score = float(scores[idx])
    if score < threshold:
        return {
            "answer": "I couldn't find a reliable FAQ match. Please contact your support team.",
            "intent": "unknown", "score": score
        }
    return {"answer": faqs[idx]["answer"], "intent": faqs[idx]["intent"], "score": score}

def add_faq(question, answer, intent, keywords=""):
    question, answer, intent = question.strip(), answer.strip(), intent.strip()
    if not question or not answer or not intent:
        raise ValueError("Question, answer and intent are required.")
    faqs = load_faqs()
    faqs.append({
        "question": question, "answer": answer,
        "intent": intent, "keywords": keywords.strip()
    })
    with FAQ_FILE.open("w", encoding="utf-8") as f:
        json.dump(faqs, f, indent=2, ensure_ascii=False)
