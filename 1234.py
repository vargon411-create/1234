import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Список предопределённых цитат
quotes = [
    {"text": "Жизнь — это то, что происходит, пока вы заняты другими планами.", "author": "Джон Леннон", "theme": "Жизнь"},
    {"text": "Будьте реалистами, требуйте невозможного!", "author": "Че Гевара", "theme": "Вдохновение"},
    {"text": "Счастье — это не цель, а способ путешествия.", "author": "Артур Эш", "theme": "Счастье"},
    {"text": "Изменения — это закон жизни. И те, кто смотрит только в прошлое или настоящее, наверняка упустят будущее.", "author": "Джон Кеннеди", "theme": "Изменения"},
    {"text": "Успех — это не случайность, это труд, упорство, обучение, жертвы и, главное, любовь к тому, что вы делаете или изучаете.", "author": "Пеле", "theme": "Успех"},
]

# Функция загрузки истории из файла
def load_history():
    if os.path.exists("quote_history.json"):
        with open("quote_history.json", "r") as file:
            return json.load(file)
    return []

# Функция сохранения истории в файл
def save_history():
    with open("quote_history.json", "w") as file:
        json.dump(history, file)

# Функция для генерации случайной цитаты
def generate_quote():
    quote = random.choice(quotes)
    history.append(quote)
    update_quote_display(quote)
    update_history_list()

# Функция для отображения цитаты
def update_quote_display(quote):
    quote_display.config(text=f"{quote['text']}\n\n- {quote['author']}")

# Функция для обновления списка истории
def update_history_list():
    history_list.delete(0, tk.END)
    for quote in history:
        history_list.insert(tk.END, f"{quote['text']} - {quote['author']}")

# Функция для фильтрации
def filter_history():
    author = author_entry.get().strip()
    theme = theme_entry.get().strip()
    filtered = []

    for quote in history:
        if (author in quote['author']) and (theme in quote['theme']):
            filtered.append(quote)

    display_filtered_history(filtered)

# Функция для отображения отфильтрованной истории
def display_filtered_history(filtered):
    history_list.delete(0, tk.END)
    for quote in filtered:
        history_list.insert(tk.END, f"{quote['text']} - {quote['author']}")

# Проверка корректности входа
def add_quote(author, text, theme):
    if not author or not text or not theme:
        messagebox.showwarning("Ошибка", "Поля не могут быть пустыми.")
        return

    new_quote = {"text": text, "author": author, "theme": theme}
    quotes.append(new_quote)

# Основной код приложения
history = load_history()

root = tk.Tk()
root.title("Генератор случайных цитат")

# Кнопка для генерации цитаты
generate_button = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
generate_button.pack(pady=10)

# Область для отображения текущей цитаты
quote_display = tk.Label(root, wraplength=400, justify="center", font=("Arial", 14))
quote_display.pack(pady=10)

# Поля для фильтрации
author_entry = tk.Entry(root, width=20)
author_entry.insert(0, "Автор")
author_entry.pack(pady=5)

theme_entry = tk.Entry(root, width=20)
theme_entry.insert(0, "Тема")
theme_entry.pack(pady=5)

filter_button = tk.Button(root, text="Фильтровать историю", command=filter_history)
filter_button.pack(pady=5)

# Список истории
history_list = tk.Listbox(root, width=50)
history_list.pack(pady=20)

# Загрузка истории при запуске
update_history_list()

# Сохранение истории при закрытии
def on_closing():
    save_history()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
