import os
from dotenv import load_dotenv

from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.utils.vectorize import HFTextVectorizer
from redisvl.utils.rerank import HFCrossEncoderReranker

# === Load environment variables ===
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
HF_MODEL = os.getenv("HF_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
HF_RERANK_MODEL = os.getenv("HF_RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

# === Disable tokenizer parallelism (avoids HuggingFace warnings) ===
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# === Load the RedisVL index from schema ===
index = SearchIndex.from_yaml("schema.yaml", redis_url=REDIS_URL)
if not index.exists():
    print("Index not found. Creating index...")
    index.create(overwrite=True)

# === Load the embedding model ===
vectorizer = HFTextVectorizer(model=HF_MODEL)

# === Load the reranking model ===
reranker = HFCrossEncoderReranker(
    model=HF_RERANK_MODEL,
    limit=5,
    return_score=True
)

# === Helper: Join RedisJSON fields into one rerankable string ===
def join_fields(doc: dict) -> str:
    return " ".join([f"{k}: {v}" for k, v in doc.items()])

# === CLI loop for querying products ===
def search_loop():
    print("🔍 Vector Search CLI — type 'exit' to quit.")
    while True:
        query_str = input("Query: ").strip()
        if query_str.lower() in {"exit", "quit"}:
            break

        # Step 1: Embed query
        embedding = vectorizer.embed(query_str)

        # Step 2: Run vector search against Redis
        vector_query = VectorQuery(
            vector=embedding,
            vector_field_name="embedding",
            return_fields=[
                "$.name", "$.brand", "$.price", "$.category",
                "$.description", "$.vector_distance"
            ],
            num_results=10  # fetch more for stronger rerank
        )
        results = index.query(vector_query)

        if not results:
            print("[NO RESULTS]")
            continue

        # Step 3: Print top 5 raw KNN results before reranking
        print("\n🔎 Top 5 KNN Results (before reranking):")
        for i, doc in enumerate(results[:5], start=1):
            print(
                f"\n[{i}] {doc.get('$.name', 'N/A')} - {doc.get('$.brand', 'N/A')} | "
                f"R${doc.get('$.price', 'N/A')} ({doc.get('$.category', 'N/A')})"
            )
            print(f"Distance: {doc.get('vector_distance', 'N/A')}")

        # Step 4: Prepare plain text docs for reranking
        joined_docs = [join_fields(doc) for doc in results]

        # Step 5: Run reranker on top-K results
        reranked_docs, reranked_scores = reranker.rank(query=query_str, docs=joined_docs)
        print("\n[DEBUG] Raw reranked_scores:")
        print(reranked_scores)

        # Step 6: Match reranked docs back with metadata
        final_results = [
            {**results[i], "score": reranked_scores[i]}
            for i in range(min(len(results), len(reranked_scores)))
        ]
        # Sort results by rerank score (higher score = higher relevance)
        final_results.sort(key=lambda x: x["score"], reverse=True)

        # Step 7: Print top 5 reranked results
        print("\n🏆 Top 5 Reranked Results:")
        for i, doc in enumerate(final_results[:5], start=1):
            print(
                f"\n[{i}] {doc.get('$.name', 'N/A')} - {doc.get('$.brand', 'N/A')} | "
                f"R${doc.get('$.price', 'N/A')} ({doc.get('$.category', 'N/A')})"
            )
            score = doc.get("score", "N/A")
            score_fmt = f"{score:.4f}" if isinstance(score, (float, int)) else str(score)
            print(f"Distance: {doc.get('vector_distance', 'N/A')} | Rerank Score: {score_fmt}")
        print("-" * 40)

# === Entry point ===
if __name__ == "__main__":
    search_loop()