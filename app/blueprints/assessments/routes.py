import os, uuid
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from ...extensions import db
from ...models.org import Company, JobRole
from ...models.ergo import Assessment, CorrectiveAction
from ...models.media import Media
from ...scoring import compute_rula_full, compute_reba_full, risk_band
from ...scoring.niosh import compute_niosh
from . import bp
from .forms import AssessmentForm
from ...security import roles_required

@bp.route('/assessment/new', methods=['GET','POST'])
@login_required
@roles_required('Admin','Assessor')
def new():
    form = AssessmentForm()
    form.jobrole_id.choices = [(jr.id, f"{jr.title}") for jr in JobRole.query.join(Company).filter(Company.owner_id==current_user.id)]
    if form.validate_on_submit():
        rula = compute_rula_full(dict(
            upper_arm=form.rula_upper_arm.data, lower_arm_band=form.rula_lower_arm_band.data,
            wrist=form.rula_wrist.data, wrist_twist=form.rula_wrist_twist.data,
            neck=form.rula_neck.data, trunk=form.rula_trunk.data, legs=form.rula_legs.data,
            muscle_use=form.rula_muscle_use.data, force_load=form.rula_force_load.data,
        ))
        reba = compute_reba_full(dict(
            trunk=form.reba_trunk.data, neck=form.reba_neck.data, legs=form.reba_legs.data,
            upper_arm=form.reba_upper_arm.data, lower_arm=form.reba_lower_arm.data, wrist=form.reba_wrist.data,
            coupling=form.reba_coupling.data, load=form.reba_load.data,
            activity_static=form.reba_activity_static.data, activity_repeat=form.reba_activity_repeat.data, activity_rapid=form.reba_activity_rapid.data,
        ))
        li, rwl = compute_niosh(form.weight.data, form.h.data, form.v.data, form.d.data, form.a.data, form.f.data, form.c.data)
        category = max((risk_band('RULA', rula)['category'], risk_band('REBA', reba)['category']), key=lambda x: {'Low':1,'Medium':2,'High':3}[x])
        a = Assessment(jobrole_id=form.jobrole_id.data, assessor=current_user.name, observation=form.observation.data,
                       rula=rula, reba=reba, niosh_li=li, recommended_weight=rwl, risk_category=category)
        db.session.add(a); db.session.commit()

        files = request.files.getlist('media')
        for f in files:
            if not f or not f.filename: continue
            ext = os.path.splitext(f.filename)[1].lower()
            if ext not in {'.jpg','.jpeg','.png','.gif','.mp4','.mov','.avi','.webm'}: continue
            fn = f"{uuid.uuid4().hex}{ext}"
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], fn)
            f.save(path)
            m = Media(assessment_id=a.id, filename=fn, original_name=f.filename, media_type=('video' if ext in {'.mp4','.mov','.avi','.webm'} else 'image'))
            db.session.add(m)
        db.session.commit()
        flash('Assessment saved','success')
        return redirect(url_for('assessments.view', assessment_id=a.id))
    return render_template('assessments/new.html', form=form)

@bp.route('/assessment/<int:assessment_id>')
@login_required
def view(assessment_id):
    a = Assessment.query.get_or_404(assessment_id)
    acts = CorrectiveAction.query.filter_by(assessment_id=a.id).all()
    return render_template('assessments/view.html', a=a, actions=acts)

@bp.route('/assessments/print/<int:assessment_id>')
@login_required
def print_assessment(assessment_id):
    a = Assessment.query.get_or_404(assessment_id)
    return render_template('assessments/print.html', a=a)

@bp.route('/assessment/<int:assessment_id>/action', methods=['POST'])
@login_required
@roles_required('Admin','Assessor')
def add_action(assessment_id):
    a = Assessment.query.get_or_404(assessment_id)
    action = request.form.get('action'); resp = request.form.get('responsible'); due = request.form.get('due_date')
    due_d = datetime.strptime(due, '%Y-%m-%d').date() if due else None
    db.session.add(CorrectiveAction(assessment_id=a.id, action=action, responsible=resp, due_date=due_d))
    db.session.commit()
    return redirect(url_for('assessments.view', assessment_id=assessment_id))

# Filters helper
def _apply_filters(query):
    company_id = request.args.get('company_id', type=int)
    jobrole_id = request.args.get('jobrole_id', type=int)
    date_from = request.args.get('date_from', type=str)
    date_to = request.args.get('date_to', type=str)
    risk = request.args.get('risk', type=str)
    if company_id:
        query = query.join(JobRole, Assessment.jobrole_id == JobRole.id).filter(JobRole.company_id == company_id)
    if jobrole_id:
        query = query.filter(Assessment.jobrole_id == jobrole_id)
    def parse_date(s):
        try: return datetime.strptime(s, '%Y-%m-%d')
        except Exception: return None
    if date_from:
        d1 = parse_date(date_from)
        if d1: query = query.filter(Assessment.created_at >= d1)
    if date_to:
        d2 = parse_date(date_to)
        if d2: query = query.filter(Assessment.created_at < d2.replace(hour=23, minute=59, second=59))
    if risk in {'Low','Medium','High'}:
        query = query.filter(Assessment.risk_category == risk)
    return query

@bp.route('/assessments')
@login_required
def list_all():
    q = _apply_filters(Assessment.query.order_by(Assessment.created_at.desc()))
    asses = q.all()
    companies = Company.query.all()
    company_id = request.args.get('company_id', type=int)
    if company_id:
        jobroles = JobRole.query.filter_by(company_id=company_id).all()
    else:
        jobroles = JobRole.query.all()
    rows = []
    for a in asses:
        jr = db.session.get(JobRole, a.jobrole_id)
        rows.append(dict(
            id=a.id,
            date=a.created_at.strftime('%Y-%m-%d') if a.created_at else '',
            job_title=(jr.title if jr else f"Job #{a.jobrole_id}"),
            rula=a.rula, reba=a.reba, niosh_li=a.niosh_li, risk=a.risk_category,
        ))
    sel = dict(
        company_id=company_id,
        jobrole_id=request.args.get('jobrole_id', type=int),
        date_from=request.args.get('date_from',''),
        date_to=request.args.get('date_to',''),
        risk=request.args.get('risk',''),
    )
    return render_template('assessments/list.html', rows=rows, companies=companies, jobroles=jobroles, sel=sel)

@bp.route('/assessments/export.csv')
@login_required
def export_csv():
    q = _apply_filters(Assessment.query.order_by(Assessment.created_at.desc()))
    asses = q.all()
    rows = []
    for a in asses:
        jr = db.session.get(JobRole, a.jobrole_id)
        rows.append(dict(
            id=a.id,
            date=a.created_at.strftime('%Y-%m-%d') if a.created_at else '',
            jobrole_id=a.jobrole_id,
            job_title=(jr.title if jr else ''),
            assessor=a.assessor or '',
            observation=a.observation or '',
            rula=a.rula, reba=a.reba, niosh_li=a.niosh_li, rwl=a.recommended_weight, risk=a.risk_category,
        ))
    from ...services.exports import export_assessments_csv
    return export_assessments_csv(rows)

@bp.route('/assessments/export.pdf')
@login_required
def export_pdf():
    q = _apply_filters(Assessment.query.order_by(Assessment.created_at.desc()))
    asses = q.all()
    rows = []
    for a in asses:
        jr = db.session.get(JobRole, a.jobrole_id)
        rows.append(dict(
            id=a.id,
            date=a.created_at.strftime('%Y-%m-%d') if a.created_at else '',
            job_title=(jr.title if jr else ''),
            rula=a.rula, reba=a.reba, niosh_li=a.niosh_li, risk=a.risk_category,
        ))
    from ...services.pdf import send_assessments_pdf
    return send_assessments_pdf(rows)

@bp.route('/assessment/<int:assessment_id>/export.pdf')
@login_required
def export_pdf_single(assessment_id):
    a = Assessment.query.get_or_404(assessment_id)
    jr = db.session.get(JobRole, a.jobrole_id)
    from ...models.org import Company
    comp = db.session.get(Company, jr.company_id) if jr else None
    a_dict = dict(
        id=a.id,
        date=a.created_at.strftime('%Y-%m-%d') if a.created_at else '',
        assessor=a.assessor or '',
        job_title=(jr.title if jr else f"Job #{a.jobrole_id}"),
        company=(comp.name if comp else ''),
        site=(comp.site if comp else ''),
        rula=a.rula, reba=a.reba, niosh_li=a.niosh_li, rwl=a.recommended_weight, risk=a.risk_category,
        observation=a.observation or '',
    )
    media_q = Media.query.filter_by(assessment_id=a.id, media_type='image').all()
    media_paths = [os.path.join(current_app.config['UPLOAD_FOLDER'], m.filename) for m in media_q]
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../static/logo.png"))
    if not os.path.exists(logo_path): logo_path = None
    from ...services.pdf import send_assessment_pdf
    return send_assessment_pdf(a_dict, media_paths, logo_path)
