from string import Template

menu = "Главное Меню 🕹"

no_advertisements = "На данный момент объявлений ещё не было 📄"

advertisements_text = Template("${text}\n\n${dt}")

no_information = "Актуальная информация ещё не добавлена 📄"

information_heads = "Выберите раздел:"

no_groups = "Группы ещё не добавлены 📄"

groups_names = "Выберите группу:"

coaches_names = "Выберите тренера:"

no_coaches = "Тренеры ещё не добавлены 📄"

no_workouts = "Домашняя тренировка отсутствует 📄"

workouts_text = Template("${text}\n\nМетод выполнения:\n${method_text}")

schedule_category = "Выберите раздел расписания:"

schedule_weekdays = "Выберите день недели:"

schedule_no_lessons = "_Тренировок нет_"

schedule_lesson_group = Template("*Группа:* ${name}\n*Время тренировки:* ${time_start}-${time_end}\n\n")

schedule_lesson_coach = Template("*Тренер:* ${name}\n*Время тренировки:* ${time_start}-${time_end}\n\n")
