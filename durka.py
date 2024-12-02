from aiogram import Bot, Dispatcher, executor, types
import yt_dlp
import os

# Вставьте ваш токен от BotFather
BOT_TOKEN = "8090251052:AAHzUK9gVCMvl190CRRmg4pA53Sadt0FYdI"

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Папка для сохранения видео
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# Функция для скачивания видео
def download_videos(url):
    options = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',  # Скачиваем лучшее качество
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(result)


# Хэндлер для обработки команд /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на видео, и я скачаю его для тебя.")


# Хэндлер для обработки ссылок
@dp.message_handler()
async def handle_url(message: types.Message):
    url = message.text
    await message.reply("Пожалуйста, подождите. Видео загружается...")
    try:
        video_path = download_videos(url)
        with open(video_path, 'rb') as video:
            await bot.send_video(message.chat.id, video)
        os.remove(video_path)  # Удаляем файл после отправки
    except Exception as e:
        await message.reply(f"Ошибка: {e}")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
