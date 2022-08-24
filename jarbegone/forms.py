from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, FileField, SelectMultipleField, RadioField
from wtforms.validators import InputRequired, ValidationError


class FileForm(FlaskForm):
    file = FileField(validators=[InputRequired()])
    submit = SubmitField('Submit')

class SummaryConfigForm(FlaskForm):


    length = RadioField('What length would you like your summary to be?',
                        choices=[('short', 'Short (10% of original length)'),
                                ('medium', 'Medium (20% of original length)'),
                                ('long', 'Long (30% of original length)')],
                        validators=[InputRequired()])
    submit = SubmitField('Generate Summary')
