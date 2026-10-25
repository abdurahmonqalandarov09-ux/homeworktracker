from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from dotenv import load_dotenv
from service import *
from connection import *
import asyncio
import os
from datetime import *

load_dotenv()

token = os.getenv("bot_token")

bot = Bot(token=token)
dp = Dispatcher()



main_kb = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text="📚 Задания")], [KeyboardButton(text="📊 Мои оценки")],
        [KeyboardButton(text="🆘 Помошь")],
    ],

    resize_keyboard=True,
)





@dp.message(CommandStart())
async def start_bot(message: Message):
    if await get_users(message.from_user.id):
        await message.answer(f"Hello @{message.from_user.username} этот бот поможет контроировать твои задания или оценки", reply_markup=main_kb)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"Hello @{message.from_user.username} этот бот поможет контроировать твои задания или оценки", reply_markup=main_kb)



@dp.message(F.text == "🆘 Помошь")
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("""

    /add_assignment - <title> <deadline> - Добавляет задание
    /assignments -  -  - Показывает задания, которые пользователь ещё не сдал
    /submit - <assignment_id - Отмечает, что пользователь сдал задание
    /set_grade - <assignment_id> <grade> - Проставляет оценку за сданное задание
    /my_grades -  -  -  Показывает все оценки пользователя
    /average_grade -  -  - Показывает средний балл пользователя

""") 





@dp.message(Command("add_assignment"))
async def add_assignment_bot_create(message: Message, command: CommandObject):
    if not command.args:
        await message.answer(f"Вы не указали название и дедлайн")
        return

    data = command.args.split("/")


    if len(data) == 1:
        await message.answer(f"Не хватает второго аргумента нужно указать название и дедлайн через <</>>")
        return

    if len(data) > 2:
        await message.answer("Слишком много аргументов, нужно название и дедлайн через <</>>")
        return

    title, due_str = data

    try:
        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
    except ValueError:
        await message.answer(f"Не удалось распознать дату, используйте формат: ГГ-ММ-ДД пример: 2026-10-25")
        return

    await add_asignment(title, due_date)
    await message.answer(f"Задание {title} добавлено успешно, Дедлайн: {due_date}")





@dp.message(Command("submit"))
async def submit_bot_create(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Укажите assignment_id")
        return

    data = command.args.split()
    
    await submit(message.from_user.id, data[0])




async def main():
    await create_table_db()
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())