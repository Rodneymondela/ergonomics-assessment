from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ...extensions import db
from ...models.org import Company
from . import bp
from .forms import CompanyForm
from ...security import roles_required
@bp.route('/')
@login_required
def dashboard():
    companies = Company.query.filter_by(owner_id=current_user.id).all()
    return render_template('org/dashboard.html', companies=companies)
@bp.route('/company/new', methods=['GET','POST'])
@login_required
@roles_required('Admin','Assessor')
def company_new():
    form = CompanyForm()
    if form.validate_on_submit():
        c = Company(name=form.name.data, site=form.site.data, owner_id=current_user.id)
        db.session.add(c); db.session.commit()
        flash('Company saved','success')
        return redirect(url_for('org.dashboard'))
    return render_template('org/company_form.html', form=form)
