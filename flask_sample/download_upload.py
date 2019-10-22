import os
from flask import Flask, request, send_from_directory, send_file
app = Flask(__name__)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
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
    return send_from_directory(directory=os.getcwd() + '/UPLOAD_FOLDER',
                               filename=filename)


if __name__ == "__main__":
    app.run(debug=True, port=8888)
