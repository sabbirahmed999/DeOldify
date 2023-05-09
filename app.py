from flask import Flask, request, send_from_directory, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *

device.set(device=DeviceId.GPU0)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            colorizer = get_image_colorizer()
            colorized_image_path = colorizer.plot_transformed_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return send_from_directory(app.config['UPLOAD_FOLDER'], colorized_image_path, as_attachment=True)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload an Image</title>
    <h1>Upload an Image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
