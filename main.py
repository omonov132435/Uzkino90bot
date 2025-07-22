# main.py
from aiogram import Bot, Dispatcher, types, executor
import json
from config import BOT_TOKEN, ADMIN_USERNAME

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

with open("movies.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

def get_movie_list(vip_only=False):
    result = ""
    for movie in movies:
        if vip_only and not movie.get("is_vip"):
            continue
        result += f"🎬 <b>{movie['title']}</b>\n📄 {movie['description']}\n🔗 {movie['url']}\n\n"
    return result or "🎥 Hozircha kino yo'q."

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("🎬 Xush kelibsiz!\n\nVIP kinolar: /vip\nBepul kinolar: /free", parse_mode="HTML")

@dp.message_handler(commands=["vip"])
async def vip_handler(message: types.Message):
    await message.answer("🔐 VIP kinolar:\n\n" + get_movie_list(vip_only=True), parse_mode="HTML")

@dp.message_handler(commands=["free"])
async def free_handler(message: types.Message):
    result = ""
    for movie in movies:
        if not movie.get("is_vip"):
            result += f"🎬 <b>{movie['title']}</b>\n📄 {movie['description']}\n🔗 {movie['url']}\n\n"
    await message.answer("🆓 Bepul kinolar:\n\n" + (result or "Hozircha yo'q"), parse_mode="HTML")

@dp.message_handler(commands=["add"])
async def add_movie(message: types.Message):
    if message.from_user.username != ADMIN_USERNAME:
        return await message.reply("❌ Siz admin emassiz!")
    try:
        _, title, description, url, is_vip = message.text.split(" | ")
        movies.append({
            "title": title,
            "description": description,
            "url": url,
            "is_vip": is_vip.lower() == "true"
        })
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
        await message.answer("✅ Kino qo‘shildi.")
    except:
        await message.reply("❌ Format noto‘g‘ri. To‘g‘ri format:\n/add | title | description | url | true/false")

if __name__ == "__main__":
    executor.start_polling(dp)
