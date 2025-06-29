from app.models import Blindstick, LogBlindstick

async def run():
    print("Seeding blindsticks...")

    mac_addresses = [
        "00:1A:2B:3C:4D:5E",
        "01:2B:3C:4D:5E:6F",
        "02:3C:4D:5E:6F:70",
        "03:4D:5E:6F:70:81",
        "04:5E:6F:70:81:92",
        "05:6F:70:81:92:A3",
        "06:70:81:92:A3:B4",
        "07:81:92:A3:B4:C5",
    ]

    for mac in mac_addresses:
        await Blindstick.create(mac_address=mac)

    logs = [
        {
            "status" : "normal",
            "description" : "Blindstick jatuh"
        }, 
        {
            "status" : "danger",
            "description" : "User menekan tombol darurat!"
        },
        {
            "status" : "danger",
            "description" : "User menekan tombol darurat!"
        }
    ]

    first_blindstick = await Blindstick.first()
    for log in logs:
        await LogBlindstick.create(
            blindstick_id=first_blindstick.id,
            status=log['status'],
            description=log['description']
        )


    print("Blindsticks seeded successfully.")