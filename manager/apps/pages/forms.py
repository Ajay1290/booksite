from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Optional
from wtforms_components import EmailField, Email


class FeedbackForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Content',  validators=[DataRequired()])