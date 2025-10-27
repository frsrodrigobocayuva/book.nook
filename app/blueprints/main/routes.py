from flask import Blueprint, render_template, request, Response, redirect, url_for

index_bp = Blueprint('Index', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')