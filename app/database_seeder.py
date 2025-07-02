import asyncio
from tortoise import Tortoise, run_async
import app.seeders as seeders
from dotenv import load_dotenv
import os

load_dotenv()

async def init():
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASS", "postgres")
    db_name = os.getenv("DB_NAME", "sightway_db")

    await Tortoise.init(
        db_url = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        modules={"models": ["app.models"]},
    )
    await Tortoise.generate_schemas()

async def seed():
    await init()
    print("Seeding database...")

    await seeders.seed_roles()
    await seeders.seed_categories()
    await seeders.seed_tags()
    await seeders.seed_blindsticks()
    await seeders.seed_users()

    print("Database seeded successfully.")

if __name__ == "__main__":
    run_async(seed())