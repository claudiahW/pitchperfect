from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255),unique=True,index=True)
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure  = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('Pitch',backref='author', lazy='dynamic')
    

    @property
    def password(self):
                raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
                self.pass_secure = generate_password_hash(password)
    
    
    def verify_password(self,password):
                return check_password_hash(self.pass_secure,password)
    
    def save_user(self):
            db.session.add(self)
            db.session.commit()
            
    def __repr__(self):
            return f'User{self.username}'
    
    
class Pitch(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    pitch = db.Column(db.Text(),nullable = False)
    category = db.Column(db.String(255), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    upvote = db.relationship('Upvote',backref='pitch',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='pitch',lazy='dynamic')
    comment = db.relationship('Comment',backref='pitch',lazy='dynamic' )

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_pitches(cls,id):
        pitches = Pitch.query.filter_by(user_id=id).all()
        return pitches

class Comment(db.Model):
    __tablename__ = 'comments' 
    id = db.Column(db.Integer, primary_key = True)
    comments = db.Column(db.Text())
    pitch_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_comments(cls,pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()

        return comments
        
    def __repr__(self):
        return f'Comment{self.comments}' 
         
class Upvote(db.Model):
  _tablename_ = 'upvotes'
  id = db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
  pitch_id = db.Column(db.Integer,db.ForeignKey('users.id'))
  def save(self):
    db.session.add(self)
    db.session.commit()
    
  @classmethod
  def get_upvotes(cls,id):
    upvote = Upvote.query.filter_by(post_id=id).all()
    return upvote
  def _repr_(self):
      return f'{self.user_id}:{self.post_id}'
      
class Downvote(db.Model):
  _tablename_ = 'downvotes'
  id = db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
  pitch_id = db.Column(db.Integer,db.ForeignKey('users.id'))
  def save(self):
    db.session.add(self)
    db.session.commit()
  @classmethod
  def get_downvotes(cls,id):
    downvote = Downvote.query.filter_by(post_id=id).all()
    return downvote
  def _repr_(self):
    return f'{self.user_id}:{self.post_id}'              