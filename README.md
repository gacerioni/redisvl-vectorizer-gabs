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

## Product data in PT-BR
```
JSON.SET product:1001 $ '{"id":1001,"name":"Malbec Desodorante Colônia","description":"Fragrância amadeirada marcante, com notas de vinho, ideal para homens sofisticados.","price":189.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1002 $ '{"id":1002,"name":"Egeo Dolce Desodorante Colônia","description":"Doce e envolvente, com notas de marshmallow e baunilha para mulheres divertidas.","price":149.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1003 $ '{"id":1003,"name":"Lily Eau de Parfum","description":"Perfume floral intenso com toque de lírio e musk branco, sofisticação em cada borrifada.","price":289.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1004 $ '{"id":1004,"name":"Malbec Bleu Colônia","description":"Versão mais fresca e aquática do clássico Malbec, perfeita para o dia a dia.","price":194.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1005 $ '{"id":1005,"name":"Floratta Red Desodorante Colônia","description":"Inspirada na flor da macieira, essa fragrância é romântica, jovem e vibrante.","price":129.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1006 $ '{"id":1006,"name":"Cuide-se Bem Nuvem Loção Hidratante 400ml","description":"Hidratação leve com fragrância suave e textura que absorve rapidinho.","price":38.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1007 $ '{"id":1007,"name":"Match Esquadrão do Brilho Shampoo 250ml","description":"Limpa sem ressecar e ativa o brilho dos fios desde a primeira aplicação.","price":49.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1008 $ '{"id":1008,"name":"Botik Sérum de Alta Potência Ácido Hialurônico","description":"Reduz linhas finas, hidrata profundamente e melhora a firmeza da pele.","price":129.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1009 $ '{"id":1009,"name":"Make B. Base Líquida Hyaluronic FPS 70","description":"Base com cobertura média e proteção solar alta, uniformiza e trata a pele.","price":89.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1010 $ '{"id":1010,"name":"Malbec Club Antitranspirante Aerossol","description":"Proteção 48h com a fragrância icônica de Malbec. Para homens confiantes.","price":26.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1011 $ '{"id":1011,"name":"Egeo Blue Desodorante Colônia","description":"Fragrância jovem e fresca com notas aromáticas e frutadas. Ideal para o dia.","price":149.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1012 $ '{"id":1012,"name":"Floratta Rose Desodorante Colônia","description":"Floral romântico com toque de frutas vermelhas e musk. Leve e apaixonante.","price":129.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1013 $ '{"id":1013,"name":"Coffee Woman Seduction","description":"Perfume sensual com notas de café e frutas vermelhas. Para noites marcantes.","price":199.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1014 $ '{"id":1014,"name":"Quasar Next Colônia","description":"Aromático e energizante, com notas cítricas e toque herbal refrescante.","price":114.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1015 $ '{"id":1015,"name":"Botik Creme Firmador Vitamina C","description":"Hidratação com ação antioxidante. Uniformiza o tom e dá viço à pele.","price":109.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1016 $ '{"id":1016,"name":"Intense Máscara Superfix","description":"Alonga e define os cílios com fórmula resistente à água e efeito por 24h.","price":42.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1017 $ '{"id":1017,"name":"Glamour Love Me Desodorante Colônia","description":"Delicada e feminina, mistura flores e frutas em uma fragrância envolvente.","price":169.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1018 $ '{"id":1018,"name":"Cuide-se Bem Beijinho Creme para Mãos","description":"Nutre profundamente e deixa as mãos macias e perfumadas.","price":24.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1019 $ '{"id":1019,"name":"Men Shower Gel 3 em 1 Cabelo, Corpo e Barba","description":"Praticidade total com limpeza eficiente e fragrância masculina marcante.","price":34.90,"category":"Beleza","brand":"O Boticário"}'

JSON.SET product:1020 $ '{"id":1020,"name":"Malbec X Colônia","description":"Fragrância intensa e moderna com notas de madeira e especiarias.","price":199.90,"category":"Beleza","brand":"O Boticário"}'
```

---

Built by Gabs the Nerdola to show how semantic search can be dead simple with Redis.
