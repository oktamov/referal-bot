from pathlib import Path

import yaml
from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot Token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati

config_dir = Path(__file__).parent.parent.resolve() / "data"

with open(config_dir / "url.yml", 'r') as f:
    url_yaml = yaml.safe_load(f)

MONEY_ADMIN = env.str("MONEY_ADMIN")
