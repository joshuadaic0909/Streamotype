from flask import render_template, request
from app.main import bp 
import pandas as pd

from config import Config

@bp.route('/')
def index():

    return render_template('index.html')
