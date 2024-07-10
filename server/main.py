from flask import Flask, request, jsonify, render_template
from datetime import datetime
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from database import Database
import base64
import os

load_dotenv()  # Загрузка переменных из .env файла


app = Flask(__name__)

chunks_storage = {}  # Временное хранилище чанков изображения

ImageLimit = int(os.getenv('IMAGE_LIMIT')) 

app.config['UPLOAD_FOLDER'] = 'gallery'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/image", methods=["POST"])
def process_image():
    data = request.get_json()

    image_data = data['base64']
    title = data['title']
    image_size = data['size']
    description = data['description']
    tags = data['tags']
    extension = data['extension']

    if not title.strip():
        response = {
            "status": "422",
            "message": "Empty image title"
        }
        log_status("422", "Empty image title", title)
        return jsonify(response), 422  # семантически неправильный запрос

    try:
        header, image_data = image_data.split(",", 1)
        image = base64.b64decode(image_data)

        if float(image_size[:-3]) >= ImageLimit:
            response = {
                "status": "413",
                "message": f"The file size is limited to {ImageLimit/1024} MB"
            }
            log_status("413", f"The file size is limited to {ImageLimit/1024} MB", title)
            return jsonify(response), 413  # слишком большой объем данных

        # Проверка валидности файла
        image = Image.open(BytesIO(image))
        image.verify()  # Фактическая проверка

        # Сохранение изображения
        filename = f"{title}.{extension}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        image.save(image_path)

        db = Database()
        db.insert_image(title, image_path, image_size, description, tags, extension)
        db.close()

        response = {
            "status": "200",
            "message": "Image uploaded successfully!",
            "path": image_path
        }

        log_status("200", "Image uploaded successfully!", title)
        return jsonify(response), 200  # успешно

    except (IOError, SyntaxError):
        response = {
            "status": "415",
            "message": "The file is not a valid image"
        }
        log_status("415", "The file is not a valid image", title)
        return jsonify(response), 415  # неподдерживаемый формат


@app.route("/image-chunks", methods=["POST"])
def handle_chunks():
    data = request.get_json()

    chunk_id = data['id']
    total_chunks = data['total']
    chunk_data = data['chunk']

    title = data['title']

    if title not in chunks_storage:
        chunks_storage[title] = [''] * total_chunks

    chunks_storage[title][chunk_id - 1] = chunk_data

    if all(chunk != '' for chunk in chunks_storage[title]):
        full_image_data = ''.join(chunks_storage[title])
        del chunks_storage[title]

        data['base64'] = full_image_data
        return process_image(data)

    return jsonify({"message": f"{chunk_id}/{total_chunks} received"}), 200  # успешно


def log_status(status, message, title):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('date:%m/%d/%y time:%H:%M:%S')}"
                       f" - code:{status} | message: {message} | file name: '{title}'\n")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
