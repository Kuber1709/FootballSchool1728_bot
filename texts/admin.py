from database import requests as rq

start = ("Добро пожаловать!⚽\nИнформационный бот Футбольной школы 17/28 поможет вам получать самую актуальную "
         "информацию о ней!🏆\n\nВы - Администратор, можете редактировать всю информацию в этом боте🤖")

menu = "Главное Меню 🕹"

back = "Назад 🔙"

advertisements = "Объявления 📢"

no_advertisements = "На данный момент объявлений ещё не было 📄"

advertisements_del_proof = "Вы точно хотите удалить данное объявление?"

advertisements_del = "Объявление успешно удалено ✅"

advertisement_create = "Создать объявление 📢"

advertisement_add = ("Отправьте мне ваше объявление одним сообщением, оно может быть голосовым или видео, "
                     "содержать ровно один медиафайл или документ 📄")

advertisements_add_proof = "Подтвердите публикацию объявления:"

advertisement_undo = "Отмена 🚫"


async def get_advertisement_text(number: int):
    advertisement = await rq.get_advertisement(number)
    return advertisement[0] + "\n\n" + "_" + advertisement[1].strftime("%d.%m.%Y %H:%M") + "_"
