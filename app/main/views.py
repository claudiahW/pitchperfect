from flask import render_template,request,redirect,url_for
from flask_login import login_required
from . import main
from .. import db,photos

# from .forms import ReviewForm
# from ..models import Review

# Views
@main.route('/')
def index():
 @login_required
 def new_review(id):

    '''
    View root page function that returns the index page and its data
    '''

    message = 'Hello World'
    return render_template('index.html',message = message)
    
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
