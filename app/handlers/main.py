import os
import uuid

from aiogram import Router, Bot, types, F
import aiohttp
import asyncio
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from app.database.requests import get_user, add_user, user_subscribe, get_statistics
from app.keyboards.main import *
from app.texts.main import *
from decouple import config as env_config

from app.utils.functions import create_report
from app.utils.state import UserState

main_handler = Router()


@main_handler.inline_query()
async def inline_referral(query: InlineQuery, bot: Bot):
    ref = query.query
    text = f"""https://t.me/egor_is_typing_report_bot?start={ref}"""
    title = """Поделиться"""
    await query.answer([
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=title,
            input_message_content=InputTextMessageContent(
                message_text=text
            )
        )
    ],
        cache_time=0)


async def send_postback(clickid):
    url = "https://offers-socialjet-cpa.affise.com/postback"
    params = {
        'clickid': clickid
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    print(f"Успех: {clickid} — {await response.text()}")
                else:
                    print(f"Ошибка: {clickid} — статус {response.status}")
        except Exception as e:
            print(f"Исключение при запросе {clickid}: {e}")


@main_handler.message(Command("statistics"))
async def cmd_message(message: types.Message, bot: Bot):
    stats = await get_statistics()
    msg = f"""Всего пользователей: {stats['total_users']}
Всего генераций: {len(os.listdir("/home/bot/users_report"))}


"""
    for click_name, count in stats['total_click_id']:
        msg += f"{click_name}: {count}\n"

    await message.answer(msg)



@main_handler.message(Command("start"))
async def cmd_message(message: types.Message, bot: Bot, command: Command):
    user = await get_user(message.from_user.id)
    if not user:
        args = command.args
        click_id = None

        if args and args.isdigit():
            click_id = "referral"
            await message.answer_document(FSInputFile(f"users_report/{args}.png"),
                                          caption=ref_msg,
                                          reply_markup=start_ref)
            await add_user(message.from_user.id, message.from_user.first_name, message.from_user.username,
                           message.from_user.full_name, click_id=click_id)
            return
        elif args and len(args) == 24:
            await send_postback(f"{args}{message.from_user.id}")
            click_id = "click_id"
        elif args:
            click_id = args

        await message.answer(start_msg, reply_markup=start_btn, disable_web_page_preview=True)
        await add_user(message.from_user.id, message.from_user.first_name, message.from_user.username,
                       message.from_user.full_name, click_id=click_id)

    elif not user.subscribed:
        await message.answer(subscribe_msg, reply_markup=subscribe_btn)
    else:
        await message.answer(answer_1_msg, reply_markup=answer_1_btn)


@main_handler.callback_query(F.data == "start")
async def answer_message(callback: types.CallbackQuery, bot: Bot):
    await callback.message.answer(subscribe_msg, reply_markup=subscribe_btn)


@main_handler.callback_query(F.data == "check_subscribe")
async def answer_message(callback: types.CallbackQuery, bot: Bot):
    member = await bot.get_chat_member(chat_id=env_config('CHANNEL_ID'), user_id=callback.from_user.id)
    if member.status in ("member", "administrator", "creator"):
        await callback.message.answer(answer_1_msg, reply_markup=answer_1_btn)
        await user_subscribe(callback.from_user.id)
    else:
        await callback.message.answer(unsubscribe_msg, reply_markup=subscribe_btn)


@main_handler.callback_query(F.data == "report")
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer(answer_1_msg, reply_markup=answer_1_btn)


@main_handler.callback_query(F.data.contains("answer_1_"))
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    answer = callback.data.split("_")[-1]
    await state.update_data(answers={1: answer})
    await callback.message.answer(answer_2_msg, reply_markup=answer_2_btn)


@main_handler.callback_query(F.data.contains("answer_2_"))
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    answer = callback.data.split("_")[-1]
    data = await state.get_data()
    data["answers"][2] = answer
    await state.update_data(answers=data["answers"])
    await callback.message.answer(answer_3_msg)
    await state.set_state(UserState.text_1)


@main_handler.message(UserState.text_1)
async def answer_message(message: types.Message, bot: Bot, state: FSMContext):
    if message.text:
        if len(message.text) <= 50:
            await state.update_data(text_1=message.text)
            data = await state.get_data()
            data["answers"][3] = 1
            await state.update_data(answers=data["answers"])
            media = [
                InputMediaPhoto(media=FSInputFile(env_config("GLOBAL_PATH") + "app/src/mems_1.png")),
                InputMediaPhoto(media=FSInputFile(env_config("GLOBAL_PATH") + "app/src/mems_2.png")),
                InputMediaPhoto(media=FSInputFile(env_config("GLOBAL_PATH") + "app/src/mems_3.png")),
            ]
            await bot.send_media_group(chat_id=message.chat.id, media=media)
            await message.answer(answer_4_msg, reply_markup=answer_4_btn)
            await state.set_state(UserState.start)
        else:
            await message.answer(answer_3_error_msg)
    else:
        await message.answer(answer_3_error_msg)


@main_handler.callback_query(F.data.contains("answer_4_"))
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    answer = callback.data.split("_")[-1]
    data = await state.get_data()
    data["answers"][4] = answer
    await state.update_data(answers=data["answers"])
    await callback.message.answer(answer_5_msg)
    await state.set_state(UserState.text_2)


@main_handler.message(UserState.text_2)
async def answer_message(message: types.Message, bot: Bot, state: FSMContext):
    if message.text:
        await state.update_data(text_2=message.text)
        data = await state.get_data()
        data["answers"][5] = 1
        await state.update_data(answers=data["answers"])
        await message.answer_photo(caption=answer_6_msg,
                                   reply_markup=answer_6_btn,
                                   photo=FSInputFile(env_config("GLOBAL_PATH") + "app/src/visual.png"))
        await state.set_state(UserState.start)
    else:
        await message.answer(answer_5_error_msg)


@main_handler.callback_query(F.data.contains("answer_6_"))
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    answer = callback.data.split("_")[-1]
    data = await state.get_data()
    data["answers"][6] = answer
    await state.update_data(answers=data["answers"])
    await callback.message.answer(answer_7_msg, reply_markup=answer_7_btn)


@main_handler.callback_query(F.data.contains("answer_7_"))
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    answer = callback.data.split("_")[-1]
    data = await state.get_data()
    data["answers"][7] = answer
    await state.update_data(answers=data["answers"])
    await callback.message.answer(answer_8_msg, reply_markup=answer_8_btn)


@main_handler.callback_query(F.data.contains("answer_8_"))
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    answer = callback.data.split("_")[-1]
    data = await state.get_data()
    data["answers"][8] = answer
    await state.update_data(answers=data["answers"])
    await callback.message.answer(answer_9_msg, reply_markup=answer_9_btn)
    await state.set_state(UserState.generatePhoto)


@main_handler.callback_query(F.data.contains("answer_9_"), UserState.generatePhoto)
async def answer_message(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    msg = await callback.message.answer("Отчет в работе, подожди немного.")
    await state.set_state(UserState.start)
    answer = callback.data.split("_")[-1]
    data = await state.get_data()
    data["answers"][9] = answer
    await create_report(data["answers"], data["text_1"], data["text_2"], callback.from_user.id)
    await callback.message.answer_document(FSInputFile(f"users_report/{callback.from_user.id}.png"), caption=end_msg,
                                           reply_markup=get_end_btn(callback.from_user.id))
    await msg.delete()
