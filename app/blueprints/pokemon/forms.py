from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonName(FlaskForm):
    pokemon = StringField('Pokemon: ', validators=[DataRequired()])
    submit = SubmitField('Enter')
    catch = SubmitField('Catch Pokemon')