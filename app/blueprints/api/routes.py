from flask import jsonify, request
from ...models.ergo import Assessment
from ...models.org import JobRole
from . import bp
@bp.get('/assessments')
def list_assessments():
    rows = Assessment.query.order_by(Assessment.created_at.desc()).limit(50).all()
    return jsonify([dict(id=a.id, jobrole_id=a.jobrole_id, rula=a.rula, reba=a.reba, niosh_li=a.niosh_li, category=a.risk_category, created=a.created_at.isoformat()) for a in rows])
@bp.get('/jobroles')
def jobroles():
    company_id = request.args.get('company_id', type=int)
    q = JobRole.query
    if company_id:
        q = q.filter_by(company_id=company_id)
    roles = q.order_by(JobRole.title.asc()).all()
    return jsonify([dict(id=r.id, title=r.title, company_id=r.company_id) for r in roles])
