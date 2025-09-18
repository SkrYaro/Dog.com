# Використовуємо стабільну версію Python для Kivy
FROM python:3.11-slim

# Оновлюємо pip
RUN pip install --upgrade pip

# Створюємо робочу папку
WORKDIR /app

# Копіюємо лише requirements спочатку
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Виставляємо змінну середовища
ENV PYTHONUNBUFFERED=1

# Опціонально: відкритий порт для Django/ASGI
EXPOSE 8000

# Команда за замовчуванням (можна змінити під свій проєкт)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
