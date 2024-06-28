## Возможности 

- Проверка типа загружаемого изображения (поддерживаются форматы .png, .jpg, .jpeg, .webp, .ico, .svg).
- Проверка размера файла (не более 1 МБ).
- Сохранение валидных изображений в папке `gallery`.
- Сохранение метаданных изображений в базе данных PostgreSQL.


   ```
   git clone https://github.com/yourusername/image-upload-service.git
   
   pip install -r requirements.txt
   ```

Убедитесь, что PostgreSQL установлен и запущен на вашем компьютере. 
Создайте базу данных и таблицу, используя файл images.sql в папке `backup`

