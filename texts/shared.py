from string import Template

menu = "Главное Меню 🕹"

no_advertisements = "На данный момент объявлений ещё не было 📄"

advertisements_text = Template("${text}\n\n${dt}")

no_information = "Актуальная информация ещё не добавлена 📄"

information_heads = "Выберите раздел:"

no_groups = "Группы ещё не добавлены 📄"

groups_names = "Выберите группу:"

no_workouts = "Домашняя тренировка отсутствует 📄"

workouts_text = Template("${text}\n\nМетод выполнения:\n${method_text}")
