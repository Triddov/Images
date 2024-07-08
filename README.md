## Сервис загрузки изображений 

- Проверка типа загружаемого изображения (поддерживаются форматы .png, .jpg, .jpeg, .webp, .ico, .svg).
- Проверка размера файла (не более 1 МБ).
- Сохранение валидных изображений в папке `gallery`.
- Сохранение метаданных изображений в базе данных PostgreSQL.
- Ведение логов в файле logs.txt

1. Убедитесь, что PostgreSQL установлен и запущен на вашем компьютере. 
2. Создайте базу данных и таблицу, используя файл images.sql в папке `backup`
3. Выполните команды в корне проекта:

   ```
   git clone https://github.com/Triddov/Images.git
   
   docker-compose up --build -d
   ```

Для того, чтобы запустить приложение локально без использования Docker,
в файле `.env` заменить значение переменнной DB_HOST на localhost

   ```
   git clone https://github.com/Triddov/Images.git
   
   pip install -r requirements.txt
   ```