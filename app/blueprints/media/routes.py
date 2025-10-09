import os
from flask import send_from_directory, render_template, request, redirect, url_for, current_app, flash
from flask_login import login_required
from ...models.media import Media
from ...extensions import db
from . import bp
@bp.route('/media/<path:filename>')
@login_required
def serve(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
@bp.route('/media/<int:media_id>/annotate', methods=['GET','POST'])
@login_required
def annotate(media_id):
    m = db.session.get(Media, media_id)
    if not m:
        flash('Media not found','danger')
        return redirect('/')
    if request.method == 'POST':
        m.annotations_json = request.form.get('annotations_json')
        db.session.commit()
        flash('Saved','success')
        return redirect(request.referrer or '/')
    return render_template('media/annotate.html', m=m)
