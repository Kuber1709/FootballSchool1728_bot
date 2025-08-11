from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic_settings import BaseSettings, SettingsConfigDict

ph = PasswordHasher()

BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env" if (BASE_DIR / ".env").exists() else BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    BOT_TOKEN: str = None
    ADMINS_PASSWORD_HASH: str = None

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def is_password_correct(self, password: str) -> bool:
        try:
            return ph.verify(self.ADMINS_PASSWORD_HASH, password)

        except VerifyMismatchError:
            return False

    def change_password(self, new_password: str):
        self.ADMINS_PASSWORD_HASH = ph.hash(new_password)
        self.save_to_env()

    def save_to_env(self):
        with open(ENV_PATH, 'w', encoding='utf-8') as f:
            f.write(f"BOT_TOKEN={self.BOT_TOKEN}\n")
            f.write(f"ADMINS_PASSWORD_HASH={self.ADMINS_PASSWORD_HASH}\n")
