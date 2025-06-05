from database import requests as rq

start = ("Добро пожаловать!⚽\nИнформационный бот Футбольной школы 17/28 поможет вам получать самую актуальную "
         "информацию о ней!🏆")

menu = "Главное Меню 🕹"

back = "Назад 🔙"

advertisements = "Объявления 📢"

no_advertisements = "На данный момент объявлений ещё не было 📄"

info = "Информация ℹ"

no_information = "Актуальная информация пока не добавлена 📄"

get_info = "Выберите интересующий вас раздел:"


async def get_advertisement_text(number: int):
    advertisement = await rq.get_advertisement(number)
    return advertisement[0] + "\n\n" + "_" + advertisement[1].strftime("%d.%m.%Y %H:%M") + "_"


async def get_information_text(number):
    inf = await rq.get_information(number)
    return "**" + inf[0] + "**" + "\n\n" + inf[1]
