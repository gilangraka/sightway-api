from app.models import Blindstick

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

    print("Blindsticks seeded successfully.")