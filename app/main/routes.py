from app.main import bp
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
import subprocess
import time
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'ipynb', 'py'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

streamlit_process = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @bp.route('/', methods=['GET', 'POST'])
# def index():
#     global streamlit_process
#     show_streamlit = False

#     if request.method == 'POST':
#         file = request.files.get('file')

#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
#             file.save(filepath)
            
#             if filename.rsplit('.', 1)[1].lower() == 'py':
#                 if streamlit_process:
#                     # Kill the previous streamlit process if exists
#                     streamlit_process.terminate()
                
#                 # Run the Streamlit app in a separate process
#                 streamlit_process = subprocess.Popen([
#                     "streamlit", 
#                     "run", 
#                     filepath,
#                     "--server.headless", "true",   
#                     "--browser.serverAddress", "0.0.0.0", 
#                     "--server.runOnSave", "false"
#                 ])
                
#                 # Set the flag to True when the Streamlit app is uploaded
#                 show_streamlit = True
#                 time.sleep(5)  # Give it a few seconds to start up

#     return render_template('index.html', show_streamlit=show_streamlit)


# @bp.route('/stop_streamlit', methods=['POST'])
# def stop_streamlit():
#     global streamlit_process
#     if streamlit_process:
#         streamlit_process.terminate()
#         streamlit_process = None
#     return redirect(url_for('main.index'))

# Dictionary to hold the streamlit processes and ports for each session
sessions = {}

@bp.route('/', methods=['GET', 'POST'])
def index():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    show_streamlit = False
    port = None  # default value for port

    if request.method == 'POST':
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            if filename.rsplit('.', 1)[1].lower() == 'py':
                port = find_available_port()
                sessions[session_id] = {
                    'process': start_streamlit_process(filepath, port),
                    'port': port
                }

                show_streamlit = True
                time.sleep(5)  # Give it a few seconds to start up
                print(port)
                print(session_id)

    return render_template('index.html', show_streamlit=show_streamlit, session_id=session_id, port=port)


@bp.route('/<session_id>/stop_streamlit', methods=['POST'])
def stop_streamlit(session_id):
    if session_id in sessions:
        sessions[session_id]['process'].terminate()
        del sessions[session_id]
    return redirect(url_for('main.index'))


def start_streamlit_process(filepath, port):
    return subprocess.Popen([
        "streamlit",
        "run",
        filepath,
        "--server.headless", "true",
        "--browser.serverAddress", "0.0.0.0",
        "--server.port", str(port),
        "--server.runOnSave", "false"
    ])


def find_available_port():
    for port in range(8502, 8600):  # Define a range of port numbers
        if port not in [session['port'] for session in sessions.values()]:
            return port
    raise Exception("No available ports")
