from app.main import bp
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
import subprocess
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'ipynb', 'py'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

streamlit_process = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def index():
    global streamlit_process
    show_streamlit = False

    if request.method == 'POST':
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            if filename.rsplit('.', 1)[1].lower() == 'py':
                if streamlit_process:
                    # Kill the previous streamlit process if exists
                    streamlit_process.terminate()
                
                # Run the Streamlit app in a separate process
                streamlit_process = subprocess.Popen([
                    "streamlit", 
                    "run", 
                    filepath,
                    "--server.headless", "true",   
                    "--browser.serverAddress", "0.0.0.0", 
                    "--server.runOnSave", "false"
                ])
                
                # Set the flag to True when the Streamlit app is uploaded
                show_streamlit = True
                time.sleep(5)  # Give it a few seconds to start up

    return render_template('index.html', show_streamlit=show_streamlit)


@bp.route('/stop_streamlit', methods=['POST'])
def stop_streamlit():
    global streamlit_process
    if streamlit_process:
        streamlit_process.terminate()
        streamlit_process = None
    return redirect(url_for('main.index'))
