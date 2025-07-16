# 🧠 Redis Vector Search Playground (with RedisVL + HuggingFace)

This is a minimal, no-nonsense demo that:

- Generates fake products using `Faker`
- Embeds product data using Hugging Face Sentence Transformers
- Stores everything as RedisJSON
- Runs fast vector search from the terminal using RedisVL

---

## 📦 Project Structure

```
.
├── fake_product_loader.py     # Generates fake product documents in Redis
├── vectorizer.py              # Embeds products with HuggingFace and stores vectors
├── search.py                  # Interactive CLI for vector search
├── schema.yaml                # RedisVL index definition
└── requirements.txt
```

---

## 🚀 Quickstart

### 1. Clone the repo & create virtual env

```bash
git clone <this-repo>
cd redisvl-vectorizer-gabs
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up your `.env`

Create a `.env` file in the root:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_PREFIX=product:
HF_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

You can use any multilingual HF sentence transformer model here.

---

### 3. Start Redis (Docker example)

```bash
docker run -it --rm -p 6379:6379 redis/redis-stack:latest
```

---

### 4. Load fake product data

```bash
python fake_product_loader.py
```

This will generate 1000 fake products like:

```json
{
  "id": 42,
  "name": "A nova geração do desempenho extremo",
  "description": "Sistema com desempenho superior e visual elegante.",
  "category": "Eletrônicos",
  "brand": "TechPower",
  "price": 1999.90
}
```

---

### 5. Embed with HuggingFace

```bash
python vectorizer.py
```

This will vectorize all products using name, brand, category, and description fields, and store them as `.embedding`.

---

### 6. Run vector search

```bash
python search.py
```

Search with natural language, like:

```
Query: celular com boa câmera e bateria
```

Returns top-5 most semantically similar products using cosine distance.

---

## 📎 Notes

- All data is stored as `RedisJSON` using key prefix like `product:123`.
- Vector embeddings are stored under `$.embedding`.
- Distance metric is `cosine`, with `flat` algorithm.
- You can change the model via `HF_MODEL` env var.

---

## 📚 Dependencies

Everything is listed in `requirements.txt`, including:

- `redis`
- `redisvl`
- `sentence-transformers`
- `faker`
- `python-dotenv`
- `tqdm`

---

## 🧼 Cleanup

To wipe Redis:

```bash
redis-cli FLUSHALL
```

---

Built by Gabs the Nerdola to show how semantic search can be dead simple with Redis.
