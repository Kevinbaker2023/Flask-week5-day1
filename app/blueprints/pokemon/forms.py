from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonName(FlaskForm):
    pokemon = StringField(validators=[DataRequired()])
    submit = SubmitField('Enter')
    catch = SubmitField('Catch Pokemon')

class CatchPoke(FlaskForm):
    pokemon = StringField('Please re-enter pokemon below! ', validators=[DataRequired()])
    catch = SubmitField('Catch Pokemon')