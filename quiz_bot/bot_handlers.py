from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from quiz_bot.quiz import cmd_new_quiz
from aiogram import Dispatcher

from quiz_bot.answer import right_answer, wrong_answer
from quiz_bot.database import get_user_score
from quiz_bot.read_file import read_file

quiz_data = read_file()


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))

    dp.message.register(cmd_new_quiz, F.text == "Начать игру")
    dp.message.register(cmd_new_quiz, Command("quiz"))

    dp.message.register(cmd_show_statistics,
                        F.text == "Посмотреть статистику")

    dp.callback_query.register(right_answer, F.data == "right_answer")
    dp.callback_query.register(wrong_answer, F.data == "wrong_answer")


async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Посмотреть статистику"))
    await message.answer("Добро пожаловать в квиз!",
                         reply_markup=builder.as_markup(resize_keyboard=True))


async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await cmd_new_quiz(message)


async def cmd_show_statistics(message: types.Message):
    user_id = message.from_user.id
    user_score = await get_user_score(user_id)
    if user_score is not None:
        await message.answer(f"Ваш последний результат: {user_score}"
                             f" из {len(quiz_data)}.")
    else:
        await message.answer("У вас пока нет результатов. Начните квиз,"
                             " чтобы они появились.")
