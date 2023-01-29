import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

open_weather_token = "c051b9a49b61bc011a9ec9d94330035f"
tg_bot_token = "5946167776:AAF45UeNp6CBp0n8CeEu7cSl-ujPvUZmn3U"

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привіт! Напиши мені назву міста для відображення погоди!")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Морось \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B",
    }
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric" 
        )
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивися у вікно"
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        country = data["sys"]["country"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        await message.reply(f"----{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}----\n")
        await message.reply(f"Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Тиск: {pressure}\n"
              f"Вологість: {humidity}%\nШвидкість вітру: {wind}м/с\n"
              f"Країна: {country}\nСвітанок: {sunrise_timestamp}\nЗахід: {sunset_timestamp}\n"
              f"Тривалість дня: {lenght_of_the_day}\n"
             )
    except:
        await message.reply("\U00002620 Перевірте назву міста \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)