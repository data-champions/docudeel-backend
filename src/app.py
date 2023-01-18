import logging
import os.path
import os
import json
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, flash, jsonify, make_response
from werkzeug.utils import secure_filename

from db import debiteur_nummer_exist
from response import get_response
import requests
from datetime import datetime
from s3 import upload_file_to_s3
from slack import send_slack_message
import boto3


def make_filename(debiteur_nummer: str,
                  description: str,
                  file_ext: str) -> str:
    now = str(datetime.now())[:19]
    fn = f"{debiteur_nummer}_{description}_{now}{file_ext}"
    fn = fn.replace(' ', '_').replace(':', '_')
    return fn

## TODO unit test
# no : in filename
# no space in filename
# no . in filename
# no .. before extension



logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

app = Flask(__name__, template_folder='.')
#  https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/#:~:text=Improving%20Uploads&text=The%20code%20above%20will%20limit,will%20raise%20a%20RequestEntityTooLarge%20exception.
MAX_MB_REQUEST = 250
app.config['MAX_CONTENT_LENGTH'] = MAX_MB_REQUEST * 1024 * 1024
CORS(app)

URL_MAKE = 'https://hook.eu1.make.com/wqy2x2k2owdng5ldqkr5d8fcvu95itu3'



@app.route('/', methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

S3_BUCKET = "docudeel-temp-storage"
def upload_to_s3(file, filename):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    s3 = boto3.client("s3")
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        filename,
    )

@app.route('/', methods=['POST'])
def upload_files():
    try:
        logging.info('Starting file upload')
        user_id = request.form.get('user_id')
        email = request.form.get('email')
        description = request.form.get('description')
        lang = request.form.get('lang', 'en')
        logging.info(f'{user_id=}')
        logging.info(f'{email=}')
        logging.info(f'{description=}')
        logging.info(f'{lang=}')
        
        if user_id is None or email is None or description is None:
            resp = dict(message="Param user_id, email or description is missing")
            return make_response(jsonify(resp), 400)

        clean_user_id = user_id.replace(' ', '').replace('-', '')
        is_client = debiteur_nummer_exist(clean_user_id)
        if not is_client:
            logging.info(f"{user_id=} {clean_user_id=} not found in records!")
            resp = get_response(response_type='debitnummer_notfound', lang=lang)
            return make_response(jsonify(resp), 400)
        # logging.info("*" * 50)

        # for file in request.files.getlist("files[]"):
        #     logging.info(file.filename)
        #     logging.info(file.stream)
        # # logging.info(dir(request.files))
        # logging.info("/" * 50)
        

        file = request.files['file']
        # obtaining the name of the destination file
        original_fn = file.filename
        if original_fn == '':
            logging.info('Invalid file')
            resp = dict(message="No file selected for uploading")
            return make_response(jsonify(resp), 400)
        else:
            logging.info('Selected file is= [%s]', original_fn)
            file_ext = os.path.splitext(original_fn)[1]
            upload_file = file.stream
            
            files = {'upload_file': upload_file}
            filename = make_filename(debiteur_nummer=clean_user_id,
                                     description=description,
                                     file_ext=file_ext)
            data = {'filename': filename, "file": files}
            print(f'{data=}')
            print(type(upload_file))
            logging.info(f'sending files to {URL_MAKE=}')
            r = requests.post(URL_MAKE, files=files,
                              data=data)
            logging.info(f'{r.status_code=}')
            logging.info(f'{r.text=}')
            
            if r.status_code == 413:
                logging.info('File too large')
                file.seek(0)
                # file.save(fp)
                upload_to_s3(file=file, filename=filename)
                mx = f""" 
                File too large: {filename} uploaded to {S3_BUCKET=}
                """
                send_slack_message(mx)

            resp = get_response(response_type='ok', lang=lang,
                                original_filename=original_fn)
            return make_response(jsonify(resp), 200)
    except Exception as e:
        logging.exception("Error")
        lang = "en"
        resp = get_response(response_type='fallback', lang=lang)
        return make_response(jsonify(resp), 500)


@app.errorhandler(413)
def request_entity_too_large(error):
    resp = dict(message='File Too Large')
    return make_response(jsonify(resp), 413)

 
if __name__ == '__main__':
 
    # Development only: run "python app.py" and open http://localhost:5000
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')