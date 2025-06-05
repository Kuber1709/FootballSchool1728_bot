from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class CallbackPrefixFilter(BaseFilter):
    def __init__(self, prefix):
        self.prefix = prefix

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.startswith(self.prefix)
