import os
import traceback
from flask import Flask, request, send_from_directory, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'sh'])


@app.errorhandler(Exception)
def all_exception_handler(e):
    error = str(traceback.format_exc())
    return error


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    """[
        This method for download a file from server
        Test:
            wget http://127.0.0.1:8888/download/test.txt
            wget http://127.0.0.1:8888/download/child/test.txt
    ]

    Arguments:
        filename {[string]} -- [path name of file to download]

    Returns:
        [byte] -- [content of file]
    """
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                               filename=filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """[
        This method for upload file to flask server
        Reference: http://flask.palletsprojects.com/en/1.0.x/patterns/fileuploads/
        Test: allow extensions: 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'sh'
            curl -F "UPLOADED_FILE=@/home/xuananh/data/Temp/temp.sh" http://127.0.0.1:8888/upload
    ]

    Returns:
        [string] -- [url to download uploaded file]
    """
    if request.method == 'POST':
        try:
            if 'UPLOADED_FILE' not in request.files:
                flash('No file part')
                return redirect(request.url)
        except ValueError:
            traceback.print_exc()
            return 'False'
        file = request.files['UPLOADED_FILE']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', filename=filename))
            return "Success"
        else:
            return "Cannot get uploaded file or file extension is not allowed"


if __name__ == "__main__":
    app.run(debug=True, port=8888)
