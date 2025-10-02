from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
class JobRoleForm(FlaskForm):
    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])
    title = StringField('Job Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')
