import os
import random
from faker import Faker
from redis import Redis
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_PREFIX = os.getenv("REDIS_PREFIX", "product:")

# === Redis client ===
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

# === Faker ===
fake = Faker('pt_BR')

CATEGORIES = [
    "Eletrônicos", "Casa", "Escritório", "Moda", "Livros", "Games", "Mercado", "Beleza", "Esportes", "Automotivo"
]

def generate_fake_product(product_id: int) -> dict:
    return {
        "id": product_id,
        "name": fake.catch_phrase(),
        "description": fake.text(max_nb_chars=120),
        "price": round(random.uniform(10, 5000), 2),
        "category": random.choice(CATEGORIES),
        "brand": fake.company()
    }

def insert_product_redis(product: dict):
    key = f"{REDIS_PREFIX}{product['id']}"
    redis_client.json().set(key, "$", product)

def main():
    num_products = 1000  # Ajustável
    print(f"Generating {num_products} fake products...")

    for i in range(1, num_products + 1):
        product = generate_fake_product(i)
        insert_product_redis(product)
        if i % 100 == 0:
            print(f"[OK] Inserted {i} products")

    print("✅ Done.")

if __name__ == "__main__":
    main()