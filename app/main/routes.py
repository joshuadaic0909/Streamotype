from app.main import bp
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'ipynb', 'py'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bp.route('/', methods=['GET', 'POST'])
def index():
    code_cells = []

    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            return redirect(request.url)
        
        filename = file.filename
        if not filename:
            return redirect(request.url)

        file_ext = filename.rsplit('.', 1)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return redirect(request.url)
        
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        file.save(filepath)

        if file_ext == 'ipynb':
            with open(filepath, 'r') as f:
                notebook = json.load(f)
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    code_cells.append(''.join(cell['source']))
        elif file_ext == 'py':
            with open(filepath, 'r') as f:
                content = f.read()
            code_cells.append(content)

    return render_template('index.html', code_cells=code_cells)
