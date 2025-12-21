from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from decouple import config

start_btn = InlineKeyboardBuilder()
start_btn.row(
    types.InlineKeyboardButton(
        text="Начнем!", callback_data="start"
    )
)
start_btn = start_btn.as_markup()

subscribe_btn = InlineKeyboardBuilder()
subscribe_btn.row(
    types.InlineKeyboardButton(
        text="Подписаться на канал",
        url=f"https://t.me/{config('CHANNEL_NAME')}"
    )
)
subscribe_btn.row(
    types.InlineKeyboardButton(
        text="Проверить подписку",
        callback_data="check_subscribe"
    )
)
subscribe_btn = subscribe_btn.as_markup()

report_btn = InlineKeyboardBuilder()
report_btn.row(
    types.InlineKeyboardButton(
        text="Создать свой отчет",
        callback_data="report"
    )
)
report_btn = report_btn.as_markup()

answer_1_btn = InlineKeyboardBuilder()
answer_1_btn.row(
    types.InlineKeyboardButton(
        text="Личностным ростом",
        callback_data="answer_1_1"
    )
)
answer_1_btn.row(
    types.InlineKeyboardButton(
        text="Рабочим подвигом",
        callback_data="answer_1_2"
    )
)
answer_1_btn.row(
    types.InlineKeyboardButton(
        text="Я просто выжил(а)",
        callback_data="answer_1_3"
    )
)
answer_1_btn = answer_1_btn.as_markup()

answer_2_btn = InlineKeyboardBuilder()
answer_2_btn.row(
    types.InlineKeyboardButton(
        text="Десятый круг правок",
        callback_data="answer_2_1"
    )
)
answer_2_btn.row(
    types.InlineKeyboardButton(
        text="Срочный созвон",
        callback_data="answer_2_2"
    )
)
answer_2_btn.row(
    types.InlineKeyboardButton(
        text="Второй месяц согласования",
        callback_data="answer_2_3"
    )
)
answer_2_btn = answer_2_btn.as_markup()

answer_4_btn = InlineKeyboardBuilder()
answer_4_btn.row(
    types.InlineKeyboardButton(
        text="1",
        callback_data="answer_4_1"
    )
)
answer_4_btn.row(
    types.InlineKeyboardButton(
        text="2",
        callback_data="answer_4_2"
    )
)
answer_4_btn.row(
    types.InlineKeyboardButton(
        text="3",
        callback_data="answer_4_3"
    )
)
answer_4_btn = answer_4_btn.as_markup()

answer_6_btn = InlineKeyboardBuilder()
answer_6_btn.row(
    types.InlineKeyboardButton(
        text="Одно мне",
        callback_data="answer_6_1"
    )
)
answer_6_btn.row(
    types.InlineKeyboardButton(
        text="Два коллеге",
        callback_data="answer_6_2"
    )
)
answer_6_btn = answer_6_btn.as_markup()

answer_7_btn = InlineKeyboardBuilder()
answer_7_btn.row(
    types.InlineKeyboardButton(
        text="Входить в режим энергосбережения",
        callback_data="answer_7_1"
    )
)
answer_7_btn.row(
    types.InlineKeyboardButton(
        text="Работать",
        callback_data="answer_7_2"
    )
)
answer_7_btn.row(
    types.InlineKeyboardButton(
        text="Составлять карту желаний",
        callback_data="answer_7_3"
    )
)
answer_7_btn = answer_7_btn.as_markup()

answer_8_btn = InlineKeyboardBuilder()
answer_8_btn.row(
    types.InlineKeyboardButton(
        text="Много",
        callback_data="answer_8_1"
    )
)
answer_8_btn.row(
    types.InlineKeyboardButton(
        text="Достаточно",
        callback_data="answer_8_2"
    )
)
answer_8_btn.row(
    types.InlineKeyboardButton(
        text="Мало",
        callback_data="answer_8_3"
    )
)
answer_8_btn = answer_8_btn.as_markup()

answer_9_btn = InlineKeyboardBuilder()
answer_9_btn.row(
    types.InlineKeyboardButton(
        text="Игнорировать токсичных коллег",
        callback_data="answer_9_1"
    )
)
answer_9_btn.row(
    types.InlineKeyboardButton(
        text="Не работать на выходных",
        callback_data="answer_9_2"
    )
)
answer_9_btn.row(
    types.InlineKeyboardButton(
        text="Уделять больше времени себе",
        callback_data="answer_9_3"
    )
)
answer_9_btn = answer_9_btn.as_markup()

result_btn = InlineKeyboardBuilder()
result_btn.row(
    types.InlineKeyboardButton(
        text="Получить отчет",
        callback_data="result"
    )
)
result_btn = result_btn.as_markup()

end_btn = InlineKeyboardBuilder()
end_btn.row(
    types.InlineKeyboardButton(
        text="Поделиться с другом",
        callback_data="share"
    )
)
end_btn.row(
    types.InlineKeyboardButton(
        text="Пройти опрос еще раз",
        callback_data="report"
    )
)
end_btn = end_btn.as_markup()