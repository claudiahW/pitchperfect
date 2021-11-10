from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from .forms import PitchForm, CommentForm, BioForm
from . import main
from .. import db,photos
from . import User, Pitch, Comment 
from flask_login import login_required, current_user 
from flask import jsonify
from multiprocessing import Value

# import markdown2  

# Views
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/new_pitch', methods=['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = form.my_pitches.data
        category = form.my_category.data
        new_pitch=Pitch(pitch=pitch,category=category,user_id=current_user.id)

        new_pitch.save_pitch()

        if category == 'Sales' :
            return redirect(url_for('main.sales_pitches'))
        
        elif category == 'Entertainment':
            return redirect(url_for('main.entertain_pitches'))
        
        elif category == 'Marketing':
            return redirect(url_for('main.marketeting_pitches'))
        
        else:
            return redirect(url_for('.index'))

    return render_template('new_pitch.html', review_form=form)

@main.route('/pitches/sales_pitches')
def sales_pitches():
    pich = Pitch.query.all()
    promotional = Pitch.query.filter_by(category='Sales').all()
    return render_template('sales.html',sales=sales)

@main.route('/pitches/entertainment_pitches')
def scholar_pitches():
    pich = Pitch.query.all()
    scholarship = Pitch.query.filter_by(category='Entertainment').all()
    return render_template('entertain.html',entertainment=entertainment)


@main.route('/pitches/marketing_pitches')
def marketing_pitches():
    pich = Pitch.query.all()
    marketing = Pitch.query.filter_by(category='Marketing').all()
    return render_template('marketing.html',marketing=marketing)
 
@main.route('/pitches/comments/<int:pitch_id>', methods=['GET','POST'])
@login_required
def leave_comment(pitch_id):
    comment_form = CommentForm()
    pitches = Pitch.query.get(pitch_id)
    comment = Comment.query.filter_by(pitch_id=pitch_id).all()
    if comment_form.validate_on_submit():
        comments = comment_form.comment.data
        
        pitch_id= pitch_id
        user_id = current_user._get_current_object().id
        new_comment= Comment(comments=comments,pitch_id=pitch_id, user_id=user_id)
        new_comment.save_comment()      
        
        return redirect(url_for('main.pitch_page',comment_form=comment_form,pitch_id=pitch_id))
        
    return render_template('new_comment.html',comment_form=comment_form, comment=comment,pitch_id=pitch_id)
  
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


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user.id
    pitch = Pitch.query.filter_by(user_id=user_id).all()

    if user is None:
        abort(404)
        
    return render_template("profile/profile.html", user = user, pitch=pitch)

    



   
    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data

        # Updated review instance
        new_review = Review(pitch_id=pitch.id,pitch_title=title,image_path=pitch.poster,pitch_review=review,user=current_user)

        # save review method
        new_review.save_review()
        return redirect(url_for('.pitch',id = pitch.id ))

    title = f'{pitch.title} review'
    return render_template('new_review.html',title = title, review_form=form, pitch=pitch)    
@main.route('/review/<int:id>')
def single_review(id):
    review=Review.query.get(id)
    if review is None:
        abort(404)
    format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('review.html',review = review,format_review=format_review)