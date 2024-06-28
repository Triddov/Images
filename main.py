from flask import Flask, request, jsonify, render_template
import psycopg2
import base64
import os
from PIL import Image
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

DB_HOST = 'localhost'
DB_NAME = 'Images'
DB_USER = 'postgres'
DB_PASS = 'qwerty09876'
DB_PORT = '5432'

pg = psycopg2.connect(f"""
    host={DB_HOST}
    dbname={DB_NAME} 
    user={DB_USER}
    password={DB_PASS}
    port={DB_PORT}
""")

ImageLimit = 1024 # KB

app.config['UPLOAD_FOLDER'] = 'gallery'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/image", methods=["POST"])
def handle_image():
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
        log_status("422", "Empty image title")
        return jsonify(response), 422 #семантически неправльный запрос

    try:
        header, image_data = image_data.split(",", 1)
        image = base64.b64decode(image_data)

        if float(image_size[:-3]) >= ImageLimit:
            response = {
                "status": "413",
                "message": f"The file size is limited to {ImageLimit/1024} MB"
            }
            log_status("413", f"The file size is limited to {ImageLimit/1024} MB")
            return jsonify(response), 413 #слишком большой объем данных

        # Check if it's a valid image
        image = Image.open(BytesIO(image))
        image.verify()  # Verify that it is, in fact, an image

        # Сохранение изображения
        filename = f"{data['title']}.{data['extension']}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        image.save(image_path)

        cursor = pg.cursor()
        cursor.execute('''
                    INSERT INTO images (title, path, size, description, tags, extension)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (title, image_path, image_size, description, tags, extension))
        pg.commit()

        response = {
            "status": "200",
            "message": "Image uploaded successfully!",
            "path": image_path
        }

        log_status("200", "Image uploaded successfully!")
        return jsonify(response), 200 #успешно

    except (IOError, SyntaxError):
        response = {
            "status": "415",
            "message": "The file is not a valid image"
        }
        log_status("415", "The file is not a valid image")
        return jsonify(response), 415 #неподдерживаемый формат


def log_status(status, message):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%d, %m, %y, %H:%M:%S')} - {status}, {message}\n")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
