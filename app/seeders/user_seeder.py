from app.models import Role, User, Penyandang, Pemantau
from app.helpers import hash_password

async def run():
    print("Seeding users...")

    users = [
        {
            "name": "Super Admin",
            "email": "superadmin@gmail.com",
            "password": "superadmin123",
            "roles": "superadmin"
        },
        {
            "name": "Admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "roles": "admin"
        },
        {
            "name": "Pemantau",
            "email": "pemantau@gmail.com",
            "password": "pemantau123",
            "roles": "pemantau"
        },
        {
            "name": "Penyandang",
            "email": "penyandang@gmail.com",
            "password": "penyandang123",
            "roles": "penyandang"
        }
    ]

    for user_data in users:
        # Create user
        user = await User.create(
            name=user_data["name"],
            email=user_data["email"],
            password=hash_password(user_data["password"])
        )
        # Assign role
        role = await Role.get(name=user_data["roles"])
        await user.roles.add(role)

    # Add to table pemantau & penyandang
    penyandang = await User.filter(email="penyandang@gmail.com").first()
    await Penyandang.create(
        user_id=penyandang.id,
        blindstick_id=1
    )

    pemantau = await User.filter(email="pemantau@gmail.com").first()
    await Pemantau.create(
        user_id=pemantau.id
    )

    print("Users seeded successfully.")