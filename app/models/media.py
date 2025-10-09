from datetime import datetime
from ..extensions import db
class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255))
    media_type = db.Column(db.String(20))  # image|video
    annotations_json = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
