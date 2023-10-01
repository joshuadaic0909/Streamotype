from app.main import bp
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import json
import os
import subprocess
import time
import uuid
from threading import Thread


from app.utils.activity_tracker import LastActivityTracker
from app.code_gen.gen_streamlit import get_ui_code_summary, get_uo_code_summary, jupytertostreamlit

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'ipynb', 'py'}
activity_tracker = LastActivityTracker()
INACTIVITY_TIMEOUT = 600

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

streamlit_process = None
sessions = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def index():
    session_id = str(uuid.uuid4())  
    show_streamlit = False
    port = None  
    streamlit_url = None
    file_content = None
    optimized_content = None

    if request.method == 'POST':
        # ui_application = request.form.get('userOption')
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # read the content of upload file
            with open(filepath, 'r') as f:  
                file_content = f.read()
                optimized_content = jupytertostreamlit(file_content)

            # Save the optimized content to a new file
            optimized_filepath = os.path.join(UPLOAD_FOLDER, f"optimized_{filename}")
            with open(optimized_filepath, 'w') as f:
                f.write(optimized_content)


            if filename.rsplit('.', 1)[1].lower() == 'py':
                port = find_available_port()
                sessions[session_id] = {
                    'process': start_streamlit_process(optimized_filepath, port),
                    'port': port
                }


                streamlit_url = port_to_streamlit_url(port)
                activity_tracker.update_activity_time(session_id)
                show_streamlit = True
                time.sleep(10) 

    return render_template('index.html', show_streamlit=show_streamlit
                                        , streamlit_url=streamlit_url
                                        , session_id=session_id
                                        , port=port
                                        )


@bp.route('/<session_id>/stop_streamlit', methods=['POST'])
def stop_streamlit(session_id):
    if session_id in sessions:
        sessions[session_id]['process'].terminate()
        del sessions[session_id]
        activity_tracker.remove_activity_time(session_id)
    return redirect(url_for('main.index'))


def port_to_streamlit_url(port):
    nginx_url = os.environ.get("NGINX_URL", 'localhost:5000') 
    server_path = f"/streamlit_apps/{port}"
    return f"{nginx_url}{server_path}"



def start_streamlit_process(filepath, port):
    server_path = f"/streamlit_apps/{port}"
    return subprocess.Popen([
        "streamlit",
        "run",
        filepath,
        "--server.headless", "true",
        "--browser.serverAddress", "0.0.0.0",
        "--server.port", str(port),
        "--server.runOnSave", "false",
        f"--server.baseUrlPath", server_path
    ])


def find_available_port():
    for port in range(8502, 8600):  # Define a range of port numbers
        if port not in [session['port'] for session in sessions.values()]:
            return port
    raise Exception("No available ports")

def inactivity_check():
    while True:
        inactive_sessions = activity_tracker.get_inactive_sessions(INACTIVITY_TIMEOUT)
        for session_id in inactive_sessions:
            if session_id in sessions:
                sessions[session_id]['process'].terminate()
                del sessions[session_id]
                activity_tracker.remove_activity_time(session_id)
        time.sleep(60)  # Check every minute

# Start the inactivity check thread
inactivity_check_thread = Thread(target=inactivity_check, daemon=True)
inactivity_check_thread.start()
