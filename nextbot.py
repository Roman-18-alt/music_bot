import asyncio
from random import choice, randint
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3

dp = Dispatcher()
con = "music.db"

class ChoosingTrack(StatesGroup):
    choose_track = State()
    checking = State()
    deleteion = State()



def init_db():
    connection = sqlite3.connect(con)
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS music (
        track_id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist TEXT,
        song_name TEXT NOT NULL)''')
    
    connection.commit()
    connection.close()
    
init_db()


@dp.message(Command("start"))
async def hello(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выбрать песню"),
                                              KeyboardButton(text="Отказаться")],
                                             [KeyboardButton(text="Посмотреть добавленные треки")],
                                             [KeyboardButton(text="Удалить трек")]], resize_keyboard=True)
    await message.answer("Здравствуйте, я бот музыкант", reply_markup=keyboard)

@dp.message(F.text == "Отказаться")
async def say_good_bye(message: Message, state:FSMContext):
    await state.clear()
    await message.answer("Хорошо, до скорой встречи!")


@dp.message(F.text == "Посмотреть добавленные треки")
async def check(message:Message, state:FSMContext):
    await state.set_state(ChoosingTrack.checking)
    
    connection = sqlite3.connect(con)
    cursor = connection.cursor()
    
    try:
        cursor.execute('''SELECT song_name, artist, track_id FROM music''')
        tracks = cursor.fetchall()
        connection.close()
    
        for track in tracks:
            await message.answer(f"{track[2]} Трек {track[0]}, исполнитель {track[1]}")
            
    except Exception as e:
        print("В базе данных ещё нет треков")
        connection.close()


@dp.message(F.text == "Выбрать песню")
@dp.message(F.text == "Следующий")
async def get_song(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❤️", callback_data="like")],
                                    [InlineKeyboardButton(text="👎", callback_data="dislike")]])
    
    await state.set_state(ChoosingTrack.choose_track)
    
    genres = ["pop", "techno", "electronic"]
    genre = choice(genres)
    
    url = f"https://api.deezer.com/search?q=genre:{genre}&limit=50"
    
    response = requests.get(url)
    data = response.json()
    
    track = data["data"][randint(0, 49)]
    track_data = {
        "id": track["id"],
        "title": track["title"],
        "artist": track["artist"]["name"],
        "preview": track["preview"]
    }
    
    await state.update_data(choosing_track=track_data)
    
    await message.answer_audio(
        audio = track_data["preview"],
        caption=f"{track_data['artist']}\n"
        f"{track_data['title']}", reply_markup=keyboard)

@dp.callback_query(F.data == "like")
async def like_track(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    data = await state.get_data()
    track_data = data.get("choosing_track")
    
    connection = sqlite3.connect(con)
    cursor = connection.cursor()
    
    cursor.execute('''SELECT 1 FROM music WHERE track_id = ?''', (str(track_data["id"]),))
    exists = cursor.fetchone()
    
    if exists:
        await callback.message.answer("Такой трек уже добавлен!")
        connection.close()
        return
      
    else:
        cursor.execute(
            '''INSERT INTO music (track_id, artist, song_name) VALUES (?, ?, ?)''',
            (str(track_data["id"]), track_data["artist"], track_data["title"])
        )
    
        connection.commit()
        connection.close()
    
        await callback.message.answer("Добавлен в базу данных!")

    
@dp.callback_query(F.data == "dislike")
async def dislike_track(callback: CallbackQuery):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Следующий")],
                                             [KeyboardButton(text="Хватит")]], resize_keyboard=True) 
    await callback.answer()  
    await callback.message.answer("Хотите следующий трек?", reply_markup=keyboard)

@dp.message(F.text == "Удалить трек")
async def first_check(message: Message, state: FSMContext):
    
    await state.set_state(ChoosingTrack.deleteion)
    
    connection = sqlite3.connect(con)
    cursor = connection.cursor()
    
    cursor.execute('''SELECT track_id, artist, song_name FROM music''') 
    info = cursor.fetchall()
    connection.close()
    
    if info:
        for i, track in enumerate(info):
            await message.answer(f"Номер трека: {i + 1}. {track[2]} — {track[1]} (ID: {track[0]})")
        await state.update_data(delet=info)
    else:
        await message.answer("Ничего не найдено!")
    
    await message.answer("Введите номер трека который хотите удалить")

@dp.message(ChoosingTrack.deleteion)
async def deletion(message: Message, state: FSMContext):
   data = await state.get_data()
   track_data = data.get("delet")
   
   try:
        number = int(message.text) - 1
        track_id = track_data[number][0]
   except Exception as e:
       print("Введите число!")
   
   connection = sqlite3.connect(con)
   cursor = connection.cursor()
   
   try:
        cursor.execute('''DELETE FROM music WHERE track_id = ? ''', (track_id,))
        await message.answer("Трек успешно удалён!")
        await state.clear()
   except Exception as e:
       print("Error!")
       await state.clear()
   connection.commit()
   connection.close()
   
 
@dp.message(F.text == "Хватит")
async def stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Хорошо, до скорой встречи!")
 
 
    
async def main():
    TOKEN = "YOUR TOKEN"
    bot = Bot(TOKEN)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("ERROR")
        
if __name__ == "__main__":

    asyncio.run(main())
