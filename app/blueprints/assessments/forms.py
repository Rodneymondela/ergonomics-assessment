from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
class AssessmentForm(FlaskForm):
    jobrole_id = SelectField('Job Role', coerce=int, validators=[DataRequired()])
    observation = TextAreaField('Observation / Task description')
    # RULA
    rula_upper_arm = IntegerField('Upper Arm (1-6)', default=3)
    rula_lower_arm_band = IntegerField('Lower Arm Band (1-3)', default=2)
    rula_wrist = IntegerField('Wrist (1-4)', default=2)
    rula_wrist_twist = IntegerField('Wrist Twist (1-2)', default=1)
    rula_neck = IntegerField('Neck (1-6)', default=3)
    rula_trunk = IntegerField('Trunk (1-6)', default=3)
    rula_legs = IntegerField('Legs (1-4)', default=2)
    rula_muscle_use = IntegerField('Muscle Use (0/1)', default=0)
    rula_force_load = IntegerField('Force/Load (0..2)', default=0)
    # REBA
    reba_trunk = IntegerField('Trunk (1-5)', default=3)
    reba_neck = IntegerField('Neck (1-3)', default=2)
    reba_legs = IntegerField('Legs (1-2)', default=1)
    reba_upper_arm = IntegerField('Upper Arm (1-6)', default=3)
    reba_lower_arm = IntegerField('Lower Arm (1-3)', default=2)
    reba_wrist = IntegerField('Wrist (1-3)', default=2)
    reba_coupling = IntegerField('Coupling (0..3)', default=0)
    reba_load = IntegerField('Load/Force (0..3)', default=0)
    reba_activity_static = IntegerField('Static >1min (0/1)', default=0)
    reba_activity_repeat = IntegerField('Repeat >4/min (0/1)', default=0)
    reba_activity_rapid = IntegerField('Rapid/jerky (0/1)', default=0)
    # NIOSH
    weight = FloatField('Lift Weight (kg)', default=10.0)
    h = FloatField('H (cm)', default=30.0)
    v = FloatField('V (cm)', default=75.0)
    d = FloatField('D (cm)', default=25.0)
    a = FloatField('A (deg)', default=0.0)
    f = FloatField('Freq (lifts/min)', default=0.2)
    c = FloatField('Coupling (1,0.95,0.9)', default=1.0)
    submit = SubmitField('Save Assessment')
