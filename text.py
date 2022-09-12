
"""
 say - бот это говорит!
 text - это текст для кнопок
"""

def say_menu(): return "✈️Добро пожаловать в главное меню чат-бота Управляющей компании \"УЭР-ЮГ\". Здесь Вы сможете оставить заявку для управляющей компании или направить своё предлжение по управлению домом. Просто поспользуйтесь кнопками меню, чтобы взаимодействовать с функциями бота."

def say_start(): return "Доброго времени суток. Бот создан, чтобы обрабатывать заявки и обращения пользователей. Чтобы возпользоваться этим, пришлите для начала Ваше имя и Фамелию."

def say_correct_name(): return "📞Теперь отправте Ваш номер через +7 следующим сообщением: "

def say_discorrect_name(): return "⛔Имя и Фамилия должны быть введины через один пробел и должны быть написаны через кириллицу. Также должны быть заглавные буквы. Учтите формат и попробуйте снова"


def text_number_phone(): return "Поделиться номером!"

def text_request(): return "⛔Оставить заявку"

def text_settings(): return "⚙️Настройки"

def text_contacts(): return "☎️Полезные контакты"

def text_contact(): return "📞Связаться"

def text_request_request(): return "Оставить заявку"

def text_request_suggestion(): return "Поделиться предложением"

def text_request_back(): return "Назад"

def text_complete_contact(): return "Завершить диолог"


def say_request_complain1(): return f"<b>Шаг 1/3</b>. 📋Напишите адрес или орентир проблеммы( улицу, номер дома, пожъезд, этаж и квартиру) или пропустите этот пункт"

def say_request_complain2(): return f"<b>Шаг</b> 2/3. 🏞Прикрепите фотографию или видео к заявке или пропустите этот пункт"

def say_request_complain3(): return f"<b>Шаг</b> 3/3. ⛔Напишите причину обращения в подробностях!"

def say_request_complain3_text(user_name, name, phone, data):

    message = f"Поступила новая жалоба!\n\n@{user_name}\nИмя и Фамилия: {name}\nТелефон: {phone}"
    if "complaint1_text" in data:
        return f"{message}\nадрес: {data['complaint1_text']}\nСодержание: {data['text']}"

    else:
        return f"{message}\nСодержание: {data['text']}"

def say_leave_a_request(): return "Выберите категорию, по которой Вы хотите оставить заявку в УК:"

def say_settings(): return "⚙Тут Вы сможете изменить <b>Имя</b> и <b>Фамилию</b> в базе данных нашего бота или же можете поменять Ваш <b>номер телефона</b>, если он изменился. Выберите, что хотите поменять или вернитесь в <b>главное меню<b/>."

def say_settings_name(): return "⚒Отправте своё Имя и Фамелию, чтобы поменять настройки"

def say_settings_update(): return "⚒✅⚒Настройки имени успешно применены!"

