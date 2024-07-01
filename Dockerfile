# Используем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы и директории из директории server внутрь контейнера
COPY server/ .
COPY .env .

# Настройка PYTHONPATH
ENV PYTHONPATH=/app/server

# Определяем команду для запуска вашего приложения
CMD ["python", "main.py"]
