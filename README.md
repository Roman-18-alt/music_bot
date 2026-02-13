<div align="center">

# 🎵 Music Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-0FA4F8?style=flat&logo=telegram&logoColor=white)](https://aiogram.dev)
[![License MIT](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)

</div>

<div align="center">
<img src="https://github.com/Roman-18-alt/music_bot/raw/main/screenshot1.png" width="300" alt="Главное меню"/>
<img src="https://github.com/Roman-18-alt/music_bot/raw/main/screenshot2.png" width="300" alt="Аудио плеер"/>  
<img src="https://github.com/Roman-18-alt/music_bot/raw/main/screenshot3.png" width="300" alt="Удаление трека"/>
</div>

## 📝 Описание

**Telegram бот для поиска и управления музыкой** 🎧

Полноценный **CRUD бот** с **Finite State Machine (FSM)** для меломанов. Ищет треки через **Deezer API**, сохраняет в **SQLite** и позволяет управлять плейлистом.

## ✨ Функционал

| Функция | Описание |
|---------|----------|
| 🔍 **Deezer API** | Поиск в жанрах: pop, techno, electronic |
| ❤️💔 **Кнопки** | Интерактивный лайк/дизлайк треков |
| 💾 **SQLite** | Полный CRUD (Create/Read/Update/Delete) |
| 📋 **Просмотр** | Список всех сохранённых треков |
| 🗑 **FSM** | Удаление трека по номеру |

## 📱 Демо

### 1. Главное меню
![screenshot1.png](screenshot1.png)

### 2. Аудио + кнопки
![screenshot2.png](screenshot2.png)

### 3. Удаление (FSM)
![screenshot3.png](screenshot3.png)

## 🚀 Быстрый старт (5 минут)

### Предварительные требования
- Python 3.10+
- Telegram Bot Token от [@BotFather](https://t.me/botfather)

### Установка
```bash
# 1. Клонировать репозиторий
git clone [https://github.com/Roman-18-alt/music_bot.git](https://github.com/Roman-18-alt/music_bot.git)
cd music_bot

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить
python bot.py


СТРУКТУРА БД
CREATE TABLE music (
    track_id INTEGER PRIMARY KEY,  -- Deezer track ID
    artist TEXT NOT NULL AUTOINCREMENT,
    song_name TEXT NOT NULL
);
FSM логика удаления:
"Удалить трек" 
    ↓
SELECT → [(id1,artist1,song1), (id2,...)]
    ↓ 
state.update_data(tracks_list=список)
    ↓  
"1" → index 0 → track_id → DELETE


АВТОР
Роман 15 лет
Python Developer (Beginer)
Voronezh

Лицензия
MIT License — свободное использование!

<div align="center"> <b>⭐ Star проект, если понравился!</b> </div> ``` Вот мой файл README, дальше просто закинуть 4 файла на сайте и нажать commit?
