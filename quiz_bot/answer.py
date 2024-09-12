from aiogram import types

from quiz_bot.database import (get_quiz_index, update_quiz_index,
                               update_user_score)
from quiz_bot.read_file import read_file
from quiz_bot.quiz import get_question

quiz_data = read_file()


async def handle_answer(callback: types.CallbackQuery, is_right_answer: bool):
    selected_button_text = get_selected_button_text(callback)

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    if is_right_answer:
        await callback.message.answer(f"Ваш ответ - {selected_button_text}."
                                      f" Верно!")
        await update_user_score(callback.from_user.id, True)
    else:
        current_question_index = await get_quiz_index(callback.from_user.id)
        correct_i = quiz_data[current_question_index]['correct_option']
        correct_answer = quiz_data[current_question_index]['options'][correct_i]
        await callback.message.answer(f"Ваш ответ - {selected_button_text}."
                                      f" Неправильно. Правильный ответ:"
                                      f" {correct_answer}")
        await update_user_score(callback.from_user.id, False)

    current_question_index = await get_quiz_index(callback.from_user.id)
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос."
                                      " Квиз завершен!")


def get_selected_button_text(callback: types.CallbackQuery):
    selected_data = callback.data
    return next(
        (btn.text for row in callback.message.reply_markup.inline_keyboard
         for btn in row if btn.callback_data == selected_data), "неизвестный")


async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, True)


async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, False)
