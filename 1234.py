import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Функция для загрузки данных из файла
def load_movies():
    if os.path.exists("movies.json"):
        with open("movies.json", "r") as file:
            return json.load(file)
    return []

# Функция для сохранения данных в файл
def save_movies():
    with open("movies.json", "w") as file:
        json.dump(movies, file)

# Функция для добавления фильма
def add_movie():
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены.")
        return

    if not year.isdigit() or not (1888 <= int(year) <= 2023):  # Проверка года
        messagebox.showwarning("Ошибка", "Год должен быть числом от 1888 до 2023.")
        return

    try:
        rating = float(rating)
        if rating < 0 or rating > 10:  # Проверка рейтинга
            raise ValueError
    except ValueError:
        messagebox.showwarning("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
        return

    movie = {"title": title, "genre": genre, "year": int(year), "rating": rating}
    movies.append(movie)
    clear_entries()
    update_movie_list()

# Функция для очистки полей ввода
def clear_entries():
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

# Функция для обновления списка фильмов
def update_movie_list(filtered_movies=None):
    movie_list.delete(*movie_list.get_children())
    current_movies = filtered_movies if filtered_movies is not None else movies
    for movie in current_movies:
        movie_list.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

# Функция для фильтрации фильмов
def filter_movies():
    genre = genre_filter_entry.get().strip()
    year = year_filter_entry.get().strip()
    filtered = movies

    if genre:
        filtered = [movie for movie in filtered if genre.lower() in movie["genre"].lower()]
    if year and year.isdigit():
        filtered = [movie for movie in filtered if movie["year"] == int(year)]

    update_movie_list(filtered)

# Основной код приложения
movies = load_movies()

root = tk.Tk()
root.title("Личная кинотека")

# Поля ввода для создания и фильтрации фильмов
tk.Label(root, text="Название").grid(row=0, column=0)
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1)

tk.Label(root, text="Жанр").grid(row=1, column=0)
genre_entry = tk.Entry(root)
genre_entry.grid(row=1, column=1)

tk.Label(root, text="Год выпуска").grid(row=2, column=0)
year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1)

tk.Label(root, text="Рейтинг (0-10)").grid(row=3, column=0)
rating_entry = tk.Entry(root)
rating_entry.grid(row=3, column=1)

add_button = tk.Button(root, text="Добавить фильм", command=add_movie)
add_button.grid(row=4, columnspan=2)

# Поля для фильтрации
tk.Label(root, text="Жанр для фильтрации").grid(row=5, column=0)
genre_filter_entry = tk.Entry(root)
genre_filter_entry.grid(row=5, column=1)

tk.Label(root, text="Год для фильтрации").grid(row=6, column=0)
year_filter_entry = tk.Entry(root)
year_filter_entry.grid(row=6, column=1)

filter_button = tk.Button(root, text="Фильтровать", command=filter_movies)
filter_button.grid(row=7, columnspan=2)

# Таблица для отображения фильмов
movie_list = ttk.Treeview(root, columns=("title", "genre", "year", "rating"), show="headings")
movie_list.heading("title", text="Название")
movie_list.heading("genre", text="Жанр")
movie_list.heading("year", text="Год")
movie_list.heading("rating", text="Рейтинг")
movie_list.grid(row=8, columnspan=2)

# Загрузка фильмов при запуске
update_movie_list()

# Сохранение данных при закрытии
def on_closing():
    save_movies()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
