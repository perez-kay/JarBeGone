"""
This script contains two custom form fields used in the Flask App.
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, RadioField
from wtforms.validators import InputRequired

class FileForm(FlaskForm):
    """
    This class represents a form for uploading a file. Inherits from the
    base class FlaskForm. 

    Attributes
    ----------
    file : wtforms.FileField
        Represents the field for uploading a file. Requires input.
    submit : wtforms.SubmitField
        Represents a "Submit" button to submit the form.
    """

    file = FileField(validators=[InputRequired()])
    submit = SubmitField('Submit')

class SummaryConfigForm(FlaskForm):
    """
    This class represents the Summary Configuration form. Inherits from the
    base class FlaskForm. 

    Attributes
    ----------
    length : wtforms.RadioField
        Represents raido buttons used to choose the length of outputted summary.
    submit : wtforms.SubmitField
        Represents a "Submit" button to submit the form.
    """
    length = RadioField('What length would you like your summary to be?',
                        choices=[('short', 'Short (10% of original length)'),
                                ('medium', 'Medium (20% of original length)'),
                                ('long', 'Long (30% of original length)')],
                        validators=[InputRequired()])
    submit = SubmitField('Generate Summary')
