from flask import Flask, request, send_from_directory, send_file
app = Flask(__name__)
    
@app.route('/send_from_dir/<path:filename>')
def send_file_from_dir(filename):
    return send_from_directory(directory = '/media/xuananh/data/Downloads/plugin', 
                               filename = filename)
    
if __name__ == "__main__":
    app.run(debug=True)   