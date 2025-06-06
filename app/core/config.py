import os
from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv("DB_HOST"),
                'port': os.getenv("DB_PORT"),
                'user': os.getenv("DB_USER"),
                'password': os.getenv("DB_PASS"),
                'database': os.getenv("DB_NAME"),
            }
        },
    },

    "apps": {   
        "models": {
            "models": [
                "app.models.user", 
                "app.models.role",
                "app.models.app_history",
                "app.models.m_category",
                "app.models.m_tag",
                "app.models.post",
                "app.models.blindstick",
                "app.models.penyandang",
                "app.models.pemantau",
                "app.models.log_user",
                "app.models.log_penyandang_map",
                "app.models.log_penyandang_status",
                "app.models.log_penyandang_cam",
                "app.models.log_blindstick",

                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}