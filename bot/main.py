import asyncio
import logging
import os
from datetime import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE = os.getenv("API_BASE")  # URL бекенда, напр. https://myapp.up.railway.app

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

USERS_FILE = "users.txt"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return [int(x) for x in f.read().split()]

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            f.write("\n".join(map(str, users)))

@dp.message(Command("add_me"))
async def add_me(message: types.Message):
    save_user(message.from_user.id)
    await message.answer("👌 Тебе додано до списку учасників.")

async def send_daily_questions():
    users = load_users()
    keyboard = [
        [
            types.InlineKeyboardButton(text="Так", callback_data="yes"),
            types.InlineKeyboardButton(text="Ні", callback_data="no")
        ]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)

    for user_id in users:
        try:
            await bot.send_message(
                chat_id=user_id,
                text="Ти виконав свою задачу сьогодні?",
                reply_markup=markup
            )
        except:
            pass

@dp.callback_query()
async def on_answer(callback: types.CallbackQuery):
    answer = callback.data
    user_id = callback.from_user.id

    async with aiohttp.ClientSession() as session:
        await session.post(f"{API_BASE}/answer", json={
            "user_id": user_id,
            "answer": answer
        })

    await callback.message.edit_text(f"Відповідь записано: {answer.capitalize()}")

async def main():
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(send_daily_questions, "cron", hour=14, minute=0)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

