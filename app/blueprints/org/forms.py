from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class CompanyForm(FlaskForm):
    name = StringField('Company', validators=[DataRequired()])
    site = StringField('Site')
    submit = SubmitField('Save')
