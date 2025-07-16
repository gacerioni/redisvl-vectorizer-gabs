import os
import json
from dotenv import load_dotenv
from redis import Redis
from redisvl.utils.vectorize import HFTextVectorizer
from tqdm import tqdm

# === Load environment variables ===
load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_PREFIX = os.getenv("REDIS_PREFIX", "product:")
HF_MODEL = os.getenv("HF_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 128))

# === Redis client ===
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# === Hugging Face Vectorizer ===
os.environ["TOKENIZERS_PARALLELISM"] = "false"
vectorizer = HFTextVectorizer(model=HF_MODEL)

def get_all_product_keys(prefix: str):
    return [key for key in redis_client.scan_iter(match=f"{prefix}*")]

def fetch_products(keys: list[str]) -> list[dict]:
    return [redis_client.json().get(key) for key in keys]

def prepare_texts(products: list[dict]) -> list[str]:
    texts = []
    for p in products:
        if not p:
            texts.append("")
            continue
        name = p.get("name", "")
        brand = p.get("brand", "")
        category = p.get("category", "")
        description = p.get("description", "")
        texts.append(f"{name} {brand} {category} {description}")
    return texts

def update_embeddings(keys: list[str], embeddings: list[list[float]]):
    for key, emb in zip(keys, embeddings):
        try:
            redis_client.json().set(key, "$.embedding", emb)
        except Exception as e:
            print(f"[ERROR] Failed to update {key}: {e}")

def process_all_products():
    keys = get_all_product_keys(REDIS_PREFIX)
    print(f"Found {len(keys)} products.")
    for i in tqdm(range(0, len(keys), BATCH_SIZE), desc="Batches"):
        batch_keys = keys[i:i+BATCH_SIZE]
        products = fetch_products(batch_keys)
        texts = prepare_texts(products)
        try:
            embeddings = vectorizer.embed_many(texts)
            update_embeddings(batch_keys, embeddings)
        except Exception as e:
            print(f"[ERROR] Batch failed [{batch_keys[0]}..{batch_keys[-1]}]: {e}")

def main():
    print("== Redis Product Embedder (Batched) ==")
    process_all_products()
    print("== Done ==")

if __name__ == "__main__":
    main()