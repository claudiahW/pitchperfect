from flask import render_template,request,redirect,url_for
from . import main
# from .forms import ReviewForm
# from ..models import Review

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    message = 'Hello World'
    return render_template('index.html',message = message)