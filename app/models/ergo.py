from datetime import datetime
from ..extensions import db
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobrole_id = db.Column(db.Integer, db.ForeignKey('job_role.id'), nullable=False)
    assessor = db.Column(db.String(160))
    observation = db.Column(db.Text)
    rula = db.Column(db.Integer)
    reba = db.Column(db.Integer)
    niosh_li = db.Column(db.Float)
    recommended_weight = db.Column(db.Float)
    risk_category = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class CorrectiveAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    responsible = db.Column(db.String(160))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(40), default='Open')
