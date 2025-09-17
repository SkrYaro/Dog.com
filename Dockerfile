# Використовуємо офіційний образ Python
FROM python:3.12
# Встановлюємо робочу директорію у контейнері
WORKDIR /app
# Копіюємо файл залежностей у контейнер
COPY requirements.txt .
# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt
# Копіюємо вміст проекту в контейнер
COPY . .
# Відкриваємо порт, який використовується Django
EXPOSE 8000
# Запускаємо сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
