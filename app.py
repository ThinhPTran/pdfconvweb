from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Ensure the upload and download folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    download_link = None
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Run the shell script to convert the file
            subprocess.run(['./convert.sh', filepath, app.config['DOWNLOAD_FOLDER']])

            # Generate the download link
            new_filename = f"{os.path.splitext(file.filename)[0]}_converted{os.path.splitext(file.filename)[1]}"
            download_link = url_for('download_file', filename=new_filename)

    # List files in the download folder
    #files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    files = [f for f in os.listdir(app.config['DOWNLOAD_FOLDER']) if f.endswith('.pdf')]
    return render_template('index.html', download_link=download_link, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000",debug=True)

