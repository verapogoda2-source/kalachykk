import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FILENAME = 'records.json'

# Загрузка существующих данных
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение данных
def save_data(data):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = load_data()

        self.filtered_records = self.records.copy()

        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля для ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Дата
        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5)

        # Температура
        tk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, padx=5)
        self.temp_entry = tk.Entry(input_frame)
        self.temp_entry.grid(row=0, column=3, padx=5)

        # Описание
        tk.Label(input_frame, text="Описание погоды:").grid(row=1, column=0, padx=5)
        self.desc_entry = tk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5)

        # Осадки (да/нет)
        self.rain_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Осадки", variable=self.rain_var).grid(row=2, column=0, padx=5)

        # Кнопка добавить
        add_button = tk.Button(self.root, text="Добавить запись", command=self.add_record)
        add_button.pack(pady=5)

        # Фильтр по дате
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5)
        self.filter_date_entry = tk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=1, padx=5)

        # Фильтр по температуре
        tk.Label(filter_frame, text="Минимальная температура:").grid(row=0, column=2, padx=5)
        self.temp_filter_entry = tk.Entry(filter_frame, width=10)
        self.temp_filter_entry.grid(row=0, column=3, padx=5)

        # Кнопки фильтрации
        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=5)

        show_all_btn = tk.Button(filter_frame, text="Показать все", command=self.show_all)
        show_all_btn.grid(row=0, column=5, padx=5)

        # Таблица для отображения записей
        columns = ("Дата", "Температура", "Описание", "Осадки")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def add_record(self):
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        rain = self.rain_var.get()

        # Проверка даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return

        # Проверка температуры
        try:
            temperature = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return

        # Проверка описания
        if not desc:
            messagebox.showerror("Ошибка", "Поле описания не должно быть пустым.")
            return

        record = {
            "date": date_str,
            "temperature": temperature,
            "description": desc,
            "rain": rain
        }

        self.records.append(record)
        save_data(self.records)
        self.update_table()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.rain_var.set(False)

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        for rec in self.records:
            rain_text = "Да" if rec["rain"] else "Нет"
            self.tree.insert("", tk.END, values=(
                rec["date"],
                rec["temperature"],
                rec["description"],
                rain_text
            ))

    def apply_filter(self):
        date_filter = self.filter_date_entry.get().strip()
        temp_filter = self.temp_filter_entry.get().strip()

        self.filtered_records = self.records.copy()

        # Фильтр по дате
        if date_filter:
            try:
                datetime.strptime(date_filter, "%Y-%m-%d")
                self.filtered_records = [r for r in self.filtered_records if r["date"] == date_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты для фильтра.")
                return

        # Фильтр по температуре
        if temp_filter:
            try:
                min_temp = float(temp_filter)
                self.filtered_records = [r for r in self.filtered_records if r["temperature"] >= min_temp]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректное значение температуры для фильтра.")
                return

        # Обновляем таблицу
        self.tree.delete(*self.tree.get_children())
        for rec in self.filtered_records:
            rain_text = "Да" if rec["rain"] else "Нет"
            self.tree.insert("", tk.END, values=(
                rec["date"],
                rec["temperature"],
                rec["description"],
                rain_text
            ))

    def show_all(self):
        self.filter_date_entry.delete(0, tk.END)
        self.temp_filter_entry.delete(0, tk.END)
        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
