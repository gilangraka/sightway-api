from app.models import MCategory
from app.helpers import generate_slug

async def run():
    print("Seeding categories...")

    categories = [
        {"name": "Teknologi Bantu"},
        {"name": "Edukasi & Pelatihan"},
        {"name": "Kebijakan & Hukum"},
        {"name": "Cerita & Inspirasi"},
        {"name": "Kesehatan Mata"},
        {"name": "Aksesibilitas Digital"},
        {"name": "Komunitas & Event"},
    ]

    for category_data in categories:
        category_data["slug"] = generate_slug(category_data["name"])
        await MCategory.create(**category_data)

    print("Categories seeded successfully.")