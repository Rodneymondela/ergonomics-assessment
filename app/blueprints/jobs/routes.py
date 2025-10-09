from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ...extensions import db
from ...models.org import Company, JobRole
from . import bp
from .forms import JobRoleForm
from ...security import roles_required
@bp.route('/job/new', methods=['GET','POST'])
@login_required
@roles_required('Admin','Assessor')
def job_new():
    form = JobRoleForm()
    form.company_id.choices = [(c.id, c.name) for c in Company.query.filter_by(owner_id=current_user.id)]
    if form.validate_on_submit():
        jr = JobRole(title=form.title.data, description=form.description.data, company_id=form.company_id.data)
        db.session.add(jr); db.session.commit()
        flash('Job role saved','success')
        return redirect(url_for('org.dashboard'))
    return render_template('jobs/jobrole_form.html', form=form)
