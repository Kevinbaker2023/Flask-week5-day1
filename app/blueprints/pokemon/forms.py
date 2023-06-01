from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonName(FlaskForm):
    pokemon = StringField('Pokemon: ', validators=[DataRequired()])
    submit_btn = SubmitField('Enter')
    catch_btn = SubmitField('Catch Pokemon')