import logging
import os.path
import os
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, flash, jsonify, make_response
from werkzeug.utils import secure_filename
 
# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
# logging config]
 
 
app = Flask(__name__, template_folder='.')
# 16 gb https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/#:~:text=Improving%20Uploads&text=The%20code%20above%20will%20limit,will%20raise%20a%20RequestEntityTooLarge%20exception.
# https://github.com/pallets/flask/issues/3874
MAX_MB_REQUEST = 100
app.config['MAX_CONTENT_LENGTH'] = MAX_MB_REQUEST * 1024 * 1024
app.secret_key = "somesecretkey"
CORS(app)

@app.route('/', methods=['GET'])
def index():
    logging.info('Showing index page')
    return render_template('upload.html')
 
 
@app.route('/', methods=['POST'])
def upload_files():
    logging.info(os.getcwd())
    logging.info(os.listdir())
    logging.info('Starting file upload')

    user_id = request.form.get('user_id')
    email = request.form.get('email')
    description = request.form.get('description')
    logging.info(f'{request.form=}')
    logging.info("last update...")
    logging.info(f'{request=}')
    logging.info(f'{request.files=}')
    if 'file' not in request.files:
        flash('No file part')
        logging.info("'No file part'...")
        resp = dict(message="No file sent in request")
        return make_response(jsonify(resp), 400)
    if user_id is None or email is None or description is None:
        resp = dict(message="Param user_id, email or description is missing")
        return make_response(jsonify(resp), 400)
    file = request.files['file']
    # obtaining the name of the destination file
    filename = file.filename
    if filename == '':
        logging.info('Invalid file')
        resp = dict(message="No file selected for uploading")
        return make_response(jsonify(resp), 400)
    else:
        logging.info('Selected file is= [%s]', filename)
        file_ext = os.path.splitext(filename)[1]
        # TODO
        logging.info('Upload is successful')
        resp = dict(message='OK')
        return make_response(jsonify(resp), 200)


@app.errorhandler(413)
def request_entity_too_large(error):
    resp = dict(message='File Too Large')
    return make_response(jsonify(resp), 413)

 
if __name__ == '__main__':
 
    # Development only: run "python app.py" and open http://localhost:5000
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')