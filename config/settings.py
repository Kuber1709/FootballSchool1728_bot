from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    BOT_TOKEN: str = None
    ADMINS: List[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def add_admin(self, admin_id: str) -> int:
        """
        return:
        0 - админ успешно добавлен
        1 - передано пустое значение
        2 - админ уже добавлен
        """

        if not admin_id:
            return 1

        if admin_id in self.ADMINS:
            return 2

        self.ADMINS.append(admin_id)
        self.save_to_env()
        return 1

    def del_admin(self, admin_id: str) -> int:
        """
        return:
        0 - админ успешно удалён
        1 - передано пустое значение
        2 - админа не существует
        """
        if not admin_id:
            return 1

        if not admin_id in self.ADMINS:
            return 2

        self.ADMINS.remove(admin_id)
        self.save_to_env()
        return 1

    def save_to_env(self):
        env_path = ".env"

        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        updated_lines = []
        for line in lines:
            if line.startswith("ADMINS="):
                line = f'ADMINS=['
                for admin_id in self.ADMINS:
                    line += f'"{admin_id}",'
                line = line[:-1] + ']'

            updated_lines.append(line)

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)

config = Settings()