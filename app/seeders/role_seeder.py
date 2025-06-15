from app.models import Role

async def run():
    print("Seeding roles...")

    roles = ['superadmin', 'admin', 'pemantau', 'penyandang']
    for role_name in roles:
        await Role.create(name=role_name)

    print("Roles seeded successfully.")