import os
from dotenv import load_dotenv
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.utils.vectorize import HFTextVectorizer

# === Load env ===
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
HF_MODEL = os.getenv("HF_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# === Load index ===
index = SearchIndex.from_yaml("schema.yaml", redis_url=REDIS_URL)
if not index.exists():
    print("Index not found. Creating index...")
    index.create(overwrite=True)

# === Load vectorizer ===
os.environ["TOKENIZERS_PARALLELISM"] = "false"
vectorizer = HFTextVectorizer(model=HF_MODEL)

# === CLI loop ===
def search_loop():
    print("🔍 Vector Search CLI — type 'exit' to quit.")
    while True:
        query_str = input("Query: ").strip()
        if query_str.lower() in {"exit", "quit"}:
            break

        embedding = vectorizer.embed(query_str)
        query = VectorQuery(
            vector=embedding,
            vector_field_name="embedding",
            return_fields=["$.name", "$.brand", "$.price", "$.category", "$.vector_distance"],
            num_results=5
        )

        results = index.query(query)
        if not results:
            print("[NO RESULTS]")
        else:
            for i, doc in enumerate(results, start=1):
                name = doc.get("$.name")
                brand = doc.get("$.brand")
                price = doc.get("$.price")
                category = doc.get("$.category")
                dist = doc["vector_distance"]  # <- this is safe

                print(f"\n[{i}] {name} - {brand} | R${price} ({category})\nDistance: {dist}")
            print("-" * 40)

if __name__ == "__main__":
    search_loop()