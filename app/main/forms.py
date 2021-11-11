# from flask import FlaskForm, StringField , TextAreaField, Required , SubmitField

# class ReviewForm(FlaskForm):

#  title = StringField('Review title',validators=[Required()])

#  review = TextAreaField('Pitch review')

#  submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required 

class PitchForm(FlaskForm):
    my_category = SelectField('Category', choices=[('Sales','Sales'),('Entertainment','Entertainment'),('Marketing','Marketing')],validators=[Required()])
    my_pitches = TextAreaField('Enter Pitch', validators=[Required()])
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Kindly write your comment here..', validators=[Required()])
    submit = SubmitField('Submit Comments')
    
class BioForm(FlaskForm):
    bio = TextAreaField('Tell us about yourself.',validators = [Required()])
    submit = SubmitField('Submit')