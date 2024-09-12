from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from quiz_bot.database import (get_quiz_index, update_quiz_index,
                      reset_user_score)

from quiz_bot.read_file import read_file

quiz_data = read_file()


async def cmd_new_quiz(message):
    user_id = message.from_user.id
    await reset_user_score(user_id)
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=(
                "right_answer" if option == right_answer else "wrong_answer")))
    builder.adjust(1)
    return builder.as_markup()


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}",
                         reply_markup=kb)
