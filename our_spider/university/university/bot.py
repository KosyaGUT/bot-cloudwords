import numpy as np
from PIL import Image
from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from formating import univer_dict
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
from random import randrange
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
emoji_sad = ['😢', '🫠', '😔', '😞', '🥲', '🤕']
emoji_good = ['✨', '🌟', '🎉', '👑']


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, "Напишите название направления или его код")


@dp.message_handler()
async def get_direction_info(message: types.Message):
    direction_code = message.text.capitalize()
    try:
        university = univer_dict[direction_code][0]
        program = univer_dict[direction_code][1]
        subjects1 = univer_dict[direction_code][2]
        subjects = univer_dict[direction_code][2]
        text = " ".join(subjects)

        python_mask = np.array(Image.open("cloud.png"))

        wordcloud = WordCloud(stopwords=STOPWORDS,
                              mask=python_mask,
                              background_color='white',
                              contour_color="black",
                              contour_width=3,
                              min_font_size=3,
                              max_words=400).generate(text)

        buf = BytesIO()
        wordcloud.to_image().save(buf, 'PNG')
        buf.seek(0)

        em_anser = emoji_good[randrange(4)]
        message_text = f"{em_anser} По направлению <b>{program}</b> университет <b>{university}</b> — лучший{em_anser}\n\n"

        for num in range(5):
            message_text += '#' + subjects1[num].replace(u' ', u'_') + " "

        await bot.send_photo(chat_id=message.from_user.id, photo=buf, caption=message_text, parse_mode='HTML')

    except KeyError:
        em_anser = emoji_sad[randrange(6)]
        message_text = f"{em_anser}Не получилось найти «{direction_code}»{em_anser}"

        with open(f"img\{randrange(0, 4)}.jpg", 'rb') as photo:  # указать путь к изображению на диске
            await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=message_text)

if __name__ == '__main__':
    executor.start_polling(dp)