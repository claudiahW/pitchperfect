from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from .forms import PitchForm, CommentForm, BioForm
from . import main
from .. import db,photos
from ..models import User,Pitch, Comment ,Upvote,Downvote 
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
            return redirect(url_for('main.entertainment_pitches'))
        
        elif category == 'Marketing':
            return redirect(url_for('main.marketing_pitches'))
        
        else:
            return redirect(url_for('.index'))

    return render_template('n_pitch.html', review_form=form)

@main.route('/pitches/sales_pitches')
def sales_pitches():
    pitch = Pitch.query.all()
    sales = Pitch.query.filter_by(category='Sales').all()
    return render_template('sales.html',sales=sales)

@main.route('/pitches/entertainment_pitches')
def entertainment_pitches():
    pitch = Pitch.query.all()
    entertainment= Pitch.query.filter_by(category='Entertainment').all()
    return render_template('entertainment.html',entertainment=entertainment)


@main.route('/pitches/marketing_pitches')
def marketing_pitches():
    pitch = Pitch.query.all()
    marketing= Pitch.query.filter_by(category='Marketing').all()
    return render_template('marketing.html',marketing=marketing)
 
@main.route('/pitches/comments/<int:pitch_id>', methods=['GET','POST'])
@login_required
def leave_comment(pitch_id):
    comment_form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    comment = Comment.query.filter_by(pitch_id=pitch_id).all()
    if comment_form.validate_on_submit():
        comments = comment_form.comment.data
        
        pitch_id= pitch_id
        user_id = current_user._get_current_object().id
        new_comment= Comment(comments=comments,pitch_id=pitch_id, user_id=user_id)
        new_comment.save_comment()      
        
        return redirect(url_for('main.pitch_page',comment_form=comment_form,pitch_id=pitch_id))
        
    return render_template('n_comment.html',comment_form=comment_form, comment=comment,pitch_id=pitch_id)
  
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
    user_id = current_user._get_current_object().id
    pitch = Pitch.query.filter_by(user_id=user_id).all()

    if user is None:
        abort(404)
        
    return render_template("profile/profile.html", user = user, pitch=pitch)


@main.route('/user/<uname>/pitches',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    
    if user is None:
        abort(404)

    form = PitchForm()

    if form.validate_on_submit():
        pitch = form.my_pitches.data
        category = form.my_category.data
        
        new_pitch=Pitch(pitch=pitch,category=category,user_id=current_user.id)
        
        new_pitch.save_pitch()
        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/bio',methods = ['GET','POST'])
@login_required
def update_bio(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    bioform = BioForm()

    if bioform.validate_on_submit():
        user.bio = bioform.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/bio.html',bioform=bioform)

@main.route('/pitches')
def pitch_page():    
    user = User.query.all()
    pitches = Pitch.query.all()
    user=current_user
    return render_template('pitches.html',pitches=pitches,user=user)  

# @main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    pitch = Pitch.query.get(id)
    if pitch is None:
        abort(404)
    # check if the user has already liked the pitch
    like = Upvote.query.filter_by(user_id=current_user.id, pitch_id=id).first()
    if like is not None:
        # if the user has already liked the pitch, delete the like
        db.session.delete(like)
        db.session.commit()
        
        return redirect(url_for('.index'))
    # if the user has not liked the pitch, add a like
    new_like = Upvote(
        user_id=current_user.id,
        pitch_id=id
    )
    db.session.add(new_like)
    db.session.commit()
    
    return redirect(url_for('.index'))

@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def dislike(id):
    pitch = Pitch.query.get(id)
    if pitch is None:
        abort(404)
    # check if the user has already disliked the pitch
    dislike = Downvote.query.filter_by(
        user_id=current_user.id, pitch_id=id).first()
    if dislike is not None:
        # if the user has already disliked the pitch, delete the dislike
        db.session.delete(dislike)
        db.session.commit()
        
        return redirect(url_for('.index'))
    # if the user has not disliked the pitch, add a dislike
    new_dislike = Downvote(
    user_id=current_user.id,
    pitch_id=id
    )
    db.session.add(new_dislike)
    db.session.commit()
    
    return redirect(url_for('.index')) 


   
