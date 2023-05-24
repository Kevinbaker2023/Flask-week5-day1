from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Pokemon_Name(FlaskForm):
    pokemon = StringField('Pokemon', validators=[DataRequired()])
    submit_btn = SubmitField('Enter')