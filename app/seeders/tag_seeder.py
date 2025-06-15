from app.models import MTag
from app.helpers import generate_slug

async def run():
    print("Seeding tags...")

    tags = [
        {"name": "braille"},
        {"name": "screen reader"},
        {"name": "navigasi mandiri"},
        {"name": "low vision"},
        {"name": "low vision"},
        {"name": "inovasi"},
        {"name": "pengalaman pribadi"},
    ]

    for tag_data in tags:
        tag_data["slug"] = generate_slug(tag_data["name"])
        await MTag.create(**tag_data)

    print("Tags seeded successfully.")
